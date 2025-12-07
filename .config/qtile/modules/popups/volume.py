from modules.popups.templates.slider import center_bottom_slider
from utils.structure import SCRIPTS_DIR
from utils.dotlogs import log
import os, subprocess, time

class VolumeController:
    def __init__(self):
        self.popup = None
    
    def _make_popup(self, level):
        """Show volume popup."""
        if not isinstance(level, int):
            raise TypeError("_make_popup: level must be an integer")
        if level == 192168:  # muted
            level = 0
            text = "Volume: Muted"
        else:
            text = f"Volume: {level}%"
        
        try:
            if self.popup:
                self.popup.hide()
                log.debug("Hiding existing volume popup")
                self.popup = None
        except Exception as e:
            log.error("Error doodad line 26 existing volume popup: " + str(e))
            pass

        self.popup = center_bottom_slider(
            self.qtile,
            text=text,
            level=level
        )


        self.popup.show()

        time.sleep(1)
        #self.popup.close()
        self.popup.hide()
        try:
            del self.popup
        except Exception as e:
            log.error("Error deleting volume popup: " + str(e))

    def _change_volume(self, change: int | str):
        """Change volume by change (positive or negative or mute).
        Args:
            qtile: Qtile instance (via lazy.function)
            change: int - positive or negative value to change volume by
                    str - "mute" to toggle mute
        """
        log.debug(f"Changing volume by: {change}")

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
            current_volume = 50  # Default if command fails
            is_muted = False

        # Calculate new volume
        

        # Show popup
        if change == "mute":
            # toggle mute
            subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "volumecontrol.sh"), "mute"])

            if not is_muted:
                # If volume was not previously muted, show muted popup
                self._make_popup(192168)
            else:
                # If volume *was* previously muted, show current volume popup
                self._make_popup(current_volume)

        elif isinstance(change, int):
            if is_muted:
                # If muted, unmute first as changing volume implies unmuting
                subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "volumecontrol.sh"), "mute"])

            new_volume = min(100, max(0, current_volume + change))
            subprocess.run(["bash", os.path.join(SCRIPTS_DIR, "volumecontrol.sh"), "set", str(int(new_volume))])
            self._make_popup(new_volume)
        else:
            log.error("_change_volume: change must be int or 'mute'")

    def volume_up(self, qtile ,step=5):
        """Increase volume by step%."""
        self.qtile = qtile
        try:
            self._change_volume(step)
        except Exception as e:
            log.error("Error increasing volume: " + str(e))

    def volume_down(self, qtile, step=5):
        """Decrease volume by step%."""
        self.qtile = qtile
        try:
            self._change_volume(-step)
        except Exception as e:
            log.error("Error decreasing volume: " + str(e))

    def volume_mute(self, qtile):
        """Toggle mute."""
        self.qtile = qtile
        try:
            self._change_volume("mute")
        except Exception as e:
            log.error("Error toggling mute: " + str(e)) 