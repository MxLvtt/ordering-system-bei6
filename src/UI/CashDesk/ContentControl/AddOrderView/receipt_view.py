from tkinter import *
from functools import partial
from ContentControl.AddOrderView.added_meal_tile import AddedMealTile
from EventHandler.Event import Event
from Templates.radio_button import RadioButton, RadioButtonGroup
from Templates.fonts import Fonts
from Templates.scroll_list import ScrollList
from Templates.scrollable import Scrollable
import Templates.references as REFS


class ReceiptView(Frame):
    def __init__(self, parent, background, shown: bool = False, order = None):
        super().__init__(
            master=parent,
            cnf={},
            background='#696969'
        )

        self.parent = parent
        self.table = None
        self.scrolllist = None

        # Assure that the frame won't resize with the contained widgets
        self.pack_propagate(0)
        self.grid_propagate(0)

        # Private members
        self._is_hidden = shown
        self._background = background

        # Initialize visibility-state
        if not shown:
            self.hide_view()
        else:
            self.show_view(order)

    @property
    def is_shown(self) -> bool:
        return not self._is_hidden

    def _update_view(self, order):
        if self.scrolllist == None or self.table == None:
            self.update()
            width = self.parent.winfo_width()

            self.table = Frame(
                master=self, 
                background='#F4F4F4', 
                width=int(width/3)
            )
            self.table.pack(side=TOP, fill='y', expand=1, pady=10)

            self.scrolllist = ScrollList(
                parent=self.table,
                spacing=0,
                background='#696969'
            )
        else:
            self.scrolllist.remove_all()

        receipt = Receipt(
            parent=self.scrolllist,
            order=order
        )

        self.scrolllist.add_row(receipt, update=False)
        self.scrolllist.update_view()

    def hide_view(self):
        if self._is_hidden:
            return
        
        self.pack_forget()
        self._is_hidden = True

    def show_view(self, order):
        if not self._is_hidden:
            return

        if order == None:
            raise RuntimeError("Order must not be of Nonetype.")

        self._update_view(order)

        self.pack(side=TOP, expand=1, fill='both')
        self._is_hidden = False

class Receipt(Scrollable):
    def __init__(self, parent, order, background='white'):
        super().__init__(
            parent=parent,
            height=800,
            background=background
        )

        self._background = background

        # self._edit_img = IMAGES.create(IMAGES.EDIT)
        # self._check_img = IMAGES.create(IMAGES.CHECK_MARK)
        # self._down_img = IMAGES.create(IMAGES.DOWN)
        # self._up_img = IMAGES.create(IMAGES.UP)

        ########## COLUMNS ##########

        self.row_frame = Frame(
            master=self,
            background=background
        )
        self.row_frame.pack(side=TOP, fill='x')

        self._text = Label(
            master=self.row_frame,
            text="Hi! :)",
            background=background
        )
        self._text.pack(side=LEFT, padx=5, pady=5)
