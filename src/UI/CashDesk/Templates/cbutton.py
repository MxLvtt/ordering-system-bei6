from tkinter import Button
from tkinter import font as tkFont

class CButton(Button):
    def __init__(
        self,
        parent,
        text,
        command,
        width=3,
        height=1,
        fg="black",
        bg="white",
        row=0,
        column=0
    ):
        super().__init__(
            master=parent,
            text=text,
            command=command,
            width=width,
            height=height,
            fg=fg,
            bg=bg
        )

        helv36 = tkFont.Font(family='Helvetica', size=26, weight=tkFont.BOLD)

        self.config(font=helv36)

        self.grid(row=row, column=column)

        self.is_shown = True

    def _show(self) -> Button:
        if not self.is_shown:
            self.grid()
            self.is_shown = True
        return self

    def _hide(self) -> Button:
        if self.is_shown:
            self.grid_remove()
            self.is_shown = False
        return self

    def _is_shown(self) -> bool:
        return self.is_shown
    