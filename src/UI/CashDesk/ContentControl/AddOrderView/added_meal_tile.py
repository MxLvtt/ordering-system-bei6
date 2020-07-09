from tkinter import *
from functools import partial
from Services.meals_service import MealsService
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

        self.close_img = IMAGES.create(IMAGES.CLOSE)
        self.up_img = IMAGES.create(IMAGES.UP)
        self.down_img = IMAGES.create(IMAGES.DOWN)

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

        self._b_delete = Button(
            master=self._header,
            image=self.close_img,
            command=partial(remove_meal_cb, self),
            width=40, height=40
        )
        self._b_delete.pack(side=RIGHT, padx=(5,0))

        self.body_frame = Frame(
            master=self,
            background=background
        )
        self.body_frame.pack(side=TOP, padx=15, pady=(0,15), fill='both', expand=1)

        self.left_frame = Frame(
            master=self.body_frame,
            background=background
        )
        self.left_frame.pack(side=LEFT, fill='both', expand=1)

        #### Counter buttons

        self.right_frame = Frame(
            master=self.body_frame,
            background=background
        )
        self.right_frame.pack(side=RIGHT, fill='y')

        self._b_count_up = Button(
            master=self.right_frame,
            image=self.up_img,
            command=partial(self.change_amount, +1),
            width=40, height=80
        )
        self._b_count_up.pack(side=TOP, pady=(0,5))

        self._b_count_down = Button(
            master=self.right_frame,
            image=self.down_img,
            command=partial(self.change_amount, -1),
            width=40, height=80
        )
        self._b_count_down.pack(side=TOP)
        self._b_count_down.config(state="disabled")

        #### Setup size

        if len(meal.size_objects) > 0:
            self._l_size = Label(
                master=self.left_frame,
                text=f"GRÖßE:  {meal.size_objects[0].name}",
                background=background,
                foreground='black',
                font=('Helvetica', '12'),
                justify='left'
            )
            self._l_size.pack(side=TOP, padx=15, pady=(0, 15), anchor='nw')

        (meal_title,meal_text) = MealsService.meal_content_to_text(meal, indent="")
        
        self._l_content = Label(
            master=self.left_frame,
            text=meal_text,
            background=background,
            foreground='black',
            font=('Helvetica', '14'),
            justify='left'
        )
        self._l_content.pack(side=TOP, padx=15, pady=(0, 15), anchor='nw')
        
        # #### Setup ingredients list

        # # Only add ingredients, if there are any
        # if len(meal.ingredient_objects) > 0:
        #     self._l_ingredients = Label(
        #         master=self.left_frame,
        #         text='',
        #         background=background,
        #         foreground='black',
        #         font=('Helvetica', '12'),
        #         justify='left'
        #     )
        #     self._l_ingredients.pack(side=TOP, padx=15, pady=(0, 15), anchor='nw')

        #     for idx,ingr in enumerate(meal.ingredients):
        #         curr_text = self._l_ingredients.cget('text')
        #         nl = '\n'
        #         if idx == len(meal.ingredients) - 1:
        #             nl = ''
        #         self._l_ingredients.config(text=f"{curr_text}- OHNE  {ingr}{nl}")

        # #### Setup extras list

        # # Only add extras, if there are any
        # if len(meal.addons) > 0:
        #     self._l_addons = Label(
        #         master=self.left_frame,
        #         text='',
        #         background=background,
        #         foreground='black',
        #         font=('Helvetica', '12'),
        #         justify='left'
        #     )
        #     self._l_addons.pack(side=TOP, padx=15, pady=(0, 15), anchor='nw')

        #     for idx,addon in enumerate(meal.addons):
        #         curr_text = self._l_addons.cget('text')
        #         nl = '\n'
        #         if idx == len(meal.addons) - 1:
        #             nl = ''
        #         self._l_addons.config(text=f"{curr_text}+ MIT  {addon}{nl}")

        self.set_position(0, index)
        
        self.grid_propagate(0)
        self.pack_propagate(0)

    @property
    def meal(self):
        return self._meal

    def set_position(self, row, column):
        self.grid(row=row, column=column, padx=15, pady=15, sticky='nsew')

    def change_amount(self, direction):
        if direction != 1 and direction != -1:
            raise RuntimeError(f"Count direction '{direction}' has an invalid value. Must be +1 or -1.")

        self.meal.amount = self.meal.amount + direction

        if self.meal.amount == 1:
            self._b_count_down.config(state="disabled")
        else:
            self._b_count_down.config(state="normal")

        if self.meal.amount > 1:
            self._l_name.config(text=f"{self.meal.amount}x {self.meal.name}")
        else:
            self._l_name.config(text=f"{self.meal.name}")
