from tkinter import *

class AddOrderView(Frame):
    def __init__(self, parent, width=0, height=0, background="#FF00FF"):
        super().__init__(
            master=parent,
            cnf={},
            width=width,
            height=height,
            background=background
        )

        self.is_hidden = False

    def hide_frame(self):
        if not self.is_hidden:
            self.lower()
            self.is_hidden = True

    def unhide_frame(self):
        if self.is_hidden:
            self.lift()
            self.is_hidden = False

