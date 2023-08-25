# Climbing Wall Timer Script
#
# This script is designed to control and manage a climbing wall timer system using a Raspberry Pi. The functionality includes:
# 1. Handling multiple lanes with individual start, stop, and reset buttons.
# 2. Displaying the current time for each lane and managing the stopwatch behavior.
# 3. Storing and scrolling the high scores.
# 4. Allowing customization of various parameters like screen size, colors, fonts, and sounds through a configuration file (config.ini).
# 5. Providing a clean and user-friendly interface for climbing wall participants and observers.
# 6. Logging errors and exceptions to a file for troubleshooting.
#
# Dependencies:
# - pygame for rendering the graphical interface
# - RPi.GPIO for interacting with the Raspberry Pi's GPIO pins
# - time, datetime for time handling
# - configparser for reading the configuration file
# - traceback for handling exceptions
#
# The script is intended to be run on a Raspberry Pi with the appropriate hardware setup, including buttons for controlling the timers,
# and a 1080p display for output.

import pygame, sys  # Import the pygame library for game development and sys for system functions
import time         # Import the time library to handle time-related tasks
import RPi.GPIO as GPIO  # Import the Raspberry Pi GPIO library to control the GPIO pins
import traceback    # Import traceback to handle and print exceptions
import datetime     # Import datetime to handle date and time functions
import configparser # Import configparser to read INI configuration files

# Load configuration from config.ini
config = configparser.ConfigParser()  # Create a configparser object
config.read('config.ini')             # Read the configuration from 'config.ini' file

# Configuration dictionary
CONFIG = {
    "width": int(config.get('General', 'width')),                                      # Screen width
    "height": int(config.get('General', 'height')),                                    # Screen height
    "start_switches": list(map(int, config.get('General', 'start_switches').split(','))), # Start switches for lanes
    "stop_switches": list(map(int, config.get('General', 'stop_switches').split(','))),  # Stop switches for lanes
    "reset_switch": int(config.get('General', 'reset_switch')),                        # Reset switch
    "debounce_time": int(config.get('General', 'debounce_time')),                      # Debounce time for buttons
    "title_font_size": int(config.get('General', 'title_font_size')),                  # Title font size
    "timer_font_size": int(config.get('General', 'timer_font_size')),                  # Timer font size
    "high_score_font_size": int(config.get('General', 'high_score_font_size')),        # High score font size
    "colors": {  # Colors configuration
        "red": pygame.Color(*map(int, config.get('Colors', 'red').split(','))),
        "grey": pygame.Color(*map(int, config.get('Colors', 'grey').split(','))),
        "white": pygame.Color(*map(int, config.get('Colors', 'white').split(','))),
        "black": pygame.Color(*map(int, config.get('Colors', 'black').split(','))),
        "yellow": pygame.Color(*map(int, config.get('Colors', 'yellow').split(','))),
        "green": pygame.Color(*map(int, config.get('Colors', 'green').split(','))),
    },
    "title_font": config.get('Fonts', 'title_font'),          # Title font
    "timer_font": config.get('Fonts', 'timer_font'),          # Timer font
    "high_score_font": config.get('Fonts', 'high_score_font'),# High score font
    "stop_sound": config.get('Sounds', 'stop_sound'),         # Stop sound file
}

