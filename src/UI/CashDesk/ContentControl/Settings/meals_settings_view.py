from tkinter import *
from ContentControl.history_view import HistoryView, HistoryItem
from Services.meals_service import MealsService
from Templates.scroll_list import ScrollList, Scrollable
import Templates.references as REFS


class MealsSettingsView(Frame):
    def __init__(
        self,
        parent,
        background
    ):
        super().__init__(
            master=parent,
            cnf={},
            background='#696969'
        )

        self.meal_items = []

        ########## HEADER ##########

        header_bg = '#F4F4F4'

        self.header = Frame(
            master=self,
            background=header_bg,
            height=HistoryItem.HEIGHT)
        self.header.pack(side=TOP, fill='x', pady=(0,HistoryView.SPACING))
        self.header.pack_propagate(0)

        self.index_head = Label(
            master=self.header,
            background=header_bg,
            text="#",
            font=HistoryView.FONT_NORMAL,
            width=5
        )
        self.index_head.pack(side=LEFT, padx=30)

        self.category_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.MEALS_TABLE_KATEGORIE_COLUMN.capitalize(),
            font=HistoryView.FONT_NORMAL,
            width=30
        )
        self.category_head.pack(side=LEFT, padx=30)

        self.name_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.MEALS_TABLE_NAME_COLUMN.capitalize(),
            font=HistoryView.FONT_BOLD,
            width=15
        )
        self.name_head.pack(side=LEFT, padx=30)

        self.edit_head = Label(
            master=self.header,
            background=header_bg,
            # text=REFS.HISTORY_TABLE_EDIT,
            font=HistoryView.FONT_NORMAL,
            width=5
        )
        self.edit_head.pack(side=RIGHT, padx=30)
        self.edit_head.update()

        HistoryView.EDIT_HEADER_WIDTH = self.edit_head.winfo_reqwidth()
        
        self.expand_head = Label(
            master=self.header,
            background=header_bg,
            # text=REFS.HISTORY_TABLE_EXPAND,
            font=HistoryView.FONT_NORMAL,
            width=5
        )
        self.expand_head.pack(side=RIGHT, padx=(30,0))
        self.expand_head.update()

        HistoryView.EXPAND_HEADER_WIDTH = self.expand_head.winfo_reqwidth()

        self.base_price_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.MEALS_BASE_PRICE.capitalize(),
            font=HistoryView.FONT_NORMAL,
            width=8
        )
        self.base_price_head.pack(side=RIGHT, padx=30)

        ########## TABLE ##########

        self.table = Frame(master=self, background='#F4F4F4')
        self.table.pack(side=TOP, fill='both', expand=1)

        self.scrolllist = ScrollList(parent=self.table, spacing=HistoryView.SPACING, background='#696969')

    def update_view(self):
        """ Is called, when the view is selected.
        
        Therefore, the content should be updated in that case.
        """
        self.update_view_and_database_content()
        self.scrolllist.reset_scroll()

    def update_view_and_database_content(self):
        # Get all orders from the database sorted by their timestamp
        meals_sorted_by_category = MealsService.get_meal_objects(order_by=f"{REFS.MEALS_TABLE_KATEGORIE_COLUMN} ASC")
        # Safe the result in this class's array
        self.meal_items.clear()
        self.meal_items.extend(meals_sorted_by_category)

        self.refresh_view()

    def refresh_view(self):
        self.scrolllist.remove_all()

        for idx,meal in enumerate(self.meal_items):
            element = MealItem(parent=self.scrolllist, meal=meal, index=(idx+1))
            self.scrolllist.add_row(element, update=False)

        self.scrolllist.update_view()









class MealItem(Scrollable):
    def __init__(self, parent, meal, index, background='white'):
        super().__init__(
            parent=parent,
            height=HistoryItem.HEIGHT,
            background=background#'#F4F4F4'
        )

        self.index = Label(
            master=self,
            text=f"{index}",
            font=HistoryView.FONT_NORMAL,
            background=background,
            width=5
        )
        self.index.pack(side=LEFT, padx=30)
        
        self.category = Label(
            master=self,
            text=meal.category_raw,
            font=HistoryView.FONT_NORMAL,
            background=background,
            width=30
        )
        self.category.pack(side=LEFT, padx=30)
        
        self.name = Label(
            master=self,
            text=meal.name,
            font=HistoryView.FONT_BOLD,
            background=background,
            width=15
        )
        self.name.pack(side=LEFT, padx=30)
        
        ##### EDIT BUTTON #####

        self.edit_container = Frame(
            master=self,
            width=HistoryView.EDIT_HEADER_WIDTH,
            height=60,
            bg=background
        )
        self.edit_container.pack(side=RIGHT, padx=30)

        # self.edit = Button(
        #     master=self.edit_container,
        #     image=self._edit_img,
        #     command=self.edit_order_command
        # )
        # self.edit.place(relx=0.5, rely=0.5, anchor="center")

        # self.initial_button_background = self.edit.cget('background')

        # if self._order.state != REFS.OPEN and self._order.state != REFS.CHANGED:
        #     self.edit.config(state="disabled")

        ##### EXPAND BUTTON #####

        self.expand_container = Frame(
            master=self,
            width=HistoryView.EXPAND_HEADER_WIDTH,
            height=60,
            bg=background
        )
        self.expand_container.pack(side=RIGHT, padx=(30,0))

        # expand_button_cmd = partial(self.expand_button_command, HistoryItem.MEALS_CONTENT_MODE)

        # self.expand = Button(
        #     master=self.expand_container,
        #     image=self._down_img,
        #     command=expand_button_cmd
        # )
        # self.expand.place(relx=0.5, rely=0.5, anchor="center")

        ##### BASE PRICE #####

        self.base_price_head = Label(
            master=self,
            text=f"{meal.price_str}{REFS.CURRENCY}",
            font=HistoryView.FONT_NORMAL,
            background=background,
            width=8
        )
        self.base_price_head.pack(side=RIGHT, padx=30)

