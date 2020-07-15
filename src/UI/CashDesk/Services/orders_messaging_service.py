from tkinter import messagebox
import threading
import Templates.references as REFS
from EventHandler.Event import Event
from Templates.order import Order
from Templates.meals import Meal
from Handlers.database_handler import DatabaseHandler
# from Handlers.network_handler import NetworkHandler
from Handlers.timer_handler import TimerHandler
from datetime import datetime


class OrdersMessagingService():
    initialized = False
    counter = 0

    # Events
    # on_order_created_event: Event = Event()
    # on_orders_changed: Event = Event()

    def __init__(self):
        # TODO: ?

        OrdersMessagingService.initialized = True

    @staticmethod
    def notify_on_order_creation(new_order: Order):
        if not OrdersMessagingService.initialized or new_order == None:
            raise RuntimeError("OrdersMessagingService not initialized or invalid parameter")

        pass
