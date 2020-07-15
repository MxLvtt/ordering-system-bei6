from tkinter import *
from tkinter import font as tkFont
from functools import partial
from ContentControl.AddOrderView.added_meal_tile import AddedMealTile
from EventHandler.Event import Event
from Templates.radio_button import RadioButton, RadioButtonGroup
import Templates.references as REFS


class CurrentOrderView(Frame):
    NUM_COLUMNS = 4
    NUM_ROWS = 2

    def __init__(self, parent, background, shown: bool = False):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self._meal_number_changed_event: Event = Event()
        self._meal_number_changed_event.add(self._update_price)

        self._meals_frame = Frame(
            master=self,
            background='#F4F4F4'
        )
        self._meals_frame.pack(side=LEFT, fill='both', expand=1)

        self._info_frame = Frame(
            master=self,
            background=background
        )
        self._info_frame.pack(side=RIGHT, fill='y')

        form_radiobutton_group = RadioButtonGroup()

        self._order_form = REFS.DEFAULT_FORM

        def _form_button_pressed(button_form):
            self._order_form = button_form

        for idx, form in enumerate(REFS.ORDER_FORMS):
            command = partial(_form_button_pressed, idx)

            form_radio_button = RadioButton(
                master=self._info_frame,
                text=form,
                group=form_radiobutton_group,
                highlight=REFS.LIGHT_CYAN,
                font=('Helvetica', '18'),
                command=command,
                initial_state=self._order_form,
                height=3
            )
            form_radio_button.pack(side=TOP, fill='x', padx=10, pady=10)

        self._price_label = Label(
            master=self._info_frame,
            text='<price>',
            font=('Helvetica', '18'),
            background=background
        )
        self._price_label.pack(side=BOTTOM, fill='x', padx=10, pady=10)

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
        self._update_price()

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

    def _update_price(self):
        _price: float = 0.0
        for meal_tile in self._added_meal_tiles:
            _price = _price + meal_tile.meal.calculate_whole_price()
        _price_str = "{:.2f}".format(_price)

        self._price_label.config(text=f"{_price_str}{REFS.CURRENCY}")

    def add_meal(self, adapted_meal):
        """ Adds the adapted (!) meal object to the current order
        """
        added_meal = AddedMealTile(
            parent=self._meals_frame,
            meal=adapted_meal,
            index=len(self._added_meal_tiles),
            remove_meal_cb=self.remove_meal,
            on_amount_changed_cb=self._update_price
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
        for child in self._meals_frame.winfo_children():
            if not isinstance(child, AddedMealTile):
                child.destroy()

        x = 0
        y = 0

        for idx, meal_tile in enumerate(self._added_meal_tiles):
            x = idx % CurrentOrderView.NUM_COLUMNS
            y = int(idx / CurrentOrderView.NUM_COLUMNS)

            self._meals_frame.grid_columnconfigure(x, weight=1)
            self._meals_frame.grid_rowconfigure(y, weight=1)

            meal_tile.set_position(row=y, column=x)

        # -- Fill last row with empty space -- #

        needed_cols = len(self._added_meal_tiles) % CurrentOrderView.NUM_COLUMNS

        if needed_cols != 0:
            empty = CurrentOrderView.NUM_COLUMNS - needed_cols
            for i in range(0, empty):
                col = (i+x+1)

                empty_tile = Frame(
                    master=self._meals_frame,
                    background='#F4F4F4'
                )
                empty_tile.grid(row=y, column=col, padx=15, pady=15, sticky='nsew')

                self._meals_frame.grid_columnconfigure(col, weight=1)

        # -- Fill space with empty rows if necessary -- #

        if (y + 1) < CurrentOrderView.NUM_ROWS:
            for i_row in range((y + 1), CurrentOrderView.NUM_ROWS):
                empty_tile = Frame(
                    master=self._meals_frame,
                    background='#F4F4F4'
                )
                empty_tile.grid(
                    row=i_row,
                    column=0,
                    columnspan=CurrentOrderView.NUM_COLUMNS,
                    padx=15, pady=15,
                    sticky='nsew'
                )

                self._meals_frame.grid_columnconfigure(0, weight=1)
                self._meals_frame.grid_rowconfigure(i_row, weight=1)

    def hide_view(self):
        if not self._is_hidden:
            self.pack_forget()
            self._is_hidden = True

    def show_view(self):
        if self._is_hidden:
            self.pack(side=TOP, expand=1, fill='both')
            self._is_hidden = False
