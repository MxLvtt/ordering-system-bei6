from functools import partial
from tkinter import *
from ContentControl.history_view import HistoryView, HistoryItem
from Services.meals_service import MealsService
from Templates.fonts import Fonts
from Templates.cbutton import CButton
from Templates.scroll_list import ScrollList, Scrollable
from EventHandler.Event import Event
from Templates.images import IMAGES
import Templates.references as REFS


class MealsSettingsView(Frame):
    INDEX_WIDTH = 4
    CATEGORY_WIDTH = 10 # 32
    NAME_WIDTH = 32
    PRICE_WIDTH = 8

    EDIT_HEADER_WIDTH = 0
    DELETE_HEADER_WIDTH = 0

    PADDING = 30

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

        if REFS.MOBILE:
            MealsSettingsView.PADDING = 15

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
            font=Fonts.xsmall(),
            width=MealsSettingsView.INDEX_WIDTH
        )
        self.index_head.pack(side=LEFT, padx=MealsSettingsView.PADDING)

        self.category_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.MEALS_TABLE_KATEGORIE_COLUMN.capitalize(),
            font=Fonts.xsmall(),
            width=MealsSettingsView.CATEGORY_WIDTH
        )
        self.category_head.pack(side=LEFT, padx=MealsSettingsView.PADDING)

        self.name_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.MEALS_TABLE_NAME_COLUMN.capitalize(),
            font=Fonts.xsmall(bold=True),
            width=MealsSettingsView.NAME_WIDTH
        )
        self.name_head.pack(side=LEFT, padx=MealsSettingsView.PADDING)

        self.delete_head = Label(
            master=self.header,
            background=header_bg,
            # text=REFS.HISTORY_TABLE_EXPAND,
            font=Fonts.xsmall(),
            width=4
        )
        self.delete_head.pack(side=RIGHT, padx=MealsSettingsView.PADDING)
        self.delete_head.update()

        MealsSettingsView.DELETE_HEADER_WIDTH = self.delete_head.winfo_reqwidth()

        self.edit_head = Label(
            master=self.header,
            background=header_bg,
            # text=REFS.HISTORY_TABLE_EDIT,
            font=Fonts.xsmall(),
            width=4
        )
        self.edit_head.pack(side=RIGHT, padx=(MealsSettingsView.PADDING,0))
        self.edit_head.update()

        MealsSettingsView.EDIT_HEADER_WIDTH = self.edit_head.winfo_reqwidth()
        
        self.expand_head = Label(
            master=self.header,
            background=header_bg,
            # text=REFS.HISTORY_TABLE_EXPAND,
            font=Fonts.xsmall(),
            width=4
        )
        self.expand_head.pack(side=RIGHT, padx=(MealsSettingsView.PADDING,0))
        self.expand_head.update()

        MealsSettingsView.EXPAND_HEADER_WIDTH = self.expand_head.winfo_reqwidth()

        self.base_price_head = Label(
            master=self.header,
            background=header_bg,
            text=REFS.MEALS_BASE_PRICE.capitalize(),
            font=Fonts.xsmall(),
            width=MealsSettingsView.PRICE_WIDTH
        )
        self.base_price_head.pack(side=RIGHT, padx=MealsSettingsView.PADDING)

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

        add_row = AddMealItem(parent=self.scrolllist)
        add_row.meal_added_event.add(self.update_view)
        self.scrolllist.add_row(add_row, update=False)

        for idx,meal in enumerate(self.meal_items):
            element = MealItem(parent=self.scrolllist, meal=meal, index=(idx+1))
            element.meal_deleted_event.add(self.update_view)
            self.scrolllist.add_row(element, update=False)

        self.scrolllist.update_view()









