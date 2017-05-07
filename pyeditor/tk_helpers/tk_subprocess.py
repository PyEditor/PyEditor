
import queue
import subprocess
import logging

from threading import Thread


log = logging.getLogger(__name__)


class TkSubprocess:
    """
    run a subprocess and pipe output to GUI
    """
    def __init__(self, root, args, output_callback, info_callback):
        self.root = root
        self.output_callback=output_callback
        self.info_callback=info_callback
        self.process = None
        self.run(args)

    def run(self, args):
        if self.process is not None:
            returncode = self.process.poll()
            if returncode is None: # process hasn’t terminated yet
                log.info("Kill old running script, PID: %r", self.process.pid)
                self.process.kill()
            else:
                log.debug("Old script process returned with: %r", returncode)
            self.process=None

        log.info("run: %s" % " ".join(args))
        self.process = subprocess.Popen(
            args,
            bufsize=0,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        log.debug("PID: %r", self.process.pid)

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
            with self.process.stdout as pipe:
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
                returncode = self.process.poll()
                if returncode is not None:
                    self.info_callback(
                        "Process finished with exit code %r" % returncode
                    )
                    return
            else:
                log.debug("Add process output to GUI: %s", repr(line))
                self.output_callback(line)
                break # display no more than one line per 40 milliseconds

        self.root.after(40, self.update_output_loop, q) # schedule next update
