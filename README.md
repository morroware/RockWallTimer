# Rock Wall Timers

A multi-timer system suitable for a Rock wall or similar applications, designed to run on a Raspberry Pi. This code leverages Python, Pygame, and the Raspberry Pi's GPIO capabilities to manage and display three individual timers with start, stop, and reset functionality.

## Features

### Three Individual Timers

- Manage three separate stopwatches labeled Easy, Medium, and Hard.
- Track time, update the display, and handle start and stop controls for each timer.

### Start, Stop, and Reset Buttons

- Control timers using physical buttons connected to the Raspberry Pi's GPIO pins.
- Three start buttons to initiate timers.
- Three stop buttons to halt timers.
- A reset button to reset all timers simultaneously.

### High Scores

- Maintain and display a list of the top 10 high scores.
- High scores are stored in a text file, and the top scores are displayed on the screen.

### Sound Effects

- Play a sound effect when a timer is stopped, enhancing user interaction.

### Fullscreen Display

- Utilize a fullscreen graphical user interface (GUI) to display the timers, high scores, and labels.

### Error Handling

- Robust error handling, logging exceptions to a file with timestamps and tracebacks.

## Getting Started

### Setting Up Rock Wall Timers with Raspberry Pi and Seven Buttons

This guide will walk you through the process of setting up the Rock Wall Timers script on a Raspberry Pi, complete with seven physical buttons for controlling the timers.

#### Prerequisites

- Raspberry Pi (any model with GPIO pins)
- Seven tactile buttons
- Jumper wires
- Breadboard (optional)
- Python 3 and Pygame installed

#### Step-by-Step Guide

##### Step 1: Connect the Buttons

1. **Connect the Start Buttons**:
   - Connect three start buttons to GPIO pins 36, 38, and 40 on the Raspberry Pi.
   - Connect the other terminal of each button to Ground (GND).

2. **Connect the Stop Buttons**:
   - Connect three stop buttons to GPIO pins 16, 18, and 22 on the Raspberry Pi.
   - Connect the other terminal of each button to Ground (GND).

3. **Connect the Reset Button**:
   - Connect the reset button to GPIO pin 24 on the Raspberry Pi.
   - Connect the other terminal of the button to Ground (GND).

##### Software Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Rock-wall-timers.git
   cd Rock-wall-timers
   ```

2. **Install Dependencies**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pygame
   ```

3. **Running the Code**:
   ```bash
   python3 Rock_wall_timers.py
   ```

#### Usage

- **Start a Timer**: Press a start button.
- **Stop a Timer**: Press the corresponding stop button or the same start button again.
- **Reset All Timers**: Press the reset button.
- **View High Scores**: High scores are displayed on the screen.
- **Exit the Program**: Press the ESC key.

### Running the Script at Boot

If you want the Rock Wall Timers script to run automatically when the Raspberry Pi boots up, you can set up a cron job using `crontab` and edit it with the `nano` text editor. Follow these steps:

1. **Open Terminal**:
   - Open a terminal window on your Raspberry Pi.

2. **Edit the Crontab**:
   - Type `crontab -e` to edit the user's crontab using the `nano` editor (or any other editor you prefer).
   - If prompted to choose an editor, select `nano`.

3. **Add the Cron Job**:
   - Scroll to the end of the file, and on a new line, add the following:
     ```plaintext
     @reboot python3 /path/to/your/script/Rock_wall_timers.py
     ```
     Replace `/path/to/your/script/` with the actual path to the script.

4. **Save and Exit**:
   - Press `CTRL + O` to write the changes.
   - Press `ENTER` to confirm.
   - Press `CTRL + X` to exit `nano`.

5. **Verify the Cron Job**:
   - Type `crontab -l` to list all cron jobs and make sure your entry is correct.

6. **Reboot to Test**:
   - You can reboot your Raspberry Pi to test the script:
     ```bash
     sudo reboot
     ```

The Rock Wall Timers script should now start automatically at boot. If you encounter any issues, refer to the [Troubleshooting Guide](troubleshooting.md).
