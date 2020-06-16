import time
from EventHandler.Event import Event
from random import *

class Order():
    def __init__(self, meals: [], form: int):
        # Properties
        self._timestamp: int = int(time.time())
        self._id: int = -1
        self._state: int = 0
        self._form: int = form
        self._meals: [] = meals

        self._is_id_set: bool = False

        # Events
        self._state_changed_event: Event = Event()

    ### Properties

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_id: int) -> int:
        if not self._is_id_set:
            self._id = new_id
            self._is_id_set = True
        else:
            raise RuntimeError("The id of an order can't be set more than once.")

    @property
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, new_state: int):
        self._state = new_state
        self._state_changed_event()

    @property
    def form(self) -> int:
        return self._form

    @property
    def meals(self) -> []:
        return self._meals

    ### Events

    @property
    def on_state_changed(self) -> Event:
        return self._state_changed_event
