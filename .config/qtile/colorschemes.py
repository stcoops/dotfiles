"""colorschemes.py - file containing all included colorschemes. Formatting is described in the help_string below (for custom schemes and hacking on this config), note each scheme has a light and dark mode built-in. current included colorschemes are as follows:
    - Default
    -
    -
"""

help_string = """
Colorschemes are defined as dictionaries, with two keys: "light" and "dark". Each key maps to a list of color hex codes, which are used throughout the configuration.
The order of colors in the list is important, as each index corresponds to a specific UI element. The current order is as follows:
0: Background color
1: Foreground color
2: Accent color
3: Highlight color
4: Faint foreground color (slightly brighter than background)
5: Tinted foreground color (accent flavoured foreground)
"""

class ColourScheme:
    def __init__(self, scheme: list):
        self.foreground = scheme[0]
        self.background = scheme[1] 
        self.accent = scheme[2]
        self.highlight = scheme[3]
        self.faint_foreground = scheme [4] # should be slightly brighter than background
        self.tinted_foreground = scheme[5]

schemes = {}
schemes["default"] = {
        "light": [
            "#",
            "#",
            "#",
            "#",
            ],
        "dark": ColourScheme([
            "#C6C6EB",
            "#212130",
            "#5E49AA",
            "#744FEC",
            "#383846",
            "#9099E9",
            ])
            }
