"""# Qtile configuration file - config.py"""

from libqtile import hook, qtile
from libqtile.lazy import lazy

from utils.dotlogs import log # Logger instance for logging
log.info(f"Qtile configuration starting")

try:
    from utils.getmonitors import _none # runs monitor detection
    from utils.colors import _none  # ensures colors.py is loaded
    from utils.structure import _none  # ensures structure.py is loaded
    log.info("Utility modules loaded successfully.")
except Exception as e:
    log.error(f"Error loading utility modules: {e}")
    raise

try:
    from modules.groups import groups # also creates group keybindings which are accessed in keybindings.py
    log.info("Groups module loaded successfully.")
except Exception as e:
    log.error(f"Error loading groups module: {e}")
    raise

try:
    from modules.keybindings import keys
    log.info("Keybindings module loaded successfully.")
except Exception as e:
    log.error(f"Error loading keybindings module: {e}")
    raise

try:
    from modules.layouts import layouts
    log.info("Layouts module loaded successfully.")
except Exception as e:
    log.error(f"Error loading layouts module: {e}")
    raise

try:
    from modules.screens import screens # also creates taskbars with groups for each screen
    log.info("Screens module loaded successfully.")
except Exception as e:
    log.error(f"Error loading screens module: {e}")
    raise



""" Internal config settings """

dgroups_key_binder = None
groups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True



wmname = "QTile"
log.info(f"Qtile loaded, running startup hooks.")


from modules.popups.qtile_control import Qstartup

@hook.subscribe.startup_once
def start_once():
    lazy.function(Qstartup)

@hook.subscribe.startup
def start():
    from utils.colors import refresh_colors
    refresh_colors()
    log.info("Pywal colors reloaded on startup.")



log.info("Qtile configuration completed successfully.")