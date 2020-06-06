from tkinter import *
from tkinter import font as tkFont
from functools import partial
from ContentControl.content_template import ContentTemplate
from Handlers.meals_handler import MealsHandler, Meal
from ContentControl.AddOrderView.meal_details_view import MealDetailsView

class AddOrderView(ContentTemplate):
    COLUMNS = 3
    TILE_BGD = "#F4F4F4"

    def __init__(self, parent, background="white", shown: bool = False):
        super().__init__(
            parent=parent,
            title="Add new order",
            background=background,
            shown=shown
        )

        self._background = background
        self._root_category = None
        self._current_category = None
        self._meal_details_view = MealDetailsView(self, background, False)

    def root_category(self):
        return self._root_category

    def current_category(self):
        return self._current_category

    def initialize(self):
        meals_db = MealsHandler.get_raw_meals()

        print("\nNo split:")
        self._root_category = MealsHandler.split_meals_by_categories(meals_db, MealsHandler.NO_SPLIT)

        # Print a tree of all categories
        self._root_category.printc()

        print("\nSplit main categories:")
        self._root_category = MealsHandler.split_meals_by_categories(meals_db, MealsHandler.SPLIT_MAIN)

        # Print a tree of all categories
        self._root_category.printc()
        
        print("\nSplit all:")
        self._root_category = MealsHandler.split_meals_by_categories(meals_db, MealsHandler.SPLIT_ALL)

        # Print a tree of all categories
        self._root_category.printc()

        # Update the tiles on the view to match the category
        self._update_tiles(self._root_category)

    def go_back(self):
        if self._current_category != self._root_category:
            prev_category = self._current_category.parent

            if self._meal_details_view.is_shown:
                prev_category = self._current_category

            self._update_tiles(prev_category)

    def reset(self):
        if self._current_category != self._root_category:
            self._update_tiles(self._root_category)

    def _open_meal_details(self, meal: Meal):
        self._meal_details_view.update_content(meal, MealsHandler.COLUMN_NAMES, True)

        self._clear_frame()
        self._meal_details_view.show_view()

    def _update_tiles(self, root_category):
        self._clear_frame()
        self._meal_details_view.hide_view()

        self._current_category = root_category
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
                              background=self.TILE_BGD, borderwidth=2)
            meal_tile.pack(padx=5, pady=(0, 5), side=LEFT,
                           fill="both", expand=1)
            meal_tile.pack_propagate(0)
            meal_tile.grid_propagate(0)
            meal_tile.update()

            largefont = tkFont.Font(family="Helvetica", size=42, weight='bold')
            buttoncmd = partial(self._update_tiles, subcat)

            if subcat.has_meal():
                # TODO: Temporary action on button press of actual meal, no category
                buttoncmd = partial(self._open_meal_details, subcat.meal)

            meal_tile_label = Button(meal_tile,
                                     text=subcat.name,
                                     background=self.TILE_BGD,
                                     command=buttoncmd,
                                     font=largefont
                                     )
            meal_tile_label.pack(fill="both", expand=1)

            self._meal_tiles.append(meal_tile)

    def _clear_frame(self):
        for child in self.winfo_children():
            if child != self._meal_details_view:
                child.destroy()