import os
from libqtile.config import Screen

from modules.taskbar import Taskbar

from utils.structure import WALLPAPERS_DIR
from defaults import wallpaper
from utils.dotlogs import log
from modules.groups import formatted_group_names


wallpaper = os.path.join(WALLPAPERS_DIR, wallpaper)

screens = []
if wallpaper != "":
    if os.path.exists(wallpaper):
        pass
    else:
        wallpaper = ""
for monitor_id in range(len(formatted_group_names)):
    group_names = formatted_group_names[monitor_id]
    if wallpaper != "":
        
        screens.append(Screen(
            wallpaper = wallpaper,
            wallpaper_mode = "fill",
            top = Taskbar(group_names).CompileWidgets()
        ))
    else:
        screens.append(Screen(
            top = Taskbar(group_names).CompileWidgets()
            ))
    log.debug(f"Screen {monitor_id} configured with groups: {group_names}")