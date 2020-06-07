from tkinter import *
from tkinter import font as tkFont
from functools import partial
import Templates.references as REFS
import numpy as np
import math


class MealDetailsView(Frame):
    BUTTON_DEFAULT_BACKGROUND = None
    BUTTON_INGR_BACKGROUND = '#FF9B9B'
    BUTTON_ADON_BACKGROUND = '#BBFF9E'
    BUTTON_SIZE_BACKGROUND = '#B7EDFF'
    BUTTON_INACTIVE_FOREGROUND = '#606060'

    SEPARATOR_WIDTH = 10

    def __init__(self, parent, background, shown: bool = False):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

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

        largefont = tkFont.Font(family="Helvetica", size=42, weight='bold')

        self._title = Label(
            master=self,
            text="<title>",
            font=largefont,
            background=background
        )
        self._title.pack(side=TOP, padx=5, pady=(5, 0), fill='x')

        self._frame_ingredients = Frame(
            master=self,
            background=background,
        )
        self._frame_ingredients.pack(
            side=LEFT, padx=5, pady=5, fill='both', expand=1)

        # SEPARATOR
        Frame(
            master=self,
            background='#323232',
            width=MealDetailsView.SEPARATOR_WIDTH
        ).pack(side=LEFT, fill='y')

        self._frame_addons = Frame(
            master=self,
            background=background
        )
        self._frame_addons.pack(
            side=LEFT, padx=5, pady=5, fill='both', expand=1)

        # SEPARATOR
        Frame(
            master=self,
            background='#323232',
            width=MealDetailsView.SEPARATOR_WIDTH
        ).pack(side=LEFT, fill='y')

        self._frame_sizes = Frame(
            master=self,
            background='red'#,#background
            # width=500
        )
        self._frame_sizes.pack(side=LEFT, padx=5, pady=5,
                               fill='both')

        self._ingredients_states = []
        self._addons_states = []
        self._sizes_states = []

    @property
    def title(self) -> str:
        return self._title.cget("text")

    @property
    def is_shown(self) -> bool:
        return not self._is_hidden

    def update_content(self, meal, expand_title: bool = False):
        for child in self._frame_ingredients.winfo_children():
            child.destroy()

        for child in self._frame_addons.winfo_children():
            child.destroy()

        for child in self._frame_sizes.winfo_children():
            child.destroy()

        meal_last_category = meal.category[len(meal.category) - 1]

        if expand_title:
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
            self._sizes_states[0] = 1

        self._fill_frame(self._frame_ingredients,
                         meal.ingredients,
                         self._clicked_ingredients_button
                         )

        self._fill_frame(self._frame_addons,
                         meal.addons,
                         self._clicked_addon_button,
                         MealDetailsView.BUTTON_INACTIVE_FOREGROUND
                         )

        self._fill_frame(self._frame_sizes,
                         meal.sizes,
                         self._clicked_size_button,
                         MealDetailsView.BUTTON_INACTIVE_FOREGROUND,
                         cols=1
                         )
        self._update_size_buttons()

    def _fill_frame(self,
                    container: Frame,
                    button_contents: [],
                    buttonCommand,
                    default_button_foreground: str = '#000000',
                    cols=3, rows=3, no_propagate: bool = True):
        NUM_COLUMNS = cols  # Minimum number of columns
        NUM_ROWS = rows    # Minimum number of rows

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
            container_tile.pack(padx=5, pady=(0, 5), side=LEFT,
                                fill="both", expand=1)
            container_tile.pack_propagate(0)
            container_tile.update()

            foreground = default_button_foreground
            largefont = ("Helvetica", "21", "bold")

            tile_button = Button(container_tile,
                                 text=content,
                                 foreground=foreground,
                                 font=largefont
                                 )
            tile_button.pack(fill="both", expand=1)
            tile_button.config(command=partial(buttonCommand,
                                               tile_button,
                                               idx))

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
                empty_tile.pack(padx=5, pady=(0, 5), side=LEFT,
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
                empty_tile.pack(padx=5, pady=(0, 5), side=LEFT,
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

    def _clicked_size_button(self, button: Button, index: int):
        if index >= len(self._sizes_states):
            return

        self._sizes_states.fill(0)
        self._sizes_states[index] = 1

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
                            child.config(foreground=MealDetailsView.BUTTON_INACTIVE_FOREGROUND,
                                         background=MealDetailsView.BUTTON_DEFAULT_BACKGROUND)

    def hide_view(self):
        if not self._is_hidden:
            self.pack_forget()
            self._is_hidden = True

    def show_view(self):
        if self._is_hidden:
            self.pack(side=TOP, expand=1, fill='both')
            self._is_hidden = False
