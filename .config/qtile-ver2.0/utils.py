
# Logging utility for Qtile configuration
import time

class Logger:
    """A simple logger class to log messages to a specified log file. Functions include error, warning, info, debug and custom logging."""
    def __init__(self, log_file, debug_mode=False):
        self.LOG_FILE = log_file
        self.debug_mode = debug_mode

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