from tkinter import *
from EventHandler.Event import Event

class Scrollable(Frame):
    def __init__(self, parent, height: int, background="white"):
        super().__init__(
            master=parent,
            cnf={},
            background=background
        )

        self._on_height_changed_event : Event = Event()

        self._height = height
        self._initial_height = height

    @property
    def on_height_changed_event(self) -> Event:
        return self._on_height_changed_event

    @property
    def initial_height(self) -> int:
        return self._initial_height

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, h: int):
        self._height = h
        self._on_height_changed_event()

    def set_height_anonymously(self, height):
        self._height = height