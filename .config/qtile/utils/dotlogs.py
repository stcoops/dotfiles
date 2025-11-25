"""dotlogs.py - utility for logging to a dotfile log for easier debugging of qtile config issues.
 - logger class with functions for error, warning, info, debug and custom logging."""

import time
from .structure import LOG_FILE

debug_mode = True  # Set to True to enable debug logging

class Logger:
    """A simple logger class to log messages to a specified log file. Functions include error, warning, info, debug and custom logging."""
    def __init__(self):
        self.LOG_FILE = LOG_FILE
        self.debug_mode = debug_mode
        self.clear()
        self.info("log initialized.")

    def clear(self):
        """Clear the log file."""
        with open(self.LOG_FILE, "w") as f:
            f.write("")  # Clear the file contents

    def error(self, message):
        """Log an error message to the log file with a timestamp."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] ERROR: {message}\n")

    def warning(self, msg):
        """Log a warning message to the log file."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] WARNING: {msg}\n")

    def info(self, msg):
        """Log an info message to the log file."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] INFO: {msg}\n")

    def debug(self, msg):
        """Log a debug message to the log file if debug_mode is True."""
        if not self.debug_mode:
            return
        else:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(self.LOG_FILE, "a") as f:
                f.write(f"[{timestamp}] DEBUG: {msg}\n")

    def custom(self, level, msg):
        """Log a custom <LEVEL> message to the log file."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {level.upper()}: {msg}\n")

# Initialize a global logger instance
log = Logger()