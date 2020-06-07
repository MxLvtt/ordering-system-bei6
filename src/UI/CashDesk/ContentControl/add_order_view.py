from tkinter import *
from functools import partial
from ContentControl.content_template import ContentTemplate
from Handlers.meals_handler import MealsHandler, Meal
from ContentControl.AddOrderView.meal_details_view import MealDetailsView


class AddOrderView(ContentTemplate):
    COLUMNS = 4

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

        # TODO: Move to new toolbar-system
        self._breadcrumb = "<breadcrumb>"

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
            meals_db, MealsHandler.SPLIT_ALL)

        # Update the tiles on the view to match the category
        self._update_tiles(self._root_category)

    def go_back(self):
        if self._current_category != self._root_category:
        #      or (
        #     self._root_category.splitmode == MealsHandler.NO_SPLIT and
        #     self._meal_details_view.is_shown
        # )
            prev_category = self._current_category.parent

            # if self._meal_details_view.is_shown:
            #     prev_category = self._current_category

            self._update_tiles(prev_category)

    def reset(self):
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
                buttoncmd = partial(self._open_meal_details, subcat.meal, subcat)

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
            if child != self._meal_details_view:
                child.destroy()
