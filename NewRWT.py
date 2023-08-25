import pygame, sys
import time
import RPi.GPIO as GPIO
import traceback
import datetime
import configparser

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Configuration
CONFIG = {
    "width": int(config.get('General', 'width')),
    "height": int(config.get('General', 'height')),
    "start_switches": list(map(int, config.get('General', 'start_switches').split(','))),
    "stop_switches": list(map(int, config.get('General', 'stop_switches').split(','))),
    "reset_switch": int(config.get('General', 'reset_switch')),
    "debounce_time": int(config.get('General', 'debounce_time')),
    "title_font_size": int(config.get('General', 'title_font_size')),
    "timer_font_size": int(config.get('General', 'timer_font_size')),
    "high_score_font_size": int(config.get('General', 'high_score_font_size')),
    "colors": {
        "red": pygame.Color(*map(int, config.get('Colors', 'red').split(','))),
        "grey": pygame.Color(*map(int, config.get('Colors', 'grey').split(','))),
        "white": pygame.Color(*map(int, config.get('Colors', 'white').split(','))),
        "black": pygame.Color(*map(int, config.get('Colors', 'black').split(','))),
        "yellow": pygame.Color(*map(int, config.get('Colors', 'yellow').split(','))),
        "green": pygame.Color(*map(int, config.get('Colors', 'green').split(','))),
    },
    "title_font": config.get('Fonts', 'title_font'),
    "timer_font": config.get('Fonts', 'timer_font'),
    "high_score_font": config.get('Fonts', 'high_score_font'),
}

class Lane:
    def __init__(self, start_switch, stop_switch, y):
        self.run = 0
        self.s = 0
        self.m = 0
        self.timer = time.time()
        self.last_displayed_time = "00:00.0"
        self.last_start_time = 0
        self.last_stop_time = 0
        self.start_switch = start_switch
        self.stop_switch = stop_switch
        self.y = y

    def handle_stopwatch(self):
        global stop_sound
        # Handle stopwatch running state and display time
        if self.run == 1:
            elapsed_time = time.time() - self.timer
            self.m, self.s = divmod(elapsed_time, 60)
            self.s, ms = divmod(self.s, 1)
            current_time_str = f"{int(self.m):02}:{int(self.s):02}.{int(ms*10)}"
            if current_time_str != self.last_displayed_time:
                display(current_time_str, self.y, 2)
                self.last_displayed_time = current_time_str
        elif time.time() - self.timer > 1 and self.run == 0 and self.s == 0:
            display("00:00.0", self.y, 2)

        # Handle start button press
        if GPIO.input(self.start_switch) == 0 and pygame.time.get_ticks() - self.last_start_time > CONFIG["debounce_time"]:
            self.last_start_time = pygame.time.get_ticks()
            if self.run == 0:
                self.run = 1
                self.timer = time.time()
            else:
                self.run = 0
                self.s = 0
                self.m = 0
                self.timer = time.time()

        # Handle stop button press
        if GPIO.input(self.stop_switch) == 0 and self.run == 1 and pygame.time.get_ticks() - self.last_stop_time > CONFIG["debounce_time"]:
            self.last_stop_time = pygame.time.get_ticks()
            total_time = self.s + self.m * 60
            self.run = 0
            self.s = 0
            self.m = 0
            self.timer = time.time()
            stop_sound.play()
            update_high_scores(total_time)

# Initialization Functions
def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for pin in CONFIG["start_switches"] + CONFIG["stop_switches"] + [CONFIG["reset_switch"]]:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def init_pygame():
    global windowSurfaceObj, stop_sound
    pygame.init()
    pygame.mixer.init()
    windowSurfaceObj = pygame.display.set_mode((CONFIG["width"], CONFIG["height"]), pygame.FULLSCREEN)
    stop_sound = pygame.mixer.Sound('stop_sound.wav')

# High Scores Functions
def read_high_scores():
    try:
        scores = []
        with open('high_scores.txt', 'r') as file:
            for line in file.readlines():
                minutes, rest = line.strip().split(':')
                seconds, tenths = rest.split('.')
                total_seconds = float(minutes) * 60 + float(seconds) + float(tenths) / 10
                scores.append(total_seconds)
        return scores
    except FileNotFoundError:
        return [0] * 10

def write_high_scores(scores):
    with open('high_scores.txt', 'w') as file:
        for score in scores:
            formatted_score = format_high_score(score)
            file.write(formatted_score + '\n')

def update_high_scores(score):
    global high_scores
    high_scores.append(score)
    high_scores.sort()
    high_scores = high_scores[:10]
    write_high_scores(high_scores)

