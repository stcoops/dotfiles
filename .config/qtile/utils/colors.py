"""colors.py - handles pywal color scheme integration for qtile configuration.
- run_pywal: function to run pywal on a given wallpaper
- load_pywal_colors_py: function to load colors from pywal's generated colors.py file
"""
from .dotlogs import log
from .structure import HOME_DIR, WALLPAPERS_DIR

default_colors = {
    "background": "#282c34",
    "foreground": "#abb2bf",
    "cursor": "#528bff",
    "color0": "#282c34",
    "color1": "#e06c75",
    "color2": "#98c379",
    "color3": "#e5c07b",
    "color4": "#61afef",
    "color5": "#c678dd",
    "color6": "#56b6c2",
    "color7": "#dcdfe4",
    "color8": "#5c6370",
    "color9": "#e06c75",
    "color10": "#98c379",
    "color11": "#e5c07b",
    "color12": "#61afef",
    "color13": "#c678dd",
    "color14": "#56b6c2",
    "color15": "#ffffff",
}

import os, subprocess
def run_pywal(wallpaper, mode = "dark") -> None:
    """Run pywal to generate a color scheme and return it.
    - wallpaper: str - name of the wallpaper image file located in WALLPAPERS_DIR
    - mode: str - "light" or "dark" mode for pywal
    - log: Logger - logger instance for logging
    """
    try:
        if mode == "light":
            subprocess.run(["wal", "-i", os.path.join(WALLPAPERS_DIR, wallpaper), "-l"], check=True)
        else:
            subprocess.run(["wal", "-i", os.path.join(WALLPAPERS_DIR, wallpaper)], check=True)
        log.debug("Pywal ran successfully.")
    except Exception as e:
        log.warning(f"Failed to run pywal: {e}")

def _format_colors(raw_json):
    """Format raw colors from pywal into a dictionary."""
    formatted = {}
    special = raw_json.get("special", {})
    colors = raw_json.get("colors", {})
    formatted["background"] = special.get("background")
    formatted["foreground"] = special.get("foreground")
    formatted["cursor"] = special.get("cursor")
    for i in range(len(colors)):
        formatted[f"color{i}"] = colors[f"color{i}"]

    return formatted


import json

def load_pywal_colors_py():
    """Load colors from pywal's colors.py file. 
    - log: Logger - logger instance for logging
    """
    colors_json_path = os.path.join(HOME_DIR, ".cache", "wal", "colors.json")
    try:
        with open(colors_json_path, "r") as f:
            colors_data = json.load(f)
        log.debug("Pywal colors loaded from colors.json successfully.")
        return _format_colors(colors_data)
    except Exception as e:
        log.debug(f"Failed to load pywal colors: {e}")
        log.warning("Pywal colors could not be loaded.. using default colors.")

        return default_colors

def refresh_colors():
    """Reload colors from pywal's colors.py file."""
    global colors
    colors = load_pywal_colors_py()
    log.info("Colors reloaded from pywal.")

refresh_colors()



foreground = colors.get("foreground")
background = colors.get("background")
cursor = colors.get("cursor")


accent = colors.get("color4")
highlight = colors.get("color6")
faint_foreground = colors.get("color8")  # slightly brighter than background
tinted_foreground = colors.get("color5")  # accent flavoured foreground

_none = None  # placeholder to indicate module has been loaded