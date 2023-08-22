# Troubleshooting Guide for Rock Wall Timers

This guide provides solutions to common problems you may encounter while setting up and using the Rock Wall Timers script on a Raspberry Pi.

## Table of Contents

1. [Timers Don't Start or Stop](#timers-dont-start-or-stop)
2. [High Scores Aren't Being Saved](#high-scores-arent-being-saved)
3. [Sound Not Playing](#sound-not-playing)
4. [Script Doesn't Run on Boot](#script-doesnt-run-on-boot)
5. [Display Issues](#display-issues)

## Timers Don't Start or Stop

### Problem

The timers do not respond to the start, stop, or reset buttons.

### Solutions

1. **Check Button Connections**:
   - Ensure that the buttons are properly connected to the corresponding GPIO pins.
   - Check the button wiring for loose connections or incorrect pin assignments.

2. **Reboot Raspberry Pi**:
   - Reboot the Raspberry Pi to ensure that the GPIO pins are in a clean state:
     ```bash
     sudo reboot
     ```

3. **Check for Errors in the Error Logs**:
   - Review the error logs in the `error_log.txt` file within the script's directory. This file contains detailed information about any exceptions or errors that occurred, including timestamps and tracebacks.

3. **Check for Errors in Terminal**:
   - Run the script in the terminal and look for error messages or exceptions.

## High Scores Aren't Being Saved

### Problem

High scores are not being saved to the text file or are not being displayed correctly.

### Solutions

1. **Check File Permissions**:
   - Ensure that the script has write permissions for the directory where the high scores file is located.

2. **Check File Path**:
   - Verify that the path to the high scores file is correct within the script.

## Sound Not Playing

### Problem

The stop sound does not play when a timer is stopped.

### Solutions

1. **Check Sound File Path**:
   - Ensure that the path to the sound file (`stop_sound.wav`) is correct within the script.

2. **Verify Sound File Format**:
   - Make sure the sound file is in the correct format (WAV) and is not corrupted.

3. **Check Audio Configuration**:
   - Verify that the Raspberry Pi's audio output is configured correctly and that the volume is not muted.

## Script Doesn't Run on Boot

### Problem

The script does not start automatically when the Raspberry Pi boots, even though a cron job has been set up.

### Solutions

1. **Check Cron Job**:
   - Verify the cron job by typing `crontab -l` in the terminal.
   - Ensure that the path to the script is correct and that the cron job is formatted properly.

2. **Check Script Permissions**:
   - Ensure that the script has execute permissions:
     ```bash
     chmod +x /path/to/your/script/Rock_wall_timers.py
     ```

3. **Review System Logs**:
   - Examine the system logs to identify any errors related to the cron job:
     ```bash
     grep CRON /var/log/syslog
     ```

## Display Issues

### Problem

The display is not rendering correctly, or the font size and layout appear distorted.

### Solutions

1. **Adjust Screen Resolution**:
   - Ensure that the screen resolution set in the script matches the resolution of the connected display.

2. **Update Pygame**:
   - Ensure that you are using the latest version of Pygame, as older versions may have compatibility issues.

3. **Check for Errors in Terminal**:
   - Run the script in the terminal and look for error messages or exceptions related to the display.

If you encounter any issues not covered in this guide, please [open an issue](https://github.com/yourusername/Rock-wall-timers/issues) on GitHub or contact the maintainers directly.