# Class definition for a Lane
class Lane:
    def __init__(self, start_switch, stop_switch, y): # Constructor for the Lane class
        self.run = 0                    # Initialize running state to 0 (stopped)
        self.s = 0                      # Initialize seconds to 0
        self.m = 0                      # Initialize minutes to 0
        self.timer = time.time()        # Initialize timer with the current time
        self.last_displayed_time = "00:00.0" # Initialize the last displayed time
        self.last_start_time = 0        # Initialize the last start time
        self.last_stop_time = 0         # Initialize the last stop time
        self.start_switch = start_switch# Assign the start switch
        self.stop_switch = stop_switch  # Assign the stop switch
        self.y = y                      # Assign the y position

    def handle_stopwatch(self):
        global stop_sound  # Accessing the global variable for the stop sound

        # Handle stopwatch running state and display time
        if self.run == 1:  # If the timer is running
            elapsed_time = time.time() - self.timer  # Calculate the elapsed time
            self.m, self.s = divmod(elapsed_time, 60)  # Divide the elapsed time into minutes and seconds
            self.s, ms = divmod(self.s, 1)  # Divide the seconds into whole seconds and milliseconds
            current_time_str = f"{int(self.m):02}:{int(self.s):02}.{int(ms*10)}"  # Format the time string
            if current_time_str != self.last_displayed_time:  # If the time has changed since the last display
                display(current_time_str, self.y, 2)  # Display the current time
                self.last_displayed_time = current_time_str  # Update the last displayed time
        elif time.time() - self.timer > 1 and self.run == 0 and self.s == 0:
            display("00:00.0", self.y, 2)  # If the timer is not running and has been stopped for more than 1 second, display "00:00.0"

        # Handle start button press
        if GPIO.input(self.start_switch) == 0 and pygame.time.get_ticks() - self.last_start_time > CONFIG["debounce_time"]:
            self.last_start_time = pygame.time.get_ticks()  # Record the time of the last start button press
            if self.run == 0:  # If the timer is not running
                self.run = 1  # Start the timer
                self.timer = time.time()  # Record the start time
            else:  # If the timer is already running
                self.run = 0  # Stop the timer
                self.s = 0  # Reset the seconds
                self.m = 0  # Reset the minutes
                self.timer = time.time()  # Reset the timer

        # Handle stop button press
        if GPIO.input(self.stop_switch) == 0 and self.run == 1 and pygame.time.get_ticks() - self.last_stop_time > CONFIG["debounce_time"]:
            self.last_stop_time = pygame.time.get_ticks()  # Record the time of the last stop button press
            total_time = self.s + self.m * 60  # Calculate the total time in seconds
            self.run = 0  # Stop the timer
            self.s = 0  # Reset the seconds
            self.m = 0  # Reset the minutes
            self.timer = time.time()  # Reset the timer
            stop_sound.play()  # Play the stop sound
            update_high_scores(total_time)  # Update the high scores with the total time


def init_gpio():
    GPIO.setmode(GPIO.BOARD)  # Set the GPIO mode to BOARD numbering scheme
    GPIO.setwarnings(False)   # Disable warnings if GPIO channels are already in use
    for pin in CONFIG["start_switches"] + CONFIG["stop_switches"] + [CONFIG["reset_switch"]]:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up each pin as an input with a pull-up resistor

def init_pygame():
    global windowSurfaceObj, stop_sound  # Declare global variables for window surface and stop sound
    pygame.init()  # Initialize all imported pygame modules
    pygame.mixer.init()  # Initialize the mixer module for sound playback
    windowSurfaceObj = pygame.display.set_mode((CONFIG["width"], CONFIG["height"]), pygame.FULLSCREEN)  # Set up the display window in fullscreen mode with specified width and height
    stop_sound = pygame.mixer.Sound(CONFIG["stop_sound"])  # Load the stop sound from the file specified in CONFIG


# High Scores Functions

# Function to read high scores from a text file
def read_high_scores():
    try:  # Try block to handle the case where the file might not exist
        scores = []  # Initialize an empty list to store the scores
        with open('high_scores.txt', 'r') as file:  # Open the high_scores.txt file for reading
            for line in file.readlines():  # Iterate through each line in the file
                minutes, rest = line.strip().split(':')  # Split the line at the colon, separating minutes from the rest
                seconds, tenths = rest.split('.')  # Split the rest of the line at the dot, separating seconds and tenths of a second
                total_seconds = float(minutes) * 60 + float(seconds) + float(tenths) / 10  # Convert to total seconds
                scores.append(total_seconds)  # Append the total seconds to the scores list
        return scores  # Return the list of scores
    except FileNotFoundError:  # Handle the case where the file does not exist
        return [0] * 10  # Return a list of ten zeros

# Function to write high scores to a text file
def write_high_scores(scores):
    with open('high_scores.txt', 'w') as file:  # Open the high_scores.txt file for writing
        for score in scores:  # Iterate through each score in the scores list
            formatted_score = format_high_score(score)  # Format the score using the format_high_score function
            file.write(formatted_score + '\n')  # Write the formatted score to the file followed by a newline character

