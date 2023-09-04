#!/usr/bin/env python3

import pygame
import time
import RPi.GPIO as GPIO
import datetime
from pygame.locals import KEYDOWN
from pygame import Rect

def read_high_scores(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return ["00:00.00", "00:00.00", "00:00.00"]

def write_high_scores(filename, scores):
    with open(filename, 'w') as f:
        for score in scores:
            f.write(f"{score}\n")

pygame.init()
pygame.mixer.init()

stop_sound1 = pygame.mixer.Sound("stop_sound1.wav")
stop_sound2 = pygame.mixer.Sound("stop_sound2.wav")
stop_sound3 = pygame.mixer.Sound("stop_sound3.wav")

width = 1920
height = 1080

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

start_switch1 = 40
start_switch2 = 38
start_switch3 = 36
stop_switch1 = 22
stop_switch2 = 18
stop_switch3 = 16
reset_switch = 24

GPIO.setup(start_switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop_switch3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reset_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

windowSurfaceObj = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

high_scores = read_high_scores("high_scores.txt")

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
last_displayed_time1 = "00:00.00"
last_displayed_time2 = "00:00.00"
last_displayed_time3 = "00:00.00"
refresh_rate = 0.01

while True:
    # Stopwatch 1
    if (GPIO.input(start_switch1) == 0 and time.time() - timer1 > 1) or run1 == 1:
        if GPIO.input(start_switch1) == 0 and run1 == 1 and time.time() - start_time1 > 1:
            run1 = 0
            s1 = 0
            timer1 = time.time()
        elif run1 == 0 and s1 == 0:
            start_time1 = time.time()
            run1 = 1
        elif run1 == 0 and s1 > 0:
            start_time1 = time.time()
            run1 = 1

        if run1 == 1:
            now = time.time() - start_time1
            m1, s1 = divmod(now, 60)
            time1_str = f"{int(m1):02d}:{s1:05.2f}"
            if last_displayed_time1 != time1_str:
                last_displayed_time1 = time1_str

    # Stopwatch 2
    if (GPIO.input(start_switch2) == 0 and time.time() - timer2 > 1) or run2 == 1:
        if GPIO.input(start_switch2) == 0 and run2 == 1 and time.time() - start_time2 > 1:
            run2 = 0
            s2 = 0
            timer2 = time.time()
        elif run2 == 0 and s2 == 0:
            start_time2 = time.time()
            run2 = 1
        elif run2 == 0 and s2 > 0:
            start_time2 = time.time()
            run2 = 1

        if run2 == 1:
            now = time.time() - start_time2
            m2, s2 = divmod(now, 60)
            time2_str = f"{int(m2):02d}:{s2:05.2f}"
            if last_displayed_time2 != time2_str:
                last_displayed_time2 = time2_str

    # Stopwatch 3
    if (GPIO.input(start_switch3) == 0 and time.time() - timer3 > 1) or run3 == 1:
        if GPIO.input(start_switch3) == 0 and run3 == 1 and time.time() - start_time3 > 1:
            run3 = 0
            s3 = 0
            timer3 = time.time()
        elif run3 == 0 and s3 == 0:
            start_time3 = time.time()
            run3 = 1
        elif run3 == 0 and s3 > 0:
            start_time3 = time.time()
            run3 = 1

        if run3 == 1:
            now = time.time() - start_time3
            m3, s3 = divmod(now, 60)
            time3_str = f"{int(m3):02d}:{s3:05.2f}"
            if last_displayed_time3 != time3_str:
                last_displayed_time3 = time3_str

    # Check for new high scores (low times)
    if (GPIO.input(stop_switch1) == 0 and run1 == 1) or m1 == int(max_time):
        run1 = 0
        stop_sound1.play()
        if time1_str < high_scores[0]:
            high_scores[0] = time1_str
            write_high_scores("high_scores.txt", high_scores)

    if (GPIO.input(stop_switch2) == 0 and run2 == 1) or m2 == int(max_time):
        run2 = 0
        stop_sound2.play()
        if time2_str < high_scores[1]:
            high_scores[1] = time2_str
            write_high_scores("high_scores.txt", high_scores)

    if (GPIO.input(stop_switch3) == 0 and run3 == 1) or m3 == int(max_time):
        run3 = 0
        stop_sound3.play()
        if time3_str < high_scores[2]:
            high_scores[2] = time3_str
            write_high_scores("high_scores.txt", high_scores)

    # Update the display
    pygame.display.update()
    time.sleep(refresh_rate)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == 27:  # Escape key
                pygame.quit()
