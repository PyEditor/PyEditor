from tkinter import Frame, Listbox, Scrollbar, Pack, Grid, Place
from tkinter.constants import BOTTOM, LEFT, X, BOTH, HORIZONTAL

class ScrolledListbox(Listbox):
    def __init__(self, master=None, **kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.vbar.pack(side=BOTTOM, fill=X)

        kw.update({'xscrollcommand': self.vbar.set})
        Listbox.__init__(self, self.frame, **kw)
        self.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Listbox).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)

