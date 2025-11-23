import time
from qtile_extras.popup import PopupSlider, PopupText, PopupRelativeLayout

from utils.colors import background, foreground, accent, faint_foreground
from utils.dotlogs import log
from utils.getmonitors import primary_monitor

def center_bottom_slider(qtile, text, level):
    """Show a simple slider popup centered at the bottom of the primary monitor, indicating the given level (0-100).
    Args:
        qtile: Qtile instance
        level: int - level to display on the slider (0-100)
        text: str - text to display above the slider e.g f"Brightness: {level}%" or "Volume: Muted" (left rough for exactly this scenario)
    """

    # sanitize level
    if level < 0:
        level = 0
    elif level > 100:
        level = 100

    color_below = accent  # e.g green for volume/brightness below current level
    color_above = faint_foreground  # e.g gray for volume/brightness above current level

    #min-max to keep popup size reasonable on very high or low res monitors
    width = min(max(0.3 * primary_monitor["width"], 200), 400)
    height = min(max(0.15 * primary_monitor["height"], 100), 200)
    bottom_padding = min(max(0.02 * primary_monitor["height"], 20), 50)

    pos_x = (primary_monitor["width"] - width) // 2
    pos_y = primary_monitor["height"] - height - bottom_padding

    popup = PopupRelativeLayout(
        qtile,
        width=width,
        height=height,
        pos_x=pos_x,
        pos_y=pos_y,
        rows = 2,
        cols = 1,
        background=background,
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
                background=background,
                color_below=color_below,
                color_above=color_above,
                marker_size=0,
                bar_size=5,
                highlight_radius=2,
                opacity=0.8,
            ),
            PopupText(
                # show numeric level so the popup isn't just an empty box
                text=text,
                background=background,
                foreground=foreground,
                fontsize=18,
                v_align="top",
                h_align="center",
                pos_x=0.05,
                pos_y=0.55,
                width=0.9,
                height=0.35,
            ),
        ],
    )
    return popup