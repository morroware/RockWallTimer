#!/usr/bin/env python3

import pygame, sys
import time
import RPi.GPIO as GPIO
import datetime

width = 1920
height = 1080

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

start_switch1 = 36
start_switch2 = 38
start_switch3 = 40
stop_switch1 = 16
stop_switch2 = 18
stop_switch3 = 22
reset_switch = 24

GPIO.setup(start_switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reset_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
windowSurfaceObj = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

def display(msg, y, col):
    redColor = pygame.Color(255, 0, 0)
    greyColor = pygame.Color(50, 50, 50)
    whiteColor = pygame.Color(255, 255, 255)
    greenColor = pygame.Color(0, 255, 0)
    yellowColor = pygame.Color(255, 255, 0)

    fontObj = pygame.font.Font('freesansbold.ttf', int(height/5))
    pygame.draw.rect(windowSurfaceObj, greyColor, Rect(int(height/1.6), y * int(height/4), width, int(height/5)))

    if len(msg) > 5:
        if col == 0:
            msgSurfaceObj = fontObj.render(msg, False, redColor)
        elif col == 1:
            msgSurfaceObj = fontObj.render(msg, False, yellowColor)
        elif col == 2:
            msgSurfaceObj = fontObj.render(msg, False, greenColor)
    else:
        msgSurfaceObj = fontObj.render(msg, False, whiteColor)

    msgRectobj = msgSurfaceObj.get_rect()
    if len(msg) > 5:
        msgRectobj.topleft = (int(height/1.5), y * int(height/4))
    else:
        msgRectobj.topleft = (2, y * int(height/4))

    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
    pygame.display.update()

redColor = pygame.Color(255, 0, 0)
greyColor = pygame.Color(50, 50, 50)
whiteColor = pygame.Color(250, 250, 250)
blackColor = pygame.Color(0, 0, 0)

fontObj = pygame.font.Font('freesansbold.ttf', int(height/10))
msgSurfaceObj = fontObj.render("Climbing Wall Timers", False, whiteColor)
msgRectobj = msgSurfaceObj.get_rect()
msgRectobj.topleft = (2, 0)
windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)

fontObj = pygame.font.Font('freesansbold.ttf', int(height/5))
display("Easy:", 1, 0)
display("Hard:", 2, 0)
display("Med :", 3, 0)
display("00:00.0", 1, 1)
display("00:00.0", 2, 1)
display("00:00.0", 3, 1)

pygame.display.update()

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
max_time = 59

# Define variables to store the last displayed time for each stopwatch
last_displayed_time1 = "00:00.0"
last_displayed_time2 = "00:00.0"
last_displayed_time3 = "00:00.0"

