from tkinter import *
from ContentControl.ActiveOrders.order_tile_gui import OrderTileGUI
from EventHandler.Event import Event
from Templates.order import Order

class PageSystem(Frame):
    FIX_COLS = 5
    FIX_ROWS = 2

    def __init__(self, parent, background):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self._pages_changed_event: Event = Event()

        self._background = background
        self._pages = []
        self._current_page_index = 0
        self._max_orders = (PageSystem.FIX_COLS*PageSystem.FIX_ROWS)

        self._pages.append(
            Page(
                max_orders=self._max_orders
            )
        )

        self._row_container_top = Frame(self, background=self._background)
        self._row_container_bot = Frame(self, background=self._background)

        self._row_container_top.pack(
            padx=5, pady=(10, 5), side=TOP, fill="both", expand=1)
        self._row_container_bot.pack(
            padx=5, pady=(0, 5), side=TOP, fill="both", expand=1)

    @property
    def pages_changed_event(self) -> Event:
        return self._pages_changed_event

    @property
    def pages(self) -> []:
        return self._pages

    @property
    def current_page_index(self) -> int:
        return self._current_page_index

    @property
    def current_page(self) -> 'Page':
        return self._pages[self._current_page_index]

    def next_page(self):
        # We currently are already at the last page
        if self._current_page_index == (len(self._pages) - 1):
            return

        self._current_page_index = self._current_page_index + 1
        self._update_view(self.current_page.objects)
        self._pages_changed_event()
    
    def previous_page(self):
        # We currently are already at the first page
        if self._current_page_index == 0:
            return

        self._current_page_index = self._current_page_index - 1
        self._update_view(self.current_page.objects)
        self._pages_changed_event()

    def insert_object(self, order_object: Order, beginning: bool = False):
        """ Insert a new object of type Order
        """
        not_fitted_object = self._pages[0].insert_object(order_object, beginning)

        index = 1

        while(not_fitted_object != None):
            if index < len(self._pages):
                not_fitted_object = self._pages[index].insert_object(
                    not_fitted_object, beginning)
                index = index + 1
            else:
                self._pages.append(
                    Page(
                        max_orders=self._max_orders
                    )
                )
                self._pages_changed_event()

        self._update_view(self.current_page.objects)

    def _update_view(self, object_list):
        for child_top_row in self._row_container_top.winfo_children():
            child_top_row.destroy()

        for child_bot_row in self._row_container_bot.winfo_children():
            child_bot_row.destroy()

        self._current_row_container = self._row_container_top

        # Place each object on this frame in a 2 dimensional grid
        for idx, obj in enumerate(object_list):
            x_pos = idx % PageSystem.FIX_COLS
            y_pos = int(idx / PageSystem.FIX_COLS)

            if y_pos == 1:
                self._current_row_container = self._row_container_bot

            # Create OrderTileGUI for this order
            order_tile = OrderTileGUI(
                parent=self._current_row_container,
                order=obj
            )
            # Place OrderTileGUI on this frame
            order_tile.pack(padx=5, pady=(0, 5), side=LEFT,
                            fill="both", expand=1)
            order_tile.pack_propagate(0)

        # -- Fill last row with empty space -- #

        rest = len(object_list) % PageSystem.FIX_COLS

        if rest != 0:
            empty = PageSystem.FIX_COLS - rest
            for i in range(0, empty):
                empty_tile = Frame(self._current_row_container,
                                   background=self._background, borderwidth=2)
                empty_tile.pack(padx=5, pady=(0, 5), side=LEFT,
                                fill="both", expand=1)


class Page():
    def __init__(self, max_orders: int):
        self._orders = []
        self._max_orders = max_orders

    @property
    def objects(self) -> []:
        return self._orders

    def insert_object(self, order: Order, beginning: bool = False) -> Order:
        # Should the object be inserted at the end?
        if not beginning: # -> YES
            # Is the page full?
            if self._is_full(): # -> YES
                # Return it to be passed to the next page
                return order
            else: # -> NO
                # Add new object to the end
                self._orders.append(order)
        elif beginning: # -> NO
            last_obj = None

            # Is the page full?
            if self._is_full(): # -> YES
                # Remove last object but store it temporarily
                last_obj = self._orders.pop(len(self._orders) - 1)
            
                # Add new object to the beginning
            self._orders.insert(0, order)

            return last_obj

        return None

    def _is_full(self) -> bool:
        return len(self._orders) >= self._max_orders
