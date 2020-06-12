from tkinter import *
from functools import partial
from cashdesk_model import CashDeskModel
from ContentControl.content_template import ContentTemplate
from Handlers.meals_handler import MealsHandler, Meal
from ContentControl.AddOrderView.meal_details_view import MealDetailsView
from ContentControl.AddOrderView.current_order_view import CurrentOrderView
from Templates.cbutton import CButton
from Templates.images import IMAGES


class AddOrderView(ContentTemplate):
    COLUMNS = 4
    CURRENT_ORDER_TITLE = "Current order"

    def __init__(self, parent, toolbar_container: Frame, background="white", shown: bool = False):
        super().__init__(
            parent=parent,
            title="Add new order",
            toolbar_container=toolbar_container,
            background=background,
            shown=shown
        )

        self._checkmark_img = IMAGES.create(IMAGES.CHECK_MARK)
        self._add_img = IMAGES.create(IMAGES.ADD)
        self._back_img = IMAGES.create(IMAGES.BACK)
        self._trashcan_img = IMAGES.create(IMAGES.TRASH_CAN)
        self._order_img = IMAGES.create(IMAGES.ORDER)

        self._background = background
        self._root_category = None
        self._current_category = None

        self._meal_details_view = MealDetailsView(self, background, False)
        self._current_order_view = CurrentOrderView(self, background, False)

        self._current_order_view.meal_number_changed_event.add(self._added_meal_number_changed)

        ######## Setting toolbar content ########

        #### Right Button Container
        self._button_container_right = Frame(self.toolbar, background="#EFEFEF")
        self._button_container_right.grid(row=0, column=2, sticky='nsew')

        # TODO
        self._dummy_counter = 0

        self._label_meal_counter = Label(
            master=self._button_container_right,
            text='0',
            foreground='red',
            font=('Helvetica', '16', 'bold'),
            background="#EFEFEF"
        )
        self._label_meal_counter.grid(row=0, column=0, padx=15)
        
        # Button: Finish current order
        self._finish_order_button = CButton(
            parent=self._button_container_right,
            image=self._checkmark_img,
            command=self.finish_current_order,
            fg=CButton.WHITE, bg=CButton.GREEN,
            row=0, column=1
        )
        self._finish_order_button._hide()
        self._finish_order_button._disable()

        # Button: Show current order
        self._current_order_button = CButton(
            parent=self._button_container_right,
            image=self._order_img,
            command=self.show_current_order,
            fg=CButton.WHITE, bg=CButton.LIGHT,
            row=0, column=2
        )

        ### Middle Breadcrumb Container
        self._breadcrumb_container_middle = Frame(self.toolbar, background="#EFEFEF")
        self._breadcrumb_container_middle.grid(row=0, column=1, sticky='nsew')

        self._breadcrumb = Label(
            master=self._breadcrumb_container_middle,
            text='<breadcrumb>',
            font=('Helvetica', '16'),
            foreground='black',
            background='#EFEFEF'
        )
        self._breadcrumb.pack(side=LEFT, padx=10, fill='x', expand=1)

        #### Left Button Container
        self._button_container_left = Frame(self.toolbar, background="#EFEFEF")
        self._button_container_left.grid(row=0, column=0, sticky='nsew')

        self.toolbar.grid_rowconfigure(0, weight=1)
        self.toolbar.grid_columnconfigure(0, weight=0) # Left Container     -> fit
        self.toolbar.grid_columnconfigure(1, weight=1) # Middle Container   -> expand
        self.toolbar.grid_columnconfigure(2, weight=0) # Right Container    -> fit
        
        # Button: Add meal to order
        self._add_meal_to_order_button = CButton(
            parent=self._button_container_left,
            image=self._add_img,
            command=self.add_meal_to_order,
            fg=CButton.WHITE, bg=CButton.GREEN,
            spaceX=(0.0,1.0),
            row=0, column=0
        )

        # Button: Go up one category
        self._back_button = CButton(
            parent=self._button_container_left,
            image=self._back_img,
            command=self.go_back,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=1
        )

        # Button: Reset the category and content
        self._clear_button = CButton(
            parent=self._button_container_left,
            image=self._trashcan_img,
            command=self.clear_addorderview,
            fg=CButton.DARK, bg=CButton.LIGHT,
            # spaceX=(0.0,1.0),
            row=0, column=2
        )

    @property
    def root_category(self):
        return self._root_category

    @property
    def current_category(self):
        return self._current_category

    def initialize(self):
        meals_db = MealsHandler.get_raw_meals()

        # ----------------------------------------------------------------- #

        print("\nNo split:")
        self._root_category = MealsHandler.split_meals_by_categories(
            meals_db, MealsHandler.NO_SPLIT)

        # Print a tree of all categories
        self._root_category.printc()

        # ----------------------------------------------------------------- #

        print("\nSplit main categories:")
        self._root_category = MealsHandler.split_meals_by_categories(
            meals_db, MealsHandler.SPLIT_MAIN)

        # Print a tree of all categories
        self._root_category.printc()

        # ----------------------------------------------------------------- #

        print("\nSplit all:")
        self._root_category = MealsHandler.split_meals_by_categories(
            meals_db, MealsHandler.SPLIT_ALL)

        # Print a tree of all categories
        self._root_category.printc()

        # ----------------------------------------------------------------- #

        self._root_category = MealsHandler.split_meals_by_categories(
            meals_db, MealsHandler.SPLIT_MAIN)

        # Update the tiles on the view to match the category
        self._update_tiles(self._root_category)

    def go_back(self):
        # If we are in the CurrentOrderView: close it and go back to current category
        if self._current_order_view.is_shown:
            self._update_tiles(self._current_category)
            return

        if self._current_category != self._root_category:
        #      or (
        #     self._root_category.splitmode == MealsHandler.NO_SPLIT and
        #     self._meal_details_view.is_shown
        # )
            prev_category = self._current_category.parent

            if prev_category == None:
                prev_category = self._current_category

            self._update_tiles(prev_category)

    def reset(self):        
        # If we are in the CurrentOrderView: close it and go to root category
        if self._current_order_view.is_shown:
            self._update_tiles(self._root_category)
            return

        if self._current_category != self._root_category:
            self._update_tiles(self._root_category)

    def _open_meal_details(self, meal: Meal, category):
        self._current_category = category
        self._meal_details_view.update_content(meal, True)

        self._clear_frame()
        self._meal_details_view.show_view()

    def _update_tiles(self, root_category):
        self._clear_frame()
        self._meal_details_view.hide_view()
        self._current_order_view.hide_view()
        self._finish_order_button._hide()
        self._label_meal_counter.grid()
        
        self._current_category = root_category

        # Update the breadcrumb in the toolbar to fit the current category
        self._update_breadcrumb(root_category)

        if root_category.has_meal():
            self._add_meal_to_order_button._enable()
            self._open_meal_details(root_category.meal, root_category)
            return
        
        self._add_meal_to_order_button._disable()

        self._meal_tiles = []

        for idx, subcat in enumerate(root_category.subcategories):
            x = idx % AddOrderView.COLUMNS
            y = int(idx / AddOrderView.COLUMNS)

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
            foreground = '#646464'
            largefont = ("Helvetica", "42", "bold italic")
            buttoncmd = partial(self._update_tiles, subcat)

            if subcat.has_meal():
                # Button styles for 'meal'-buttons
                foreground = '#000000'
                largefont = ("Helvetica", "42", "bold")

            meal_tile_button = Button(meal_tile,
                                      text=subcat.name,
                                      foreground=foreground,
                                      #  background=self.TILE_BGD,
                                      command=buttoncmd,
                                      font=largefont
                                      )
            meal_tile_button.pack(fill="both", expand=1)

            self._meal_tiles.append(meal_tile)

    def _clear_frame(self):
        for child in self.winfo_children():
            if child != self._meal_details_view and child != self._current_order_view:
                child.destroy()

    def _update_breadcrumb(self, category):
        if category == self._root_category:
            self._breadcrumb.config(text="")
            return

        new_breadcrumb = f"{category.name}"
        curr_cat = category

        while curr_cat.parent != None:
            curr_cat = curr_cat.parent

            cat_name = ""
            if curr_cat != self._root_category:
                cat_name = f"{curr_cat.name} > "

            new_breadcrumb = f"{cat_name}{new_breadcrumb}"

        self._breadcrumb.config(text=new_breadcrumb)

    def _set_breadcrumb_text(self, text):
        self._breadcrumb.config(text=text)

    def _enable_add_button(self):
        if self._meal_details_view.is_shown:
            self._add_meal_to_order_button._enable()

    def _added_meal_number_changed(self):
        self._label_meal_counter.config(text=f"{self._current_order_view.number_of_meals}")

        if self._current_order_view.number_of_meals > 0:
            self._finish_order_button._enable()
        else:
            self._finish_order_button._disable()

    # Button Callback Functions

    def add_meal_to_order(self):
        """ Adds a new order with the information given in the add-order-view.
        """
        self._add_meal_to_order_button._disable()
        CashDeskModel.call_after_delay(self._enable_add_button, 1.0)
        
        meal_to_add = self._meal_details_view.get_adapted_meal()

        if meal_to_add == None:
            return

        # TODO: Add new (adapted) meal object to the current order
        self._current_order_view.add_meal(meal_to_add)

        # TODO: IMPLEMENT THE FOLLOWING VARIABLES
        # This is set, if the meal has been successfully added to the current order
        meal_added_successfully = True
        # This is set in the settings and can be changed later
        reset_view_after_adding = True

        if meal_added_successfully and reset_view_after_adding:
            self.reset()

    def clear_addorderview(self):
        """ Resets the add order view
        """
        if not self._current_order_view.is_shown:
            self.reset()
        else:
            self._current_order_view.remove_all()

    def show_current_order(self):
        """ Opens the view of the current order and its already added meals
        """
        # TODO: Wrong behavior - if you open the current order view while the
        # TODO: meal detail is open and then close it again, all the information
        # TODO: about the meal detail is lost!
        if not self._current_order_view.is_shown:
            if self._meal_details_view.is_shown:
                self._meal_details_view.hide_view()
            else:
                self._clear_frame()

            self._set_breadcrumb_text(AddOrderView.CURRENT_ORDER_TITLE)

            self._add_meal_to_order_button._disable()
            self._current_order_view.show_view()
            self._finish_order_button._show()
            self._label_meal_counter.grid_remove()
        else:
            self.go_back()

    def finish_current_order(self):
        """ Finished the current order
        """
        self._current_order_view.save_order()
