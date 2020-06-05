from tkinter import *
from ContentControl.content_template import ContentTemplate
from Handlers.meals_handler import MealsHandler,Meal

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

    def initialize(self):
        meals_db = MealsHandler.get_raw_meals()

        # TODO: ALl categories of the meals have to be retrieved. Should they be split in groups in MealsHandler?
        # TODO: USE THE CATEGORIES TO BUILD UP THE TILES!!!!
        self._meals_by_cats = MealsHandler.split_meals_by_categories(meals_db)

        self._meals = meals_db

        # Note: The __init__ is only called once, not everytime the view is changed

        self._meal_tiles = []

        for idx, meal in enumerate(self._meals):
            x = idx % AddOrderView.COLUMNS
            y = int(idx / AddOrderView.COLUMNS)

            if x == 0:
                self.row_container = Frame(self, background=self._background)

                paddingy = (0,5)
                if y == 0:
                    paddingy = (10,5)
                    
                self.row_container.pack(padx=5, pady=paddingy, side=TOP, fill="both", expand=1)

            meal_tile = Frame(self.row_container, background="#323232", borderwidth=2)
            meal_tile.pack(padx=5, pady=(0,5), side=LEFT, fill="both", expand=1)
            meal_tile.pack_propagate(0)
            meal_tile.grid_propagate(0)
            meal_tile.update()

            meal_tile_label = Label(meal_tile, text=meal[1], background=self.TILE_BGD)
            meal_tile_label.pack(fill="both", expand=1)

            self._meal_tiles.append(meal_tile)
