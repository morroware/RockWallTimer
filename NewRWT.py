#!/usr/bin/env python3

# Importing required libraries
import pygame, sys
import time
import RPi.GPIO as GPIO
import traceback
import datetime

# Setting the screen width and height
width = 1920
height = 1080

# Global variable to track the horizontal position of the high scores
scroll_position = 0

# Function to read high scores from a file
def read_high_scores():
    try:
        with open('high_scores.txt', 'r') as file:
            return [float(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return [0] * 10

# Function to write high scores to a file
def write_high_scores(scores):
    with open('high_scores.txt', 'w') as file:
        for score in scores:
            file.write(str(score) + '\n')

# Function to update high scores
def update_high_scores(score):
    global high_scores
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:10]
    write_high_scores(high_scores)

# Function to render and scroll the high scores
def scroll_high_scores():
    global high_scores
    global scroll_position
    fontObj = pygame.font.Font('freesansbold.ttf', int(height/20))
    y_position = int(height/8)
    text = "High Scores: " + " | ".join([f"{idx+1}. {score}" for idx, score in enumerate(high_scores)])
    msgSurfaceObj = fontObj.render(text, False, redColor)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (scroll_position, y_position)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
    scroll_position -= 5  # Speed of scrolling
    if scroll_position < -msgRectobj.width:
        scroll_position = width  # Reset to the right side of the screen

# Function to display messages on the screen
def display(msg, y, col):
    fontObj = pygame.font.Font('freesansbold.ttf', int(height/5))
    pygame.draw.rect(windowSurfaceObj, greyColor, pygame.Rect(int(height/1.6), y * int(height/4), width, int(height/5)))

    if len(msg) > 5:
        if col == 0:
            msgSurfaceObj = fontObj.render(msg, False, redColor)
        elif col == 1:
            msgSurfaceObj = fontObj.render(msg, False, yellowColor)
        elif col == 2:
            msgSurfaceObj = fontObj.render(msg, False, greenColor)  # Corrected color
    else:
        msgSurfaceObj = fontObj.render(msg, False, whiteColor)

    msgRectobj = msgSurfaceObj.get_rect()
    if len(msg) > 5:
        msgRectobj.topleft = (int(height/1.5), y * int(height/4))
    else:
        msgRectobj.topleft = (2, y * int(height/4))

    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
    pygame.display.update()

# Function to handle stopwatch logic, including displaying the running time
def handle_stopwatch(start_switch, stop_switch, run, s, m, timer, last_displayed_time, y):
    max_time = 59

    # Check if the stopwatch is already running (run == 1)
    if run == 1:
        elapsed_time = time.time() - timer
        m, s = divmod(elapsed_time, 60)
        s, ms = divmod(s, 1)
        current_time_str = f"{int(m):02}:{int(s):02}.{int(ms*10)}"
        if current_time_str != last_displayed_time:
            display(current_time_str, y, 2)  # Display current time at position y with display mode 2
            last_displayed_time = current_time_str

    # Check if the time has passed 1 second and the stopwatch is not running (run == 0) and seconds (s) is 0
    elif time.time() - timer > 1 and run == 0 and s == 0:
        display("00:00.0", y, 2)  # Display "00:00.0" at position y with display mode 2

    # Check if the start button is pressed (start_switch == 0) and time has passed 1 second
    if GPIO.input(start_switch) == 0 and time.time() - timer > 1:
        if run == 0:
            run = 1
            timer = time.time()
        else:
            run = 0  # Reset the stopwatch and start anew
            display("00:00.0", y, 1)  # Display "00:00.0" at position y with display mode 1
            s = 0
            m = 0
            timer = time.time()

    # Check if the stop button is pressed (stop_switch == 0)
    if GPIO.input(stop_switch) == 0 and run == 1:
        total_time = s + m * 60  # Calculate total time before resetting
        run = 0
        display("00:00.0", y, 1)  # Display "00:00.0" at position y with display mode 1
        s = 0
        m = 0
        timer = time.time()
        stop_sound.play()  # Play a stop sound (assuming this is a sound object)
        update_high_scores(total_time)  # Update high scores based on total time
        
    return run, s, m, timer, last_displayed_time

# Setting up the Raspberry Pi's GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Defining GPIO pins for start and stop switches for three timers and a reset switch
start_switch1 = 36
start_switch2 = 38
start_switch3 = 40
stop_switch1 = 16
stop_switch2 = 18
stop_switch3 = 22
reset_switch = 24

# Configuring the GPIO pins as input with pull-up resistors
GPIO.setup(start_switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reset_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initializing pygame and the pygame mixer
pygame.init()
pygame.mixer.init()

# Loading the stop sound
stop_sound = pygame.mixer.Sound('stop_sound.wav')

# Creating a fullscreen window
windowSurfaceObj = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Read high scores from file
high_scores = read_high_scores()

# Defining colors
redColor = pygame.Color(255, 0, 0)
greyColor = pygame.Color(50, 50, 50)
whiteColor = pygame.Color(250, 250, 250)
blackColor = pygame.Color(0, 0, 0)
yellowColor = pygame.Color(255, 255, 0)
greenColor = pygame.Color(0, 255, 0) # Added green color definition

# Displaying the title
fontObj = pygame.font.Font('freesansbold.ttf', int(height/10))
msgSurfaceObj = fontObj.render("Climbing Wall Timers", False, whiteColor)
msgRectobj = msgSurfaceObj.get_rect()
msgRectobj.topleft = (2, 0)
windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)

# Displaying initial labels and timers
fontObj = pygame.font.Font('freesansbold.ttf', int(height/5))
display("Easy:", 1, 0)
display("Hard:", 2, 0)
display("Med :", 3, 0)
display("00:00.0", 1, 1)
display("00:00.0", 2, 1)
display("00:00.0", 3, 1)

pygame.display.update()

# Initializing variables for timers
run1 = 0
run2 = 0
run3 = 0
s1 = 0
s2 = 0
s3 = 0
m1 = 0
m2 = 0
m3 = 0
timer1 = time.time()
timer2 = time.time()
timer3 = time.time()
last_displayed_time1 = "00:00.0"
last_displayed_time2 = "00:00.0"
last_displayed_time3 = "00:00.0"

# Main loop
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Press ESC to exit
                pygame.quit()
                GPIO.cleanup()  # Cleanup GPIO resources
                sys.exit()

        # Clearing the screen
        pygame.draw.rect(windowSurfaceObj, blackColor, pygame.Rect(0, int(height/8), int(width/3), int(height/7) * 10))

        # Render and scroll the high scores
        scroll_high_scores()

        # Handling the three stopwatches
        run1, s1, m1, timer1, last_displayed_time1 = handle_stopwatch(start_switch1, stop_switch1, run1, s1, m1, timer1, last_displayed_time1, 1)
        run2, s2, m2, timer2, last_displayed_time2 = handle_stopwatch(start_switch2, stop_switch2, run2, s2, m2, timer2, last_displayed_time2, 2)
        run3, s3, m3, timer3, last_displayed_time3 = handle_stopwatch(start_switch3, stop_switch3, run3, s3, m3, timer3, last_displayed_time3, 3)

        # Handling reset switch
        if GPIO.input(reset_switch) == 0:
            run1 = 0
            run2 = 0
            run3 = 0
            s1 = 0
            s2 = 0
            s3 = 0
            m1 = 0
            m2 = 0
            m3 = 0
            timer1 = time.time()
            timer2 = time.time()
            timer3 = time.time()
            display("00:00.0", 1, 1)
            display("00:00.0", 2, 1)
            display("00:00.0", 3, 1)
            stop_sound.play()

        # Updating the display
        pygame.display.update()

except Exception as e:
    # Logging errors to a file
    with open('error_log.txt', 'a') as file:
        file.write(str(datetime.datetime.now()) + '\n')
        file.write(str(e) + '\n')
        traceback.print_exc(file=file)
        file.write('\n')
finally:
    # Ensure that resources are released even if an exception occurs
    pygame.quit()
    GPIO.cleanup()
