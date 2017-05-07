import datetime
import os
import queue
import subprocess
import sys
import logging
from threading import Thread
from tkinter import StringVar, READABLE

from pyeditor.config import RUN_BAK_PATH, AUTO_BAK_PATH

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
        if self.script_proc is not None:
            returncode = self.script_proc.poll()
            if returncode is None: # process hasn’t terminated yet
                log.info("Kill old running script, PID: %r", self.script_proc.pid)
                self.script_proc.kill()
            else:
                log.debug("Old script process returned with: %r", returncode)
            self.script_proc=None

        args = [sys.executable, filepath]
        log.info("run: %s" % " ".join(args))
        self.script_proc = subprocess.Popen(
            args,
            bufsize=0,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        log.debug("PID: %r", self.script_proc.pid)

        # note: Widget.tk.createfilehandler() is not available on Windows:
        # https://docs.python.org/3.6/library/tkinter.html#file-handlers

        # launch thread to read the subprocess output
        #   (put the subprocess output into the queue in a background thread,
        #    get output from the queue in the GUI thread.
        #    Output chain: process.readline -> queue -> label)
        q = queue.Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        t = Thread(target=self.process_reader_thread, args=[q])
        t.daemon = True # close pipe if GUI process exits
        t.start()

        self.update_output_loop(q)

    def process_reader_thread(self, q):
        """Read subprocess output and put it into the queue."""
        try:
            with self.script_proc.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    line = line.decode("utf-8")
                    q.put(line)
        finally:
            q.put(None)

    def iter_queue(self, q):
        try:
            while True:
                yield q.get_nowait()
        except queue.Empty:
            return None

    def update_output_loop(self, q):
        """Update GUI with items from the queue."""
        for line in self.iter_queue(q):
            if line is None:
                returncode = self.script_proc.poll()
                if returncode is not None:
                    self.editor_window.append_exec_output(
                        "Process finished with exit code %r" % returncode
                    )
                    return
            else:
                log.debug("Add process output to GUI: %s", repr(line))
                self.editor_window.append_exec_output(line)
                break # display no more than one line per 40 milliseconds

        self.editor_window.root.after(40, self.update_output_loop, q) # schedule next update


    def run_source_listing(self, source_listing):
        run_bak_filepath = self.get_run_bak_filepath()
        log.info("Save to: %r", run_bak_filepath)
        with open(run_bak_filepath, "w") as f:
            f.write(source_listing)

        self.run(run_bak_filepath)
