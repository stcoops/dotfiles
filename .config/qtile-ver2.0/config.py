"""# Qtile configuration file - config.py"""

# importing utility variables & logger instance
from utils.dotlogs import log
from utils.getmonitors import monitors
from utils.colors import colors

# importing utility functions
from utils.makegroups import extend_groups_for_monitors


# User-defined variables
mod = "mod4"

default_apps = {
"terminal": "kitty",
"browser": "brave",
"editor": "code",
"notepad": "tjournal"
}

groups_names = [["1", "2", "3", "4", "5", "6"]]



# Extend groups based on detected monitors
groups = extend_groups_for_monitors(groups_names, monitors)


if __name__ == "__main__":
    log.info("--> running config.py as main script for testing purposes")
    log.info(f"Configured workspaces: {groups}")
    log.info(f"Using colors: {colors}")