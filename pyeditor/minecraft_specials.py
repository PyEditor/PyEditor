import logging
import shutil

import psutil
import subprocess

log = logging.getLogger(__name__)

try:
    import mcpi
except ImportError as err:
    log.info("No mcpi available: %s" % err)
    MCPI_AVAILABLE=False
else:
    MCPI_AVAILABLE=True


MINECRAFT_BIN="minecraft-pi"
MINECRAFT_PORT=4711# UDP


# from idlelib import autocomplete_w
class MinecraftSpecials:
    """
    special Minecraft features, if available
    """
    def __init__(self, editor):
        if not MCPI_AVAILABLE:
            log.debug("Skip expand editor with minecraft stuff.")
            self.mcpi_available = False
        else:
            self.minecraft_filepath=shutil.which(MINECRAFT_BIN)
            log.debug("minecraft filepath: %r", self.minecraft_filepath)
            if self.minecraft_filepath is None:
                self.mcpi_available = False
                log.info("Skip expand editor with minecraft stuff")
            else:
                self.mcpi_available = True
                self.expand_editor(editor)

    START_COMMAND_LABEL="start Minecraft"
    def expand_editor(self, editor):
        self.editor_root = editor.root
        editor.menubar.add_command(
            label=self.START_COMMAND_LABEL,
            command=self.startup_minecraft
        )
        #.config(state=Tkinter.DISABLED)

    def is_running(self):
        for ps in psutil.process_iter():
            if ps.name() == MINECRAFT_BIN:
                log.debug("minecraft is running.")
                return True
        log.debug("minecraft is not running.")
        return False

    def startup_minecraft(self):
        if self.is_running():
            log.info("Skip start minecraft, because it's already running ;)")
        else:
            log.info("Start minecraft: %r", self.minecraft_filepath)
            subprocess.Popen([self.minecraft_filepath])
