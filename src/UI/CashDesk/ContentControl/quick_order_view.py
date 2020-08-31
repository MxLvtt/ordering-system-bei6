import Templates.references as REFS
from tkinter import *
from functools import partial
from cashdesk_model import CashDeskModel
from ContentControl.content_template import ContentTemplate
from Notification.notification_service import NotificationService
from Services.meals_service import MealsService
from Services.orders_service import OrdersService
from Services.Messengers.order_messaging_service import OrderMessagingService
from ContentControl.AddOrderView.meal_details_view import MealDetailsView
from ContentControl.AddOrderView.current_order_view import CurrentOrderView
from ContentControl.AddOrderView.receipt_view import ReceiptView
from Templates.cbutton import CButton
from Templates.images import IMAGES
from Templates.fonts import Fonts
from Templates.custom_thread import CustomThread
from Templates.radio_button import RadioButton, RadioButtonGroup


class QuickOrderView(ContentTemplate):
    COLUMNS = 4
    ROWS = 3

    def __init__(self, parent, toolbar_container: Frame, background="white", shown: bool = False):
        super().__init__(
            parent=parent,
            title=REFS.ADDORDERVIEW_TITLE,
            toolbar_container=toolbar_container,
            background=background,
            shown=shown
        )

        self._root_category = None
        self._order_type = REFS.EAT_IN

        self._checkmark_img = IMAGES.create(IMAGES.CHECK_MARK)
        self._close_light_img = IMAGES.create(IMAGES.CLOSE_LIGHT)
        self._add_img = IMAGES.create(IMAGES.ADD)
        self._back_img = IMAGES.create(IMAGES.BACK)
        self._trashcan_img = IMAGES.create(IMAGES.TRASH_CAN)
        self._order_img = IMAGES.create(IMAGES.ORDER)
        self._empty_img = IMAGES.create(IMAGES.EMPTY)

        self._background = background

        ######## Setting toolbar content ########

        # #### Right Button Container
        self._button_container_right = Frame(self.toolbar, background="#EFEFEF")
        self._button_container_right.grid(row=0, column=2, sticky='nsew')

        self._radio_button_group = RadioButtonGroup()
        
        self._eat_in_button = RadioButton(
            parent=self._button_container_right,
            text=REFS.ORDER_FORMS[REFS.EAT_IN],
            image=self._empty_img,
            highlight_image=self._empty_img,
            command=self._update_order_type,
            initial_state=True,
            group=self._radio_button_group,
            fg="#000000",
            bg=REFS.LIGHT_GRAY,
            highlight=REFS.LIGHT_CYAN,
            row=0, column=0
            # width=1.5, height=0.6
        )

        # Button: Change order type to "eat in"
        # self._eat_in_button = ToggleButton(
        #     parent=self._button_container_right,
        #     text=REFS.ORDER_FORMS[REFS.EAT_IN],
        #     image=self._empty_img,
        #     highlight_image=self._empty_img,
        #     command=self._update_order_type,
        #     initial_state=True,
        #     group=self._toggle_button_group,
        #     bg=REFS.LIGHT_GRAY,
        #     highlight=REFS.LIGHT_CYAN,
        #     row=0, column=0
        # )

        self._takeaway_button = RadioButton(
            parent=self._button_container_right,
            text=REFS.ORDER_FORMS[REFS.TAKEAWAY],
            image=self._empty_img,
            highlight_image=self._empty_img,
            command=self._update_order_type,
            initial_state=False,
            group=self._radio_button_group,
            fg="#000000",
            bg=REFS.LIGHT_GRAY,
            highlight=REFS.LIGHT_CYAN,
            row=0, column=1
            # width=1.5, height=0.6
        )

        # Button: Change order type to "takeaway"
        # self._takeaway_button = ToggleButton(
        #     parent=self._button_container_right,
        #     text=REFS.ORDER_FORMS[REFS.TAKEAWAY],
        #     image=self._empty_img,
        #     highlight_image=self._empty_img,
        #     command=self._update_order_type,
        #     initial_state=False,
        #     group=self._toggle_button_group,
        #     bg=REFS.LIGHT_GRAY,
        #     highlight=REFS.LIGHT_CYAN,
        #     row=0, column=1
        # )

        self._update_order_type()

        # Middle Breadcrumb Container
        self._breadcrumb_container_middle = Frame(
            self.toolbar, background="#EFEFEF")
        self._breadcrumb_container_middle.grid(row=0, column=1, sticky='nsew')

        self._breadcrumb = Label(
            master=self._breadcrumb_container_middle,
            text='Preis letzter Bestellung: -.--€',
            font=Fonts.small(),
            foreground='black',
            background='#EFEFEF'
        )
        self._breadcrumb.pack(side=LEFT, padx=10, fill='x', expand=1)

        self.toolbar.grid_rowconfigure(0, weight=1)
        self.toolbar.grid_columnconfigure(
            0, weight=0)  # Left Container     -> fit
        self.toolbar.grid_columnconfigure(
            1, weight=1)  # Middle Container   -> expand
        self.toolbar.grid_columnconfigure(
            2, weight=0)  # Right Container    -> fit

    @property
    def root_category(self):
        return self._root_category

    def initialize(self):
        meals_db = MealsService.get_raw_meals()

        self._root_category = MealsService.split_meals_by_categories(
            meals_db, MealsService.NO_SPLIT)

        # Update the tiles on the view to match the category
        self._update_tiles(self._root_category)

    def _update_order_type(self):
        if self._eat_in_button.state:
            self._order_type = REFS.EAT_IN
            return
        if self._takeaway_button.state:
            self._order_type = REFS.TAKEAWAY
            return

    def _update_tiles(self, root_category):
        self._clear_frame()

        self._meal_tile_buttons = []

        for idx, subcat in enumerate(root_category.subcategories):
            x = idx % QuickOrderView.COLUMNS
            y = int(idx / QuickOrderView.COLUMNS)

            if x == 0:
                self.row_container = Frame(self, background=self._background)

                paddingy = (0, 5)
                if y == 0:
                    paddingy = (10, 5)

                self.row_container.pack(
                    padx=5, pady=paddingy, side=TOP, fill="both", expand=1)

            meal_tile = Frame(self.row_container,
                              background=self._background, borderwidth=2)
            meal_tile.pack(padx=5, pady=(0, 5), side=LEFT,
                           fill="both", expand=1)
            meal_tile.pack_propagate(0)
            meal_tile.grid_propagate(0)
            meal_tile.update()

            # Button styles for 'category'-buttons
            foreground = '#000000'
            largefont = Fonts.xxxlarge(bold=True)
            buttoncmd = partial(self.finish_current_order, subcat.meal)

            # Replace every space with a new line character
            button_text = f"{subcat.name}"
            button_text = button_text.replace(' ', '\n', 1)

            meal_tile_button = Button(meal_tile,
                                      text=button_text,
                                      foreground=foreground,
                                      command=buttoncmd,
                                      font=largefont                                      
                                      )
            meal_tile_button.pack(fill="both", expand=1)
            
            self._meal_tile_buttons.append(meal_tile_button)

        for meal_button in self._meal_tile_buttons:
            meal_button.update()
            meal_button.config(wraplength=meal_button.winfo_width()-20)

    def _clear_frame(self):
        for child in self.winfo_children():
            if not (child in self._views):
                child.destroy()

    def _set_breadcrumb_text(self, text):
        self._breadcrumb.config(text=text)
        
    def finish_current_order_async(self, meal, order_type):
        try:
            new_order = OrdersService.create_new_order([meal], order_type)
        except:
            print("Creating new order failed.")
            raise

        if new_order == None:
            return

        new_order._price = new_order.calculate_price()

        self._set_breadcrumb_text(text=f"Preis letzter Bestellung: {new_order.price_str}€")

        NotificationService.show_toast(
            title=REFS.ORDER_SUMMARY_TOAST[0],
            text=REFS.ORDER_SUMMARY_TOAST[1].format(new_order.id, new_order.meals[0].name, f"{new_order.price_str} {REFS.CURRENCY}")
        )

        # Send Message to other station about order creation
        OrderMessagingService.notify_of_changes(
            changed_order=new_order,
            prefix=REFS.ORDER_CREATED_PREFIX)

    def finish_current_order(self, meal):
        """ Finished the current order
        """
        new_order = None

        meal.ingredients.clear()
        meal.addons.clear()
        meal.sizes.clear()

        new_thread = CustomThread(6, "QuickOrderViewThread-1", partial(self.finish_current_order_async, meal, self._order_type))
        new_thread.start()
        