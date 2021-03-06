import time
from random import random
from tkinter import PhotoImage
from threading import Timer
from Handlers.timer_handler import TimerHandler
from Handlers.database_handler import DatabaseHandler
from Handlers.network_handler import NetworkHandler
from Handlers.encryption_handler import EncryptionHandler
from Notification.notification_service import NotificationService
from Services.meals_service import MealsService
from Services.orders_service import OrdersService
from Services.Messengers.order_messaging_service import OrderMessagingService
from EventHandler.Event import Event
from Notification.toast import Toast
from Templates.cbutton import CButton
from Templates.images import IMAGES
import Templates.references as REFS
 
class CashDeskModel():
    # PUBLIC STATIC VARIABLES
    MAIN_CYCLE_INTERVAL=0.2
    CONNECTION_CHECK_INTERVAL=5.0

    def __init__(self, root):
        # Timer to trigger the main periodical thread
        self._main_cycle_timer: Timer
        self._secondary_cycle_timer: Timer

        # Event that is triggered on every execution of the main cycle
        self._on_cycle_event: Event = Event()
        
        # Initializing the timer handler
        self.timer_handler = TimerHandler(root_object=root)

        self._notification_service = NotificationService(root=root)

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

        # EncryptionHandler
        self._encryption_handler = EncryptionHandler(key=REFS.PUBLIC_KEY_16BIT)

        # Initialize database handler
        self._database_handler = DatabaseHandler(debug=debug)

        # Initialize network handler
        self._network_handler = NetworkHandler(main_station = REFS.MAIN_STATION)
        # Start continous receive-loop
        self._network_handler.start_receive_loop()

        self._secondary_cycle_thread()

        ##### Service Registration

        # Initialize meals service (which is using the database handler)
        self._meals_service = MealsService()
        self._orders_service = OrdersService()
        self._order_messaging_service = OrderMessagingService()

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
        # self._show_toast("Cleared form")
        pass

    def add_order(self):
        """ Adds a new order with the information given in the AddOrderView.
        """
        # TODO: Save order details
            
        #self._show_toast("Added new order")
        pass

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
        self._secondary_cycle_timer.cancel()

    def _main_cycle_thread(self, curtime='', *args, **kwargs):
        """ Private function that is called periodically on a separate thread.
        """
        try:
            res: float = random()

            if res < 0.01:
                # self._show_toast("Order updated")
                pass

            # UPDATE CLOCK
            time_format = "%a, %d-%m-%Y\n%H:%M:%S"

            if REFS.MOBILE:
                time_format = "%a\n%d-%m-%y\n%H:%M:%S"

            newtime = time.strftime(time_format)
            if newtime != curtime:
                curtime = newtime
                self._current_time = curtime

            # EVENT TRIGGER
            self.on_cycle_event()
        except:
            pass
        finally:
            # REPEAT
            self._main_cycle_timer = Timer(CashDeskModel.MAIN_CYCLE_INTERVAL, self._main_cycle_thread, curtime)
            self._main_cycle_timer.start()

    def _secondary_cycle_thread(self):
        try:
            # Check if the connection to the other station is ready
            self._network_handler.check_connection_ready()
        except:
            pass
        finally:
            # REPEAT
            self._secondary_cycle_timer = Timer(CashDeskModel.CONNECTION_CHECK_INTERVAL, self._secondary_cycle_thread)
            self._secondary_cycle_timer.start()

    def _show_toast(self, text="Notification Toast"):
        """ TODO: TEMP """
        Toast(
            title=text,
            summary="This is a short summary\nof the notification."
        )
        pass
