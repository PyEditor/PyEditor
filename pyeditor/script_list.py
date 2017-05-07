from tkinter import NSEW, END

from pyeditor.tk_helpers.scrolledlistbox import ScrolledListbox


class ScriptList:
    """
    List of saved files on the right side of the editor.
    """
    def __init__(self, editor_window):
        self.root = editor_window.root
        self.python_files = editor_window.python_files

        self.file_list = ScrolledListbox(self.root)
        self.file_list.grid(row=0, column=1, rowspan=2, sticky=NSEW)

        self.fill_file_list()

    def fill_file_list(self):
        file_names = self.python_files.get_filenames()
        for file_name in file_names:
            self.file_list.insert(END, file_name)

        # files = [f for f in os.listdir(RUN_BAK_PATH) if os.path.isfile(os.path.join(RUN_BAK_PATH, f))]
        # for f in files:
        #     self.file_view.insert(END, f)
