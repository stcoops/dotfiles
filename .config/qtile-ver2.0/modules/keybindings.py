from libqtile.config import Key
from libqtile.lazy import lazy

import os

from utils.structure import SCRIPTS_DIR
from modules.popups.volume import VolumeController
from modules.popups.brightness import BrightnessController
from modules.popups.qtile_control import QtileController

class KeyBindings:

    def __init__(self, mod, terminal, editor=None, browser=None, menu_state=None, screen_count=1):
        self.mod = mod
        self.terminal = terminal
        self.browser = browser
        self.editor = editor
        self.menu_state = menu_state


        self.volume_controller = VolumeController()
        self.brightness_controller = BrightnessController()
        self.qtile_controller = QtileController()


        self.keys = []
        self._base_keys()
        self._multi_media_keys()
        if screen_count > 1:
            self._multi_screen_keys(screen_count)
        if self.browser:
            self._browser_key()
        if self.editor:
            self._file_editor()
        if self.menu_state:
            self._menu_key()

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


            Key([self.mod, "shift"], "home", lazy.function(self.qtile_controller.reload_qtile), desc="Reload the config"),
            Key([self.mod, "shift"], "end", lazy.function(self.qtile_controller.shutdown_qtile), desc="Shutdown Qtile"),

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
    menu = """
    def _menu_key(self):
        self.menu_state = MenuState()
        self.keys.append(
            Key([], "XF86MyComputer", lazy.function(self.menu_state.toggle_menu), desc="Toggle menu popup"),
            )
    """
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
        
    def _add_prompt_spawn(self):
        self.keys.append(
            Key([self.mod], "x", lazy.spawncmd(), desc="Spawn a command using a prompt widget")
        )