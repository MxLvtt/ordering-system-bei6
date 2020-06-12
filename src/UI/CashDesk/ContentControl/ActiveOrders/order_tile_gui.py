from tkinter import *


class OrderTileGUI(Frame):
    def __init__(self, parent, order, background='#525252'):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self._order = order
