import time
from random import random
from tkinter import PhotoImage
from threading import Timer
from Handlers.database_handler import DatabaseHandler
from Services.meals_service import MealsService
from Services.orders_service import OrdersService
from EventHandler.Event import Event
from Notification.toast import Toast
from Templates.cbutton import CButton
from Templates.images import IMAGES
 
class CashDeskModel():
    # PUBLIC STATIC VARIABLES
    INTERVAL=0.2

    def __init__(self):
        # Timer to trigger the main periodical thread
        self._main_cycle_timer: Timer
        # Event that is triggered on every execution of the main cycle
        self._on_cycle_event: Event = Event()

        # Event that is triggered, when the MealsHandler established the connection to the database
        self._db_connection_ready_event: Event = Event()

        # Event that is triggered, when the content of the body changes
        self._body_content_changed_event: Event = Event()

        # Holds the value of the currently displayed time
        self._current_time = "<TIME>"

    def initialize(self, debug: bool = False):
        """ Has to be called, when the GUI is finished with initialization.
        """
        self._main_cycle_thread()

        ##### Handler Registration

        # Initialize database handler
        self._database_handler = DatabaseHandler(debug=debug)

        ##### Service Registration

        # Initialize meals service (which is using the database handler)
        self._meals_service = MealsService()
        self._orders_service = OrdersService()

        # If the db connection has been established: trigger the event
        if self._database_handler.CONNECTION_READY:
            self._db_connection_ready_event()

    ### ------------------- PROPERTIES ------------------- ###

    @property
    def on_cycle_event(self) -> Event:
        return self._on_cycle_event

    @property
    def db_connection_ready_event(self) -> Event:
        return self._db_connection_ready_event

    @property
    def body_content_changed_event(self) -> Event:
        return self._body_content_changed_event

    @property
    def current_time(self) -> str:
        return self._current_time

    ### ------------------- MAIN METHODS ------------------- ###

    def clear_form(self):
        """ Resets all widgets in the AddOrderView to their default values.
        """
        self._show_toast("Cleared form")
        pass

    def add_order(self):
        """ Adds a new order with the information given in the AddOrderView.
        """
        # TODO: Save order details
            
        self._show_toast("Added new order")

    ### ------------------- HELPER METHODS ------------------- ###

    @staticmethod
    def call_after_delay(function, delay: float):
        """ Helper method to call a given function after the specified delay.
        """
        if delay > 0:
            Timer(delay, function).start()

    ### ------------------- PRIVATE METHODS ------------------- ###

    def _cancel_timer(self):
        """ Private function to stop the main cyclic thread.
        """
        self._main_cycle_timer.cancel()

    def _main_cycle_thread(self, curtime='', *args, **kwargs):
        """ Private function that is called periodically on a separate thread.
        """
        res: float = random()

        if res < 0.01:
            self._show_toast("Order updated")

        # UPDATE CLOCK
        newtime = time.strftime("%a, %d-%m-%Y\n%H:%M:%S")
        if newtime != curtime:
            curtime = newtime
            self._current_time = curtime

        # EVENT TRIGGER
        self.on_cycle_event()

        # REPEAT
        self._main_cycle_timer = Timer(self.INTERVAL, self._main_cycle_thread, curtime)
        self._main_cycle_timer.start()

    def _show_toast(self, text="Notification Toast"):
        """ TODO: TEMP """
        Toast(
            title=text,
            summary="This is a short summary\nof the notification."
        )
        pass
