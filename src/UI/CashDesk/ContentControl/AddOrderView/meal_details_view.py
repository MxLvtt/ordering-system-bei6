from tkinter import *
from tkinter import font as tkFont
from functools import partial
from Templates.fonts import Fonts
import Templates.references as REFS
import numpy as np
import math


class MealDetailsView(Frame):
    BUTTON_DEFAULT_BACKGROUND = None
    BUTTON_INGR_BACKGROUND = REFS.LIGHTEST_RED
    BUTTON_ADON_BACKGROUND = REFS.LIGHTEST_GREEN
    BUTTON_SIZE_BACKGROUND = REFS.LIGHT_CYAN
    BUTTON_INACTIVE_FOREGROUND = '#606060'
    BUTTON_FONT_SIZE = '20'

    SEPARATOR_WIDTH = 10
    SEPARATOR_COLOR = '#696969'  # '#525252'

    SIZES_FRAME_WIDTH_SMALL = 150
    SIZES_FRAME_WIDTH_LARGE = 250

    SIZES_FRAME_WIDTH = SIZES_FRAME_WIDTH_LARGE

    def __init__(self, parent, background, shown: bool = False):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        if REFS.MOBILE:
            MealDetailsView.SEPARATOR_WIDTH = 3
            MealDetailsView.SIZES_FRAME_WIDTH = MealDetailsView.SIZES_FRAME_WIDTH_SMALL

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

        # TITLE LABEL
        self._title = Label(
            master=self,
            text="<title>",
            font=Fonts.xxxxxlarge(bold=True),
            background=background
        )
        self._title.grid(row=0, columnspan=3, sticky='nsew', pady=(10, 10))

        # PRICE LABEL
        self._price = Label(
            master=self,
            text='<price>',
            font=Fonts.xxxlarge(bold=True, italic=True),
            background=background
        )
        self._price.grid(row=0, column=4, sticky='nsew', pady=(10, 10))

        # HORIZONTAL SEPARATOR
        Frame(
            master=self,
            background=MealDetailsView.SEPARATOR_COLOR,
            height=MealDetailsView.SEPARATOR_WIDTH
        ).grid(row=1, column=0, columnspan=5, sticky='nsew')

        # ZUTATEN LABEL
        self._ingredients_label = Label(
            master=self,
            text=REFS.INGREDIENTS_LABEL,
            font=Fonts.xxxlarge(bold=True, italic=True),
            background=background
        )
        self._ingredients_label.grid(
            row=2, column=0, sticky='nsew', pady=(10, 0))

        # EXTRAS LABEL
        self._extras_label = Label(
            master=self,
            text=REFS.ADDONS_LABEL,
            font=Fonts.xxxlarge(bold=True, italic=True),
            background=background
        )
        self._extras_label.grid(row=2, column=2, sticky='nsew', pady=(10, 0))

        # SIZES LABEL
        self._sizes_label = Label(
            master=self,
            text=REFS.SIZES_LABEL,
            font=Fonts.xxxlarge(bold=True, italic=True),
            background=background
        )
        self._sizes_label.grid(row=2, column=4, sticky='nsew', pady=(10, 0))

        # ZUTATEN BUTTONS FRAME
        self._frame_ingredients = Frame(
            master=self,
            background=background
        )
        self._frame_ingredients.grid(row=3, column=0, sticky='nsew')

        # VERTICAL LEFT SEPARATOR
        Frame(
            master=self,
            background=MealDetailsView.SEPARATOR_COLOR,
            width=MealDetailsView.SEPARATOR_WIDTH
        ).grid(row=2, rowspan=2, column=1, sticky='nsew')

        # EXTRAS BUTTONS FRAME
        self._frame_addons = Frame(
            master=self,
            background=background
        )
        self._frame_addons.grid(row=3, column=2, sticky='nsew')

        # VERTICAL RIGHT SEPARATOR
        Frame(
            master=self,
            background=MealDetailsView.SEPARATOR_COLOR,
            width=MealDetailsView.SEPARATOR_WIDTH
        ).grid(row=2, rowspan=2, column=3, sticky='nsew')

        # GROESSEN BUTTONS FRAME
        self._frame_sizes = Frame(
            master=self,
            background=background,
            width=MealDetailsView.SIZES_FRAME_WIDTH
        )
        self._frame_sizes.grid(row=3, column=4, sticky='nsew')
        self._frame_sizes.pack_propagate(0)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)

        self._ingredients_states = []   # state: 1 = Included, 0 = Excluded
        self._addons_states = []        # state: 1 = Added, 0 = Left Out
        self._sizes_states = []         # state: 1 = Selected, 0 = Not Selected
        self._opened_meal = None
        self._adapted_meal = None

    @property
    def title(self) -> str:
        return self._title.cget("text")

    @property
    def is_shown(self) -> bool:
        return not self._is_hidden

    @property
    def opened_meal(self):
        return self._opened_meal

    def get_adapted_meal(self):
        if self.opened_meal == None or \
                len(self.opened_meal.ingredients) != len(self._ingredients_states) or \
                len(self.opened_meal.addons) != len(self._addons_states) or \
                len(self.opened_meal.sizes) != len(self._sizes_states):
            print("Error while trying to adapt the meal in MealDetailsView!")
            return None

        meal_copy = self.opened_meal.copy()
        meal_copy.ingredients.clear()
        meal_copy.addons.clear()
        meal_copy.sizes.clear()

        for idx, i_state in enumerate(self._ingredients_states):
            if i_state == 0:
                meal_copy.ingredients.append(self._opened_meal.ingredients[idx])

        for idx, a_state in enumerate(self._addons_states):
            if a_state == 1:
                meal_copy.addons.append(self._opened_meal.addons[idx])

        for idx, s_state in enumerate(self._sizes_states):
            if s_state == 1:
                meal_copy.sizes.append(self._opened_meal.sizes[idx])

        self._adapted_meal = meal_copy

        return meal_copy

    def update_content(self, meal, expand_title: bool = False):
        self._opened_meal = meal
        self._total_price = meal.price

        for child in self._frame_ingredients.winfo_children():
            child.destroy()

        for child in self._frame_addons.winfo_children():
            child.destroy()

        for child in self._frame_sizes.winfo_children():
            child.destroy()

        if expand_title and len(meal.category) > 0:
            meal_last_category = meal.category[len(meal.category) - 1]
            self._title.config(text=f"{meal_last_category} > {meal.name}")
        else:
            self._title.config(text=meal.name)

        self._ingredients_states = np.arange(len(meal.ingredients))
        self._ingredients_states.fill(1)
        self._addons_states = np.arange(len(meal.addons))
        self._addons_states.fill(0)
        self._sizes_states = np.arange(len(meal.sizes))
        self._sizes_states.fill(0)

        if len(meal.sizes) > 0:
            found = False
            for index, size_obj in enumerate(meal.size_objects):
                if not found:
                    if size_obj.price == 0.0 or size_obj.price == meal.price:
                        self._sizes_states[index] = 1
                        found = True

        ingredient_content = self._get_button_text(meal.ingredient_objects)

        # Creating ingredient buttons
        self._fill_frame(self._frame_ingredients,
                         ingredient_content,
                         self._clicked_ingredients_button
                         )

        addon_content = self._get_button_text(meal.addon_objects)

        # Creating addon buttons
        self._fill_frame(self._frame_addons,
                         addon_content,
                         self._clicked_addon_button,
                         MealDetailsView.BUTTON_INACTIVE_FOREGROUND
                         )

        size_content = self._get_button_text(meal.size_objects)

        # Creating size buttons
        self._fill_frame(self._frame_sizes,
                         size_content,
                         self._clicked_size_button,
                         #  MealDetailsView.BUTTON_INACTIVE_FOREGROUND,
                         cols=1
                         )

        self._update_size_buttons()
        self._calculate_total_price()

    def _get_button_text(self, name_price_pair_array, show_zero: bool = False) -> []:
        content = []
        separator = '\n' # ' '
        
        for pair in name_price_pair_array:
            if not show_zero and pair.price == 0.0:
                content.append(f"{pair.name}")
            else:
                content.append(f"{pair.name}{separator}{pair.price_str}{REFS.CURRENCY}")

        return content

    def _fill_frame(self,
                    container: Frame,
                    button_contents: [],
                    buttonCommand,
                    default_button_foreground: str = '#000000',
                    cols=3, rows=3):
        pad_size = (not REFS.MOBILE) * 5

        NUM_COLUMNS = cols  # Minimum number of columns
        NUM_ROWS = rows     # Minimum number of rows

        tile_buttons = []

        for idx, content in enumerate(button_contents):
            x = idx % NUM_COLUMNS
            y = int(idx / NUM_COLUMNS)

            if x == 0:
                self.row_container = Frame(
                    container, background=self._background)

                paddingy = (0, 5)
                if y == 0:
                    paddingy = (10, 5)

                self.row_container.pack(
                    padx=5, pady=paddingy, side=TOP, fill="both", expand=1)

            container_tile = Frame(self.row_container,
                                   background=self._background, borderwidth=2)
            container_tile.pack(padx=pad_size, pady=(0, pad_size), side=LEFT,
                                fill="both", expand=1)
            container_tile.pack_propagate(0)
            container_tile.update()

            foreground = default_button_foreground

            wrap_length = 100 + (not REFS.MOBILE) * 120

            tile_button = Button(container_tile,
                                 text=content,
                                 foreground=foreground,
                                 font=Fonts.medium(bold=True),
                                 wraplength=wrap_length
                                 )
            tile_button.pack(fill="both", expand=1)
            tile_button.config(command=partial(buttonCommand,
                                               tile_button,
                                               idx))
            
            tile_buttons.append(tile_button)

            if MealDetailsView.BUTTON_DEFAULT_BACKGROUND == None:
                MealDetailsView.BUTTON_DEFAULT_BACKGROUND = tile_button.cget(
                    'background')

        # -- Fill last row with empty space -- #

        rest = len(button_contents) % NUM_COLUMNS

        if rest != 0:
            empty = NUM_COLUMNS - rest
            for i in range(0, empty):
                empty_tile = Frame(self.row_container,
                                   background=self._background, borderwidth=2)
                empty_tile.pack(padx=pad_size, pady=(0, pad_size), side=LEFT,
                                fill="both", expand=1)

        # -- Fill space with empty rows if necessary -- #

        needed_rows = math.ceil(len(button_contents) / NUM_COLUMNS)

        if needed_rows < NUM_ROWS:
            for i in range(0, (NUM_ROWS - needed_rows)):
                self.empty_row = Frame(container, background=self._background)
                self.empty_row.pack(padx=5, pady=(
                    0, 5), side=TOP, fill="both", expand=1)

                empty_tile = Frame(self.empty_row,
                                   background=self._background, borderwidth=2)
                empty_tile.pack(padx=pad_size, pady=(0, pad_size), side=LEFT,
                                fill="both", expand=1)

    def _clicked_ingredients_button(self, button: Button, index: int):
        if index >= len(self._ingredients_states):
            return

        self._ingredients_states[index] = ~self._ingredients_states[index] & 0x1

        if self._ingredients_states[index] == 1:
            button.config(foreground='#000000',
                          background=MealDetailsView.BUTTON_DEFAULT_BACKGROUND)
        elif self._ingredients_states[index] == 0:
            button.config(foreground=MealDetailsView.BUTTON_INACTIVE_FOREGROUND,
                          background=MealDetailsView.BUTTON_INGR_BACKGROUND)

        self._calculate_total_price()

    def _clicked_addon_button(self, button: Button, index: int):
        if index >= len(self._addons_states):
            return

        self._addons_states[index] = ~self._addons_states[index] & 0x1

        if self._addons_states[index] == 1:
            button.config(foreground='#000000',
                          background=MealDetailsView.BUTTON_ADON_BACKGROUND)
        elif self._addons_states[index] == 0:
            button.config(foreground=MealDetailsView.BUTTON_INACTIVE_FOREGROUND,
                          background=MealDetailsView.BUTTON_DEFAULT_BACKGROUND)

        self._calculate_total_price()

    def _clicked_size_button(self, button: Button, index: int):
        if index >= len(self._sizes_states):
            return

        self._sizes_states.fill(0)
        self._sizes_states[index] = 1

        self._calculate_total_price()
        self._update_size_buttons()

    def _update_size_buttons(self):
        # Go through every child of the "sizes" frame
        for idx, row_frame in enumerate(self._frame_sizes.winfo_children()):
            # These children are (presumably) the row-frames
            for b_container_frame in row_frame.winfo_children():
                # These row-frames contain the frame-containers of the buttons
                for child in b_container_frame.winfo_children():
                    if isinstance(child, Button):
                        if self._sizes_states[idx] == 1:
                            child.config(foreground='#000000',
                                         background=MealDetailsView.BUTTON_SIZE_BACKGROUND)
                        elif self._sizes_states[idx] == 0:
                            child.config(foreground='#000000',
                                         background=MealDetailsView.BUTTON_DEFAULT_BACKGROUND)

    def _calculate_total_price(self, update_view: bool = True):
        self._total_price = self.get_adapted_meal().calculate_whole_price()

        if update_view:
            self._total_price_str = "{:.2f}".format(self._total_price)
            self._price.config(text=f"{self._total_price_str}{REFS.CURRENCY}")

    def hide_view(self):
        if not self._is_hidden:
            self.pack_forget()
            self._is_hidden = True

    def show_view(self):
        if self._is_hidden:
            self.pack(side=TOP, expand=1, fill='both')
            self._is_hidden = False
