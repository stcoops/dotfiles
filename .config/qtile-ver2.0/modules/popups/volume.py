from popups.templates.slider import center_popup_slider
from utils.structure import SCRIPTS_DIR
from utils.dotlogs import log
import os, subprocess, time

class VolumeController:
    def __init__(self):
        self.popup = None
    
    def _make_popup(self, level):
        """Show volume popup."""
        if level < 0:
            level = 0
            text = "Volume: Muted"
        else:
            text = f"Volume: {level}%"

        if self.popup:
            self.popup.close()
            self.popup = None

        self.popup = center_popup_slider(
            self.qtile,
            text=text,
            level=level
        )

        time.sleep(1)
        self.popup.close()
        self.popup = None

    def _change_volume(self, change: int | str):
        """Change volume by change (positive or negative or mute).
        Args:
            qtile: Qtile instance (via lazy.function)
            change: int - positive or negative value to change volume by
                    str - "mute" to toggle mute
        """

        # Get current volume and mute status
        try:
            result = subprocess.run(
                ["bash", os.path.join(SCRIPTS_DIR, "volumecontrol.sh"), "get"],
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout.strip().splitlines()
            current_volume = int(output[0])
            is_muted = output[1].lower() == "mute"

        except Exception as e:
            log.error("Error getting volume: " + str(e))
            current_volume = 50.0  # Default if command fails
            is_muted = False

        # Calculate new volume
        

        # Show popup
        if change == "mute":
            # toggle mute
            subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "volumecontrol.sh"), "mute"])

            if not is_muted:
                # If volume was not previously muted, show muted popup
                self._make_popup(self.qtile, -1)
            else:
                # If volume *was* previously muted, show current volume popup
                self._make_popup(self.qtile, current_volume)

        elif isinstance(change, int):
            if is_muted:
                # If muted, unmute first as changing volume implies unmuting
                subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "volumecontrol.sh"), "mute"])

            new_volume = min(100, max(0, current_volume + change))
            subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "volumecontrol.sh"), "set", str(int(new_volume))])
            self._make_popup(self.qtile, new_volume)

    def volume_up(self, qtile ,step=5):
        """Increase volume by step%."""
        self.qtile = qtile
        self._change_volume(step)

    def volume_down(self, qtile, step=5):
        """Decrease volume by step%."""
        self.qtile = qtile
        self._change_volume(-step)

    def volume_mute(self, qtile):
        """Toggle mute."""
        self.qtile = qtile
        self._change_volume("mute")