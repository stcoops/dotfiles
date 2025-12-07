from libqtile.config import Key
from libqtile.lazy import lazy

import os


from defaults import mod, browser, editor, terminal

from utils.structure import SCRIPTS_DIR
from utils.dotlogs import log
from utils.getmonitors import monitors


from modules.popups.volume import VolumeController
from modules.popups.brightness import BrightnessController
from modules.popups.qtile_control import Qshutdown
from modules.popups.qtile_control import Qreload

from modules.groups import group_keys

class KeyBindings:

    def __init__(self):
        # Initialize controllers
        self.mod = mod
        self.terminal = terminal
        self.volume_controller = VolumeController()
        self.brightness_controller = BrightnessController()

        self.keys = []

        self._base_keys()
        self._multi_media_keys()
        self._add_group_keys()
        #self._toggle_bar()


        if len(monitors) > 1:
            self._multi_screen_keys(len(monitors))
        if browser:
            self.browser = browser
            self._browser_key()
        if editor:
            self.editor = editor
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


            Key([self.mod, "shift"], "home", lazy.function(Qreload), desc="Reload the config"),
            Key([self.mod, "shift"], "end", lazy.function(Qshutdown), desc="Shutdown Qtile"),

            Key([self.mod], "space", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
        ])
        
    def _multi_media_keys(self):
        self.keys.extend([
            Key([], "XF86AudioRaiseVolume", lazy.function(self.volume_controller.volume_up), desc="Increase volume"),
            Key([], "XF86AudioLowerVolume", lazy.function(self.volume_controller.volume_down), desc="Decrease volume"),
            Key([], "XF86AudioMute", lazy.function(self.volume_controller.volume_mute), desc="Mute/Unmute volume"),

            Key([], "XF86MonBrightnessUp", lazy.function(self.brightness_controller.increase_brightness), desc="Increase brightness"),
            Key([], "XF86MonBrightnessDown", lazy.function(self.brightness_controller.decrease_brightness), desc="Decrease brightness"),

            Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause media"), 

            Key([], "XF86KbdBrightnessUp", lazy.spawn("bash " + os.path.join(SCRIPTS_DIR, "kbd_brightness.sh")), desc="Increase keyboard backlight brightness"),
        ])

    def _add_group_keys(self):
        self.keys.extend(group_keys)

    def _toggle_bar(self):
        self.keys.append(
            Key([self.mod], "q", lazy.show_hide_bar(), desc="Toggle taskbar visibility"),
            )
        
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
        self.keys.append(
            Key([self.mod], "v", lazy.spawn(editor), desc="Launch file editor")
            )
        
keys = KeyBindings().keys