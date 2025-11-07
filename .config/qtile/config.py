"""HDOS - Hyperactivity Disorder Operating System (hyper not hypr!) Qtile Configuration File
This file contains the main configuration settings for the HDOS Qtile window manager setup.
Modularization has been implemented to enhance readability and maintainability, so please refer to the individual module files for specific configurations and hacking.
"""

# Qtile imports:

from libqtile import layout, qtile, widget, hook, bar
from libqtile.config import Click, Drag, Group, Key, Match, Screen 
#from libqtile DropDown, ScratchPad
from libqtile.lazy import lazy

# Classes

###############
# Keybindings #
###############

def _reload_qtile(qtile):
    qtile.reload_config()
    qtile.spawn("bash home/solve/.config/qtile/reloadpicom.sh")


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
            Key([self.mod, "shift"], "end", lazy.shutdown(), desc="Shutdown Qtile"),

            Key([self.mod], "space", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

            ])
        
    def _multi_media_keys(self):
        self.keys.extend([
            Key([], "XF86AudioRaiseVolume", lazy.spawn("bash /home/solve/.config/qtile/volumecontrol.sh up"), desc="Increase volume"),
            Key([], "XF86AudioLowerVolume", lazy.spawn("bash /home/solve/.config/qtile/volumecontrol.sh down"), desc="Decrease volume"),
            Key([], "XF86AudioMute", lazy.spawn("bash /home/solve/.config/qtile/volumecontrol.sh mute"), desc="Mute/Unmute volume"),

            Key([], "XF86MonBrightnessUp", lazy.spawn("bash /home/solve/.config/qtile/brightness.sh up"), desc="Increase brightness"),
            Key([], "XF86MonBrightnessDown", lazy.spawn("bash /home/solve/.config/qtile/brightness.sh down"), desc="Decrease brightness"),
            
            Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause media"),

            Key([], "XF86KbdBrightnessUp", lazy.spawn("bash /home/solve/.config/qtile/kbd_brightness.sh"), desc="Increase keyboard backlight brightness"),
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
    
    #def _make_scratchpad_group(self):
    #    scratchpad_group = Group("scratchpad", [
    #        DropDown("term", self.terminal, width=0.5, height=0.5, x=0.25, y=0.25, opacity=0.9)
    #    ])
    #    self.groups.append(scratchpad_group)
    #    self.keys.extend([
    #        Key([self.mod], "t", lazy.group["scratchpad"].dropdown_toggle("term"), desc="Toggle Scratchpad Terminal")
    #    ])
    
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
                    format = "{percent:2.0%}",
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
                    format = "%H:%M",
                    foreground = self.colors.foreground,
                    background = self.colors.background,
                    fontsize = 16,
                    #**self.widget_defaults
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

# Universal settings



mod = "mod4"
terminal = "kitty"
browser = "brave"
editor = "code"

colorscheme = ColorSchemeHandler().get_scheme("default", "dark")
monitor_count = 1  # Set to the number of monitors you have

# Keybindings
keys = KeyBindings(mod, terminal, editor, browser).keys


# Groups
group_names = ["1", "2", "3", "4", "5"] # more: , "6", "7", "8", "9"]
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
wallpaper = "/home/solve/.config/wallpapers/wp12821730.jpg" # path to wallpaper image, or None
import os
if wallpaper:
    if os.path.exists(wallpaper):
        pass
    else:
        wallpaper = None
for monitor_id in range(monitor_count):
    group_names = group_handler.group_names_split[monitor_id]
    if wallpaper:
        
        screens.append(Screen(
            wallpaper = wallpaper,
            wallpaper_mode = "fill",
            top = TaskbarHandler(colorscheme, group_names).CompileWidgets()
        ))
    else:
        screens.append(Screen(
            top = TaskbarHandler(colorscheme, group_names).CompileWidgets()
            ))
        

import subprocess
@hook.subscribe.startup_once
def auto_startup():
    subprocess.Popen(["picom", "-c"])


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
