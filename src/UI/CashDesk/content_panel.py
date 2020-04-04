from tkinter import *


class ContentPanel(Frame):
    def __init__(self, parent, width, height, padding=0, background="#696969"):
        super().__init__(
            master=parent,
            cnf={},
            width=width-padding*2,
            height=height-padding*2,
            background=background
        )

        self.is_hidden = False

        self.grid(padx=padding, pady=padding)
        self.grid_propagate(0)

    def hide_frame(self):
        if not self.is_hidden:
            self.grid_remove() # or: self.lower()
            self.is_hidden = True

    def unhide_frame(self):
        if self.is_hidden:
            self.grid() # or: self.lift()
            self.is_hidden = False
