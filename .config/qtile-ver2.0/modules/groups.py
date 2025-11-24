from libqtile.config import Group, ScratchPad, DropDown, Key
from libqtile.lazy import lazy


from utils.dotlogs import log
from utils.getmonitors import monitors

from defaults import terminal, mod, notepad, groups_names

def _format_groups(group_names):
    """Extend or adjust group names based on the number of monitors.
    """
    # if 1D array given, make it 2D based on number of monitors
    if all(isinstance(i, str) for i in group_names):
        group_names = [group_names for _ in range(len(monitors))]

    # adjust group names based on number of monitors
    if len(monitors) == 1:
        groups = [group_names[0] for _ in range(len(monitors))]
    
    else:
        groups = []
        for i in range (len(monitors)):
            if i < len(group_names):
                groups.append([group_names[i]])
            else:
                groups.append([group_names[-1]])  # recycle last workspace name if not enough monitors
    return groups # a 2D array of group names, with each sub-array for each monitor

def _focus_group_and_screen(qtile, screen_index, group_name):
    log.debug(f"Focusing screen {screen_index} and group {group_name}")
    qtile.focus_screen(screen_index)
    qtile.groups_map[group_name].toscreen()

class GroupHandler:
    def __init__(self, group_names: list[list[str]]):
        """Manage groups and associated keybindings.
        - group_names: list - Define workspaces as 1D array for one monitor or for duplicate workspaces on multiple monitors, 
        or set to a 2D array for distinct workspaces on each monitor (if not enough, will recycle last monitor's workspaces)
        """
        self.mod = mod
        self.keys = []
        self.groups= []
        self._init_groups(group_names)
        self._make_scratchpad_group()

    def _init_groups(self, group_names):
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
         
    def _make_scratchpad_group(self):
        scratchpad_group = ScratchPad(name="scratchpad", dropdowns=[
            DropDown("term", str(terminal + " htop"), width=0.6, height=0.6, x=0.2, y=0.2, opacity=0.6, on_focus_lost_hide=True),
                ], single=True
            )
        self.groups.append(scratchpad_group)
        self.keys.extend([
            Key([self.mod], "t", lazy.group["scratchpad"].dropdown_toggle("term"), desc="Toggle Scratchpad Terminal")
        ])


# Initialize groups based on user-defined names and monitors
formatted_group_names = _format_groups(groups_names)
group_handler = GroupHandler(formatted_group_names)
groups, group_keys = group_handler.get_groups_and_keys()
# group_keys --> to be imported and added to keybindings in keybindings.py
# groups --> to be imported and added to qtile config in config.py
# formatted_group_names --> to be imported in taskar in taskbar.py