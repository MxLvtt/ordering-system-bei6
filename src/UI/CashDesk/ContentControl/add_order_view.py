from tkinter import *
from ContentControl.content_template import ContentTemplate

class AddOrderView(ContentTemplate):
    def __init__(self, parent, background="white", shown: bool = False):
        super().__init__(
            parent=parent,
            title="Add new order",
            background=background,
            shown=shown
        )

