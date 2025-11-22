from utils import Logger
import os, subprocess
# User-defined variables

mod = "mod4"
terminal = "kitty"
browser = "brave"
editor = "code"
notepad = "tjournal"


# Define workspaces as 1D array for one monitor or for duplicate workspaces on multiple monitors,
# or set to a 2D array for distinct workspaces on each monitor (if not enough, will recycle last monitor's workspaces)

group_names = ["1", "2", "3", "4", "5", "6"]

colorscheme = {"default","dark"}  # see colorschemes.py for available schemes

wallpaper = os.path.join(os.path.expanduser("~"),".config" ,"wallpapers","hands.jpg") # path to wallpaper image, or None
 

#_______________________
# Auto-defined variables
#-----------------------


# Define paths
HOME_DIR = os.path.expanduser("~")
# NOTE: while developing, config is in .config/qtile-ver2.0, change when deploying
QTILE_CONFIG_DIR = os.path.join(HOME_DIR, ".config", "qtile-ver2.0")
SCRIPTS_DIR = os.path.join(QTILE_CONFIG_DIR, "scripts")
LOG_FILE = os.path.join(QTILE_CONFIG_DIR, "qtile.log")

# Initialize logger
log = Logger(LOG_FILE, debug_mode=True)
log.clear()
log.info("Qtile started, log initialized.")


# Detect monitors using external script
try:
    monitor_info = subprocess.check_output("bash " + os.path.join(SCRIPTS_DIR, "get_monitors.sh"), shell=True)

    # Handle possible errors
    if monitor_info.decode().strip() == "":
        raise Exception("No monitor info detected")
    elif monitor_info.decode().strip() == "error: xrandr failed":
        raise Exception("xrandr command failed in get_monitors.sh, likely no X server running or xrandr not installed")
    
    # Parse monitor info
    MONITORS = []
    for line in monitor_info.decode().strip().split("\n"):
        MONITORS.append({"id":str(line.split(",")[0]),"width": int(line.split(",")[1]), "height": int(line.split(",")[2])})
    MONITOR_COUNT = len(MONITORS)
    log.debug(f"Detected {MONITOR_COUNT} monitors: " + str(MONITORS))
        
# Fallback to single monitor and log error if detection fails
except Exception as e:
    MONITOR_COUNT = 1
    log.error("Error detecting monitors, defaulting to single monitor. Error: " + str(e))




# option light = wp12821730.jpg
wallpaper = os.path.join(HOME_DIR,".config" ,"wallpapers","hands.jpg") # path to wallpaper image, or None



# Initialize classes
