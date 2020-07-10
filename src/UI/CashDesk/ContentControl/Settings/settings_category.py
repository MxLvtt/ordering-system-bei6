from tkinter import *
from functools import partial

class SettingsCategory(Frame):
    def __init__(self, parent, image, title, show_view_command, view, background="white"):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self.pack_propagate(0)
        self.grid_propagate(0)

        button_font = ('Helvetica', '20')

        func = partial(show_view_command, view)

        self._button = Button(
            master=self,
            command=func,
            image=image,
            text=title,
            compound="top",
            font=button_font
        )
        self._button.pack(side=TOP, fill='both', expand=1)
