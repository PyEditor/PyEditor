#!/usr/bin/env python3
# coding: utf-8

import sys

from idlelib.ColorDelegator import ColorDelegator, color_config
from idlelib.MultiCall import MultiCallCreator
from idlelib.MultiStatusBar import MultiStatusBar
from idlelib.Percolator import Percolator
from tkinter import Text, Frame, Scrollbar, Tk, Menu, NSEW, INSERT


class EditorWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("%dx%d+%d+%d" % (
            self.root.winfo_screenwidth() * 0.6, self.root.winfo_screenheight() * 0.6,
            self.root.winfo_screenwidth() * 0.1, self.root.winfo_screenheight() * 0.1
        ))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.base_title = "PyEditor"
        self.root.title(self.base_title)

        self.menubar = Menu(root)

        # self.top = top = windows.ListedToplevel(root, menu=self.menubar)

        self.text_frame = Frame(master=self.root)
        self.vbar = Scrollbar(self.text_frame, name='vbar')

        self.text = Text(master=self.root, background="white")
        self.text.grid(row=0, column=0, sticky=NSEW)
        with open(__file__, "r") as f:
            self.text.insert("insert", f.read())
        self.text.focus_set()

        color_config(self.text)
        p = Percolator(self.text)
        d = ColorDelegator()
        p.insertfilter(d)

        self.init_statusbar()

        self.root.update()

    ###########################################################################
    # Status bar

    def init_statusbar(self):
        self.status_bar = MultiStatusBar(self.root)
        if sys.platform == "darwin":
            # Insert some padding to avoid obscuring some of the statusbar
            # by the resize widget.
            self.status_bar.set_label('_padding1', '    ', side=tkinter.RIGHT)
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

def main():
    root = Tk(className="EDITOR")
    gui = EditorWindow(root)
    gui.root.mainloop()


if __name__ == "__main__":
    main()
