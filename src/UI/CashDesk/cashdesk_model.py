import time
from random import random
from tkinter import PhotoImage
from threading import Timer
from Handlers.meals_handler import MealsHandler
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
        self._meals_db_connection_ready_event: Event = Event()

        # Image objects for the buttons
        self._checkmark_img = PhotoImage(file=IMAGES.CHECK_MARK)
        self._exit_img = PhotoImage(file=IMAGES.EXIT)
        self._add_img = PhotoImage(file=IMAGES.ADD) 
        self._back_img = PhotoImage(file=IMAGES.BACK) 
        self._add_order_view_img = PhotoImage(file=IMAGES.BURGER_DARK) 
        self._history_img = PhotoImage(file=IMAGES.HISTORY)
        self._in_progress_img = PhotoImage(file=IMAGES.IN_PROGRESS)
        self._settings_img = PhotoImage(file=IMAGES.SETTINGS)
        self._trashcan_img = PhotoImage(file=IMAGES.TRASH_CAN)
        self._order = PhotoImage(file=IMAGES.ORDER)

        # Holds the value of the currently displayed time
        self._current_time = "<TIME>"

    def initialize(self):
        """ Has to be called, when the GUI is finished with initialization.
        """
        self._main_cycle_thread()

        self._meals_handler = MealsHandler(self._meals_db_connection_ready_event)

    ### ------------------- PROPERTIES ------------------- ###

    @property
    def on_cycle_event(self):
        return self._on_cycle_event

    @property
    def meals_db_connection_ready_event(self):
        return self._meals_db_connection_ready_event

    @property
    def current_time(self) -> str:
        return self._current_time

    @property
    def checkmark_img(self):
        return self._checkmark_img

    @property
    def exit_img(self):
        return self._exit_img

    @property
    def add_img(self):
        return self._add_img

    @property
    def back_img(self):
        return self._back_img

    @property
    def add_order_view_img(self):
        return self._add_order_view_img

    @property
    def history_img(self):
        return self._history_img

    @property
    def in_progress_img(self):
        return self._in_progress_img

    @property
    def settings_img(self):
        return self._settings_img

    @property
    def trashcan_img(self):
        return self._trashcan_img

    @property
    def order_img(self):
        return self._order

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

    def call_after_delay(self, function, delay: float):
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
