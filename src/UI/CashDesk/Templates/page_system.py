import math
from functools import partial
from tkinter import *
from Templates.cbutton import CButton
from Templates.images import IMAGES
from Templates.fonts import Fonts
from EventHandler.Event import Event


class PageSystem(Frame):
    NEXT=+1
    PREVIOUS=-1

    PAGE_NUMBERING=0
    ITEM_NUMBERING=1

    def __init__(
        self,
        on_page_changed,
        items_per_page: int,
        numbering_mode: int = 0
    ):
        self.on_page_changed_event : Event = Event()
        self.on_page_changed_event.add(on_page_changed)

        self._current_items = []
        
        self.items_per_page = items_per_page
        self.page_index = 0
        self.max_pages = 1

        self.numbering_mode = numbering_mode

    @property
    def current_items(self) -> []:
        return self._current_items

    def update(self, items_list):
        self._prev_button._disable()
        self._next_button._disable()

        if items_list == None:
            raise RuntimeError("List of items is of Nonetype.")
        
        self.max_pages = math.ceil(len(items_list) / self.items_per_page)

        if self.page_index < self.max_pages - 1:
            self._next_button._enable()
        elif self.page_index == self.max_pages - 1:
            self._next_button._disable()
            
        if self.page_index > 0:
            self._prev_button._enable()
        elif self.page_index == 0:
            self._prev_button._disable()

        lower_index = self.items_per_page * self.page_index
        upper_index = lower_index + self.items_per_page

        # Extract items to be displayed on current page
        self._current_items.clear()
        self._current_items.extend(items_list[lower_index:upper_index])

        label_text = "<current page index>"

        if self.numbering_mode == PageSystem.PAGE_NUMBERING:
            label_text = f"{self.page_index + 1} / {self.max_pages}"
        elif self.numbering_mode == PageSystem.ITEM_NUMBERING:
            upper_bound = len(items_list[lower_index:upper_index]) + lower_index

            lower_bound = lower_index + 1
            if upper_bound == 0:
                lower_bound = 0
                
            label_text = f"{lower_bound} - {upper_bound} / {len(items_list)}"
        
        self._current_page_label.config(text=label_text)
    
    def config_navigation(self, button_container, label_container):
        self._back_img = IMAGES.create(IMAGES.BACK)
        self._next_img = IMAGES.create(IMAGES.NEXT)

        next_command = partial(self.switch_page, PageSystem.NEXT)
        prev_command = partial(self.switch_page, PageSystem.PREVIOUS)

        # Button: Go to previous page
        self._prev_button = CButton(
            parent=button_container,
            image=self._back_img,
            command=prev_command,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=0
        )
        self._prev_button._disable()

        # Button: Go to next page
        self._next_button = CButton(
            parent=button_container,
            image=self._next_img,
            command=next_command,
            fg=CButton.DARK, bg=CButton.LIGHT,
            row=0, column=1
        )
        self._next_button._disable()

        parent_bg = label_container.cget('background')
        
        self._current_page_label = Label(
            master=label_container,
            text='<current page index>',
            font=Fonts.small(bold=True),
            foreground='black',
            background=parent_bg
        )
        self._current_page_label.pack(side=LEFT, padx=10, fill='x', expand=1)

    def switch_page(self, direction: int):
        self.page_index = self.page_index + direction

        self.on_page_changed_event()
