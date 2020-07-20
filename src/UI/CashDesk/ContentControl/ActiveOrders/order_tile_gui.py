import Templates.references as REFS
from Templates.scroll_list import ScrollList
from Templates.scrollable import Scrollable
from Templates.meals import Meal
from Templates.order import Order
from Services.orders_service import OrdersService
from Services.meals_service import MealsService
from tkinter import *
from functools import partial
from Templates.fonts import Fonts


class OrderTileGUI(Frame):
    LIGHT_GRAY = REFS.LIGHT_GRAY
    DARK_GRAY = "#ADADA9"

    def __init__(self, parent, order: Order, background="#A2ABAD"):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self._order: Order = order
        # self._order.on_state_changed.add(self._state_changed_cb)

        self._font_S = Fonts.xxxsmall(decrement = 1)
        self._font =  Fonts.xxsmall(decrement = 1)
        self._font_bold = Fonts.xxsmall(bold = True, decrement = 1)

        ### Header

        self._header_container = Frame(
            master=self,
            background=self.LIGHT_GRAY,
            height=30
        )
        self._header_container.pack(side=TOP, fill='x')

        self._id_label = Label(
            master=self._header_container,
            background=self.LIGHT_GRAY,
            font=self._font_bold,
            text="<id>"
        )
        self._id_label.pack(side=LEFT, padx=2, pady=2)

        self._timestamp_label = Label(
            master=self._header_container,
            background=self.LIGHT_GRAY,
            font=self._font,
            text="<timestamp>"
        )
        self._timestamp_label.pack(side=RIGHT, padx=2, pady=2)

        ### Body
        
        self._body_container = Frame(
            master=self,
            background=self.LIGHT_GRAY
        )
        self._body_container.pack(side=TOP, fill='both', expand=1)

        self._meal_labels_frame = Frame(
            master=self._body_container,
            background=self.LIGHT_GRAY
        )
        self._meal_labels_frame.pack(side=TOP, fill='both', expand=1, padx=10, pady=10)

        self._meals_labels = []

        ## Scrollable List

        self.scrolllist = ScrollList(
            parent=self._meal_labels_frame,
            background=REFS.DARK_GRAY,
            spacing=1
        )

        ### Footer

        self._footer_container = Frame(
            master=self,
            background=background,
            height=30
        )
        self._footer_container.pack(side=BOTTOM, fill='x')

        self._form_label = Label(
            master=self._footer_container,
            background=background,
            font=self._font,
            text="<form>"
        )
        self._form_label.pack(side=LEFT, padx=2, pady=2)

        self._state_label = Label(
            master=self._footer_container,
            background=background,
            font=self._font_bold,
            text="<state>"
        )
        self._state_label.pack(side=RIGHT, padx=2, pady=2)
        
        self._update_content()

    @property
    def order(self) -> Order:
        return self._order

    @order.setter
    def order(self, order):
        self._order = order
        self._update_content()

    def empty_tile(self, background='white'):
        self._order = None
        
        self._id_label.config(text="")
        self._timestamp_label.config(text="")
        self._form_label.config(text="")
        self._state_label.config(text="")
        self.scrolllist.remove_all()

        self._meal_labels_frame.pack_forget()

        self.update_colors(
            background_light=background,
            background_dark=background,
            update_text=False
        )

    def _update_content(self):
        if self._order == None:
            return

        timestamp_str = OrdersService.convert_timestamp(self._order.timestamp)

        self._id_label.config(text=f"#{self._order.id}")
        self._timestamp_label.config(text=timestamp_str)
        self._form_label.config(text=REFS.ORDER_FORMS[self._order.form])
        self._state_label.config(text=REFS.ORDER_STATES[self._order.state])

        self._set_meals_list_text()
        self.update_colors(
            background_light=REFS.ORDER_STATE_COLORS[self._order.state],
            background_dark=REFS.ORDER_STATE_COLORS_BGD[self._order.state]
        )

    def _bind_all_childs(self, start_element, func):
        curr = start_element

        for child in curr.winfo_children():
            # Go through every child and repeat the process, except for the scrolllist -> stop there
            if not isinstance(child, ScrollList):
                if isinstance(child, Label) or isinstance(child, Frame):
                    child.bind("<ButtonPress-1>", func)
                self._bind_all_childs(child, func)

    def bind_on_click(self, callback):
        func = partial(callback, self)

        self.scrolllist.set_additional_pressed_event(func)

        self.bind("<ButtonPress-1>", func)

        self._bind_all_childs(start_element=self, func=func)

    def update_colors(self, background_light, background_dark, update_text=True):
        self._header_container.config(background=background_light)
        self._id_label.config(background=background_light)
        self._timestamp_label.config(background=background_light)

        self._body_container.config(background=background_dark)
        self._meal_labels_frame.config(background=background_dark)

        for element in self.scrolllist.Elements:
            element.change_background(background=background_dark)

        self._footer_container.config(background=background_light)
        self._form_label.config(background=background_light)
        self._state_label.config(background=background_light)
        if update_text:
            self._state_label.config(text=REFS.ORDER_STATES[self._order.state])

    def _set_meals_list_text(self):
        self._meal_labels_frame.pack(side=TOP, fill='both', expand=1, padx=10, pady=10)

        self.scrolllist.remove_all()

        meals : [] = self._order.meals
        
        for meal in meals:
            # Create additional text for the ingredients and addons for the meal
            (meal_name_text, meal_text) = MealsService.meal_content_to_text(meal)
            
            meal_list_item = MealListItem(
                parent=self.scrolllist,
                title=meal_name_text,
                text=meal_text,
                font_title=self._font_bold,
                font_text=self._font_S,
                background=self.LIGHT_GRAY
            )

            self.scrolllist.add_row(meal_list_item, update=False)

        self.scrolllist.update_view()
        

class MealListItem(Scrollable):
    def __init__(self, parent, title, text, font_title, font_text, background='white'):
        super().__init__(
            parent=parent,
            height=100,
            background=background
        )

        self._title = title
        self._text = text
        self._font_title = font_title
        self._font_text = font_text

        self.meal_title_label = Label(
            master=self,
            text=title,
            font=font_title,
            background=background,
            anchor='w',
            justify='left'
        )
        self.meal_title_label.pack(side=TOP, fill='x')
        self.meal_title_label_height = self.meal_title_label.winfo_reqheight()

        self.meal_text_label = None
        self.meal_text_label_height = 0

        if text != "":
            self.meal_text_label = Label(
                master=self,
                text=text,
                font=font_text,
                background=background,
                anchor='w',
                justify='left'
            )
            self.meal_text_label.pack(side=TOP, fill='x')
            self.meal_text_label_height = self.meal_text_label.winfo_reqheight()

        self.set_height_anonymously(
            self.meal_title_label_height + self.meal_text_label_height
        )

    def change_background(self, background):
        self.meal_title_label.config(background=background)

        if self.meal_text_label != None:
            self.meal_text_label.config(background=background)
