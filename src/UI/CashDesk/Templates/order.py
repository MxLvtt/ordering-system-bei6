import time
from EventHandler.Event import Event
from random import *

class Order():
    def __init__(self, meals: [], form: int, meal_codes: [] = []):
        # Properties
        self._timestamp: int = int(time.time())
        self._id: int = -1
        self._state: int = 0
        self._form: int = form
        self._meals: [] = meals
        self._meal_codes: [] = meal_codes

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

    @property
    def meal_codes(self) -> []:
        """ Returns the list of meal codes, generated using the
        given list of meals.
        """
        codes = []
        
        for meal in self.meals:
            codes.append(meal.get_meal_code())
        
        return codes

    ### Methods

    def equals(self, order: 'Order') -> bool:
        # Is id equal?
        if self.id != order.id:
            return False
        
        # Is timestamp equal?
        if self.timestamp != order.timestamp:
            return False

        # Are form and state equal?
        if self.form != order.form or self.state != order.state:
            return False

        # Calculate meal codes
        codes1: [] = self.meal_codes
        codes2: [] = order.meal_codes

        # Same number of meals?
        if len(codes1) != len(codes2):
            return False

        return True # TODO: reminder - there is no check if the actual codes are equal too (performance!)

    ### Events

    @property
    def on_state_changed(self) -> Event:
        return self._state_changed_event