class MealItem(Scrollable):
    def __init__(self, parent, meal, index, background='white'):
        super().__init__(
            parent=parent,
            height=HistoryItem.HEIGHT,
            background=background#'#F4F4F4'
        )

        self.meal = meal
        self.meal_deleted_event: Event = Event()

        self.expanded = False
        self.edit_view_shown = False
        self.details_view_shown = False

        self.row_frame = Frame(
            master=self,
            background=background,
            height=HistoryItem.HEIGHT
        )
        self.row_frame.pack(side=TOP, fill='x')
        self.row_frame.pack_propagate(0)

        self.details_frame = Frame(
            master=self,
            background='#F4F4F4'
        )

        self.set_details_content()

        self._edit_img = IMAGES.create(IMAGES.EDIT)
        self._check_img = IMAGES.create(IMAGES.CHECK_MARK)
        self._trashcan_img = IMAGES.create(IMAGES.TRASH_CAN_LIGHT)
        self._down_img = IMAGES.create(IMAGES.DOWN)
        self._up_img = IMAGES.create(IMAGES.UP)

        self.index = Label(
            master=self.row_frame,
            text=f"{index}",
            font=Fonts.xsmall(),
            background=background,
            width=MealsSettingsView.INDEX_WIDTH
        )
        self.index.pack(side=LEFT, padx=MealsSettingsView.PADDING)
        
        self.category = Label(
            master=self.row_frame,
            text=meal.category_raw,
            font=Fonts.xsmall(),
            background=background,
            width=MealsSettingsView.CATEGORY_WIDTH
        )
        self.category.pack(side=LEFT, padx=MealsSettingsView.PADDING)
        
        self.name = Label(
            master=self.row_frame,
            text=meal.name,
            font=Fonts.xsmall(bold=True),
            background=background,
            width=MealsSettingsView.NAME_WIDTH
        )
        self.name.pack(side=LEFT, padx=MealsSettingsView.PADDING)
        
        ##### DELETE BUTTON #####

        self.delete_container = Frame(
            master=self.row_frame,
            width=MealsSettingsView.DELETE_HEADER_WIDTH,
            height=60,
            bg=background
        )
        self.delete_container.pack(side=RIGHT, padx=MealsSettingsView.PADDING)

        self.delete = Button(
            master=self.delete_container,
            image=self._trashcan_img,
            command=self.delete_meal_command,
            background=CButton.DARK_RED
        )
        self.delete.place(relx=0.5, rely=0.5, anchor="center")

        ##### EDIT BUTTON #####

        self.edit_container = Frame(
            master=self.row_frame,
            width=MealsSettingsView.EDIT_HEADER_WIDTH,
            height=60,
            bg=background
        )
        self.edit_container.pack(side=RIGHT, padx=(MealsSettingsView.PADDING,0))

        self.edit = Button(
            master=self.edit_container,
            image=self._edit_img,
            command=None#self.edit_order_command
        )
        self.edit.place(relx=0.5, rely=0.5, anchor="center")
        self.edit.config(state="disabled")

        # self.initial_button_background = self.edit.cget('background')

        # if self._order.state != REFS.OPEN and self._order.state != REFS.CHANGED:
        #     self.edit.config(state="disabled")

        ##### EXPAND BUTTON #####

        self.expand_container = Frame(
            master=self.row_frame,
            width=MealsSettingsView.EXPAND_HEADER_WIDTH,
            height=60,
            bg=background
        )
        self.expand_container.pack(side=RIGHT, padx=(MealsSettingsView.PADDING,0))

        self.expand = Button(
            master=self.expand_container,
            image=self._down_img,
            command=self.expand_button_command
        )
        self.expand.place(relx=0.5, rely=0.5, anchor="center")
        self.expand.config(state="disabled")

        ##### BASE PRICE #####

        self.base_price_head = Label(
            master=self.row_frame,
            text=f"{meal.price_str}{REFS.CURRENCY}",
            font=Fonts.xsmall(),
            background=background,
            width=MealsSettingsView.PRICE_WIDTH
        )
        self.base_price_head.pack(side=RIGHT, padx=MealsSettingsView.PADDING)

    def delete_meal_command(self):
        confirmed = False

        condition = f"{REFS.MEALS_TABLE_NAME_COLUMN}='{self.meal.name}'"
        # AND " \ f"{REFS.MEALS_TABLE_KATEGORIE_COLUMN}='{self.meal.category_raw}'"
        
        try:
            confirmed = MealsService.delete_from_table(
                condition=condition,
                confirm=True)
        except:
            pass

        if confirmed:
            self.meal_deleted_event()

    def expand_button_command(self):
        def _open_details_view():
            # Show meals view
            self.details_frame.pack(side=TOP)
            self.details_frame.update()
            # Adapt the expand button
            self.expand.config(image=self._up_img)

            self.details_view_shown = True
            self.expanded = True

            # Calculate the content's height
            self.height = self.details_frame.winfo_reqheight() + self.initial_height

        def _close_details_view():
            # Hide meals view
            self.details_frame.pack_forget()
            # Reset expand button style
            self.expand.config(image=self._down_img)

            self.details_view_shown = False
            self.expanded = False
            self.height = self.initial_height

        # Item is not expanded
        if not self.expanded:
            _open_details_view()
        # Item is already expanded
        else:
            _close_details_view()

    def set_details_content(self):
        """ Defines the content to be shown in the details_frame.
        """
        bg = 'white'

        containers = []

        test_label = Label(
            master=self.details_frame,
            text="This is a test :)",
            background=bg
        )
        test_label.pack(side=LEFT, padx=20, pady=20)
        test_label.update()

        # for meal in meals:
        #     meal_container = Frame(
        #         master=self.meals_frame,
        #         background=bg
        #     )
        #     meal_container.pack(side=LEFT, padx=20, pady=20)

        #     containers.append(meal_container)

        #     (meal_title, meal_text) = MealsService.meal_content_to_text(meal)

        #     # amount_text = ""
        #     # if meal.amount > 1:
        #     #     amount_text = f"{meal.amount}x "
            
        #     # meal_title = f"{amount_text}{meal.name}"
        #     # if len(meal.sizes) != 0 and meal.sizes[0] != '':
        #     #     meal_title = f"{meal_title} ({meal.sizes[0]})"

        #     meal_title_label = Label(
        #         master=meal_container,
        #         text=meal_title,
        #         background=bg,
        #         font=Fonts.large(bold=True),
        #         justify='left',
        #         anchor='nw'
        #     )
        #     meal_title_label.pack(side=TOP, fill='x', padx=10, pady=10)

        #     if meal_text != "":
        #         # Label that contains the list of ingredients and addons of this meal
        #         meal_ingredients_label = Label(
        #             master=meal_container,
        #             text=meal_text,
        #             font=Fonts.xsmall(),
        #             background=bg,
        #             anchor='w',
        #             justify='left'
        #         )
        #         meal_ingredients_label.pack(side=TOP, fill='x', padx=10, pady=(0,10))

        #     meal_container.update()



