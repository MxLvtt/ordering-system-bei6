import Templates.references as REFS
import math
from functools import partial
from tkinter import *
from tkinter import ttk
from random import *
from ContentControl.ActiveOrders.order_tile_gui import OrderTileGUI
from Services.orders_service import OrdersService
from Services.meals_service import MealsService
from ContentControl.content_template import ContentTemplate
from ContentControl.Settings.settings_category import SettingsCategory
from Templates.cbutton import CButton
from Templates.toggle_button import ToggleButton, ToggleButtonGroup
from Templates.images import IMAGES
from Templates.order import Order
from Templates.scroll_list import ScrollList
from Templates.scrollable import Scrollable
from Templates.page_system import PageSystem
from Templates.radio_button import RadioButton, RadioButtonGroup


class HistoryView(ContentTemplate):
    SPACING = 3
    FONT_NORMAL = ('Helvetica', '14')
    FONT_BOLD = ('Helvetica', '14', 'bold')
    FONT_BOLD_XL = ('Helvetica', '20', 'bold')
    
    EDIT_HEADER_WIDTH = 0
    EXPAND_HEADER_WIDTH = 0

    ITEMS_PER_PAGE = 16

    def __init__(self, parent, toolbar_container: Frame, background='white', shown: bool = False):
        super().__init__(
            parent=parent,
            title=REFS.HISTORYVIEW_TITLE,
            toolbar_container=toolbar_container,
            background='#696969',
            shown=shown
        )

        OrdersService.on_orders_changed.add(self.update_view_and_database_content)

        self.order_items = []

        self.page_system = PageSystem(
            on_page_changed=self.update_view_and_database_content,
            items_per_page=HistoryView.ITEMS_PER_PAGE,
            numbering_mode=PageSystem.ITEM_NUMBERING
        )
        
        self._back_img = IMAGES.create(IMAGES.BACK)
        self._next_img = IMAGES.create(IMAGES.NEXT)
        self._trashcan_img = IMAGES.create(IMAGES.TRASH_CAN)

        ######## Setting toolbar content ########

        #### Right Button Container
        self._button_container_right = Frame(self.toolbar, background="#EFEFEF")
        self._button_container_right.grid(row=0, column=2, sticky='nsew')

        # Button: Clear history
        self._clear_button = CButton(
            parent=self._button_container_right,
            image=self._trashcan_img,
            command=self.clear_history,
            fg=CButton.DARK, bg=CButton.LIGHT,
            width=1.0,
            row=0, column=0
        )

        #### Page System

        # Middle Breadcrumb Container
        self._container_middle = Frame(self.toolbar, background="#EFEFEF")
        self._container_middle.grid(row=0, column=1, sticky='nsew')

        ## Left Button Container
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

        header_bg = '#F4F4F4'

        ########## HEADER ##########

        self.header = Frame(master=self, background=header_bg, height=HistoryItem.HEIGHT)
        self.header.pack(side=TOP, fill='x', pady=(0,HistoryView.SPACING))
        self.header.pack_propagate(0)

        self.timestamp_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.ORDERS_TABLE_TIMESTAMP_GER.capitalize(),
            font=HistoryView.FONT_NORMAL,
            width=18
        )
        self.timestamp_head.pack(side=LEFT, padx=30)

        self.number_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.ORDERS_TABLE_ID_GER.capitalize(),
            font=HistoryView.FONT_BOLD,
            width=8
        )
        self.number_head.pack(side=LEFT, padx=30)

        self.form_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.ORDERS_TABLE_FORM_GER.capitalize(),
            font=HistoryView.FONT_NORMAL,
            width=10
        )
        self.form_head.pack(side=LEFT, padx=30)

        self.edit_head = Label(
            master=self.header,
            background=header_bg,
            # text=REFS.HISTORY_TABLE_EDIT,
            font=HistoryView.FONT_NORMAL,
            width=5
        )
        self.edit_head.pack(side=RIGHT, padx=30)
        self.edit_head.update()

        HistoryView.EDIT_HEADER_WIDTH = self.edit_head.winfo_reqwidth()
        
        self.expand_head = Label(
            master=self.header,
            background=header_bg,
            # text=REFS.HISTORY_TABLE_EXPAND,
            font=HistoryView.FONT_NORMAL,
            width=5
        )
        self.expand_head.pack(side=RIGHT, padx=(30,0))
        self.expand_head.update()

        HistoryView.EXPAND_HEADER_WIDTH = self.expand_head.winfo_reqwidth()

        self.active_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.ORDERS_TABLE_ACTIVE_GER.capitalize(),
            font=HistoryView.FONT_NORMAL,
            width=8
        )
        self.active_head.pack(side=RIGHT, padx=30)

        self.state_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.ORDERS_TABLE_STATE_GER.capitalize(),
            font=HistoryView.FONT_NORMAL,
            width=10
        )
        self.state_head.pack(side=RIGHT, padx=30)

        ########## TABLE ##########

        self.table = Frame(master=self, background='#F4F4F4')
        self.table.pack(side=TOP, fill='both', expand=1)

        self.scrolllist = ScrollList(parent=self.table, spacing=HistoryView.SPACING, background='#696969')

    def clear_history(self):
        if OrdersService.delete_from_table(
            condition=f"{REFS.ORDERS_TABLE_ACTIVE}='{REFS.ORDERS_TABLE_ACTIVE_FALSE}'",
            confirm=True
        ):
            self.show_view()

    def show_view(self):
        """ Is called everytime this view is opened
        """
        super().show_view()

        self.update_view_and_database_content()

        self.scrolllist.reset_scroll()

    def update_view_and_database_content(self):
        # Get all orders from the database sorted by their timestamp
        orders_sorted_by_timestamp = OrdersService.get_orders(order_by=f"{REFS.ORDERS_TABLE_TIMESTAMP} DESC")
        # Safe the result in this class's array
        self.order_items.clear()
        self.order_items.extend(orders_sorted_by_timestamp)

        self.update_view()

    def update_view(self):
        self.scrolllist.remove_all()

        self.page_system.update(self.order_items)

        for order in self.page_system.current_items:
            element = HistoryItem(parent=self.scrolllist, order=order)
            self.scrolllist.add_row(element, update=False)

        self.scrolllist.update_view()


