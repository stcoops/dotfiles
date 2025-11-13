"""HDOS - Hyperactivity Disorder Operating System (hyper not hypr!) Qtile Configuration File
This file contains the main configuration settings for the HDOS Qtile window manager setup.
Modularization has been implemented to enhance readability and maintainability, so please refer to the individual module files for specific configurations and hacking.
"""

# Qtile imports:

from libqtile import layout, qtile, widget, hook, bar
from libqtile.config import Click, Drag, Group, Key, Match, Screen 
from libqtile.config import DropDown, ScratchPad
from libqtile.lazy import lazy
import subprocess, time, os
import threading
from qtile_extras.popup import PopupText, PopupSlider, PopupRelativeLayout

# Settings

HOME_DIR = os.path.expanduser("~")
QTILE_CONFIG_DIR = os.path.join(HOME_DIR, ".config", "qtile")
SCRIPTS_DIR = os.path.join(QTILE_CONFIG_DIR, "scripts")

mod = "mod4"
terminal = "kitty"
browser = "brave"
editor = "code"

group_names = ["1", "2", "3", "4", "5"] # more: , "6", "7", "8", "9"]
monitor_count = 1  # Set to the number of monitors you have

colorscheme_name = "default" # see colorschemes.py for available schemes
colorscheme_brightness = "dark"  # "light" or "dark"


wallpaper = os.path.join(HOME_DIR,".config" ,"wallpapers","wp12821730.jpg") # path to wallpaper image, or None

# Logging setup
LOG_FILE = os.path.join(QTILE_CONFIG_DIR, "qtile.log")
with open(LOG_FILE, "w") as f:
    f.write("")

