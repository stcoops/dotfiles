

group_names = ["1", "2", "3", "4", "5", "6"]

def extend_groups_for_monitors(group_names, monitors):
    """Extend or adjust group names based on the number of monitors.
    - group_names: list - Define workspaces as 1D array for one monitor or for duplicate workspaces on multiple monitors, 
    or set to a 2D array for distinct workspaces on each monitor (if not enough, will recycle last monitor's workspaces)
    - monitors: list - list of detected monitors
    """
    if len(monitors) == 1:
        groups = [group_names[0] for _ in range(len(monitors))]
    else:
        groups = []
        for i in range (len(monitors)):
            if i < len(group_names):
                groups.append([group_names[i]])
            else:
                groups.append([group_names[-1]])  # recycle last workspace name if not enough monitors
    return groups