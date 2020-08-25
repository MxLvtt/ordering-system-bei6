import Templates.references as REFS
from tkinter import *
from tkinter import ttk
from random import *
from ContentControl.content_template import ContentTemplate
from ContentControl.Settings.settings_category import SettingsCategory
from Templates.cbutton import CButton
from Templates.scrollable import Scrollable
from Templates.toggle_button import ToggleButton, ToggleButtonGroup
from Templates.images import IMAGES
from Templates.order import Order

class ScrollList(Frame):
    def __init__(self, parent, spacing : int = 0, background="white", additional_pressed_event = None):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self.parent = parent
        self.spacing = spacing
        self.height = 0
        self.y = 0

        self.elements = []
        self.update_view()

        self._additional_pressed_event = additional_pressed_event
        self._moved = False

        self.bind("<ButtonPress-1>", self._start_move)
        self.bind("<ButtonRelease-1>", self._stop_move)
        self.bind("<B1-Motion>", self._do_move)

    @property
    def Elements(self) -> []:
        return self.elements

    def set_additional_pressed_event(self, new_additional_pressed_event):
        self._additional_pressed_event = new_additional_pressed_event

    def _start_move(self, event):        
        self.y = event.y

    def _stop_move(self, event):
        # Call additional functions as long as the mouse has not been dragged
        if not self._moved and self._additional_pressed_event != None and callable(self._additional_pressed_event):
            self._additional_pressed_event()

        self._moved = False
        self.y = None

    def _do_move(self, event):
        self._moved = True

        if self.height <= self.parent.winfo_height():
            return

        deltay = event.y - self.y
        y = self.winfo_y() + deltay

        self.set_y(y)

    def set_y(self, y: int):
        if y >= 0:
            y = 0
        if y <= -(self.height - self.parent.winfo_height()):
            y = -(self.height - self.parent.winfo_height())

        self.place(y=y)

    def element_height_changed(self):
        self.update_view()

    def reset_scroll(self):
        self.place(y=0)

    def update_view(self):
        frameheight = 0
        if len(self.elements) > 0:
            frameheight = (len(self.elements) - 1) * self.spacing

        curr_y = 0

        for element in self.elements:
            element.place(relwidth=1.0, height=element.height, x=0, y=curr_y)
            curr_y = curr_y + element.height + self.spacing
            frameheight = frameheight + element.height

        self.height = frameheight
        
        y = self.winfo_y()
        if y >= 0 or self.height <= self.parent.winfo_height():
            y = 0
        elif y <= -(self.height - self.parent.winfo_height()):
            y = -(self.height - self.parent.winfo_height())

        self.place(relwidth=1.0, height=frameheight, x=0, y=y)

    def add_row(self, element, update: bool = True):
        if not isinstance(element, Scrollable):
            raise RuntimeError("The given element is not of type Scrollable")

        # TODO: Bindings have to be added to ALL widgets on the element, otherwise it will not be recognized
        element.bind("<ButtonPress-1>", self._start_move)
        element.bind("<ButtonRelease-1>", self._stop_move)
        element.bind("<B1-Motion>", self._do_move)
        self.bind_all_childs(element)

        element.on_height_changed_event.add(self.element_height_changed)
        
        self.elements.append(element)

        if update:
            self.update_view()

    def remove_all(self, update: bool = True):
        for element in self.elements:
            element.unbind("<ButtonPress-1>")
            element.unbind("<ButtonRelease-1>")
            element.unbind("<B1-Motion>")
            self.unbind_all_childs(element)
            
        for element in self.elements:
            element.destroy()
        
        self.elements.clear()
        
        self.place_forget()

        if update:
            self.update_view()

    def bind_all_childs(self, start_element):
        curr = start_element

        for child in curr.winfo_children():
            if isinstance(child, Label) or isinstance(child, Frame):
                child.bind("<ButtonPress-1>", self._start_move)
                child.bind("<ButtonRelease-1>", self._stop_move)
                child.bind("<B1-Motion>", self._do_move)
            self.bind_all_childs(child)

    def unbind_all_childs(self, start_element):
        curr = start_element

        for child in curr.winfo_children():
            if isinstance(child, Label) or isinstance(child, Frame):
                child.unbind("<ButtonPress-1>")
                child.unbind("<ButtonRelease-1>")
                child.unbind("<B1-Motion>")
            self.unbind_all_childs(child)

    def remove_row_by_element(self, element, update: bool = True):
        if not isinstance(element, Scrollable):
            raise RuntimeError("The given element is not of type Scrollable")

        self.elements.remove(element)

        element.unbind("<ButtonPress-1>")
        element.unbind("<ButtonRelease-1>")
        element.unbind("<B1-Motion>")

        if update:
            self.update_view()

    def remove_row_by_index(self, index: int):
        if index < 0 or index >= len(self.elements):
            raise RuntimeError("Index out of bounds exception")

        remove_element = self.elements[index]
        self.remove_row_by_element(remove_element)