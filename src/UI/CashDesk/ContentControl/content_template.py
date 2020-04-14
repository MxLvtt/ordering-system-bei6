from tkinter import *

class ContentTemplate(Frame):
    def __init__(self, parent, title, background="white", shown: bool = False):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self.pack_propagate(0)
        self.grid_propagate(0)

        self._title = title
        self._is_hidden = shown

        if not shown:
            self.hide_view()
        else:
            self.show_view()

    def hide_view(self):
        if not self._is_hidden:
            self.pack_forget()
            self._is_hidden = True

    def show_view(self):
        if self._is_hidden:
            self.pack(side=TOP,expand=1,fill='both',padx=5,pady=5)
            self._is_hidden = False

    def is_shown(self) -> bool:
        return not self._is_hidden

    def title(self) -> bool:
        return self._title
