
# Rock Wall Timers Controller

This script is designed to control 3 rock wall timers using a Raspberry Pi. The code is written in Python and uses the Pygame library for the graphical interface, displaying the timers, and the RPi.GPIO library to handle the GPIO pins for reading inputs from physical switches.

## Features

- Three separate timers for Easy, Medium, and Hard rock wall climbs.
- Start and Stop controls for each timer.
- Master reset control to reset all timers.
- Full-screen graphical interface displaying the current time and timers for each difficulty level.

## Dependencies

- [Python 3](https://www.python.org/downloads/)
- [Pygame](https://www.pygame.org/)
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)

## Hardware Connections

- Start switches for Easy, Medium, and Hard timers: Pins 36, 38, 40.
- Stop switches for Easy, Medium, and Hard timers: Pins 16, 18, 22.
- Master reset switch: Pin 24.

## Usage

Run the script on your Raspberry Pi connected to the required switches. The display will initialize, and the timers can be controlled using the physical buttons connected to the pins specified.

### Controls

- **Start Switches**: Begin the respective timers for each difficulty level. If already running, a press will pause and reset the timer.
- **Stop Switches**: Stop the respective timers for each difficulty level.
- **Reset Switch**: Master control to reset all timers if any of them are running or to reset the timers to "00:00.0" if none are running.


Please use this code responsibly and make sure to follow all safety precautions when connecting the Raspberry Pi to any physical hardware. The creator of this code is not responsible for any harm or damage that may occur from its use.
