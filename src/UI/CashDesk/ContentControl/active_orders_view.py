import Templates.references as REFS
from tkinter import *
from random import *
from functools import partial
from ContentControl.content_template import ContentTemplate
from ContentControl.ActiveOrders.order_tile_gui import OrderTileGUI
from Templates.cbutton import CButton
from Templates.toggle_button import ToggleButton, ToggleButtonGroup
from Templates.images import IMAGES
from Templates.order import Order
from Templates.page_system import PageSystem
from Templates.custom_thread import CustomThread
from Services.orders_service import OrdersService
from Services.Messengers.order_messaging_service import OrderMessagingService


class ActiveOrdersView(ContentTemplate):
    NUM_COLUMNS = 4 # 5
    NUM_ROWS = 3 # 2

    MARK_OFF = -1
    MARK_DONE = 0
    MARK_OPEN = 1
    MARK_CANCEL = 2

    ACTIVE_ORDERS = []

    def __init__(self, parent, toolbar_container: Frame, background="white", shown: bool = False):
        super().__init__(
            parent=parent,
            title=REFS.ACTIVEORDERSVIEW_TITLE,
            toolbar_container=toolbar_container,
            background=background,
            shown=False
        )

        if REFS.MOBILE:
            ActiveOrdersView.NUM_COLUMNS = 3
            ActiveOrdersView.NUM_ROWS = 1

        self._background = background

        # OrdersService.on_order_created_event.add(self._order_created_event)
        OrdersService.on_orders_changed.add(
            self.update_view_and_database_content
        )
        OrderMessagingService.on_database_changed_event.add(
            self.update_view_and_database_content
        )

        self._mark_mode = ActiveOrdersView.MARK_OFF
        
        self.page_system = PageSystem(
            on_page_changed=self.update_view_and_database_content,
            items_per_page=ActiveOrdersView.NUM_COLUMNS * ActiveOrdersView.NUM_ROWS,
            numbering_mode=PageSystem.PAGE_NUMBERING
        )

        ######## Setting main content ########

        self.body_container = Frame(
            master=self,
            background=background
        )
        self.body_container.pack(side=TOP, fill='both', expand=1)
        self.body_container.grid_propagate(0)

        self._order_tiles = []

        self._insert_order_tiles()

        ######## Setting toolbar content ########

        self._checkmark_img = IMAGES.create(IMAGES.CHECK_MARK)
        self._checkmark_dark_img = IMAGES.create(IMAGES.CHECK_MARK_DARK)
        self._close_img = IMAGES.create(IMAGES.CLOSE_LIGHT)
        self._close_dark_img = IMAGES.create(IMAGES.CLOSE_DARK)
        self._undo_img = IMAGES.create(IMAGES.UNDO_LIGHT)
        self._undo_dark_img = IMAGES.create(IMAGES.UNDO)

        #### Right Button Container
        self._button_container_right = Frame(self.toolbar, background="#EFEFEF")
        self._button_container_right.grid(row=0, column=2, sticky='nsew')

        self._toggle_button_group = ToggleButtonGroup()
        
        # Button: Mark orders as done
        self._mark_done_button = ToggleButton(
            parent=self._button_container_right,
            image=self._checkmark_dark_img,
            highlight_image=self._checkmark_img,
            command=self._update_mark_mode,
            initial_state=True,
            group=self._toggle_button_group,
            # bg=REFS.LIGHT_GREEN,
            bg=REFS.LIGHT_GRAY,
            # highlight=CButton.GREEN,
            highlight=REFS.LIGHT_GREEN,
            row=0, column=0
        )

        # Button: Mark orders as open
        self._mark_open_button = ToggleButton(
            parent=self._button_container_right,
            image=self._undo_dark_img,
            highlight_image=self._undo_img,
            command=self._update_mark_mode,
            initial_state=False,
            group=self._toggle_button_group,
            bg=REFS.LIGHT_GRAY,
            highlight=CButton.DARK,
            # spaceX=(0.0,1.0),
            row=0, column=1
        )

        # Button: Mark orders as canceled
        self._mark_canceled_button = ToggleButton(
            parent=self._button_container_right,
            image=self._close_dark_img,
            highlight_image=self._close_img,
            command=self._update_mark_mode,
            initial_state=False,
            group=self._toggle_button_group,
            # bg=REFS.LIGHT_RED,
            bg=REFS.LIGHT_GRAY,
            # highlight=CButton.DARK_RED,
            highlight=REFS.LIGHT_RED,
            row=0, column=2
        )

        self._update_mark_mode()

        ### Middle Breadcrumb Container
        self._container_middle = Frame(self.toolbar, background="#EFEFEF")
        self._container_middle.grid(row=0, column=1, sticky='nsew')

        #### Left Button Container
        self._button_container_left = Frame(self.toolbar, background="#EFEFEF")
        self._button_container_left.grid(row=0, column=0, sticky='nsew')

        self.page_system.config_navigation(
            button_container=self._button_container_left,
            label_container=self._container_middle
        )

        self.toolbar.grid_rowconfigure(0, weight=1)
        self.toolbar.grid_columnconfigure(0, weight=0) # Left Container     -> fit
        self.toolbar.grid_columnconfigure(1, weight=1) # Middle Container   -> expand
        self.toolbar.grid_columnconfigure(2, weight=0) # Right Container    -> fit
        
        ######## END setting toolbar content ########

        if shown:
            super().show_view()

    def show_view(self):
        """ Is called everytime this view is opened
        """
        super().show_view()

        self.update_view_and_database_content()

    def update_view_and_database_content(self):
        all_active_orders = OrdersService.get_orders(
            # Ordered by timestamp (newest first)
            order_by=f"{REFS.ORDERS_TABLE_TIMESTAMP} ASC",
            # Only orders that are active (column 'active' = 'Y')
            row_filter=f"{REFS.ORDERS_TABLE_ACTIVE}='{REFS.ORDERS_TABLE_ACTIVE_TRUE}'"
        )

        self.page_system.update(all_active_orders)
        
        self.update_view()

    def update_view(self):
        if len(self.page_system.current_items) > len(self._order_tiles):
            raise RuntimeError("More items on the page than allowed.")

        for idx in range(0, len(self._order_tiles)):
            if idx >= len(self.page_system.current_items):
                # Make order tile empty
                self._order_tiles[idx].empty_tile(self._background)
            else:
                # Fill order tile with order content
                order = self.page_system.current_items[idx]
                new_order_obj = OrdersService.convert_to_order_object(order)

                self._order_tiles[idx].order = new_order_obj

            # x_pos = idx % ActiveOrdersView.NUM_COLUMNS
            # y_pos = int(idx / ActiveOrdersView.NUM_COLUMNS)

            # new_order_obj = OrdersService.convert_to_order_object(order)

            # # Create OrderTileGUI for this order
            # order_tile = OrderTileGUI(
            #     parent=self.body_container,
            #     order=new_order_obj
            # )

            # pady = 10
            # padx = (0, 10)

            # if y_pos == 1:
            #     pady = (0, 10)
            # if x_pos == 0:
            #     padx = 10

            # # Place OrderTileGUI on this frame
            # order_tile.grid(row=y_pos, column=x_pos, padx=padx, pady=pady, sticky='news')
            # order_tile.pack_propagate(0)
            # order_tile.bind_on_click(self.on_tile_clicked)

        # -- Fill last row with empty space -- #

        # rest = len(self.page_system.current_items) % ActiveOrdersView.NUM_COLUMNS

        # if rest != 0:
        #     empty = ActiveOrdersView.NUM_COLUMNS - rest

        #     for i in range(0, empty):
        #         padx = (0, 10)

        #         if (x_pos + i + 1) == 0:
        #             padx = 10

        #         empty_tile = Frame(self.body_container, background=self.background)
        #         empty_tile.grid(row=y_pos, column=(x_pos + i + 1), padx=padx, pady=pady, sticky='news')

    def on_tile_clicked(self, clicked_order_tile, event = None):
        if self._mark_mode == ActiveOrdersView.MARK_OFF or clicked_order_tile.order == None:
            return

        prev_state = clicked_order_tile.order.state
        new_state = prev_state

        if self._mark_mode == ActiveOrdersView.MARK_DONE:
            new_state = REFS.PREPARED
        elif self._mark_mode == ActiveOrdersView.MARK_OPEN:
            new_state = REFS.OPEN
        elif self._mark_mode == ActiveOrdersView.MARK_CANCEL:
            new_state = REFS.CANCELED

        if new_state != prev_state:
            clicked_order_tile.order.state = new_state

            new_thread = CustomThread(7, "ActiveOrdersView-2", partial(self.on_tile_clicked_async, clicked_order_tile.order, new_state))
            new_thread.start()
            
    def on_tile_clicked_async(self, order, new_state):
        if REFS.MAIN_STATION:
            # If we are in CashDesk:
            OrdersService.update_order(order, active=True)

            # Send Message to other station about order creation (fire and forget)
            OrderMessagingService.notify_of_changes(
                changed_order=order,
                prefix=REFS.ORDER_CHANGED_PREFIX)
        else:
            OrderMessagingService.request_order_update(
                order=order,
                state=new_state
            )
            
        self.show_view()

    def _update_mark_mode(self):
        if self._mark_done_button.state:
            self._mark_mode = ActiveOrdersView.MARK_DONE
            return
        if self._mark_open_button.state:
            self._mark_mode = ActiveOrdersView.MARK_OPEN
            return
        if self._mark_canceled_button.state:
            self._mark_mode = ActiveOrdersView.MARK_CANCEL
            return
        
        self._mark_mode = ActiveOrdersView.MARK_OFF

    def _insert_order_tiles(self):
        if len(self._order_tiles) != 0:
            return

        for i in range(0, ActiveOrdersView.NUM_COLUMNS):
            self.body_container.grid_columnconfigure(i, weight=1)
            
        for i in range(0, ActiveOrdersView.NUM_ROWS):
            self.body_container.grid_rowconfigure(i, weight=1)

        x_pos = 0
        y_pos = 0

        std_pad = 20

        pady = std_pad
        padx = (0, std_pad)

        # Place each order tile on this frame in a 2 dimensional grid
        for idx in range(0, ActiveOrdersView.NUM_COLUMNS * ActiveOrdersView.NUM_ROWS):
            x_pos = idx % ActiveOrdersView.NUM_COLUMNS
            y_pos = int(idx / ActiveOrdersView.NUM_COLUMNS)

            # Create OrderTileGUI for this order
            order_tile = OrderTileGUI(
                parent=self.body_container,
                order=None
            )

            pady = std_pad
            padx = (0, std_pad)

            if y_pos >= 1:
                pady = (0, std_pad)
            if x_pos == 0:
                padx = std_pad

            # Place OrderTileGUI on this frame
            order_tile.grid(row=y_pos, column=x_pos, padx=padx, pady=pady, sticky='news')
            order_tile.pack_propagate(0)
            order_tile.bind_on_click(self.on_tile_clicked)

            self._order_tiles.append(order_tile)