class AddMealItem(Scrollable):
    def __init__(self, parent, background='white'):
        super().__init__(
            parent=parent,
            height=HistoryItem.HEIGHT,
            background=background#'#F4F4F4'
        )

        self.meal_added_event: Event = Event()

        self.expanded = False
        self.edit_view_shown = False
        self.details_view_shown = False

        self.row_frame = Frame(
            master=self,
            background=background,
            height=HistoryItem.HEIGHT
        )
        self.row_frame.pack(side=TOP, fill='x')
        self.row_frame.pack_propagate(0)

        self.details_frame = Frame(
            master=self,
            background='#F4F4F4'
        )
        self.set_details_content()

        self._undo_img = IMAGES.create(IMAGES.UNDO)
        self._add_img = IMAGES.create(IMAGES.ADD)
        self._down_img = IMAGES.create(IMAGES.DOWN)
        self._up_img = IMAGES.create(IMAGES.UP)

        self.index = Label(
            master=self.row_frame,
            font=Fonts.xsmall(),
            text="",
            background=background,
            width=MealsSettingsView.INDEX_WIDTH
        )
        self.index.pack(side=LEFT, padx=MealsSettingsView.PADDING)
        
        self.category = Text(
            master=self.row_frame,
            font=Fonts.xsmall(),
            background=background,
            width=MealsSettingsView.CATEGORY_WIDTH,
            height=1
        )
        self.category.pack(side=LEFT, padx=MealsSettingsView.PADDING)
        
        self.name = Text(
            master=self.row_frame,
            font=Fonts.xsmall(bold=True),
            background=background,
            width=MealsSettingsView.NAME_WIDTH+3,
            height=1
        )
        self.name.pack(side=LEFT, padx=MealsSettingsView.PADDING)
        self.name_bg = self.name.cget('background')
        
        ##### ADD BUTTON #####

        self.add_container = Frame(
            master=self.row_frame,
            width=MealsSettingsView.DELETE_HEADER_WIDTH,
            height=60,
            bg=background
        )
        self.add_container.pack(side=RIGHT, padx=MealsSettingsView.PADDING)

        self.add = Button(
            master=self.add_container,
            image=self._add_img,
            command=self.add_meal_command,
            background=CButton.GREEN
        )
        self.add.place(relx=0.5, rely=0.5, anchor="center")

        ##### UNDO BUTTON #####

        self.undo_container = Frame(
            master=self.row_frame,
            width=MealsSettingsView.EDIT_HEADER_WIDTH,
            height=60,
            bg=background
        )
        self.undo_container.pack(side=RIGHT, padx=(MealsSettingsView.PADDING,0))

        self.undo = Button(
            master=self.undo_container,
            image=self._undo_img,
            command=self.undo_command
        )
        self.undo.place(relx=0.5, rely=0.5, anchor="center")

        # self.initial_button_background = self.edit.cget('background')

        # if self._order.state != REFS.OPEN and self._order.state != REFS.CHANGED:
        #     self.edit.config(state="disabled")

        ##### EXPAND BUTTON #####

        self.expand_container = Frame(
            master=self.row_frame,
            width=MealsSettingsView.EXPAND_HEADER_WIDTH,
            height=60,
            bg=background
        )
        self.expand_container.pack(side=RIGHT, padx=(MealsSettingsView.PADDING,0))

        # self.expand = Button(
        #     master=self.expand_container,
        #     image=self._down_img,
        #     command=self.expand_button_command
        # )
        # self.expand.place(relx=0.5, rely=0.5, anchor="center")

        ##### BASE PRICE #####

        self.base_price = Text(
            master=self.row_frame,
            font=Fonts.xsmall(),
            background=background,
            width=MealsSettingsView.PRICE_WIDTH,
            height=1
        )
        self.base_price.pack(side=RIGHT, padx=MealsSettingsView.PADDING)
        self.base_price_bg = self.base_price.cget('background')
    
    def expand_button_command(self):
        def _open_details_view():
            # Show meals view
            self.details_frame.pack(side=TOP)
            self.details_frame.update()
            # Adapt the expand button
            self.expand.config(image=self._up_img)

            self.details_view_shown = True
            self.expanded = True

            # Calculate the content's height
            self.height = self.details_frame.winfo_reqheight() + self.initial_height

        def _close_details_view():
            # Hide meals view
            self.details_frame.pack_forget()
            # Reset expand button style
            self.expand.config(image=self._down_img)

            self.details_view_shown = False
            self.expanded = False
            self.height = self.initial_height

        # Item is not expanded
        if not self.expanded:
            _open_details_view()
        # Item is already expanded
        else:
            _close_details_view()

    def undo_command(self):
        self.category.delete(1.0, END)
        self.name.delete(1.0, END)
        self.base_price.delete(1.0, END)

        # TODO: clear ingredients, addons, sizes

    def add_meal_command(self):
        raw_cat = self.category.get(1.0, END).strip()
        raw_name = self.name.get(1.0, END).strip()
        raw_price = self.base_price.get(1.0, END).strip()
        price = 0.0

        if raw_name == "":
            self.name.config(background=REFS.LIGHT_RED)
            return
        else:
            self.name.config(background=self.name_bg)

        if raw_price != "":
            if REFS.CURRENCY in raw_price:
                raw_price = raw_price.replace(REFS.CURRENCY, "")
            
            try:
                price = float(raw_price)
                self.base_price.config(background=self.base_price_bg)
            except:
                self.base_price.config(background=REFS.LIGHT_RED)
                return

        MealsService.create_new_meal(
            category = raw_cat,
            name = raw_name,
            base_price = price,
            ingredients = [],   # TODO
            addons = [],        # TODO
            sizes = [])         # TODO

        self.meal_added_event()

        # confirmed = False

        # condition = f"{REFS.MEALS_TABLE_NAME_COLUMN}='{self.meal.name}' AND " \
        #     f"{REFS.MEALS_TABLE_KATEGORIE_COLUMN}='{self.meal.category_raw}'"
        
        # try:
        #     confirmed = MealsService.delete_from_table(
        #         condition=condition,
        #         confirm=True)
        # except:
        #     pass

        # if confirmed:
        #     self.meal_deleted_event()

    def set_details_content(self):
        """ Defines the content to be shown in the details_frame.
        """
        bg = 'white'

        containers = []

        test_label = Label(
            master=self.details_frame,
            text="This is a test :)",
            background=bg
        )
        test_label.pack(side=LEFT, padx=20, pady=20)
        test_label.update()

