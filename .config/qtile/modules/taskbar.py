from libqtile import bar, widget

from utils.colors import foreground, background, cursor, faint_foreground, accent, highlight, tinted_foreground
from utils.dotlogs import log
from defaults import taskbar_height, taskbar_margin

class Taskbar():
    def __init__(self, groups_for_this_screen):
        self.groups = groups_for_this_screen
        self.widgets = []
        self.widget_defaults = dict(
            font="Ubuntu Mono",
            fontsize=14,
        )

        # anything pre-spacer (left side)
        self._add_blank_space()
        self._add_group_box()
        self._add_line_separator()
        self._add_window_name()

        # add spacer
        self.widgets.append(
                widget.Spacer(
                    background = background,
                )
            )
        # anything post-spacer (right side)
        self._add_line_separator()
        self._add_battery()
        self._add_line_separator()
        self._add_clock()
        self._add_blank_space()

    def CompileWidgets(self):
        return bar.Bar(widgets = self.widgets,
                       size = taskbar_height,
                       margin = taskbar_margin,
                       background = "#00000000",
                       opacity = 0.45,
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
                    active = foreground,
                    inactive = faint_foreground,
                    this_current_screen_border = accent,
                    other_current_screen_border = faint_foreground,
                    this_screen_border = highlight,
                    other_screen_border = accent,
                    foreground = foreground,
                    background = background,
                    visible_groups = self.groups,
                    urgent_border = faint_foreground,
                    **self.widget_defaults
                    )
                )
        
    def _add_window_name(self):
        self.widgets.append(
                widget.WindowName(
                    foreground = foreground,
                    background = background,
                    fontsize = 16,
                    #**self.widget_defaults
                )
            )
        
    def _add_battery(self):
        self.widgets.append(
                widget.Battery(
                    format = "B: {percent:1.0%}",
                    foreground = foreground,
                    background = background,
                    fontsize = 16,
                    #**self.widget_defaults
                )
            )
        
    def _add_clock(self):
        self.widgets.append(
                widget.Clock(
                    #format = "%A %d %B %Y %H:%M ",
                    format = "T: %H:%M",
                    foreground = foreground,
                    background = background,
                    fontsize = 16,
                    #**self.widget_defaults
                )
            )
        
    def _add_line_separator(self):
        self.widgets.append(
                widget.Sep(
                    linewidth = 1,
                    padding = 10,

                    foreground = faint_foreground,
                    background = background,
                )
            )

    def _add_blank_space(self, linewidth=3, padding=5):
        self.widgets.append(
                widget.Sep(
                    linewidth = linewidth,
                    padding = padding,
                    foreground = background,
                    background = background,
                )
            )