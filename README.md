
# Rock Wall Timer System with Raspberry Pi

This guide will walk you through setting up a timer system for a rock-climbing wall with three lanes using a Raspberry Pi. The system will control and display timers for each lane, track the top 10 high scores, and allow users to start, stop, and reset the timers using physical switches.

## Requirements

### Hardware
- **Raspberry Pi** (any model with GPIO pins)
- **3 Start Switches**: For starting/stopping the timers for each lane
- **1 Reset Switch**: For resetting all timers
- **Monitor/Screen**: For displaying the timers and high scores
- **Speakers**: For playing a sound when a timer is stopped

### Software
- **Python 3.x**
- **Pygame**: For the graphical interface
- **RPi.GPIO**: For interfacing with the GPIO pins

## Hardware Setup

### Connections
Connect the start and reset switches to the Raspberry Pi's GPIO pins as follows:

- **Start Switches**:
  - Lane 1: GPIO 36
  - Lane 2: GPIO 38
  - Lane 3: GPIO 40
- **Stop Switches**:
  - Lane 1: GPIO 16
  - Lane 2: GPIO 18
  - Lane 3: GPIO 22
- **Reset Switch**: GPIO 24

All switches should be connected with pull-up resistors. Connect one end of the switch to the corresponding GPIO pin and the other end to the ground (GND) pin.

## Software Setup

### Installing Dependencies

1. **Install Python 3.x**: If not already installed on your Raspberry Pi.
2. **Install Pygame**: Run the following command:
   ```
   pip3 install pygame
   ```
3. **Install RPi.GPIO**: It should be pre-installed with Raspbian. If not, run:
   ```
   pip3 install RPi.GPIO
   ```

### Code Setup

1. **Copy the Code**: Copy the provided Python code into a file named `rock_wall_timer.py`.
2. **Add Sound and Font Files**: Place `stop_sound.wav` and `freesansbold.ttf` in the same directory as the Python script.

### High Scores File

Create a file named `high_scores.txt` in the same directory as the script, with the initial high scores (optional). For example:

```plaintext
120.0
115.5
110.0
100.0
95.5
90.0
85.0
80.5
75.0
70.0
```

### Running the Code

Run the Python script using the following command:

```bash
python3 rock_wall_timer.py
```

## Usage

- **Start/Stop a Timer**: Press the corresponding start switch for the lane. Press it again to stop the timer and record the time if it's a high score.
- **Reset All Timers**: Press the reset switch.
- **Exit**: Press the Escape key on a connected keyboard.

## Troubleshooting

- **Ensure Correct Permissions**: Make sure you have the necessary permissions to access the GPIO pins.
- **Check File Paths**: Ensure that the sound, font, and high scores files are in the correct location.
- **Monitor Resolution**: Adjust the `width` and `height` variables in the code to match your screen's resolution.

## Conclusion

This rock wall timer system provides a fun and interactive way to track climbing times and compete for high scores. It's a versatile system that can be customized for different setups and extended with additional features as needed.