def _log_error(message):
    """Log an error message to the log file with a timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] ERROR: {message}\n")

# Popups

def _brightness_popup(qtile, level):
    """Show a simple brightness popup with one PopupText and a visible slider."""
    # Ensure slider colors contrast with background; fall back to foreground if needed
    color_below = getattr(colorscheme, "accent", None) or colorscheme.foreground
    color_above = getattr(colorscheme, "highlight", None) or colorscheme.foreground

    popup = PopupRelativeLayout(
        qtile,
        width=360,
        height=80,
        rows = 2,
        cols = 1,
        background=colorscheme.background,
        controls=[
            PopupSlider(
                value=level,
                min_value=0,
                max_value=100,
                # explicitly size and position the slider so it is visible
                width=0.9,
                height=0.45,
                pos_x=0.05,
                pos_y=0.15,
                background=colorscheme.background,
                color_below=color_below,
                color_above=color_above,
                marker_size=0,
                bar_size=5,
                highlight_radius=2,
                opacity=0.8,
                name="brightness_slider",
            ),
            PopupText(
                # show numeric level so the popup isn't just an empty box
                text=f"Brightness: {int(level)}%",
                background=colorscheme.background,
                foreground=colorscheme.foreground,
                fontsize=18,
                v_align="top",
                h_align="center",
                pos_x=0.05,
                pos_y=0.55,
                width=0.9,
                height=0.35,
                name="brightness_label",
            ),
        ],
    )
    popup.show(relative_to_bar=True, x = (1920 - 360) //2, y = 1025)
    try:
        qtile.call_later(1.0, popup.hide)
    except Exception:
        time.sleep(1.0)
        popup.hide()

def _increase_brightness(qtile, amount=10):
    """Increase brightness by amount (0-100)."""
    _change_brightness(qtile, amount)

def _decrease_brightness(qtile, amount=-10):
    """Decrease brightness by amount (0-100)."""
    _change_brightness(qtile, amount)

def _change_brightness(qtile, amount=10):
    """Change brightness by amount (0-100)."""
    # Get current brightness
    try:
        result = subprocess.run(
            ["bash", os.path.join(SCRIPTS_DIR, "brightness.sh"), "get"],
            capture_output=True,
            text=True,
            check=True
        )
        current_brightness = float(result.stdout.strip())
    except Exception:
        _show_centered_popup(qtile, "Error getting brightness", timeout=10.0)
        current_brightness = 50.0  # Default if command fails

    # Calculate new brightness
    new_brightness = min(100, current_brightness + amount)
    new_brightness = max(10, new_brightness)  # Ensure not below 0

    string_new_brightness = str(int(new_brightness)) + "%"

    # Set new brightness
    subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "brightness.sh"), "set", string_new_brightness])

    # Show popup
    _brightness_popup(qtile, int(new_brightness))

def _volume_up(qtile):
    """Increase the volume."""
    _change_volume(qtile, 5)

def _volume_down(qtile):
    """Decrease the volume."""
    _change_volume(qtile, -5)

def _mute_volume(qtile):
    """Mute the volume."""
    _change_volume(qtile, 0, mute=True)

def _change_volume(qtile, change, mute=False):
    """Change volume by change (positive or negative or mute)."""
    # Get current volume and mute status
    try:
        result = subprocess.run(
            ["bash", os.path.join(SCRIPTS_DIR, "volumecontrol.sh"), "get"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip().splitlines()
        current_volume = float(output[0])
        try:
            is_muted = output[1].lower() == "mute"
        except IndexError:
            is_muted = False
    except Exception:
        _log_error("Error getting volume: " + str(Exception))
        _show_centered_popup(qtile, "Error getting volume", timeout=10.0)
        current_volume = 50.0  # Default if command fails
        is_muted = False

    # Calculate new volume
    

    # Show popup
    if mute:
        subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "volumecontrol.sh"), "mute"])
        _volume_popup(qtile, -1)
        if is_muted:
            # If already muted, unmute and show current volume
            _volume_popup(qtile, current_volume)
    else:
        new_volume = min(100, max(0, current_volume + change))
        subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "volumecontrol.sh"), "set", str(int(new_volume))])
        _volume_popup(qtile, new_volume)

def _volume_popup(qtile, level):
    color_below = getattr(colorscheme, "accent", None) or colorscheme.foreground
    color_above = getattr(colorscheme, "highlight", None) or colorscheme.foreground
    if level == -1:
        level = 0
        volume_text = "Volume: Muted"
    else:
        volume_text = f"Volume: {int(level)}%"
    popup = PopupRelativeLayout(
        qtile,
        width=360,
        height=80,
        rows = 2,
        cols = 1,
        background=colorscheme.background,
        controls=[
            PopupSlider(
                value=level,
                min_value=0,
                max_value=100,
                # explicitly size and position the slider so it is visible
                width=0.9,
                height=0.45,
                pos_x=0.05,
                pos_y=0.15,
                background=colorscheme.background,
                color_below=color_below,
                color_above=color_above,
                marker_size=0,
                bar_size=5,
                highlight_radius=2,
                opacity=0.8,
                name="volume_slider",
            ),
            PopupText(
                # show numeric level so the popup isn't just an empty box
                text=volume_text,
                background=colorscheme.background,
                foreground=colorscheme.foreground,
                fontsize=18,
                v_align="top",
                h_align="center",
                pos_x=0.05,
                pos_y=0.55,
                width=0.9,
                height=0.35,
                name="volume_label",
            ),
        ],
    )
    popup.show(relative_to_bar=True, x = (1920 - 360) //2, y = 1025)
    try:
        qtile.call_later(1.0, popup.hide)
    except Exception:
        time.sleep(1.0)
        popup.hide()

def _show_centered_popup(qtile, message, width=300, height=60, timeout=1.0):
    """Create a simple centered popup with one PopupText and auto-hide it."""
    popup = PopupRelativeLayout(
        qtile,
        width=width,
        height=height,
        background=colorscheme.background,
        controls=[
            PopupText(
                text=message,
                background=colorscheme.background,
                foreground=colorscheme.foreground,
                opacity=0.95,
                width=0.9,
                height=0.9,
                pos_x=0.05,
                pos_y=0.05,
                v_align="middle",
                h_align="center",
                fontsize=22,
                name="msg"
            ),
        ],
    )
    popup.show(centered=True)
    try:
        qtile.call_later(timeout, popup.hide)
    except Exception:
        time.sleep(timeout)
        popup.hide()

############
# Shutdown #
############

def _shutdown_qtile(qtile):
    _show_centered_popup(qtile, "Shutting down...", timeout=2.0)
    qtile.call_later(2.0, qtile.shutdown)

##########
# Reload #
##########

def _run_and_notify(qtile, cmd, start_msg, success_msg=None, fail_msg=None, on_success=None, start_timeout=2.0, result_timeout=3.5):
    """Run cmd in a thread, show start_msg immediately, then show success/fail when it finishes.
    on_success is called on the Qtile main loop if returncode == 0.
    cmd should be a list (no shell) or a string (shell=True)."""
    # show a start popup so user gets immediate feedback
    _show_centered_popup(qtile, start_msg, timeout=start_timeout)

    def worker():
        try:
            if isinstance(cmd, str):
                p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            else:
                p = subprocess.run(cmd, capture_output=True, text=True)
            out = p.stdout or ""
            err = p.stderr or ""
            rc = p.returncode
        except Exception as e:
            rc = 1
            out = ""
            err = str(e)

        def finish():
            if rc == 0:
                if success_msg:
                    _show_centered_popup(qtile, success_msg + ("\n" + out if out else ""), timeout=result_timeout)
                if on_success:
                    # schedule on_success after the success popup timeout so the popup isn't cleared by reload
                    def call_on_success():
                        try:
                            on_success()
                        except Exception as e:
                            _show_centered_popup(qtile, "on_success callback failed:\n" + str(e), timeout=result_timeout)
                    qtile.call_later(result_timeout + 0.1, call_on_success)
            else:
                msg = (fail_msg or "Command failed") + "\n" + (err or out or f"exit {rc}")
                _log_error(msg)
                _show_centered_popup(qtile, msg, timeout=result_timeout)
        # schedule UI changes on qtile's loop
        qtile.call_later(0, finish)

    threading.Thread(target=worker, daemon=True).start()


def _reload_qtile(qtile, startup=False):
    if startup:
        # at startup just fire the helper scripts quickly (no need to wait)
        _run_and_notify(qtile, ["bash", os.path.join(SCRIPTS_DIR, "reloadpicom.sh")], "Starting picom...", "Picom started", "Picom start failed")
        _run_and_notify(qtile, ["bash", os.path.join(SCRIPTS_DIR, "reloadxcape.sh")], "Starting xcape...", "Xcape started", "Xcape start failed")
        _run_and_notify(qtile, ["bash", os.path.join(SCRIPTS_DIR, "touchpadsetup.sh"), "reset"], "Resetting touchpad...", "Touchpad reset complete", "Touchpad reset failed")
        return

    # Restart picom and xcape and report when each actually completes
    _run_and_notify(
        qtile,
        ["bash", os.path.join(SCRIPTS_DIR, "reloadpicom.sh")],
        "Reloading picom...",
        "Picom reload complete",
        "Picom reload failed",
        start_timeout=1.0,
        result_timeout=1.5
    )

    _run_and_notify(
        qtile,
        ["bash", os.path.join(SCRIPTS_DIR, "reloadxcape.sh")],
        "Reloading xcape...",
        "Xcape reload complete",
        "Xcape reload failed",
        start_timeout=1.0,
        result_timeout=0.5
    )

    _run_and_notify(
        qtile,
        ["bash", os.path.join(SCRIPTS_DIR, "touchpadsetup.sh"), "reset"],
        "Resetting touchpad...",
        "Touchpad reset complete",
        "Touchpad reset failed",
        start_timeout=1.0,
        result_timeout=0.5
    )

    # Run py_compile and reload only when it succeeds
    def on_config_ok():
        try:
            qtile.reload_config()
            _show_centered_popup(qtile, "Reload complete", timeout=1.5)
        except Exception as e:
            _log_error("Error reloading config: " + str(e))
            _show_centered_popup(qtile, "Reload failed:\n" + str(e), timeout=3.5)

    _run_and_notify(
        qtile,
        ["python", "-m", "py_compile", os.path.join(QTILE_CONFIG_DIR, "config.py")],
        "Testing qtile config...",
        "Config OK",
        "Config error",
        on_success=on_config_ok,
        start_timeout=1.5,
        result_timeout=0.5
    )
###############
# Keybindings #
###############

class KeyBindings:

    def __init__(self, mod, terminal, editor=None, browser=None, screen_count=1):
        self.mod = mod
        self.terminal = terminal
        self.browser = browser
        self.editor = editor
        self.keys = []
        self._base_keys()
        self._multi_media_keys()
        if screen_count > 1:
            self._multi_screen_keys(screen_count)
        if self.browser:
            self._browser_key()
        if self.editor:
            self._file_editor()

    def _base_keys(self):
        self.keys.extend([
            Key([self.mod], "Left", lazy.layout.left(), desc="Move window focus up"),
            Key([self.mod], "Right", lazy.layout.next(), desc="Move window focus to other window"),
            Key([self.mod, "shift"], "Right", lazy.layout.shuffle_down(), desc="Move window down"),
            Key([self.mod, "shift"], "Left", lazy.layout.shuffle_up(), desc="Move window up"),


            Key([self.mod], "Tab", lazy.next_layout(), desc="Toggle layout"),
            Key([self.mod], "x", lazy.layout.grow(), desc="Grow current window"),
            Key([self.mod], "z", lazy.layout.shrink(), desc="Shrink current window"),
            Key([self.mod], "s", lazy.layout.normalize(), desc="Reset all window sizes"),


            Key([self.mod], "Return", lazy.spawn(self.terminal), desc="Launch terminal"),
            Key([self.mod], "c", lazy.window.kill(), desc="Kill focused window"),
            Key([self.mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),


            Key([self.mod, "shift"], "home", lazy.function(_reload_qtile), desc="Reload the config"),
            #Key([self.mod, "shift"], "home", lazy.reload_config(), desc="Reload the config"),
            Key([self.mod, "shift"], "end", lazy.function(_shutdown_qtile), desc="Shutdown Qtile"),

            Key([self.mod], "space", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

            ])
        
    def _multi_media_keys(self):
        self.keys.extend([
            Key([], "XF86AudioRaiseVolume", lazy.function(_volume_up), desc="Increase volume"),
            Key([], "XF86AudioLowerVolume", lazy.function(_volume_down), desc="Decrease volume"),
            Key([], "XF86AudioMute", lazy.function(_mute_volume), desc="Mute/Unmute volume"),

            #Key([], "XF86AudioRaiseVolume", lazy.spawn("bash /home/solve/.config/qtile/volumecontrol.sh up"), desc="Increase volume"),
            #Key([], "XF86AudioLowerVolume", lazy.spawn("bash /home/solve/.config/qtile/volumecontrol.sh down"), desc="Decrease volume"),
            #Key([], "XF86AudioMute", lazy.spawn("bash /home/solve/.config/qtile/volumecontrol.sh mute"), desc="Mute/Unmute volume"),


            Key([], "XF86MonBrightnessUp", lazy.function(_increase_brightness), desc="Increase brightness"),
            Key([], "XF86MonBrightnessDown", lazy.function(_decrease_brightness), desc="Decrease brightness"),

            #Key([], "XF86MonBrightnessUp", lazy.spawn("bash /home/solve/.config/qtile/brightness.sh up"), desc="Increase brightness"),
            #Key([], "XF86MonBrightnessDown", lazy.spawn("bash /home/solve/.config/qtile/brightness.sh down"), desc="Decrease brightness"),
            
            Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause media"),

            Key([], "XF86KbdBrightnessUp", lazy.spawn("bash " + os.path.join(SCRIPTS_DIR, "kbd_brightness.sh")), desc="Increase keyboard backlight brightness"),
])
        
    def _multi_screen_keys(self, screen_count):
        for i in range(screen_count):
            self.keys.extend([
                Key([self.mod, "Control"], str(i), lazy.focus_screen(i), desc=f"focus screen {i}"),
                ])

    def _browser_key(self):
        self.keys.append(
            Key([self.mod], "b", lazy.spawn(self.browser), desc="Launch web browser"),
            )
    
    def _file_editor(self):
        if self.editor == "nvim":
            editor = "kitty -e nvim"
        else:
            editor = self.editor

        self.keys.append(
            Key([self.mod], "v", lazy.spawn(editor), desc="Launch file editor")
            )

#######################
# Group functionality #
#######################

def split_array(arr, B):
    n = len(arr)
    q, r = divmod(n, B)
    parts = []
    start = 0
    for i in range(B):
        end = start + q + (1 if i < r else 0)
        parts.append(arr[start:end])
        start = end
    return parts

def _focus_group_and_screen(qtile, screen_index, group_name):
    qtile.focus_screen(screen_index)
    qtile.groups_map[group_name].toscreen()


class GroupHandler:
    def __init__(self, mod: str, group_names: list[str], monitor_count: int = 1):
        """automatically appends to keys_list and saves groups to self.groups"""
        self.mod = mod
        self.keys = []
        self.groups= []
        self.group_names_split = split_array(group_names, monitor_count)
        self.init_groups(self.group_names_split)
        self._make_scratchpad_group()
        self._make_control_center_scratchpad()
        #self._make_center_notification_scratchpad()

    def init_groups(self, group_names):
        # Initializing
        group_number = 0
        # loop through groups to add
        for screen_index in range(len(group_names)):
            for group_index in range(len(group_names[screen_index])):
                # appending to groups for qtile
                current_group_name = group_names[screen_index][group_index]
                self.groups.append(Group(name = current_group_name, screen_affinity = screen_index))
            
                # Keybindings
                self.keys.extend([
                Key(
                    [self.mod],
                    str(group_number+1),
                    lazy.function(_focus_group_and_screen, screen_index, current_group_name),
                    desc = f"Switch to group {group_number}: {current_group_name}"
                    )])
                self.keys.extend([
                Key(
                    [self.mod, "shift"],
                    str(group_number+1),
                    lazy.window.togroup(current_group_name),
                    lazy.function(_focus_group_and_screen, screen_index, current_group_name),
                    desc = f"Switch to & move focused window to group {group_number}: {current_group_name}",
                    )])
                group_number += 1
        
    def get_groups_and_keys(self):
        return self.groups, self.keys
    
    def _make_scratchpad_group(self):
        scratchpad_group = ScratchPad(name="scratchpad", dropdowns=[
            DropDown("term", str(terminal + " htop"), width=0.6, height=0.6, x=0.2, y=0.15, opacity=0.6, on_focus_lost_hide=True),
                ], single=True
            )
        self.groups.append(scratchpad_group)
        self.keys.extend([
            Key([self.mod], "t", lazy.group["scratchpad"].dropdown_toggle("term"), desc="Toggle Scratchpad Terminal")
        ])
    
    def _make_control_center_scratchpad(self):
        control_center_scratchpad = ScratchPad(name="control_center_scratchpad", dropdowns=[
            DropDown("control_center_dropdown", 
                     str(terminal + " python /home/solve/.config/qtile/control_center.py"),
                     width = 0.3, height = 0.4, x = 0.6975, y = 0.003#
                     , opacity = 0.6, on_focus_lost_hide = True
                     )], single=True)
        self.groups.append(control_center_scratchpad)
        self.keys.extend([
            Key([], "XF86MyComputer", lazy.group["control_center_scratchpad"].dropdown_toggle("control_center_dropdown"), desc="Toggle Control Center")
        ])

#################
# Color Schemes #
#################

class ColorSchemeHandler:
    def __init__(self):
        self._load_schemes()
        self.default = self.schemes["default"]["dark"]

    def get_scheme(self, scheme_name: str, light_dark: str):
#        Note: Improve error handling (flash screen if error?)
#        also could be improved to store schemes in json file and read on call (for efficiency)
        if light_dark not in ["light", "dark"]:
            return self.default
        if scheme_name not in self.schemes:
            return self.default

#       if no errors:
        return self.schemes[scheme_name][light_dark]
    
    def check_scheme_exists(self, scheme_name: str, light_dark: str):
        return scheme_name in self.schemes and light_dark in self.schemes[scheme_name]



    def _load_schemes(self):
        from colorschemes import schemes
        self.schemes = schemes
            

class TaskbarHandler():
    def __init__(self, colorscheme, groups_for_this_screen):
        self.groups = groups_for_this_screen
        self.colors = colorscheme
        self.widgets = []
        self.widget_defaults = dict(
            font="Ubuntu Mono",
            fontsize=14,
        )

        # anything pre-spacer (left side)
        self._add_blank_space()
        self._add_group_box()

        # add spacer
        self.widgets.append(
                widget.Spacer(
                    background = self.colors.background,
                )
            )
        # anything post-spacer (right side)
        self._add_battery()
        self._add_line_separator()
        self._add_clock()
        self._add_line_separator()
        self._add_control_center()
        self._add_blank_space()

    def CompileWidgets(self):
        return bar.Bar(widgets = self.widgets,
                       size = 35,
                       margin = [5, 5, 0, 5],
                       background = "#00000000",
                       opacity = 0.75,
                       )



    def _add_group_box(self):
        self.widgets.append(
                widget.GroupBox(
                    margin_y = 3,
                    margin_x = 3,
                    padding_y = 5,
                    padding_x = 5,
                    borderwidth = 2,
                    #highlight_method = "block",
                    active = self.colors.foreground,
                    inactive = self.colors.faint_foreground,
                    this_current_screen_border = self.colors.accent,
                    other_current_screen_border = self.colors.faint_foreground,
                    this_screen_border = self.colors.highlight,
                    other_screen_border = self.colors.accent,
                    foreground = self.colors.foreground,
                    background = self.colors.background,
                    visible_groups = self.groups,
                    urgent_border = self.colors.faint_foreground,
                    **self.widget_defaults
                    )
                )
        
    def _add_battery(self):
        self.widgets.append(
                widget.Battery(
                    format = "B: {percent:2.0%}",
                    foreground = self.colors.foreground,
                    background = self.colors.background,
                    fontsize = 16,
                    #**self.widget_defaults
                )
            )
        
    def _add_clock(self):
        self.widgets.append(
                widget.Clock(
                    #format = "%A %d %B %Y %H:%M ",
                    format = "T: %H:%M",
                    foreground = self.colors.foreground,
                    background = self.colors.background,
                    fontsize = 16,
                    #**self.widget_defaults
                )
            )
    
    def _add_control_center(self):
        self.widgets.append(
                widget.TextBox(
                    text = "⚙",
                    fontsize = 18,
                    foreground = self.colors.foreground,
                    background = self.colors.background,
                    mouse_callbacks = {
                        "Button1": lazy.group["control_center_scratchpad"].dropdown_toggle("control_center_dropdown")
                        #"Button1": lambda: qtile.cmd_spawn("python /home/solve/.config/qtile/control_center.py")
                    }
                )
            )
        
    def _add_line_separator(self):
        self.widgets.append(
                widget.Sep(
                    linewidth = 1,
                    padding = 10,

                    foreground = self.colors.faint_foreground,
                    background = self.colors.background,
                )
            )

    def _add_blank_space(self):
        self.widgets.append(
                widget.Sep(
                    linewidth = 3,
                    padding = 5,

                    foreground = self.colors.background,
                    background = self.colors.background,
                )
            )


colorhandler = ColorSchemeHandler()
if colorhandler.check_scheme_exists(colorscheme_name, colorscheme_brightness):
    colorscheme = colorhandler.get_scheme(colorscheme_name, colorscheme_brightness)
else:
    colorscheme = colorhandler.get_scheme(colorscheme_name := "default", colorscheme_brightness := "dark")


# Keybindings
keys = KeyBindings(mod, terminal, editor, browser).keys


# Groups

group_handler = GroupHandler(mod, group_names, monitor_count) 
groups, group_keys = group_handler.get_groups_and_keys()
keys.extend(group_keys)
# NOTE : also need to add GroupHandler Scratchpad group for menus


# Layouts
layout_theme = {
    "border_on_single": True,
    "border_width": 1,
    "margin": [3, 5, 5, 5],
    "border_focus": colorscheme.highlight,
    "border_normal": colorscheme.faint_foreground
    }

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Zoomy(**layout_theme)
    ]


#NOTE: need to configure taskbar, widgets, screens, startup

screens = []
if wallpaper != "":
    if os.path.exists(wallpaper):
        pass
    else:
        wallpaper = ""
for monitor_id in range(monitor_count):
    group_names = group_handler.group_names_split[monitor_id]
    if wallpaper != "":
        
        screens.append(Screen(
            wallpaper = wallpaper,
            wallpaper_mode = "fill",
            top = TaskbarHandler(colorscheme, group_names).CompileWidgets()
        ))
    else:
        screens.append(Screen(
            top = TaskbarHandler(colorscheme, group_names).CompileWidgets()
            ))
        
@hook.subscribe.startup_once
def auto_startup():
    #subprocess.Popen(["bash", "/home/solve/.config/qtile/autostart.sh"])
    _reload_qtile(qtile, startup=True)


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
