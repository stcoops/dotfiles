from modules.groups import _format_groups
from utils.getmonitors import monitors

if __name__ == "__main__":
    print("Testing groups module")
    group_names = ["1","2","3","4","5","6"]
    # group_names = [["1", "2", "3"], ["A", "B", "C"]]
    print("Formatted groups:", _format_groups(group_names))