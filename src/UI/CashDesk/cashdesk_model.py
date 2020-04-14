import time
from tkinter import PhotoImage
from threading import Timer
from EventHandler.Event import Event
from Templates.cbutton import CButton
from Templates.images import IMAGES
from Templates.toast import Toast
 
class CashDeskModel():
    INTERVAL=0.2

    def __init__(self):
        self._main_cycle_timer: Timer
        self._on_cycle_event: Event = Event()

        self._checkmark_img = PhotoImage(file=IMAGES.CHECK_MARK)
        self._exit_img = PhotoImage(file=IMAGES.EXIT)
        self._history_img = PhotoImage(file=IMAGES.HISTORY)
        self._in_progress_img = PhotoImage(file=IMAGES.IN_PROGRESS)
        self._settings_img = PhotoImage(file=IMAGES.SETTINGS)
        self._trashcan_img = PhotoImage(file=IMAGES.TRASH_CAN)

        self._current_time = "<TIME>"

    def initialize(self):
        self._main_cycle_thread()

    @property
    def on_cycle_event(self):
        return self._on_cycle_event

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

    def call_after_delay(self, function, delay: float):
        if delay > 0:
            Timer(delay, function).start()

    def clear_form(self):
        """ Resets all widgets in the AddOrderView to their default values.
        """
        pass

    def add_order(self):
        """ Adds a new order with the information given in the AddOrderView.
        """
        # TODO: Save order details
            
        self._show_toast()

    def _cancel_timer(self):
        self._main_cycle_timer.cancel()

    def _main_cycle_thread(self, curtime='', *args, **kwargs):
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

    def _show_toast(self):
        Toast(
            title="Notification Toast",
            summary="This is a short summary\nof the notification."
        )
        pass
