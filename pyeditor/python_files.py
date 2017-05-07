
import datetime
import fnmatch
import glob
import os
import shutil
import sys
import logging

import re

from pyeditor.config import BASE_PATH, RUN_BAK_PATH, AUTO_BAK_PATH
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

        self.file_list={}

    def get_filenames(self):
        self.file_list.clear()

        filename_re = re.compile("(?P<date>\d{4}-\d{2}-\d{2} \d{1,2}h\d{1,2}m\d{1,2}s) (?P<filename>.*?)\.py")

        # glob with recursive=True is new in Python 3.5, but we want to support 3.4, too ;)
        for root, dirs, files in os.walk(BASE_PATH):
            for filename in files:
                if not fnmatch.fnmatch(filename, "*.py"):
                    log.debug("Skip non *.py file: %r", filename)
                    continue

                filepath = os.path.join(root, filename)

                re_result = filename_re.match(filename)
                if re_result is not None:
                    # remove date string from filename
                    date_string = re_result.group("date")
                    filename = re_result.group("filename")
                    # print(filename, date_string, filename)

                if filename not in self.file_list:
                    self.file_list[filename]=[filepath]
                else:
                    self.file_list[filename].append(filepath)

        filenames = list(self.file_list.keys())
        filenames.sort()

        return filenames

    def generate_filename(self, filename):
        dt = datetime.datetime.now(tz=None)
        filename = "{date} {name}.py".format(
            date=dt.strftime("%Y-%m-%d %Hh%Mm%Ss"),
            name=filename
        )
        return filename

    def get_run_bak_filepath(self, filename):
        filepath = self.generate_filename(filename)
        run_bak_filepath = os.path.join(
            RUN_BAK_PATH, filepath
        )
        return run_bak_filepath

    def get_auto_bak_filepath(self, filename):
        filepath = self.generate_filename(filename)
        auto_bak_filepath = os.path.join(
            AUTO_BAK_PATH, filepath
        )
        return auto_bak_filepath

    def run(self, filepath):
        TkSubprocess(
            self.editor_window.root,
            args = [sys.executable, filepath],
            output_callback=self.editor_window.append_exec_output,
            info_callback=self.editor_window.append_feedback_to_output
        )

    def run_source_listing(self, source_listing, filename):
        run_bak_filepath = self.get_run_bak_filepath(filename)
        log.info("Save to: %r", run_bak_filepath)
        with open(run_bak_filepath, "w") as f:
            f.write(source_listing)

        self.run(run_bak_filepath)

    def move_to_backup(self, filepath):
        filename = os.path.split(filepath)[1]
        destination_path = self.get_auto_bak_filepath(filename)
        log.info("move %r -> %r", filepath, destination_path)
        shutil.move(filepath, destination_path)

