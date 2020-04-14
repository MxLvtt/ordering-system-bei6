from tkinter import *
from ContentControl.content_template import ContentTemplate

class ActiveOrdersView(ContentTemplate):
    def __init__(self, parent, background="white", shown: bool = False):
        super().__init__(
            parent=parent,
            title="Active orders overview",
            background=background,
            shown=shown
        )

