#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import logging
import subprocess
import datetime

log = logging.getLogger(__name__)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

log.info("Python v%s", sys.version.replace("\n", ""))

from idlelib.ColorDelegator import ColorDelegator
from idlelib.MultiCall import MultiCallCreator
from idlelib.MultiStatusBar import MultiStatusBar
from idlelib.Percolator import Percolator

from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter import Text, Frame, Scrollbar, Tk, Menu, NSEW, INSERT, RIGHT, END



DEFAULT_SCRIPT="""\
from mcpi import minecraft

mc = minecraft.Minecraft.create()
mc.postToChat("Hello world, from PyEditor!")
"""

# from idlelib import autocomplete_w
class RaspberryPi:
    """
    special RPi/Minecraft features, if available
    """
    def __init__(self, editor):
        nodename = os.uname().nodename
        is_on_rpi = nodename=="raspberrypi"
        log.debug("is_on_rpi=%r (uname nodename: %r)", is_on_rpi, nodename)
        if is_on_rpi:
            self.expand_editor(editor)

    def expand_editor(self, editor):
        self.editor_root = editor.root
        self.editor_root.menubar.add_command(
            label="Startup Minecraft",
            command=self.startup_mindecraft
        )
    def startup_mindecraft(self):
        print("TODO")



class PythonFiles:
    """
    Handle file load/save/run stuff
    """
    def __init__(self):
        self.base_dir=os.path.expanduser("~/PyEditor files")
        self.run_bak_path=os.path.expanduser("~/PyEditor files/run backups")
        self.auto_bak_path=os.path.expanduser("~/PyEditor files/auto backups")

        os.makedirs(self.run_bak_path, mode=0o766, exist_ok=True)
        os.makedirs(self.auto_bak_path, mode=0o766, exist_ok=True)

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
            self.run_bak_path, filename
        )
        return run_bak_filepath

    def run(self, filepath):
        args = [sys.executable, filepath]
        log.info("run: %s" % " ".join(args))
        subprocess.Popen(args)

    def run_source_listing(self, source_listing):
        run_bak_filepath = self.get_run_bak_filepath()
        log.info("Save to: %r", run_bak_filepath)
        with open(run_bak_filepath, "w") as f:
            f.write(source_listing)

        self.run(run_bak_filepath)



class EditorWindow:
    DEFAULT_FILETYPES=[ # for askopenfile, asksaveasfile, etc.
        ("Python files", "*.py", "TEXT"),
        ("All files", "*"),
    ]
    DEFAULTEXTENSION = "*.py"

    def __init__(self, root):
        self.root = root

        self.python_files = PythonFiles()


        self.root.geometry("%dx%d+%d+%d" % (
            self.root.winfo_screenwidth() * 0.6, self.root.winfo_screenheight() * 0.6,
            self.root.winfo_screenwidth() * 0.1, self.root.winfo_screenheight() * 0.1
        ))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.base_title = "PyEditor"
        self.root.title(self.base_title)

        # self.top = top = windows.ListedToplevel(root, menu=self.menubar)

        self.text_frame = Frame(master=self.root)
        self.vbar = Scrollbar(self.text_frame, name='vbar')

        self.text = Text(master=self.root, background="white")
        self.text.grid(row=0, column=0, sticky=NSEW)
        self.set_content(DEFAULT_SCRIPT)
        self.text.focus_set()

        # autocomplete_w.AutoCompleteWindow(self.text)

        p = Percolator(self.text)
        d = ColorDelegator()
        p.insertfilter(d)

        # add statusbar to window
        self.init_statusbar()

        # add menu to window
        self.init_menu()

        # Add special RPi/Minecraft features, if available
        self.rpi = RaspberryPi(self)

        self.root.update()

    ###########################################################################
    # Status bar

    def init_statusbar(self):
        self.status_bar = MultiStatusBar(self.root)
        if sys.platform == "darwin":
            # Insert some padding to avoid obscuring some of the statusbar
            # by the resize widget.
            self.status_bar.set_label('_padding1', '    ', side=RIGHT)
        self.status_bar.grid(row=1, column=0)

        self.text.bind("<<set-line-and-column>>", self.set_line_and_column)
        self.text.event_add("<<set-line-and-column>>",
                            "<KeyRelease>", "<ButtonRelease>")
        self.text.after_idle(self.set_line_and_column)

    def set_line_and_column(self, event=None):
        line, column = self.text.index(INSERT).split('.')
        self.status_bar.set_label('column', 'Column: %s' % column)
        self.status_bar.set_label('line', 'Line: %s' % line)

    ###########################################################################
    # Menu

    def init_menu(self):
        self.menubar = Menu(self.root)
        filemenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_command(label="Run", command=self.command_run)
        self.menubar.add_command(label="Load", command=self.command_load_file)
        # filemenu.add_command(label="Load", command=self.command_load_file)
        self.menubar.add_command(label="Save", command=self.command_save_file)
        self.menubar.add_command(label="Exit", command=self.root.quit)
        #
        # self.menubar.add_cascade(label="File", menu=filemenu)

        self.root.config(menu=self.menubar)

    def command_run(self):
        source_listing = self.get_content()
        self.python_files.run_source_listing(source_listing)

    def command_load_file(self):
        infile = askopenfile(
            parent=self.root,
            mode="r",
            title="Select a Python file to load",
            filetypes=self.DEFAULT_FILETYPES,
            initialdir=self.python_files.base_dir,
        )
        if infile is not None:
            source_listing = infile.read()
            infile.close()
            self.set_content(source_listing)

            # self.setup_filepath(infile.name)

    def command_save_file(self):
        outfile = asksaveasfile(
            parent=self.root,
            mode="w",
            filetypes=self.DEFAULT_FILETYPES,
            defaultextension=self.DEFAULTEXTENSION,
            initialdir=self.python_files.base_dir,
        )
        if outfile is not None:
            content = self.get_content()
            outfile.write(content)
            outfile.close()
            # self.setup_filepath(outfile.name)

    ###########################################################################

    def get_content(self):
        content = self.text.get("1.0", END)
        content = content.strip()
        return content

    def set_content(self, source_listing):
#        self.text.config(state=Tkinter.NORMAL)
        self.text.delete("1.0", END)

        log.critical("insert listing:")
        self.text.insert(END, source_listing)

#        self.text.config(state=Tkinter.DISABLED)
        self.text.mark_set(INSERT, '1.0') # Set cursor at start
        self.text.focus()

    ###########################################################################

def main():
    root = Tk(className="EDITOR")
    gui = EditorWindow(root)
    gui.root.mainloop()


if __name__ == "__main__":
    main()