# Function to format the high scores in "MM:SS.s" format
def format_high_score(score_seconds):
    minutes, seconds = divmod(score_seconds, 60)
    seconds, tenths = divmod(seconds, 1)
    tenths *= 10
    return f"{int(minutes):02}:{int(seconds):02}.{int(tenths)}"

def scroll_high_scores():
    global scroll_position
    fontObj = pygame.font.Font(CONFIG["high_score_font"], CONFIG["high_score_font_size"]) # High score scroller font size
    y_position = int(CONFIG["height"]/8)
    text = "High Scores: " + " | ".join([f"{idx+1}. {format_high_score(score)}" for idx, score in enumerate(high_scores)])
    msgSurfaceObj = fontObj.render(text, False, CONFIG["colors"]["red"])
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (scroll_position, y_position)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
    scroll_position -= 5
    if scroll_position < -msgRectobj.width:
        scroll_position = CONFIG["width"]

# Display Function
def display(msg, y, col):
    fontObj = pygame.font.Font(CONFIG["timer_font"], CONFIG["timer_font_size"]) # Timer font size
    pygame.draw.rect(windowSurfaceObj, CONFIG["colors"]["grey"],
                     pygame.Rect(CONFIG["timer_offset"], y * CONFIG["lane_height"], CONFIG["width"], CONFIG["lane_height"]))

    if len(msg) > 5:
        if col == 0:
            msgSurfaceObj = fontObj.render(msg, False, CONFIG["colors"]["red"])
        elif col == 1:
            msgSurfaceObj = fontObj.render(msg, False, CONFIG["colors"]["yellow"])
        elif col == 2:
            msgSurfaceObj = fontObj.render(msg, False, CONFIG["colors"]["green"])
    else:
        msgSurfaceObj = fontObj.render(msg, False, CONFIG["colors"]["white"])

    msgRectobj = msgSurfaceObj.get_rect()
    if len(msg) > 5:
        msgRectobj.topleft = (CONFIG["timer_offset"] + int(CONFIG["height"]/1.5), y * CONFIG["lane_height"])
    else:
        msgRectobj.topleft = (CONFIG["timer_offset"] + 2, y * CONFIG["lane_height"])

    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
    pygame.display.update()

# Main initialization
init_gpio()
init_pygame()

# Create lane objects
lanes = [Lane(CONFIG["start_switches"][i], CONFIG["stop_switches"][i], i + 1) for i in range(3)]

# Read high scores from file
high_scores = read_high_scores()

# Initialize scroll_position for scrolling high scores
scroll_position = CONFIG["width"]

# Displaying the title
fontObj = pygame.font.Font(CONFIG["title_font"], CONFIG["title_font_size"]) # Title font size
msgSurfaceObj = fontObj.render("Climbing Wall Timers", False, CONFIG["colors"]["white"])
msgRectobj = msgSurfaceObj.get_rect()
msgRectobj.topleft = (CONFIG["timer_offset"] + 2, 0)
windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)

# Displaying initial labels and timers
display("Lane 1:", 1, 0)
display("Lane 2:", 2, 0)
display("Lane 3:", 3, 0)
display("00:00.0", 1, 1)
display("00:00.0", 2, 1)
display("00:00.0", 3, 1)
pygame.display.update()

# Main loop and other logic
# Define last_reset_time for debouncing
last_reset_time = 0
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                GPIO.cleanup()
                sys.exit()

        pygame.draw.rect(windowSurfaceObj, CONFIG["colors"]["black"], pygame.Rect(0, int(CONFIG["height"]/8), int(CONFIG["width"]/3), int(CONFIG["height"]/7) * 10))
        scroll_high_scores()

        for lane in lanes:
            lane.handle_stopwatch()

        # Handling reset switch with debouncing
        if GPIO.input(CONFIG["reset_switch"]) == 0 and pygame.time.get_ticks() - last_reset_time > CONFIG["debounce_time"]:
            last_reset_time = pygame.time.get_ticks()
            for lane in lanes:
                lane.run = 0
                lane.s = 0
                lane.m = 0
                lane.timer = time.time()
                display("00:00.0", lane.y, 1)
            stop_sound.play()

        pygame.display.update()
        pygame.time.delay(10)

except Exception as e:
    with open('error_log.txt', 'a') as file:
        file.write(str(datetime.datetime.now()) + '\n')
        file.write(str(e) + '\n')
        traceback.print_exc(file=file)
        file.write('\n')
finally:
    pygame.quit()
    GPIO.cleanup()
