import curses
import json
import os
import shlex
import subprocess
import tempfile
from typing import List, Dict

#!/usr/bin/env python3
"""
A simple curses-based control panel for a window manager (qtile-friendly).

- Presents a list of actions (shell commands) you can run from the UI.
- Saves actions at ~/.config/qtile/control_center_actions.json
- Default actions include common qtile/pulse/brightness examples; adjust as needed.
- Navigate with Up/Down, Enter to run, "a" add, "e" edit, "d" delete, "r" rename,
    "o" toggle output pane, "q" quit. Output of the last command shown in the right/bottom pane.

Note: this program runs shell commands. For qtile control you can use whatever CLI you have,
for example the `qtile` CLI (e.g. "qtile cmd-obj -o / -f cmd_restart") or custom scripts.
"""


CONFIG_PATH = os.path.expanduser("~/.config/qtile/control_center_actions.json")


DEFAULT_ACTIONS = [
        {"name": "Reload qtile", "cmd": "qtile cmd-obj -o / -f reload"},
        {"name": "Restart qtile", "cmd": "qtile cmd-obj -o / -f restart"},
        {"name": "Shutdown qtile", "cmd": "qtile cmd-obj -o / -f shutdown"},
        {"name": "Toggle focused floating", "cmd": "qtile cmd-obj -o / -f toogle_floating || true"},
        {"name": "Spawn terminal", "cmd": "alacritty"},
        {"name": "Volume +5%", "cmd": "pactl set-sink-volume @DEFAULT_SINK@ +5%"},
        {"name": "Volume -5%", "cmd": "pactl set-sink-volume @DEFAULT_SINK@ -5%"},
        {"name": "Mute toggle", "cmd": "pactl set-sink-mute @DEFAULT_SINK@ toggle"},
        {"name": "Brightness +10%", "cmd": "brightnessctl set +10%"},
        {"name": "Brightness -10%", "cmd": "brightnessctl set 10%-"},
        {"name": "Run custom command...", "cmd": ""},  # placeholder to prompt user
]


def ensure_config():
        d = os.path.dirname(CONFIG_PATH)
        if not os.path.isdir(d):
                os.makedirs(d, exist_ok=True)
        if not os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                        json.dump(DEFAULT_ACTIONS, f, indent=2)


def load_actions() -> List[Dict]:
        ensure_config()
        try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                        actions = json.load(f)
                        if not isinstance(actions, list):
                                raise ValueError
                        return actions
        except Exception:
                return DEFAULT_ACTIONS.copy()


def save_actions(actions: List[Dict]):
        ensure_config()
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(actions, f, indent=2)


def run_cmd(cmd: str, timeout: int = 10) -> str:
        if not cmd:
                return "Empty command."
        # expand env-like @DEFAULT_SINK@ -> leave as-is (Pulse accepts @DEFAULT_SINK@)
        try:
                p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
                out = p.stdout.strip()
                err = p.stderr.strip()
                rc = p.returncode
                res = f"$ {cmd}\n\nReturn code: {rc}\n"
                if out:
                        res += "\nSTDOUT:\n" + out + "\n"
                if err:
                        res += "\nSTDERR:\n" + err + "\n"
                return res
        except subprocess.TimeoutExpired:
                return f"Command timed out after {timeout} seconds: {cmd}"


