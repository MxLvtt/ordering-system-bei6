from tkinter import *

class SettingsCategory(Frame):
    def __init__(self, parent, image, title, command, background="white"):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self.pack_propagate(0)
        self.grid_propagate(0)

        button_font = ('Helvetica', '20')

        self._button = Button(
            master=self,
            command=command,
            image=image,
            text=title,
            compound="top",
            font=button_font
        )
        self._button.pack(side=TOP, fill='both', expand=1)
