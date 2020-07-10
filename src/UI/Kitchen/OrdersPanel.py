from tkinter import *
from ordertile import OrderTileGUI
from random import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import messagebox
from page_system import PageSystem


class OrdersPanel(Frame):
    def __init__(self, parent, panelbackground):
        super().__init__(
              master=parent,
              cnf={},
             #  width= panelwidth,
             #  height= panelheight,
              background=panelbackground,
        )
        self._idx = 1
        self._idxr = 0

        self._page_system = PageSystem(parent=self, background=panelbackground)
        self._page_system.pack(side=TOP, fill='both', expand=1)
        self._page_system.pages_changed_event.add(self._pages_changed)

        self._active_orders = []


    def _pages_changed(self):
        self._current_page_label.config(
            text=f"{self._page_system.current_page_index + 1}/{len(self._page_system.pages)}"
        )
        
        if self._page_system.current_page_index == 0:
            self._prev_button._disable()
        else:
            self._prev_button._enable()
        
        if self._page_system.current_page_index == (len(self._page_system.pages) - 1):
            self._next_button._disable()
        else:
            self._next_button._enable()

    def go_to_prev_page(self):
        self._page_system.previous_page()

    def go_to_next_page(self):
        self._page_system.next_page()

    def add_order_tile(self):
        # rh = random() * 200 + 500
        # OrderTileGUI(parent=self, row=self._idxr, column=self._idx, height=rh)
        # self._idx = self._idx + 1
        # if self._idx == 4:
        #     self._idx = 0
        #     self._idxr = self._idxr + 1
        # curr_x = len(self._active_orders) % ActiveOrdersView.NUM_COLUMNS

        # rh = random() * 200 + 500

        # tile_frame = Frame(
        #     master=self._column_frames[curr_x],
        #     background='#525252',
        #     height=rh,
        #     width=200
        # )
        # tile_frame.pack(side=TOP, padx=15, pady=(15,0), fill='x', expand=1)

        test_frame = Frame()

        self._active_orders.append(test_frame)

        self._page_system.insert_object(test_frame, False)






# root = Tk()

# OrdersPanel(parent=root,panelbackground="grey")

# mainloop()
