from tkinter import *
from content_panel import ContentPanel

class AddOrderView(ContentPanel):
    def __init__(self, parent, width, height, padding=0, background="#696969"):
        super().__init__(
            parent=parent,
            width=width,
            height=height,
            padding=padding,
            background=background
        )

        self.is_hidden = False

        self.grid(padx=padding, pady=padding)
        self.grid_propagate(0)