# Function to update the high scores list with a new score
def update_high_scores(score):
    global high_scores  # Access the global high_scores variable
    high_scores.append(score)  # Append the new score to the high_scores list
    high_scores.sort()  # Sort the high_scores list in ascending order
    high_scores = high_scores[:10]  # Keep only the top 10 scores
    write_high_scores(high_scores)  # Write the updated high_scores list to the file

# Function to format the high scores in "MM:SS.s" format
def format_high_score(score_seconds):
    minutes, seconds = divmod(score_seconds, 60)  # Divide the score_seconds into minutes and seconds
    seconds, tenths = divmod(seconds, 1)  # Divide the seconds into whole seconds and tenths of a second
    tenths *= 10  # Multiply tenths by 10 to get the correct value
    return f"{int(minutes):02}:{int(seconds):02}.{int(tenths)}"  # Return the formatted string in "MM:SS.s" format

def scroll_high_scores():                          # Define a function to scroll the high scores on the screen
    global scroll_position                         # Declare scroll_position as a global variable, so changes will affect the variable outside of this function
    fontObj = pygame.font.Font(CONFIG["high_score_font"], CONFIG["high_score_font_size"]) # Create a font object using the high score font and size specified in the configuration
    y_position = int(CONFIG["height"]/8)           # Calculate the y-position for the high scores, at one-eighth the height of the display
    text = "High Scores: " + " | ".join([f"{idx+1}. {format_high_score(score)}" for idx, score in enumerate(high_scores)]) # Create the text string for high scores, formatted as "1. MM:SS.s | 2. MM:SS.s | ..."
    msgSurfaceObj = fontObj.render(text, False, CONFIG["colors"]["red"]) # Render the text string in red color using the font object
    msgRectobj = msgSurfaceObj.get_rect()          # Get the rectangular area of the rendered text
    msgRectobj.topleft = (scroll_position, y_position) # Set the top-left position of the rectangular area, using scroll_position for the x-coordinate
    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj) # Draw the rendered text on the window surface at the specified position
    scroll_position -= 5                           # Decrement the scroll_position by 5, to move the text to the left
    if scroll_position < -msgRectobj.width:        # Check if the text has completely scrolled off the screen to the left
        scroll_position = CONFIG["width"]          # If it has, reset scroll_position to the width of the display, so the text starts scrolling again from the right


# Display Function
def display(msg, y, col):
    height = CONFIG["height"]  # Get height from the configuration
    width = CONFIG["width"]    # Get width from the configuration
    greyColor = CONFIG["colors"]["grey"] # Get grey color from the configuration
    lane_height = int(height / 5)  # Calculate the height of each lane as one-fifth of the total height
    fontObj = pygame.font.Font(CONFIG["timer_font"], lane_height) # Create the font object
    pygame.draw.rect(windowSurfaceObj, greyColor, pygame.Rect(int(height/1.6), (y - 1) * lane_height, width, lane_height)) # Draw the rectangle

    if len(msg) > 5:  # If the message length is greater than 5
        if col == 0:  # If the color code is 0
            msgSurfaceObj = fontObj.render(msg, False, CONFIG["colors"]["red"])  # Render the message in red
        elif col == 1:  # If the color code is 1
            msgSurfaceObj = fontObj.render(msg, False, CONFIG["colors"]["yellow"])  # Render the message in yellow
        elif col == 2:  # If the color code is 2
            msgSurfaceObj = fontObj.render(msg, False, CONFIG["colors"]["green"])  # Render the message in green
    else:  # If the message length is 5 or less
        msgSurfaceObj = fontObj.render(msg, False, CONFIG["colors"]["white"])  # Render the message in white

    msgRectobj = msgSurfaceObj.get_rect()  # Get the rectangular area of the rendered message
    if len(msg) > 5:  # If the message length is greater than 5
        msgRectobj.topleft = (int(height/1.6) + 2, (y - 1) * lane_height)  # Set the top-left position
    else:  # If the message length is 5 or less
        msgRectobj.topleft = (int(height/1.6) + 2, (y - 1) * lane_height)  # Set the top-left position

    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)  # Draw the message on the window surface
    pygame.display.update()  # Update the display to show the new content

