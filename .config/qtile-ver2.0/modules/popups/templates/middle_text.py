from libqtile.popup import PopupRelativeLayout, PopupText

from utils.colors import background, foreground
from utils.dotlogs import log
from utils.getmonitors import primary_monitor
import time

def middle_center_popup_text(qtile, message):
    """Create a simple centered popup with one PopupText, in the center middle of the screen."""

    #min-max to keep popup size reasonable on very high or low res monitors
    width = min(max(0.4 * primary_monitor["width"], 300), 500)
    height = min(max(0.2 * primary_monitor["height"], 150), 250)
    
    popup = PopupRelativeLayout(
        qtile,
        width=width,
        height=height,
        background=background,
        controls=[
            PopupText(
                text=message,
                background=background,
                foreground=foreground,
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
    return popup