class HistoryItem(Scrollable):
    HEIGHT=80
    EXPAND_HEIGHT=600

    MEALS_CONTENT_MODE = 0
    EDIT_CONTENT_MODE = 1

    def __init__(self, parent, order, background='white'):
        super().__init__(
            parent=parent,
            height=HistoryItem.HEIGHT,
            background='#F4F4F4'
        )

        self._background = '#F4F4F4'

        self._order = OrdersService.convert_to_order_object(order)
        self.expanded = False

        self._changed_order = self._order.copy()

        self.edit_view_shown = False
        self.meals_view_shown = False

        column_names: [] = OrdersService.get_column_names()

        self._edit_img = IMAGES.create(IMAGES.EDIT)
        self._check_img = IMAGES.create(IMAGES.CHECK_MARK)
        self._down_img = IMAGES.create(IMAGES.DOWN)
        self._up_img = IMAGES.create(IMAGES.UP)

        ########## COLUMNS ##########

        self.row_frame = Frame(
            master=self,
            background=background,
            height=HistoryItem.HEIGHT
        )
        self.row_frame.pack(side=TOP, fill='x')
        self.row_frame.pack_propagate(0)

        self.meals_frame = Frame(
            master=self,
            background='#F4F4F4'
        )

        self.set_meals_content()

        self.edit_frame = Frame(
            master=self,
            background='#F4F4F4'
        )

        self.set_edit_view()

        ##### TIMESTAMP #####

        timestamp_i = column_names.index(REFS.ORDERS_TABLE_TIMESTAMP)
        self.timestamp = Label(
            master=self.row_frame,
            text=OrdersService.convert_timestamp(order[timestamp_i], extended=True),
            font=HistoryView.FONT_NORMAL,
            background=background,
            width=18
        )
        self.timestamp.pack(side=LEFT, padx=30)

        ##### NUMBER #####

        number_i = column_names.index(REFS.ORDERS_TABLE_ID)
        self.number = Label(
            master=self.row_frame,
            text=f"#{order[number_i]}",
            font=HistoryView.FONT_BOLD,
            background=background,
            width=8
        )
        self.number.pack(side=LEFT, padx=30)

        ##### FORM #####

        form_i = column_names.index(REFS.ORDERS_TABLE_FORM)
        self.form = Label(
            master=self.row_frame,
            text=OrdersService.convert_form(order[form_i]),
            font=HistoryView.FONT_NORMAL,
            background=background,
            width=10
        )
        self.form.pack(side=LEFT, padx=30)

        ##### EDIT BUTTON #####

        self.edit_container = Frame(
            master=self.row_frame,
            width=HistoryView.EDIT_HEADER_WIDTH,
            height=60,
            bg=background
        )
        self.edit_container.pack(side=RIGHT, padx=30)

        self.edit = Button(
            master=self.edit_container,
            image=self._edit_img,
            command=self.edit_order_command
        )
        self.edit.place(relx=0.5, rely=0.5, anchor="center")

        self.initial_button_background = self.edit.cget('background')

        if self._order.state != REFS.OPEN and self._order.state != REFS.CHANGED:
            self.edit.config(state="disabled")

        ##### EXPAND BUTTON #####

        self.expand_container = Frame(
            master=self.row_frame,
            width=HistoryView.EXPAND_HEADER_WIDTH,
            height=60,
            bg=background
        )
        self.expand_container.pack(side=RIGHT, padx=(30,0))

        expand_button_cmd = partial(self.expand_button_command, HistoryItem.MEALS_CONTENT_MODE)

        self.expand = Button(
            master=self.expand_container,
            image=self._down_img,
            command=expand_button_cmd
        )
        self.expand.place(relx=0.5, rely=0.5, anchor="center")

        ##### ACTIVE #####

        active_i = column_names.index(REFS.ORDERS_TABLE_ACTIVE)
        self.active = Label(
            master=self.row_frame,
            text=OrdersService.convert_active(order[active_i]),
            font=HistoryView.FONT_NORMAL,
            background=background,
            width=8
        )
        self.active.pack(side=RIGHT, padx=30)

        ##### STATUS #####

        state_i = column_names.index(REFS.ORDERS_TABLE_STATE)
        self.state = Label(
            master=self.row_frame,
            text=OrdersService.convert_status(order[state_i]),
            font=HistoryView.FONT_NORMAL,
            background=REFS.ORDER_STATE_COLORS[int(order[state_i])],
            width=10
        )
        self.state.pack(side=RIGHT, padx=30)

    def _save_order(self):
        OrdersService.update_order(self._changed_order)

        self._order = self._changed_order.copy()

        self.form.config(text=OrdersService.convert_form(self._order.form))
        self.state.config(text=OrdersService.convert_status(self._order.state))
        self.state.config(background=REFS.ORDER_STATE_COLORS[self._order.state])
        
        if self._order.state != REFS.OPEN and self._order.state != REFS.CHANGED:
            self.edit.config(state="disabled")

    def _has_order_changed(self):
        if self._changed_order.form != self._order.form:
            return True

        if self._changed_order.state != self._order.state:
            return True

        # TODO: Add check for any other property that can be changed

        return False

    def edit_order_command(self):
        # Step 1: Connect to database and check if the order is still in state "OPEN" or "CHANGED"
            # Still "OPEN" or "CHANGED"?
            # -> Y: Continue with Step 2
            # -> N: Disable the edit button and return from this method
        results = OrdersService.get_orders(row_filter=f"{REFS.ORDERS_TABLE_ID}={self._order.id}")

        if results == None or len(results) == 0 or results[0] == "":
            raise RuntimeError("Order doesn't exist in the database")

        new_order_obj = OrdersService.convert_to_order_object(results[0])

        if new_order_obj.state != REFS.OPEN and new_order_obj.state != REFS.CHANGED:
            self.edit.config(state="disabled")
            return

        # Step 2: Open the actual editor view
        self.expand_button_command(mode=HistoryItem.EDIT_CONTENT_MODE)

    def expand_button_command(self, mode):
        def _open_edit_view():
            # Show edit view
            self.edit_frame.pack(side=TOP, fill='x')
            self.edit_frame.update()
            # Adapt the edit button
            self.edit.config(image=self._check_img)
            self.edit.config(background=CButton.GREEN)

            self.edit_view_shown = True
            self.expanded = True
            # Calculate the content's height
            self.height = self.edit_frame.winfo_reqheight() + self.initial_height

        def _open_meals_view():
            # Show meals view
            self.meals_frame.pack(side=TOP)
            self.meals_frame.update()
            # Adapt the expand button
            self.expand.config(image=self._up_img)

            self.meals_view_shown = True
            self.expanded = True
            # Calculate the content's height
            self.height = self.meals_frame.winfo_reqheight() + self.initial_height

        def _close_edit_view(safe_content: bool = False):
            if safe_content:
                if self._has_order_changed():
                    self._save_order()

            # Hide edit view
            self.edit_frame.pack_forget()
            # Reset edit button style
            self.edit.config(image=self._edit_img)
            self.edit.config(background=self.initial_button_background)

            self.edit_view_shown = False
            self.expanded = False
            self.height = self.initial_height

        def _close_meals_view():
            # Hide meals view
            self.meals_frame.pack_forget()
            # Reset expand button style
            self.expand.config(image=self._down_img)

            self.meals_view_shown = False
            self.expanded = False
            self.height = self.initial_height

        if mode == HistoryItem.MEALS_CONTENT_MODE:
            # Item is not expanded
            if not self.expanded:
                _open_meals_view()
            # Item is already expanded
            else:
                # Is the meals view currently open?
                if self.meals_view_shown:
                    _close_meals_view()
                # Is the edit view currently open?
                elif self.edit_view_shown:
                    _close_edit_view()
                    _open_meals_view()
        elif mode == HistoryItem.EDIT_CONTENT_MODE:
            # Item is not expanded
            if not self.expanded:
                _open_edit_view()
            # Item is already expanded
            else:
                # Is the meals view currently open?
                if self.meals_view_shown:
                    _close_meals_view()
                    _open_edit_view()
                # Is the edit view currently open?
                elif self.edit_view_shown:
                    _close_edit_view(safe_content=True)

    def set_meals_content(self):
        """ Defines the content to be shown in the meals_frame.
        """
        meals = self._order.meals
        bg = 'white'

        containers = []

        for meal in meals:
            meal_container = Frame(
                master=self.meals_frame,
                background=bg
            )
            meal_container.pack(side=LEFT, padx=20, pady=20)

            containers.append(meal_container)

            (meal_title, meal_text) = MealsService.meal_content_to_text(meal)

            # amount_text = ""
            # if meal.amount > 1:
            #     amount_text = f"{meal.amount}x "
            
            # meal_title = f"{amount_text}{meal.name}"
            # if len(meal.sizes) != 0 and meal.sizes[0] != '':
            #     meal_title = f"{meal_title} ({meal.sizes[0]})"

            meal_title_label = Label(
                master=meal_container,
                text=meal_title,
                background=bg,
                font=HistoryView.FONT_BOLD_XL,
                justify='left',
                anchor='nw'
            )
            meal_title_label.pack(side=TOP, fill='x', padx=10, pady=10)

            if meal_text != "":
                # Label that contains the list of ingredients and addons of this meal
                meal_ingredients_label = Label(
                    master=meal_container,
                    text=meal_text,
                    font=HistoryView.FONT_NORMAL,
                    background=bg,
                    anchor='w',
                    justify='left'
                )
                meal_ingredients_label.pack(side=TOP, fill='x', padx=10, pady=(0,10))

            meal_container.update()

    def set_edit_view(self):
        """ Defines the content to be shown in the edit_frame.
        """
        ### FORM SETTINGS CONTAINER

        form_container = Frame(master=self.edit_frame, background=self._background)
        form_container.pack(side=LEFT, padx=20, pady=20, fill='y')

        form_title_label = Label(
            master=form_container,
            text=f"{REFS.ORDERS_TABLE_FORM_GER}",
            font=HistoryView.FONT_BOLD,
            background=self._background
        )
        form_title_label.pack(side=TOP, fill='x')

        form_radiobutton_group = RadioButtonGroup()

        def _form_button_pressed(button_form):
            self._changed_order.form = button_form

        for idx, form in enumerate(REFS.ORDER_FORMS):
            initial_state = (self._order.form == idx)
            command = partial(_form_button_pressed, idx)

            form_radio_button = RadioButton(
                master=form_container,
                text=form,
                group=form_radiobutton_group,
                highlight=REFS.LIGHT_CYAN,
                font=HistoryView.FONT_NORMAL,
                initial_state=initial_state,
                command=command
            )
            form_radio_button.pack(side=TOP, fill='x', pady=10)

        form_container.update()

        ### STATE SETTINGS CONTAINER

        state_container = Frame(master=self.edit_frame, background=self._background)
        state_container.pack(side=LEFT, padx=20, pady=20, fill='y')

        state_title_label = Label(
            master=state_container,
            text=f"{REFS.ORDERS_TABLE_STATE_GER}",
            font=HistoryView.FONT_BOLD,
            background=self._background
        )
        state_title_label.pack(side=TOP, fill='x')
        
        state_container.update()
