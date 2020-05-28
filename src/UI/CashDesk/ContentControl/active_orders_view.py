from tkinter import *
from random import *
from ContentControl.content_template import ContentTemplate
from ContentControl.ordertileprototype import OrderTileGUI

class ActiveOrdersView(ContentTemplate):
    def __init__(self, parent, background="white", shown: bool = False):
        super().__init__(
            parent=parent,
            title="Active orders overview",
            background=background,
            shown=shown
        )

        self._idx = 0
        self._idxr = 0

    def add_order_tile(self):
        print("Adding order tile")
        rh = random() * 200 + 500
        OrderTileGUI(parent=self, row=self._idxr, column=self._idx, height=rh)
        self._idx = self._idx + 1
        if self._idx == 4:
            self._idx = 0
            self._idxr = self._idxr + 1