def prompt_popup(stdscr, prompt: str, default: str = "") -> str:
        curses.echo()
        h, w = stdscr.getmaxyx()
        win_h = 3
        win_w = max(40, len(prompt) + 10)
        win = curses.newwin(win_h, win_w, (h - win_h) // 2, (w - win_w) // 2)
        win.border()
        win.addstr(0, 2, " input ")
        win.addstr(1, 2, prompt)
        win.refresh()
        stdscr.move((h - win_h) // 2 + 1, (w - win_w) // 2 + 2 + len(prompt))
        stdscr.clrtoeol()
        try:
                s = stdscr.getstr((h - win_h) // 2 + 1, (w - win_w) // 2 + 2 + len(prompt), 1024)
                val = s.decode("utf-8") if isinstance(s, bytes) else str(s)
        except Exception:
                val = default
        curses.noecho()
        return val if val else default


def edit_in_editor(initial: str) -> str:
        EDITOR = os.environ.get("EDITOR", "vi")
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".tmp") as tf:
                tf.write(initial)
                tf.flush()
                path = tf.name
        try:
                subprocess.run([EDITOR, path])
                with open(path, "r", encoding="utf-8") as f:
                        return f.read().rstrip("\n")
        finally:
                try:
                        os.unlink(path)
                except Exception:
                        pass


def show_text_popup(stdscr, text: str):
        """Show a centered, scrollable popup with the given text. Close with 'q' or Enter."""
        curses.curs_set(0)
        h, w = stdscr.getmaxyx()
        lines = text.splitlines() or [""]
        win_h = min(h - 4, max(10, min(len(lines) + 2, h - 4)))
        # width based on longest line but not wider than terminal
        max_line_len = max((len(l) for l in lines), default=40)
        win_w = min(w - 4, max(40, max_line_len + 4))
        starty = (h - win_h) // 2
        startx = (w - win_w) // 2
        win = curses.newwin(win_h, win_w, starty, startx)
        win.keypad(True)
        scroll = 0
        inner_h = win_h - 2
        while True:
                win.clear()
                win.border()
                title = " Output (Up/Down to scroll, q to close) "
                try:
                        win.addstr(0, max(2, (win_w - len(title)) // 2), title, curses.A_REVERSE)
                except curses.error:
                        pass
                # adjust scroll range
                if scroll + inner_h > len(lines):
                        scroll = max(0, len(lines) - inner_h)
                visible = lines[scroll : scroll + inner_h]
                for i, line in enumerate(visible):
                        try:
                                win.addnstr(1 + i, 1, line, win_w - 2)
                        except curses.error:
                                pass
                win.refresh()
                ch = win.getch()
                if ch in (curses.KEY_UP, ord("k")):
                        scroll = max(0, scroll - 1)
                elif ch in (curses.KEY_DOWN, ord("j")):
                        if scroll + inner_h < len(lines):
                                scroll += 1
                elif ch in (ord("q"), 27, 10, 13):
                        break


def draw(stdscr):
        curses.curs_set(0)
        actions = load_actions()
        selected = 0
        list_scroll = 0

        while True:
                stdscr.clear()
                h, w = stdscr.getmaxyx()

                # Title centered
                title = "Control Center"
                try:
                        stdscr.addstr(1, max(0, (w - len(title)) // 2), title, curses.A_BOLD | curses.A_UNDERLINE)
                except curses.error:
                        pass

                # Prepare list layout
                max_visible = max(1, h - 8)
                # ensure selected is visible
                if selected < list_scroll:
                        list_scroll = selected
                if selected >= list_scroll + max_visible:
                        list_scroll = selected - max_visible + 1

                visible_actions = actions[list_scroll : list_scroll + max_visible]
                # compute content width to center horizontally
                names = [a.get("name", "") for a in visible_actions]
                longest = max((len(n) for n in names), default=20)
                content_w = min(longest + 6, w - 6)
                start_y = max(3, (h - len(visible_actions)) // 2)
                start_x = max(2, (w - content_w) // 2)

                for i, act in enumerate(visible_actions):
                        idx = list_scroll + i
                        name = act.get("name", "")
                        prefix = "▶ " if idx == selected else "  "
                        line = f"{prefix}{name}"
                        # center line within content_w
                        pad = max(0, (content_w - len(line)) // 2)
                        x = start_x + pad
                        y = start_y + i
                        try:
                                if idx == selected:
                                        stdscr.addstr(y, x, line[:content_w], curses.A_REVERSE)
                                else:
                                        stdscr.addstr(y, x, line[:content_w])
                        except curses.error:
                                pass

                # Selected command preview (centered)
                if actions:
                        sel_cmd = actions[selected].get("cmd", "")
                        preview = "Cmd: " + (sel_cmd if sel_cmd else "<empty>")
                        try:
                                stdscr.addstr(start_y + len(visible_actions) + 1, max(0, (w - len(preview)) // 2), preview[: w - 4])
                        except curses.error:
                                pass

                # Footer / help (centered)
                #help_text = "Enter: run  a:add  e:edit  d:delete  r:rename  q:quit"
                #try:
                #        stdscr.addstr(h - 2, max(0, (w - len(help_text)) // 2), help_text)
                #except curses.error:
                #        pass

                stdscr.refresh()
                ch = stdscr.getch()
                if ch in (curses.KEY_UP, ord("k")):
                        selected = max(0, selected - 1)
                elif ch in (curses.KEY_DOWN, ord("j")):
                        selected = min(len(actions) - 1, selected + 1)
                elif ch in (curses.KEY_NPAGE,):
                        selected = min(len(actions) - 1, selected + 5)
                elif ch in (curses.KEY_PPAGE,):
                        selected = max(0, selected - 5)
                elif ch in (10, 13):  # Enter
                        if not actions:
                                show_text_popup(stdscr, "No actions configured.")
                        else:
                                cmd = actions[selected].get("cmd", "")
                                if not cmd:
                                        # prompt for a command
                                        cmd = prompt_popup(stdscr, "Command: ")
                                        if not cmd:
                                                # cancelled
                                                continue
                                        actions[selected]["cmd"] = cmd
                                        save_actions(actions)
                                out = run_cmd(cmd, timeout=30)
                                show_text_popup(stdscr, out)
                elif ch == ord("q"):
                        break
                elif ch == ord("a"):
                        name = prompt_popup(stdscr, "Name: ")
                        cmd = prompt_popup(stdscr, "Command: ")
                        if name:
                                actions.append({"name": name, "cmd": cmd})
                                save_actions(actions)
                                selected = len(actions) - 1
                elif ch == ord("d"):
                        if actions:
                                confirm = prompt_popup(stdscr, f"Delete '{actions[selected]['name']}'? (y/N): ", "n")
                                if confirm.lower().startswith("y"):
                                        actions.pop(selected)
                                        selected = max(0, selected - 1)
                                        save_actions(actions)
                elif ch == ord("e"):
                        if actions:
                                # open editor for command
                                cur = actions[selected].get("cmd", "")
                                new = edit_in_editor(cur)
                                actions[selected]["cmd"] = new
                                save_actions(actions)
                elif ch == ord("r"):
                        if actions:
                                newname = prompt_popup(stdscr, "New name: ", actions[selected].get("name", ""))
                                if newname:
                                        actions[selected]["name"] = newname
                                        save_actions(actions)
                else:
                        # ignore unknown keys
                        pass


def main():
        curses.wrapper(draw)


if __name__ == "__main__":
        main()