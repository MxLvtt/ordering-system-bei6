from tkinter import Frame

class ContentPanel(Frame):
    def __init__(self, parent, width=0, height=0, background="#EFEFEF"):
        super().__init__(
            master=parent,
            cnf={},
            width=width,
            height=height,
            background=background
        )

        self.add_order_visible: bool = True # TEMPORARY

    def is_add_order_visible(self) -> bool:
        return self.add_order_visible

    def set_add_order_visibilty(self, visible: bool):
        self.add_order_visible = visible
