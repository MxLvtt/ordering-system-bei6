from tkinter import Button, LEFT
import Templates.references as REFS

class CButton(Button):
    SIZE = 72

    WHITE = "#FFFFFF"
    LIGHT = "#DDDFE3"
    DARK = "#535B5D"
    GREEN = "#63B719"#7DAB55"
    YELLOW = "#E9C545"
    DARK_RED = "#A62921"

    def __init__(
        self,
        parent,
        image,
        command,
        width=-1,
        height=1.0,
        fg=DARK,
        bg=WHITE,
        row=0,
        column=0,
        spaceX=(0.0,0.0), # As a multiple of the buttons standard SIZE
        spaceY=(0.0,0.0)  # As a multiple of the buttons stamdard SIZE
    ):
        if width == -1:
            width = 1.0 + (not REFS.MOBILE)

        if REFS.MOBILE:
            height = 0.6

        super().__init__(
            master=parent,
            command=command,
            image=image,
            width=width*self.SIZE,
            height=height*self.SIZE,
            fg=fg,
            bg=bg
        )

        # helv36 = tkFont.Font(family='Helvetica', size=26, weight=tkFont.BOLD)
        # self.config(font=helv36)

        self.grid(row=row, column=column)

        sY = (self.SIZE*spaceY[0], self.SIZE*spaceY[1])
        sX = (self.SIZE*spaceX[0], self.SIZE*spaceX[1])

        self.grid(padx=sX, pady=sY)

        self.is_shown = True

    def _enable(self):
        self.config(state="normal")

    def _disable(self):
        self.config(state="disabled")

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
    