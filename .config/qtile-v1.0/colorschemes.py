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
    "light": ColourScheme([
        "#F7F9FC",
        "#2B2D42",
        "#5E49AA",
        "#744FEC",
        "#E6E7EE",
        "#6D5FE3",
    ]),
    "dark": ColourScheme([
        "#C6C6EB",
        "#212130",
        "#5E49AA",
        "#744FEC",
        "#383846",
        "#9099E9",
    ])
}

schemes["solarized"] = {
    "light": ColourScheme([
        "#fdf6e3",
        "#657b83",
        "#b58900",
        "#93a1a1",
        "#eee8d5",
        "#6c71c4",
    ]),
    "dark": ColourScheme([
        "#002b36",
        "#839496",
        "#b58900",
        "#268bd2",
        "#073642",
        "#93a1a1",
    ])
}

schemes["gruvbox"] = {
    "light": ColourScheme([
        "#fbf1c7",
        "#3c3836",
        "#d65d0e",
        "#bdae93",
        "#f2e5bc",
        "#a5763a",
    ]),
    "dark": ColourScheme([
        "#282828",
        "#ebdbb2",
        "#fb4934",
        "#fabd2f",
        "#3c3836",
        "#b8bb26",
    ])
}

schemes["dracula"] = {
    "light": ColourScheme([
        "#f8f8f2",
        "#282a36",
        "#bd93f9",
        "#ff79c6",
        "#f1eff8",
        "#6272a4",
    ]),
    "dark": ColourScheme([
        "#282a36",
        "#f8f8f2",
        "#bd93f9",
        "#ff79c6",
        "#44475a",
        "#50fa7b",
    ])
}

schemes["nord"] = {
    "light": ColourScheme([
        "#eceff4",
        "#2e3440",
        "#5e81ac",
        "#88c0d0",
        "#e5e9f0",
        "#81a1c1",
    ]),
    "dark": ColourScheme([
        "#2e3440",
        "#d8dee9",
        "#81a1c1",
        "#88c0d0",
        "#3b4252",
        "#8fbcbb",
    ])
}

schemes["tokyo-night"] = {
    "light": ColourScheme([
        "#f6f9fb",
        "#202328",
        "#2ac3de",
        "#7aa2f7",
        "#dce7ef",
        "#5cc3f6",
    ]),
    "dark": ColourScheme([
        "#1a1b26",
        "#c0caf5",
        "#7aa2f7",
        "#9ece6a",
        "#2a2b3a",
        "#7dcfff",
    ])
}

schemes["material"] = {
    "light": ColourScheme([
        "#ffffff",
        "#2b2b2b",
        "#e06c75",
        "#98c379",
        "#f0f0f0",
        "#61afef",
    ]),
    "dark": ColourScheme([
        "#282c34",
        "#abb2bf",
        "#e06c75",
        "#98c379",
        "#3b4048",
        "#56b6c2",
    ])
}
