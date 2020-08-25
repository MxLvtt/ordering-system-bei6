import Templates.references as REFS
from functools import partial
from tkinter import *
from tkinter import ttk
from random import *
from ContentControl.content_template import ContentTemplate
from ContentControl.Settings.settings_category import SettingsCategory
from ContentControl.Settings.meals_settings_view import MealsSettingsView
from Templates.cbutton import CButton
from Templates.toggle_button import ToggleButton, ToggleButtonGroup
from Templates.images import IMAGES
from Templates.order import Order
from Services.orders_service import OrdersService

class SettingsView(ContentTemplate):
    def __init__(self, parent, toolbar_container: Frame, background="white", shown: bool = False):
        super().__init__(
            parent=parent,
            title=REFS.SETTINGSVIEW_TITLE,
            toolbar_container=toolbar_container,
            background=background,
            shown=shown
        )

        self._checkmark_img = IMAGES.create(IMAGES.CHECK_MARK)
        self._checkmark_dark_img = IMAGES.create(IMAGES.CHECK_MARK_DARK)
        self._add_img = IMAGES.create(IMAGES.ADD)
        self._back_img = IMAGES.create(IMAGES.BACK)
        self._next_img = IMAGES.create(IMAGES.NEXT)
        self._trashcan_img = IMAGES.create(IMAGES.TRASH_CAN)
        self._order_img = IMAGES.create(IMAGES.ORDER)
        self._burger_img = IMAGES.create(IMAGES.BURGER_DARK)

        self.main_view = Frame(master=self, background=background)
        self.main_view.pack(side=TOP, fill='both', expand=1)
        
        self._active_view = self.main_view

        ######## Setting main content ########

        self._top_row_frame = Frame(master=self.main_view, background=background)
        self._top_row_frame.pack(side=TOP, fill='both', expand=1)

        ### ORDERS CATEGORY

        self.orders_cat_view = MealsSettingsView(self, background)
        
        self._cat_orders : SettingsCategory = SettingsCategory(
            parent=self._top_row_frame,
            image=self._order_img,
            title="Orders",
            show_view_command=self.switch_to_view,
            view=self.orders_cat_view
        )
        self._cat_orders.pack(side=LEFT, padx=10, pady=10, fill='both', expand=1)

        ### MEALS CATEGORY

        self.meals_cat_view = MealsSettingsView(self, background)
        
        self._cat_meals : SettingsCategory = SettingsCategory(
            parent=self._top_row_frame,
            image=self._burger_img,
            title="Meals",
            show_view_command=self.switch_to_view,
            view=self.meals_cat_view
        )
        self._cat_meals.pack(side=LEFT, padx=10, pady=10, fill='both', expand=1)

        ######## Setting toolbar content ########

        #### Right Button Container
        self._button_container_right = Frame(self.toolbar, background="#EFEFEF")
        self._button_container_right.grid(row=0, column=2, sticky='nsew')

        #### Middle Breadcrumb Container
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

        go_back_command = partial(self.switch_to_view, self.main_view)

        # Button: Go back
        self._back_button = CButton(
            parent=self._button_container_left,
            image=self._back_img,
            command=go_back_command,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=0
        )
        self._back_button._disable()

        self.toolbar.grid_rowconfigure(0, weight=1)
        self.toolbar.grid_columnconfigure(0, weight=0) # Left Container     -> fit
        self.toolbar.grid_columnconfigure(1, weight=1) # Middle Container   -> expand
        self.toolbar.grid_columnconfigure(2, weight=0) # Right Container    -> fit
        
        ######## END setting toolbar content ########

    def switch_to_view(self, view: Frame):
        if view != self.main_view:
            self._back_button._enable()
        else:
            self._back_button._disable()

        self._active_view.pack_forget()
        view.pack(side=TOP, fill='both', expand=1)

        try:
            view.update_view()
        except:
            pass

        self._active_view = view
