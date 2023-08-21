
# Rock Climbing Wall Timers

This project provides a timer system for a rock climbing wall with three lanes (Easy, Medium, Hard). Each lane has start and stop buttons, and the system keeps track of the top ten high scores.

## Features

- Three separate timers for different difficulty levels.
- Start and stop buttons for each lane.
- Sound notification at the top of each lane.
- Displays the last top ten high scores.
- Full-screen display using Pygame.
- Error logging to a file.

## Requirements

- Raspberry Pi
- Python 3
- Pygame
- RPi.GPIO

# How to Use the Rock Climbing Wall Timers Script

This guide provides step-by-step instructions on how to set up and use the rock climbing wall timers script.

## Step 1: Hardware Setup

### Connect the Start and Stop Buttons
- Connect the start buttons for the Easy, Medium, and Hard lanes to the GPIO pins 36, 38, and 40 respectively on the Raspberry Pi.
- Connect the stop buttons for the Easy, Medium, and Hard lanes to the GPIO pins 16, 18, and 22 respectively.
- Connect the reset switch to GPIO pin 24.

## Step 2: Software Setup

### Clone the Repository
```bash
git clone https://github.com/your-username/rock-climbing-wall-timers.git
```

### Navigate to the Project Directory
```bash
cd rock-climbing-wall-timers
```

### Install the Required Libraries
```bash
pip install pygame RPi.GPIO
```

## Step 3: Running the Script

### Run the Script
```bash
python3 rock_wall.py
```

## Step 4: Using the Timers

### Start a Timer
- Press the corresponding start button for the lane you want to time.

### Stop a Timer
- Press the corresponding stop button for the lane you want to stop.

### Reset All Timers
- Press the reset switch.

## Step 5: Viewing High Scores

- The top ten high scores are displayed on the screen.

## Troubleshooting

- Ensure that the GPIO pins are correctly connected.
- Check the `error_log.txt` file for any error messages.
- Make sure the sound file `stop_sound.wav` is in the same directory as the script.

## Conclusion

You should now have a fully functional rock climbing wall timer system with three lanes, sound notifications, and high score tracking. Enjoy your climbing experience!





