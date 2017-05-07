
import datetime
import os
import sys
import logging

from pyeditor.config import RUN_BAK_PATH, AUTO_BAK_PATH
from pyeditor.tk_helpers.tk_subprocess import TkSubprocess


log = logging.getLogger(__name__)


class PythonFiles:
    """
    Handle file load/save/run stuff
    """
    def __init__(self, editor_window):
        self.editor_window = editor_window

        self.script_proc = None

        os.makedirs(RUN_BAK_PATH, mode=0o766, exist_ok=True)
        os.makedirs(AUTO_BAK_PATH, mode=0o766, exist_ok=True)

        self.current_filename="unnamed"

    def generate_filename(self):
        dt = datetime.datetime.now(tz=None)
        filename = "{date} {name}.py".format(
            date=dt.strftime("%Y-%m-%d %Hh%Mm%Ss"),
            name=self.current_filename
        )
        return filename

    def get_run_bak_filepath(self):
        filename = self.generate_filename()
        run_bak_filepath = os.path.join(
            RUN_BAK_PATH, filename
        )
        return run_bak_filepath

    def run(self, filepath):
        TkSubprocess(
            self.editor_window.root,
            args = [sys.executable, filepath],
            callback=self.editor_window.append_exec_output
        )

    def run_source_listing(self, source_listing):
        run_bak_filepath = self.get_run_bak_filepath()
        log.info("Save to: %r", run_bak_filepath)
        with open(run_bak_filepath, "w") as f:
            f.write(source_listing)

        self.run(run_bak_filepath)
