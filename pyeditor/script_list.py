from tkinter import NSEW, END, INSERT

import logging

from pyeditor.tk_helpers.scrolledlistbox import ScrolledListbox

log = logging.getLogger(__name__)

class ScriptList:
    """
    List of saved files on the right side of the editor.
    """
    def __init__(self, editor_window):
        self.root = editor_window.root
        self.python_files = editor_window.python_files

        self.file_list = ScrolledListbox(self.root)
        self.file_list.grid(row=0, column=1, rowspan=2, sticky=NSEW)

        self.file_list.bind("<Button-1>", self.click_handler)

        self.fill_file_list()

    def fill_file_list(self):
        file_names = self.python_files.get_filenames()
        for file_name in file_names:
            self.file_list.insert(END, file_name)

    def click_handler(self, event):
        print("Click:", event)
        widget = event.widget
        index = event.widget.nearest(event.y) # FIXME
        value = widget.get(index)
        log.debug("Clicked on item %d: '%s'", index, value)
