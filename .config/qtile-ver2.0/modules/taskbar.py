from libqtile import bar, widget

from groups import formatted_group_names

class TaskbarHandler():
    def __init__(self, colorscheme, groups_for_this_screen, menu_state = None):
        self.groups = groups_for_this_screen
        self.colors = colorscheme
        self.widgets = []
        self.menu_state = menu_state
        self.widget_defaults = dict(
            font="Ubuntu Mono",
            fontsize=14,
        )

        # anything pre-spacer (left side)
        self._add_blank_space()
        self._add_group_box()
        self._add_line_separator()
        self._add_prompt_spawn()

        # add spacer
        self.widgets.append(
                widget.Spacer(
                    background = self.colors.background,
                )
            )
        # anything post-spacer (right side)
        self._add_window_name()
        self.widgets.append(
                widget.Spacer(
                    background = self.colors.background,
                )
            )
        self._add_line_separator()
        self._add_battery()
        self._add_line_separator()
        self._add_clock()
        if self.menu_state is not None:
            self._add_line_separator()
            self._add_control_center(self.menu_state)
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
        
    def _add_prompt_spawn(self):
        self.widgets.append(
                widget.Prompt(
                    prompt = "Run: ",
                    foreground = self.colors.foreground,
                    background = self.colors.background,
                    fontsize = 16,
                    #**self.widget_defaults
                )
            )
        
    def _add_window_name(self):
        self.widgets.append(
                widget.WindowName(
                    foreground = self.colors.foreground,
                    background = self.colors.background,
                    fontsize = 16,
                    #**self.widget_defaults
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
    
    def _add_control_center(self, menu):
        self.widgets.append(
                widget.TextBox(
                    text = "⚙",
                    fontsize = 18,
                    foreground = self.colors.foreground,
                    background = self.colors.background,
                    # use a direct callable so the popup receives the current qtile argument
                    mouse_callbacks = {
                        "Button1": lambda qtile, m=menu: m.toggle_menu(qtile)
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

    def _add_blank_space(self, linewidth=3, padding=5):
        self.widgets.append(
                widget.Sep(
                    linewidth = linewidth,
                    padding = padding,
                    foreground = self.colors.background,
                    background = self.colors.background,
                )
            )