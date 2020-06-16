import Templates.references as REFS
from tkinter import *
from random import *
from ContentControl.content_template import ContentTemplate
from ContentControl.ActiveOrders.page_system import PageSystem
from Templates.cbutton import CButton
from Templates.toggle_button import ToggleButton, ToggleButtonGroup
from Templates.images import IMAGES
from Templates.order import Order
from Services.orders_service import OrdersService

class ActiveOrdersView(ContentTemplate):
    NUM_COLUMNS = 5

    def __init__(self, parent, toolbar_container: Frame, background="white", shown: bool = False):
        super().__init__(
            parent=parent,
            title=REFS.ACTIVEORDERSVIEW_TITLE,
            toolbar_container=toolbar_container,
            background=background,
            shown=shown
        )

        OrdersService.on_order_created_event.add(self._order_created_event)

        self._page_system = PageSystem(parent=self, background=background)
        self._page_system.pack(side=TOP, fill='both', expand=1)
        self._page_system.pages_changed_event.add(self._pages_changed)

        self._active_orders = []

        ######## Setting toolbar content ########

        self._checkmark_img = IMAGES.create(IMAGES.CHECK_MARK)
        self._checkmark_dark_img = IMAGES.create(IMAGES.CHECK_MARK_DARK)
        self._add_img = IMAGES.create(IMAGES.ADD)
        self._back_img = IMAGES.create(IMAGES.BACK)
        self._next_img = IMAGES.create(IMAGES.NEXT)
        self._trashcan_img = IMAGES.create(IMAGES.TRASH_CAN)
        self._order_img = IMAGES.create(IMAGES.ORDER)

        #### Right Button Container
        self._button_container_right = Frame(self.toolbar, background="#EFEFEF")
        self._button_container_right.grid(row=0, column=2, sticky='nsew')

        self._toggle_button_group = ToggleButtonGroup()
        
        # Button: Mark orders as done
        self._mark_done_button = ToggleButton(
            parent=self._button_container_right,
            image=self._checkmark_dark_img,
            highlight_image=self._checkmark_img,
            command=None,
            initial_state=True,
            group=self._toggle_button_group,
            bg=REFS.LIGHT_GREEN, highlight=CButton.GREEN,
            row=0, column=0
        )

        # Button: Mark orders as open
        self._mark_open_button = ToggleButton(
            parent=self._button_container_right,
            image=self._checkmark_dark_img,
            highlight_image=self._checkmark_img,
            command=None,
            initial_state=False,
            group=self._toggle_button_group,
            bg=REFS.LIGHT_GRAY, highlight=CButton.DARK,
            spaceX=(0.0,1.0),
            row=0, column=1
        )

        # Button: Mark orders as canceled
        self._mark_canceled_button = ToggleButton(
            parent=self._button_container_right,
            image=self._checkmark_dark_img,
            highlight_image=self._checkmark_img,
            command=None,
            initial_state=False,
            group=self._toggle_button_group,
            bg=REFS.LIGHT_RED, highlight=CButton.DARK_RED,
            row=0, column=2
        )

        ### Middle Breadcrumb Container
        self._container_middle = Frame(self.toolbar, background="#EFEFEF")
        self._container_middle.grid(row=0, column=1, sticky='nsew')

        self._current_page_label = Label(
            master=self._container_middle,
            text='1 / 1',
            font=('Helvetica', '16', 'bold'),
            foreground='black',
            background='#EFEFEF'
        )
        self._current_page_label.pack(side=LEFT, padx=10, fill='x', expand=1)

        #### Left Button Container
        self._button_container_left = Frame(self.toolbar, background="#EFEFEF")
        self._button_container_left.grid(row=0, column=0, sticky='nsew')

        self.toolbar.grid_rowconfigure(0, weight=1)
        self.toolbar.grid_columnconfigure(0, weight=0) # Left Container     -> fit
        self.toolbar.grid_columnconfigure(1, weight=1) # Middle Container   -> expand
        self.toolbar.grid_columnconfigure(2, weight=0) # Right Container    -> fit
        
        # Button: Go to previous page
        self._prev_button = CButton(
            parent=self._button_container_left,
            image=self._back_img,
            command=self.go_to_prev_page,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=0
        )
        self._prev_button._disable()

        # Button: Go to next page
        self._next_button = CButton(
            parent=self._button_container_left,
            image=self._next_img,
            command=self.go_to_next_page,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=1
        )
        self._next_button._disable()

        ######## END setting toolbar content ########

    def _order_created_event(self, order: Order):
        self.add_order_tile(order)

    def _pages_changed(self):
        self._current_page_label.config(
            text=f"{self._page_system.current_page_index + 1} / {len(self._page_system.pages)}"
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

    def add_order_tile(self, order: Order):
        self._active_orders.append(order)

        self._page_system.insert_object(
            order_object=order,
            beginning=True
        )
