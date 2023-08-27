#!/usr/bin/env python3

# Importing required libraries for GUI, time handling, and GPIO operations
import pygame, sys
import time
import RPi.GPIO as GPIO
import traceback
import datetime

# Function to read high scores from a file
def read_high_scores():
    try:
        with open('high_scores.txt', 'r') as file:
            # Convert "MM:SS.S" to seconds
            return [convert_to_seconds(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return [0] * 10

# Function to write high scores to a file
def write_high_scores(scores):
    with open('high_scores.txt', 'w') as file:
        for score in scores:
            # Convert seconds to "MM:SS.S" format
            file.write(convert_to_str(score) + '\n')

# Convert time in seconds to "MM:SS.S" format
def convert_to_str(seconds):
    minutes, remainder = divmod(int(seconds), 60)
    return f"{minutes:02d}:{remainder:04.1f}"

# Convert time in "MM:SS.S" format to seconds
def convert_to_seconds(time_str):
    minutes, seconds = map(float, time_str.split(":"))
    return minutes * 60 + seconds


# Function to update high scores
def update_high_scores(score):
    global high_scores  # Use the global variable high_scores
    high_scores.append(score)  # Add new score
    high_scores.sort(reverse=True)  # Sort scores in descending order
    high_scores = high_scores[:10]  # Keep the top 10 scores
    write_high_scores(high_scores)  # Write updated scores to file

# Function to display messages on the screen
def display(msg, y, col):
    # Define font and rectangle for the message
    fontObj = pygame.font.Font('freesansbold.ttf', int(height/5))
    pygame.draw.rect(windowSurfaceObj, greyColor, pygame.Rect(int(height/1.6), y * int(height/4), width, int(height/5)))
    
    # Choose color based on length of message and color index provided
    if len(msg) > 5:
        if col == 0:
            msgSurfaceObj = fontObj.render(msg, False, redColor)
        elif col == 1:
            msgSurfaceObj = fontObj.render(msg, False, yellowColor)
        elif col == 2:
            msgSurfaceObj = fontObj.render(msg, False, greenColor)
    else:
        msgSurfaceObj = fontObj.render(msg, False, whiteColor)

    # Position the message
    msgRectobj = msgSurfaceObj.get_rect()
    if len(msg) > 5:
        msgRectobj.topleft = (int(height/1.5), y * int(height/4))
    else:
        msgRectobj.topleft = (2, y * int(height/4))

    # Display the message and update the screen
    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
    pygame.display.update()

# Function to handle stopwatch logic
def handle_stopwatch(start_switch, stop_switch, run, s, m, timer, last_displayed_time, y, state):
    max_time = 59  # Maximum time in seconds for each minute on the stopwatch
    
    # State: 0 = reset, 1 = running, 2 = stopped
    # If the state is reset and not running, display 00:00.0
    if state == 0 and run == 0:
        display("00:00.0", y, 2)
    
    # If the start button is pressed and at least 1 second has passed since last press
    if GPIO.input(start_switch) == 0 and time.time() - timer > 1:
        # Handling state transitions
        if state == 1:
            run = 0
            state = 0
        elif state == 2:
            state = 1
            run = 1
        else:
            state = 1
            run = 1

        # Reset seconds and minutes, record the current time, and display 00:00.0
        s = 0
        m = 0
        timer = time.time()
        display("00:00.0", y, 1)

    # If stop button is pressed while the timer is running
    if GPIO.input(stop_switch) == 0 and run == 1:
        run = 0  # Stop running
        state = 2  # Set state to stopped
        stop_sound.play()  # Play stop sound
        update_high_scores(s + m * 60)  # Update high scores

    # Return updated variables
    return run, s, m, timer, last_displayed_time, state

# Screen dimensions
width = 1920
height = 1080

# Initialize Raspberry Pi's GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Define GPIO pins for start and stop switches and reset switch
start_switch1 = 36
start_switch2 = 38
start_switch3 = 40
stop_switch1 = 16
stop_switch2 = 18
stop_switch3 = 22
reset_switch = 24

# Configure GPIO pins as input with pull-up resistors
GPIO.setup(start_switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reset_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize pygame and its mixer
pygame.init()
pygame.mixer.init()

# Load the stop sound
stop_sound = pygame.mixer.Sound('stop_sound.wav')

# Create a fullscreen window
windowSurfaceObj = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Read high scores from file
high_scores = read_high_scores()

# Define colors
redColor = pygame.Color(255, 0, 0)
greyColor = pygame.Color(50, 50, 50)
whiteColor = pygame.Color(250, 250, 250)
blackColor = pygame.Color(0, 0, 0)
yellowColor = pygame.Color(255, 255, 0)

# Display title on screen
fontObj = pygame.font.Font('freesansbold.ttf', int(height/10))
msgSurfaceObj = fontObj.render("Climbing Wall Timers", False, whiteColor)
msgRectobj = msgSurfaceObj.get_rect()
msgRectobj.topleft = (2, 0)
windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)

# Display initial labels and timers
display("Lane 1:", 1, 0)
display("Lane 2:", 2, 0)
display("Lane 3:", 3, 0)
display("00:00.0", 1, 1)
display("00:00.0", 2, 1)
display("00:00.0", 3, 1)

# Update the display
pygame.display.update()

# Initialize variables for timers
run1 = 0
run2 = 0
run3 = 0
s1 = 0
s2 = 0
s3 = 0
m1 = 0
m2 = 0
m3 = 0
state1 = 0
state2 = 0
state3 = 0
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
            # If the ESC key is pressed, exit the program
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                GPIO.cleanup()
                sys.exit()

        # Handle each stopwatch
        run1, s1, m1, timer1, last_displayed_time1, state1 = handle_stopwatch(start_switch1, stop_switch1, run1, s1, m1, timer1, last_displayed_time1, 1, state1)
        run2, s2, m2, timer2, last_displayed_time2, state2 = handle_stopwatch(start_switch2, stop_switch2, run2, s2, m2, timer2, last_displayed_time2, 2, state2)
        run3, s3, m3, timer3, last_displayed_time3, state3 = handle_stopwatch(start_switch3, stop_switch3, run3, s3, m3, timer3, last_displayed_time3, 3, state3)

        # If reset switch is pressed, reset all timers
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
            state1 = 0
            state2 = 0
            state3 = 0
            timer1 = time.time()
            timer2 = time.time()
            timer3 = time.time()
            display("00:00.0", 1, 1)
            display("00:00.0", 2, 1)
            display("00:00.0", 3, 1)
            stop_sound.play()

        # Update the display
        pygame.display.update()

except Exception as e:
    # Log errors to a file
    with open('error_log.txt', 'a') as file:
        file.write(str(datetime.datetime.now()) + '\n')
        file.write(str(e) + '\n')
        traceback.print_exc(file=file)
        file.write('\n')
finally:
    # Make sure to release resources even if an exception occurs
    pygame.quit()
    GPIO.cleanup()
