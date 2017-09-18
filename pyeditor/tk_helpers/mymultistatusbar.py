from tkinter import Entry, SUNKEN, W, LEFT, END

# https://docs.python.org/3/whatsnew/3.6.html#idlelib-and-idle
try:
    # Python 3.5
    from idlelib.MultiStatusBar import MultiStatusBar
except ModuleNotFoundError:
    # Python 3.6
    from idlelib.statusbar import MultiStatusBar


class MyMultiStatusBar(MultiStatusBar):

    def __init__(self, master, **kw):
       MultiStatusBar.__init__(self, master, **kw)
       self.entrys = {}

    def new_textEntry(self, name, text='', side=LEFT, callback=None):
        if name not in self.entrys:
            entry = Entry(self, bd=1, relief=SUNKEN)
            entry.pack(side=side)
            self.entrys[name] = entry
        else:
            entry = self.entrys[name]
        entry.insert(0, text)
        if callback:
            entry.bind('<FocusOut>', callback)

    def set_textEntry(self, name, text=''):
        if name not in self.entrys:
            return None
        entry = self.entrys[name]
        entry.delete(0, END)
        entry.insert(0, text)

    def get_textEntry(self, name):
        if name not in self.entrys:
            return None
        entry = self.entrys[name]
        return entry.get()
