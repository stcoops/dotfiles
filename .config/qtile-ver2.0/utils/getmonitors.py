import os, subprocess

from .structure import UTILS_DIR
from .dotlogs import log

def detect_monitors():
    try:
        monitor_info = subprocess.check_output("bash " + os.path.join(UTILS_DIR, "get_monitors.sh"), shell=True)

        # Handle possible known errors
        if monitor_info.decode().strip() == "":
            exception_known = True
            raise Exception("No monitor info detected")
        elif monitor_info.decode().strip() == "error: xrandr failed":
            exception_known = True
            raise Exception("xrandr command failed in get_monitors.sh, likely no X server running or xrandr not installed")
        
        exception_known = False
        # Parse monitor info
        monitors = []
        for line in monitor_info.decode().strip().split("\n"):
            monitors.append({"id":str(line.split(",")[0]),"width": int(line.split(",")[1]), "height": int(line.split(",")[2])})
        log.debug(f"Detected {len(monitors)} monitors: " + str(monitors))
            
    # Fallback to single monitor and log error if detection fails
    except Exception as e:
        monitors = [{"id": "1", "width": 1920, "height": 1080}]
        if not exception_known:
            log.error("Unexpected error detecting monitors, defaulting to single monitor.")
            log.error("|-> python error details: " + str(e))
            log.error("└─> subprocess output: " + str(monitor_info.decode().strip()))
        log.error("Error detecting monitors, defaulting to single monitor. Error: " + str(e))
    return monitors

monitors = detect_monitors()
primary_monitor = monitors[0]