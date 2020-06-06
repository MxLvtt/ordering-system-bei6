from tkinter import *
from tkinter import font as tkFont
import Templates.references as REFS

class MealDetailsView(Frame):
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
            background=background,
            padx=10
        )
        self._title.pack(side=TOP)

    @property
    def title(self) -> str:
        return self._title.cget("text")

    @property
    def is_shown(self) -> bool:
        return not self._is_hidden

    def update_content(self, meal, db_column_names, expand_title: bool = False):
        meal_category = meal.database_content[db_column_names.index(
            REFS.MEALS_TABLE_KATEGORIE_COLUMN)]
        meal_name = meal.database_content[db_column_names.index(
            REFS.MEALS_TABLE_NAME_COLUMN)]

        _cats = meal_category.split("/")
        meal_last_category = _cats[len(_cats) - 1]

        if expand_title:
            self._title.config(text=f"{meal_last_category} > {meal_name}")
        else:
            self._title.config(text=meal_name)

        # TODO

    def hide_view(self):
        if not self._is_hidden:
            self.pack_forget()
            self._is_hidden = True

    def show_view(self):
        if self._is_hidden:
            self.pack(side=TOP, expand=1, fill='both')
            self._is_hidden = False
