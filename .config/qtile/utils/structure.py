"""structure.py - defines directory structure constants for qtile configuration.
- HOME_DIR: str - path to the user's home directory
- QTILE_CONFIG_DIR: str - path to the qtile configuration directory
- SCRIPTS_DIR: str - path to the scripts directory within the qtile config
- LOG_FILE: str - path to the log file for qtile logging"""

directory_structure = """

"""

import os


HOME_DIR = os.path.expanduser("~")
DOTCONFIG_DIR = os.path.join(HOME_DIR, ".config")

# NOTE: while developing, config is in .config/qtile-ver2.0, change when deploying
QTILE_DIR = os.path.join(DOTCONFIG_DIR, "qtile")


LOG_FILE = os.path.join(QTILE_DIR, "qtile.log")

WALLPAPERS_DIR = os.path.join(DOTCONFIG_DIR, "wallpapers")

SCRIPTS_DIR = os.path.join(QTILE_DIR, "scripts")
UTILS_DIR = os.path.join(QTILE_DIR, "utils")

_none = None  # placeholder to indicate module has been loaded