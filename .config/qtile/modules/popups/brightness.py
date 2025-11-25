from modules.popups.templates.slider import center_bottom_slider
from utils.structure import SCRIPTS_DIR
from utils.dotlogs import log
import os, subprocess, time

class BrightnessController:
    """Class to handle brightness control and popups."""
    def __init__(self):
        self.popup = None

    def _make_popup(self, level):
        """Show brightness popup."""
        if self.popup:
            self.popup.close()
            self.popup = None
        self.popup = center_bottom_slider(
            self.qtile,
            text=f"Brightness: {level}%",
            level=level
        )
        time.sleep(1)
        self.popup.close()
        self.popup = None

    def _change_brightness(self, signed_step):
        try:
            result = subprocess.run(
                ["bash", os.path.join(SCRIPTS_DIR, "brightness.sh"), "get"],
                capture_output=True,
                text=True,
                check=True
            )
            current_brightness = float(result.stdout.strip())
        except Exception as e:
            log.error("Error fetching brightness" + str(e))
            current_brightness = 100  # Default if command fails

        # calculate new brightness
        new_brightness = current_brightness + signed_step

        # clamp new brightness between |signed_step| and 100 (where |x| is positive value of x)
        if signed_step > 0 and new_brightness > 100:
            new_brightness = 100
        elif signed_step < 0 and new_brightness < -1*signed_step:
            new_brightness = -1*signed_step
        
        subprocess.run(
            ["bash", os.path.join(SCRIPTS_DIR, "brightness.sh"), "set", str(new_brightness)]
        )

        self._make_popup(int(new_brightness))

    def increase_brightness(self, qtile, step=10):
        """Increase brightness by 10%."""
        self.qtile = qtile
        self._change_brightness(step)

    def decrease_brightness(self, qtile, step=10):
        """Decrease brightness by 10%."""
        self.qtile = qtile
        self._change_brightness(-1*step)