# Rest of the code remains the same...


# Main initialization
init_gpio()  # Call the function to initialize the GPIO pins
init_pygame()  # Call the function to initialize Pygame

# Create lane objects
lanes = [Lane(CONFIG["start_switches"][i], CONFIG["stop_switches"][i], i + 1) for i in range(3)]  # Create lanes using the start and stop switches

# Read high scores from file
high_scores = read_high_scores()  # Call the function to read the high scores from the file

# Initialize scroll_position for scrolling high scores
scroll_position = CONFIG["width"]  # Set the initial scroll position to the width of the display

# Displaying the title
fontObj = pygame.font.Font(CONFIG["title_font"], CONFIG["title_font_size"])  # Create a font object for the title
msgSurfaceObj = fontObj.render("Climbing Wall Timers", False, CONFIG["colors"]["white"])  # Render the title in white
msgRectobj = msgSurfaceObj.get_rect()  # Get the rectangular area of the rendered title
msgRectobj.topleft = (CONFIG["timer_offset"] + 2, 0)  # Set the top-left position of the title
windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)  # Draw the title on the window surface

# Displaying initial labels and timers
display("Lane 1:", 1, 0)  # Display the label for Lane 1
display("Lane 2:", 2, 0)  # Display the label for Lane 2
display("Lane 3:", 3, 0)  # Display the label for Lane 3
display("00:00.0", 1, 1)  # Display the initial timer for Lane 1
display("00:00.0", 2, 1)  # Display the initial timer for Lane 2
display("00:00.0", 3, 1)  # Display the initial timer for Lane 3
pygame.display.update()   # Update the display to show the initial content

# Main loop and other logic
# Define last_reset_time for debouncing
last_reset_time = 0  # Initialize the variable to store the time of the last reset

try:  # Try block to catch exceptions
    while True:  # Infinite loop to keep the program running
        for event in pygame.event.get():  # Iterate through all pygame events
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # If the event is a key press and the key is Escape
                pygame.quit()  # Quit pygame
                GPIO.cleanup()  # Clean up GPIO pins
                sys.exit()  # Exit the program

        # Draw a black rectangle covering a specific part of the screen
        pygame.draw.rect(windowSurfaceObj, CONFIG["colors"]["black"], pygame.Rect(0, int(CONFIG["height"]/8), int(CONFIG["width"]/3), int(CONFIG["height"]/7) * 10))
        scroll_high_scores()  # Call the function to scroll high scores

        for lane in lanes:  # Iterate through all lane objects
            lane.handle_stopwatch()  # Call the handle_stopwatch method for each lane

        # Handling reset switch with debouncing
        if GPIO.input(CONFIG["reset_switch"]) == 0 and pygame.time.get_ticks() - last_reset_time > CONFIG["debounce_time"]:
            last_reset_time = pygame.time.get_ticks()  # Update the time of the last reset
            for lane in lanes:  # Iterate through all lane objects
                lane.run = 0  # Stop the timer for the lane
                lane.s = 0  # Reset seconds for the lane
                lane.m = 0  # Reset minutes for the lane
                lane.timer = time.time()  # Reset the timer for the lane
                display("00:00.0", lane.y, 1)  # Display "00:00.0" for the lane
            stop_sound.play()  # Play the stop sound

        pygame.display.update()  # Update the display to show the changes
        pygame.time.delay(10)  # Delay for 10 milliseconds

except Exception as e:  # Catch any exceptions
    with open('error_log.txt', 'a') as file:  # Open the error_log.txt file for appending
        file.write(str(datetime.datetime.now()) + '\n')  # Write the current date and time
        file.write(str(e) + '\n')  # Write the exception message
        traceback.print_exc(file=file)  # Print the traceback to the file
        file.write('\n')  # Write a newline character
finally:
    pygame.quit()  # Quit pygame in the finally block to ensure it's called
    GPIO.cleanup()  # Clean up GPIO pins in the finally block to ensure it's called
