from libqtile import layout

from utils.colors import highlight, faint_foreground
from utils.dotlogs import log
from defaults import layout_margin


layout_theme = {
    "border_on_single": True,
    "border_width": 1,
    "margin": layout_margin,
    "border_focus": highlight,
    "border_normal": faint_foreground
    }

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Zoomy(**layout_theme)
    ]

log.debug(f"Layouts configured: {[type(l).__name__ for l in layouts]}")