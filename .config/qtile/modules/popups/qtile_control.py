from utils.structure import SCRIPTS_DIR, QTILE_DIR
import os
import subprocess
import threading
from modules.popups.templates.middle_text import middle_center_popup_text
from utils.dotlogs import log

from defaults import wallpaper
from utils.structure import WALLPAPERS_DIR
from utils.colors import refresh_colors


class QtileController:
    """Class to handle Qtile control actions like shutdown and reload."""

    def shutdown_qtile(self, qtile):
        middle_center_popup_text(qtile, "Shutting down...")
        qtile.call_later(2.0, qtile.shutdown)

    ##########
    # Reload #
    ##########

    def _run_and_notify(self, qtile, cmd, start_msg, success_msg=None, fail_msg=None, on_success=None, start_timeout=2.0, result_timeout=3.5, error_timeout=5.0):
        """Run cmd in a thread, show start_msg immediately, then show success/fail when it finishes.
        on_success is called on the Qtile main loop if returncode == 0.
        cmd should be a list (no shell) or a string (shell=True)."""
        log.debug(f"Preparing to run command: {str(cmd)}")
        # show a start popup so user gets immediate feedback
        middle_center_popup_text(qtile, start_msg)

        def worker():
            try:
                if isinstance(cmd, str):
                    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, start_new_session=True)
                else:
                    p = subprocess.run(cmd, capture_output=True, text=True, start_new_session=True)
                out = p.stdout or ""
                err = p.stderr or ""
                rc = p.returncode
            except Exception as e:
                rc = 1
                out = ""
                err = str(e)

            def finish():
                if rc == 0:
                    if success_msg:
                        middle_center_popup_text(qtile, success_msg + ("\n" + out if out else ""))
                    if on_success:
                        # schedule on_success after the success popup timeout so the popup isn't cleared by reload
                        def call_on_success():
                            try:
                                on_success()
                            except Exception as e:
                                middle_center_popup_text(qtile, "on_success callback failed:\n" + str(e))
                        qtile.call_later(result_timeout + 0.1, call_on_success)
                else:
                    msg = (fail_msg or "Command failed") + "\n" + (err or out or f"exit {rc}")
                    log.error(msg)
                    middle_center_popup_text(qtile, msg)
            # schedule UI changes on qtile's loop
            qtile.call_later(0, finish)

        threading.Thread(target=worker, daemon=True).start()


    def reload_qtile(self, qtile, startup=False):
        log.info("Reloading qtile configuration")
        if startup:
            # at startup just fire the helper scripts quickly (no need to wait)
            self._run_and_notify(qtile, ["bash", os.path.join(SCRIPTS_DIR, "reloadpicom.sh")], "Starting picom...", "Picom started", "Picom start failed")
            self._run_and_notify(qtile, ["wal", "-i", os.path.join(WALLPAPERS_DIR, wallpaper)], "Starting pywal with wallpaper...", "pywal started", "Pywal start failed")
            self._run_and_notify(qtile, ["bash", os.path.join(SCRIPTS_DIR, "reloadxcape.sh")], "Starting xcape...", "Xcape started", "Xcape start failed")
            self._run_and_notify(qtile, ["bash", os.path.join(SCRIPTS_DIR, "touchpadsetup.sh")], "setting touchpad...", "Touchpad started", "Touchpad start failed")
            return

        # Restart picom and xcape and report when each actually completes
        log.debug("Running helper scripts for reload")
        self._run_and_notify(
            qtile,
            ["bash", os.path.join(SCRIPTS_DIR, "reloadpicom.sh")],
            "Reloading picom...",
            "Picom reload complete",
            "Picom reload failed",
            start_timeout=0.5,
            result_timeout=0.5
        )

        self._run_and_notify(
            qtile,
            ["wal", "-i", os.path.join(WALLPAPERS_DIR, wallpaper)],
            "Reloading pywal with wallpaper...",
            "pywal reload complete",
            "pywal reload failed",
            start_timeout=0.5,
            result_timeout=3
        )

        refresh_colors()

        self._run_and_notify(
            qtile,
            ["bash", os.path.join(SCRIPTS_DIR, "reloadxcape.sh")],
            "Reloading xcape...",
            "Xcape reload complete",
            "Xcape reload failed",
            start_timeout=0.5,
            result_timeout=0.5
        )

        self._run_and_notify(
            qtile,
            ["bash", os.path.join(SCRIPTS_DIR, "touchpadsetup.sh"), "reset"],
            "Resetting touchpad...",
            "Touchpad reset complete",
            "Touchpad reset failed",
            start_timeout=0.5,
            result_timeout=0.5
        )

        # Run py_compile and reload only when it succeeds

        def on_config_ok():
            try:
                qtile.reload_config()
                middle_center_popup_text(qtile, "Reload complete")
            except Exception as e:
                log.error("Error reloading config: " + str(e))
                middle_center_popup_text(qtile, "Reload failed:\n" + str(e))

        self._run_and_notify(
            qtile,
            ["python", "-m", "py_compile", os.path.join(QTILE_DIR, "config.py")],
            "Testing qtile config...",
            "Config OK",
            "Config error",
            on_success=on_config_ok,
            start_timeout=1.5,
            result_timeout=0.5
        )

qtile_controller = QtileController()

def Qstartup(qtile):
    qtile_controller.reload_qtile(qtile, startup=True)

def Qshutdown(qtile):
    qtile_controller.shutdown_qtile(qtile)

def Qreload(qtile):
    qtile_controller.reload_qtile(qtile)