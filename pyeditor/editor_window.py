import os
import sys
import logging

from tkinter import Frame, NSEW, RIGHT, INSERT, Menu, END, Tk, DISABLED, NORMAL
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.scrolledtext import ScrolledText

from pyeditor.tk_helpers.scrolledlistbox import ScrolledListbox
from pyeditor.tk_helpers.mymultistatusbar import MyMultiStatusBar
from pyeditor.script_list import ScriptList

# https://docs.python.org/3/whatsnew/3.6.html#idlelib-and-idle
try:
    # Python 3.5
    from idlelib.ColorDelegator import ColorDelegator
except ModuleNotFoundError:
    # Python 3.6
    from idlelib.colorizer import ColorDelegator

try:
    # Python 3.5
    from idlelib.MultiStatusBar import MultiStatusBar
except ModuleNotFoundError:
    # Python 3.6
    from idlelib.statusbar import MultiStatusBar

try:
    # Python 3.5
    from idlelib.Percolator import Percolator
except ModuleNotFoundError:
    # Python 3.6
    from idlelib.percolator import Percolator

from pyeditor.config import DEFAULT_FILETYPES, BASE_PATH, RUN_BAK_PATH, DEFAULTEXTENSION
from pyeditor.constants import BREAK
from pyeditor.example_scripts import DEFAULT_MCPI_SCRIPT, DEFAULT_SCRIPT
from pyeditor.minecraft_specials import MinecraftSpecials
from pyeditor.python_files import PythonFiles
from pyeditor.version import __version__


log = logging.getLogger(__name__)


class EditorWindow:
    def __init__(self):
        self.root = Tk(className="EDITOR")

        self.python_files = PythonFiles(self)

        self.root.geometry("%dx%d+%d+%d" % (
            self.root.winfo_screenwidth() * 0.5, self.root.winfo_screenheight() * 0.4,
            # self.root.winfo_screenwidth() * 0.1, self.root.winfo_screenheight() * 0.1
            0,0
        ))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.base_title = "PyEditor v%s" % __version__
        self.root.title(self.base_title)

        self.text_frame = Frame(master=self.root)

        self.text = ScrolledText(master=self.root, background="white")
        self.text.bind("<Tab>", self.tab_event)
        self.text.grid(row=0, column=0, sticky=NSEW)

        #TODO: find a right height
        self.exec_output = ScrolledText(
            master=self.root, height=10,
            state=DISABLED, background="#dddddd"
        )

        # for information text like load/save/run:
        self.exec_output.tag_config("info",
            foreground="#0000ff",
            #background="#eeeeee"
        )

        self.exec_output.grid(row=1, column=0, sticky=NSEW)

        self.text.focus_set()

        # self.script_list = ScriptList(self)

        p = Percolator(self.text)
        d = ColorDelegator()
        p.insertfilter(d)

        # add statusbar to window
        self.init_statusbar()

        # add menu to window
        self.init_menu()

        # Add special RPi/Minecraft features, if available
        self.rpi = MinecraftSpecials(self)

        if self.rpi.mcpi_available:
            # minecraft is available
            self.set_content(DEFAULT_MCPI_SCRIPT)
            if not self.rpi.is_running:
                self.rpi.startup_minecraft()
        else:
            # no minecraft available
            self.set_content(DEFAULT_SCRIPT)

        self.root.update()

    ###########################################################################
    # Status bar

    FILENAME_LABEL="filename"

    def get_filename(self):
        filename = self.status_bar.get_textEntry(self.FILENAME_LABEL)
        return filename

    def set_filename(self, filename):
        filename = os.path.split(filename)[-1]
        self.status_bar.set_textEntry(self.FILENAME_LABEL, filename)

    def update_filename(self, event=None):
        filename = self.get_filename()
        if filename and not filename.endswith(".py"):
            filename = "%s.py" % filename
            self.set_filename(filename)

    def init_statusbar(self):
        self.status_bar = MyMultiStatusBar(self.root)
        if sys.platform == "darwin":
            # Insert some padding to avoid obscuring some of the statusbar
            # by the resize widget.
            self.status_bar.set_label('_padding1', '    ', side=RIGHT)
        self.status_bar.grid(row=2, column=0)

        self.text.bind("<<set-line-and-column>>", self.set_line_and_column)
        self.text.event_add("<<set-line-and-column>>",
                            "<KeyRelease>", "<ButtonRelease>")
        self.text.after_idle(self.set_line_and_column)
        self.status_bar.new_textEntry(
            self.FILENAME_LABEL, 'unnamed.py',
            callback=self.update_filename
        )

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
        self.exec_output.config(state=NORMAL)
        self.exec_output.delete("1.0", END)
        filename = self.get_filename()
        self.python_files.run_source_listing(source_listing, filename)
        log.debug("Adding to terminal out")
        #self.exec_output.insert(END, "Run Script")
        self.exec_output.config(state=DISABLED)

    def command_load_file(self):
        infile = askopenfile(
            parent=self.root,
            mode="r",
            title="Select a Python file to load",
            filetypes=DEFAULT_FILETYPES,
            initialdir=BASE_PATH,
        )
        if infile is not None:
            source_listing = infile.read()
            infile.close()
            self.set_content(source_listing)

            self.set_filename(infile.name) # FIXME: insert only name!
            self.append_feedback_to_output("Script %r loaded." % infile.name)

    def command_save_file(self):
        self.update_filename() # FIXME: add .py if missing

        content = self.get_content()
        filename = self.get_filename()
        filepath = os.path.join(BASE_PATH, filename)

        if os.path.isfile(filepath):
            self.python_files.move_to_backup(filepath)

        with open(filepath, "w") as f:
            f.write(content)

        self.append_feedback_to_output("Save to: %r" % filepath)

    ###########################################################################

    def get_content(self):
        content = self.text.get("1.0", END)
        content = content.strip()
        return content

    def set_content(self, source_listing):
        self.text.delete("1.0", END)

        log.critical("insert %i Bytes listing.", len(source_listing))
        self.text.insert(END, source_listing)

        self.text.mark_set(INSERT, '1.0') # Set cursor at start
        self.text.focus()

    def append_exec_output(self, text):
        self.exec_output.config(state=NORMAL)
        self.exec_output.insert(END, text)
        self.exec_output.config(state=DISABLED)

    def append_feedback_to_output(self, text):
        text = "%s\n" % text.rstrip()
        self.exec_output.config(state=NORMAL)
        self.exec_output.insert(END, text, "info")
        self.exec_output.config(state=DISABLED)

    ###########################################################################

    indent_pad=" "*4
    def tab_event(self, event):
        log.debug("Tab event")
        self.text.insert("insert", self.indent_pad)
        return BREAK

    ###########################################################################