while True:
    now = datetime.datetime.now()
    pygame.draw.rect(windowSurfaceObj, blackColor, Rect(0, int(height/8), int(width/3), int(height/7)))
    fontObj = pygame.font.Font('freesansbold.ttf', int(height/10))
    msgSurfaceObj = fontObj.render(str(now)[11:19], False, redColor)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (0, int(height/8))
    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)

    # Stopwatch 1
    if time.time() - timer1 > 1 and run1 == 0 and s1 == 0:
        display("00:00.0", 1, 2)

    if (GPIO.input(start_switch1) == 0 and time.time() - timer1 > 1) or run1 == 1:
        if GPIO.input(start_switch1) == 0 and run1 == 1 and time.time() - start_time1 > 1:
            run1 = 0
            display("00:00.0", 1, 1)
            s1 = 0
            timer1 = time.time()
        elif run1 == 0 and s1 == 0:
            start_time1 = time.time()
            run1 = 1
        elif run1 == 0 and s1 > 0:
            display("00:00.0", 1, 1)
            s1 = 0
            timer1 = time.time()

        if run1 == 1:
            now = time.time() - start_time1
            m1, s1 = divmod(now, 60)
            h1, m1 = divmod(m1, 60)
            msg = "%02d:%02d" % (m1, s1)
            psec = str(now - int(now))
            pstr = psec[1:3]
            msg = msg + str(pstr)

            # Update the display only when a new run starts or stops
            if last_displayed_time1 != msg:
                display(msg, 1, 0)
                last_displayed_time1 = msg  # Store the current time as the last displayed time




    # Stopwatch 2
    if time.time() - timer2 > 1 and run2 == 0 and s2 == 0:
        display("00:00.0", 2, 2)

    if (GPIO.input(start_switch2) == 0 and time.time() - timer2 > 1) or run2 == 1:
        if GPIO.input(start_switch2) == 0 and run2 == 1 and time.time() - start_time2 > 1:
            run2 = 0
            display("00:00.0", 2, 1)
            s2 = 0
            timer2 = time.time()
        elif run2 == 0 and s2 == 0:
            start_time2 = time.time()
            run2 = 1
        elif run2 == 0 and s2 > 0:
            display("00:00.0", 2, 1)
            s2 = 0
            timer2 = time.time()

        if run2 == 1:
            now = time.time() - start_time2
            m2, s2 = divmod(now, 60)
            h2, m2 = divmod(m2, 60)
            msg = "%02d:%02d" % (m2, s2)
            psec = str(now - int(now))
            pstr = psec[1:3]
            msg = msg + str(pstr)

            # Update the display only when a new run starts or stops
            if last_displayed_time2 != msg:
                display(msg, 2, 0)
                last_displayed_time2 = msg  # Store the current time as the last displayed time

    # Stopwatch 3
    if time.time() - timer3 > 1 and run3 == 0 and s3 == 0:
        display("00:00.0", 3, 2)

    if (GPIO.input(start_switch3) == 0 and time.time() - timer3 > 1) or run3 == 1:
        if GPIO.input(start_switch3) == 0 and run3 == 1 and time.time() - start_time3 > 1:
            run3 = 0
            display("00:00.0", 3, 1)
            s3 = 0
            timer3 = time.time()
        elif run3 == 0 and s3 == 0:
            start_time3 = time.time()
            run3 = 1
        elif run3 == 0 and s3 > 0:
            display("00:00.0", 3, 1)
            s3 = 0
            timer3 = time.time()

        if run3 == 1:
            now = time.time() - start_time3
            m3, s3 = divmod(now, 60)
            h3, m3 = divmod(m3, 60)
            msg = "%02d:%02d" % (m3, s3)
            psec = str(now - int(now))
            pstr = psec[1:3]
            msg = msg + str(pstr)

            # Update the display only when a new run starts or stops
            if last_displayed_time3 != msg:
                display(msg, 3, 0)
                last_displayed_time3 = msg  # Store the current time as the last displayed time

    # Check for stop buttons
    if (GPIO.input(stop_switch1) == 0 and run1 == 1) or m1 == int(max_time):
        run1 = 0

    if (GPIO.input(stop_switch2) == 0 and run2 == 1) or m2 == int(max_time):
        run2 = 0

    if (GPIO.input(stop_switch3) == 0 and run3 == 1) or m3 == int(max_time):
        run3 = 0

    # Master stop and reset
    if GPIO.input(reset_switch) == 0 and (run1 == 1 or run2 == 1 or run3 == 1):
        run1 = 0
        run2 = 0
        run3 = 0
        time.sleep(0.25)

    if GPIO.input(reset_switch) == 0 and run1 == 0 and run2 == 0 and run3 == 0:
        run1 = 0
        run2 = 0
        run3 = 0
        s1 = 0
        s2 = 0
        s3 = 0
        display("00:00.0", 1, 1)
        display("00:00.0", 2, 1)
        display("00:00.0", 3, 1)
        timer1 = time.time()
        timer2 = time.time()
        timer3 = time.time()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == 27:
                pygame.quit()
