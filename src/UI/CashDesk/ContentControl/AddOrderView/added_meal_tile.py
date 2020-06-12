from tkinter import *
from functools import partial
from Templates.images import IMAGES

class AddedMealTile(Frame):
    def __init__(self, parent, meal, index, remove_meal_cb, background='#F4F4F4'):
        super().__init__(
            master=parent,
            cnf={},
            background=background,
            highlightbackground='#606060',
            highlightthickness=2
        )

        self._meal = meal

        # TODO: Maybe as subheading to the name title we can add the last category of the meal

        #### Setup header

        self._header = Frame(
            master=self,
            background=background
        )
        self._header.pack(side=TOP, padx=15, pady=15, fill='x')

        self._l_name = Label(
            master=self._header,
            text=meal.name,
            background=background,
            foreground='black',
            font=('Helvetica', '20', 'bold')
        )
        self._l_name.pack(side=LEFT, fill='x', expand=1)

        self.close_img = IMAGES.create(IMAGES.CLOSE)

        self._b_delete = Button(
            master=self._header,
            image=self.close_img,
            command=partial(remove_meal_cb, self),
            width=40, height=40
        )
        self._b_delete.pack(side=RIGHT, padx=(5,0))

        #### Setup size

        if len(meal.sizes) > 0:
            self._l_size = Label(
                master=self,
                text=f"GRÖßE:  {meal.sizes[0]}",
                background=background,
                foreground='black',
                font=('Helvetica', '12'),
                justify='left'
            )
            self._l_size.pack(side=TOP, padx=15, pady=(0, 15), anchor='nw')

        #### Setup ingredients list

        # Only add ingredients, if there are any
        if len(meal.ingredients) > 0:
            self._l_ingredients = Label(
                master=self,
                text='',
                background=background,
                foreground='black',
                font=('Helvetica', '12'),
                justify='left'
            )
            self._l_ingredients.pack(side=TOP, padx=15, pady=(0, 15), anchor='nw')

            for idx,ingr in enumerate(meal.ingredients):
                curr_text = self._l_ingredients.cget('text')
                nl = '\n'
                if idx == len(meal.ingredients) - 1:
                    nl = ''
                self._l_ingredients.config(text=f"{curr_text}- OHNE  {ingr}{nl}")

        #### Setup extras list

        # Only add extras, if there are any
        if len(meal.addons) > 0:
            self._l_addons = Label(
                master=self,
                text='',
                background=background,
                foreground='black',
                font=('Helvetica', '12'),
                justify='left'
            )
            self._l_addons.pack(side=TOP, padx=15, pady=(0, 15), anchor='nw')

            for idx,addon in enumerate(meal.addons):
                curr_text = self._l_addons.cget('text')
                nl = '\n'
                if idx == len(meal.addons) - 1:
                    nl = ''
                self._l_addons.config(text=f"{curr_text}+ MIT  {addon}{nl}")

        self.set_position(0, index)
        
        self.grid_propagate(0)
        self.pack_propagate(0)

    @property
    def meal(self):
        return self._meal

    def set_position(self, row, column):
        self.grid(row=row, column=column, padx=15, pady=15, sticky='nsew')
