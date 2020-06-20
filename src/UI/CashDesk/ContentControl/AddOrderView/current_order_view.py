from tkinter import *
from tkinter import font as tkFont
from functools import partial
from ContentControl.AddOrderView.added_meal_tile import AddedMealTile
from EventHandler.Event import Event
import Templates.references as REFS


class CurrentOrderView(Frame):
    NUM_COLUMNS = 5
    NUM_ROWS = 2

    def __init__(self, parent, background, shown: bool = False):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self._meal_number_changed_event: Event = Event()

        # Assure that the frame won't resize with the contained widgets
        self.pack_propagate(0)
        self.grid_propagate(0)

        # Private members
        self._is_hidden = shown
        self._background = background

        # Initialize visibility-state
        if not shown:
            self.hide_view()
        else:
            self.show_view()

        self._added_meal_tiles = []
        self._order_form = 0 # TODO

    @property
    def added_meal_tiles(self) -> []:
        return self._added_meal_tiles

    @property
    def added_meals(self) -> []:
        meals = []

        for meal_tile in self._added_meal_tiles:
            meals.append(meal_tile.meal)

        return meals

    @property
    def order_form(self) -> int:
        return self._order_form

    @property
    def is_shown(self) -> bool:
        return not self._is_hidden

    @property
    def number_of_meals(self) -> int:
        return len(self._added_meal_tiles)

    @property
    def meal_number_changed_event(self) -> Event:
        return self._meal_number_changed_event

    def add_meal(self, adapted_meal):
        """ Adds the adapted (!) meal object to the current order
        """
        added_meal = AddedMealTile(
            parent=self,
            meal=adapted_meal,
            index=len(self._added_meal_tiles),
            remove_meal_cb=self.remove_meal
        )
        self._added_meal_tiles.append(added_meal)    # Add meal tile to list
        self._meal_number_changed_event()       # Trigger event to notify add order view
        self._update_view()                     # Update the view

    def remove_meal(self, meal_tile: AddedMealTile):
        self._added_meal_tiles.remove(meal_tile)
        self._meal_number_changed_event()

        meal_tile.destroy()
        self._update_view()

    def remove_all(self):
        for meal in self._added_meal_tiles:
            meal.destroy()

        self._added_meal_tiles.clear()
        self._meal_number_changed_event()
        self._update_view()

    def _update_view(self):
        for child in self.winfo_children():
            if not isinstance(child, AddedMealTile):
                child.destroy()

        x = 0
        y = 0

        for idx, meal_tile in enumerate(self._added_meal_tiles):
            x = idx % CurrentOrderView.NUM_COLUMNS
            y = int(idx / CurrentOrderView.NUM_COLUMNS)

            self.grid_columnconfigure(x, weight=1)
            self.grid_rowconfigure(y, weight=1)

            meal_tile.set_position(row=y, column=x)

        # -- Fill last row with empty space -- #

        needed_cols = len(self._added_meal_tiles) % CurrentOrderView.NUM_COLUMNS

        if needed_cols != 0:
            empty = CurrentOrderView.NUM_COLUMNS - needed_cols
            for i in range(0, empty):
                col = (i+x+1)

                empty_tile = Frame(self, background=self._background)
                empty_tile.grid(row=y, column=col, padx=15, pady=15, sticky='nsew')

                self.grid_columnconfigure(col, weight=1)

        # -- Fill space with empty rows if necessary -- #

        if (y + 1) < CurrentOrderView.NUM_ROWS:
            for i_row in range((y + 1), CurrentOrderView.NUM_ROWS):
                empty_tile = Frame(self, background=self._background)
                empty_tile.grid(
                    row=i_row,
                    column=0,
                    columnspan=CurrentOrderView.NUM_COLUMNS,
                    padx=15, pady=15,
                    sticky='nsew'
                )

                self.grid_columnconfigure(0, weight=1)
                self.grid_rowconfigure(i_row, weight=1)

    def hide_view(self):
        if not self._is_hidden:
            self.pack_forget()
            self._is_hidden = True

    def show_view(self):
        if self._is_hidden:
            self.pack(side=TOP, expand=1, fill='both')
            self._is_hidden = False
