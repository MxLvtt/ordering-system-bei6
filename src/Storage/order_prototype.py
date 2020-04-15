

class Order(object):
    def __init__(
        self,
        number=-1,
        timestamp=None,
        category=-1,
        status=-1
    ):
        self._number = number # Unique order id
        self._timestamp = timestamp # Time of order creation
        self._category = category # Eat in (0) or Takeaway (1)
        self._status = status # Todo (0), In-Progress (1), Done (2) or Canceled (3)

        if number == -1 or timestamp == None or category == -1 or status == -1:
            self._preset_properties_with_random_values() # TEMP

        self._print_details()

    def _preset_properties_with_random_values(self):
        self._number = 42
        self._timestamp = "10:09:43"
        self._category = 1
        self._status = 2

    def _print_details(self):
        print(f"Created new Order [#{self._number} @ {self._timestamp} - {self._category} - {self._status}]")

    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, number: int):
        self._number = number
        
    @property
    def timestamp(self) -> str:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: str):
        self._timestamp = timestamp
        
    @property
    def category(self) -> int:
        return self._category

    @category.setter
    def category(self, category: int):
        self._category = category
        
    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, status: int):
        self._status = status
        

