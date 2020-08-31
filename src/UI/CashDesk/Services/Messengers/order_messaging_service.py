from tkinter import messagebox
import threading
import Templates.references as REFS
from functools import partial
from EventHandler.Event import Event
from Templates.order import Order
from Templates.meals import Meal
from Templates.custom_thread import CustomThread
from Handlers.database_handler import DatabaseHandler
from Handlers.network_handler import NetworkHandler
from Handlers.timer_handler import TimerHandler
from Notification.notification_service import NotificationService
from Services.Messengers.messenger import Messenger
from Services.orders_service import OrdersService
from datetime import datetime


class OrderMessagingService(Messenger):
    """ Provides methods for interaction with the NetworkHandler, in order
    to act, whenever a specific message is coming in or to construct the
    message body for a new message about ot be sent.
    """

    # TODO ###################################################
    # TODO ###################################################
    # TODO ###################################################
    # TODO ###################################################
    # TODO ###################################################
    # TODO ###################################################

    initialized = False

    on_database_changed_event: Event = Event()

    def __init__(self):
        super().__init__(self)
    
        OrderMessagingService.IDENTIFIER = self.identifier
        OrderMessagingService.initialized = True

    def process_message(self, message: str):
        """ Gets called, whenever the network handler receives a message,
        that is for this specific service.

        message: contains only the main body; no service- and msg-id
        """
        print("Message to process:", message)

        # Message says: DB content has changed
        if message.startswith(REFS.DB_CHANGED_PREFIX):
            if not message[1:].startswith(REFS.SILENT_PREFIX):
                order_id = message[2:]

                toast_title = "DB CHANGED"
                toast_text = "<text>"

                # More precise: a new order has been created
                if message[1:].startswith(REFS.ORDER_CREATED_PREFIX):
                    order_timestamp = OrdersService.get_orders(
                        row_filter=f"{REFS.ORDERS_TABLE_ID}={order_id}",
                        columns=[f"{REFS.ORDERS_TABLE_TIMESTAMP}"]
                    )[0][0]
                    order_timestamp = OrdersService.convert_timestamp(order_timestamp)
                    
                    toast_title = REFS.ORDER_CREATED_TOAST[0]
                    toast_text = REFS.ORDER_CREATED_TOAST[1].format(order_id, order_timestamp)
                # More precise: a new order has been changed
                elif message[1:].startswith(REFS.ORDER_CHANGED_PREFIX):
                    order_details = OrdersService.get_orders(
                        row_filter=f"{REFS.ORDERS_TABLE_ID}={order_id}",
                        columns=[f"{REFS.ORDERS_TABLE_TIMESTAMP}", f"{REFS.ORDERS_TABLE_STATE}"]
                    )[0]
                    order_timestamp = OrdersService.convert_timestamp(order_details[0])

                    order_change = f"Status > {REFS.ORDER_STATES[int(order_details[1])]}"
                    
                    toast_title = REFS.ORDER_CHANGED_TOAST[0]
                    toast_text = REFS.ORDER_CHANGED_TOAST[1].format(
                        order_id,
                        order_timestamp,
                        order_change)

                NotificationService.show_toast(
                    title=toast_title,
                    text=toast_text,
                    keep_alive=False
                )

            # Fire event to inform subscribed classes, like views
            OrderMessagingService.on_database_changed_event()
        # Message says: Request to change given order in DB
        elif message.startswith(REFS.ORDER_CHANGE_REQUEST_PREFIX) and REFS.MAIN_STATION:
            order_id = message[2:-2]
            change = message[3:]

            print("Order id:", order_id)
            print("Change to:", change)

            # First: get the order's current data
            result = OrdersService.get_orders(
                row_filter=f"{REFS.ORDERS_TABLE_ID}={order_id}"
            )

            if result == None or len(result) == 0:
                raise RuntimeError("The given order can not be changed because it's not in the database.")

            old_order = OrdersService.convert_to_order_object(result[0])

            if message[1:].startswith(REFS.ORDER_STATUS_CHANGED_PREFIX):
                old_order.state = change
            elif message[1:].startswith(REFS.ORDER_TYPE_CHANGED_PREFIX):
                old_order.form = change

            OrdersService.update_order(old_order, active=True)

            # # Send Message to other station about order creation (fire and forget)
            # OrderMessagingService.notify_of_changes(
            #     changed_order=clicked_order_tile.order,
            #     prefix=REFS.ORDER_CHANGED_PREFIX)

            # Fire event to inform subscribed classes, like views
            OrderMessagingService.on_database_changed_event()

    @staticmethod
    def notify_of_changes(changed_order: Order, prefix: str) -> bool:
        if not NetworkHandler.CONNECTION_READY:
            return False
            
        # CONSTRUCT MESSAGE BODY
        message_body = f"{REFS.DB_CHANGED_PREFIX}" \
            f"{prefix}" \
            f"{changed_order.id}"

        message_body = Messenger.attach_service_id(
            service_id = OrderMessagingService.IDENTIFIER,
            message = message_body
        )

        new_thread = CustomThread(2, "MessangerThread-2", partial(OrderMessagingService._send, message_body))
        new_thread.start()

        return True

    @staticmethod
    def request_order_update(order: Order, state: int = -1, form: int = -1):
        if not NetworkHandler.CONNECTION_READY:
            return False

        if state != -1:
            prefix = REFS.ORDER_STATUS_CHANGED_PREFIX
            change = state
        elif form != -1:
            prefix = REFS.ORDER_TYPE_CHANGED_PREFIX
            change = form
        else:
            return False

        # CONSTRUCT MESSAGE BODY
        message_body = f"{REFS.ORDER_CHANGE_REQUEST_PREFIX}" \
            f"{prefix}" \
            f"{order.id}" \
            f"{change}"

        print("Message to send:", message_body)

        message_body = Messenger.attach_service_id(
            service_id = OrderMessagingService.IDENTIFIER,
            message = message_body
        )
        
        print("Message to send:", message_body)

        new_thread = CustomThread(3, "MessangerThread-3", partial(OrderMessagingService._send, message_body))
        new_thread.start()

        return True


    @staticmethod
    def _send(message):
        NetworkHandler.send_with_handshake(message)












#     @staticmethod
#     def convert_form(form: int) -> str:
#         if form < 0 or form >= len(REFS.ORDER_FORMS):
#             raise RuntimeError(f"Form index {form} is invalid for an order")

#         return REFS.ORDER_FORMS[form]

#     @staticmethod
#     def convert_status(state: int) -> str:
#         if state < 0 or state >= len(REFS.ORDER_STATES):
#             raise RuntimeError(f"State index {state} is invalid for an order")

#         return REFS.ORDER_STATES[state]

#     @staticmethod
#     def convert_active(active: str) -> str:
#         if active != REFS.ORDERS_TABLE_ACTIVE_TRUE and active != REFS.ORDERS_TABLE_ACTIVE_FALSE:
#             raise RuntimeError(f"Active character is invalid, must be {REFS.ORDERS_TABLE_ACTIVE_TRUE} or {REFS.ORDERS_TABLE_ACTIVE_FALSE}")

#         if active == REFS.ORDERS_TABLE_ACTIVE_TRUE:
#             return REFS.ORDERS_TABLE_ACTIVE_TRUE_GER
#         elif active == REFS.ORDERS_TABLE_ACTIVE_FALSE:
#             return REFS.ORDERS_TABLE_ACTIVE_FALSE_GER

#     @staticmethod
#     def convert_timestamp(timestamp: int, extended: bool = False) -> str:
#         dateTimeObj = datetime.fromtimestamp(timestamp)

#         tformat = OrdersService.TIMESTAMP_FORMAT
#         if extended:
#             tformat = OrdersService.TIMESTAMP_FORMAT_EXTENDED
        
#         return dateTimeObj.strftime(tformat)

#     @staticmethod
#     def get_column_names() -> []:
#         if OrdersService.COLUMN_NAMES == None:
#             OrdersService.COLUMN_NAMES = DatabaseHandler.get_table_information(table_name=REFS.ORDERS_TABLE_NAME)[1]
            
#         return OrdersService.COLUMN_NAMES

#     @staticmethod
#     def convert_to_order_object(db_content: []) -> Order:
#         """ Converts the db content array to an order object
#         """
#         col_names = OrdersService.get_column_names()

#         id_i = col_names.index(REFS.ORDERS_TABLE_ID)
#         id_db = db_content[id_i]

#         time_i = col_names.index(REFS.ORDERS_TABLE_TIMESTAMP)
#         time_db = db_content[time_i]

#         form_i = col_names.index(REFS.ORDERS_TABLE_FORM)
#         form_db = db_content[form_i]

#         state_i = col_names.index(REFS.ORDERS_TABLE_STATE)
#         state_db = db_content[state_i]

#         price_i = col_names.index(REFS.ORDERS_TABLE_PRICE)
#         price_db = db_content[price_i]

#         meals_i = col_names.index(REFS.ORDERS_TABLE_MEALS)
#         meals_db = db_content[meals_i]
#         meals_list = []
#         for meal_code in meals_db.split(REFS.MEAL_CODES_DELIMITER):
#             meals_list.append(Meal.get_meal_from_code(meal_code))

#         order = Order(
#             meals=meals_list,
#             form=form_db,
#             timestamp=time_db,
#             id=id_db,
#             state=state_db,
#             price=price_db
#         )

#         return order

#     @staticmethod
#     def delete_from_table(condition: str = "", confirm: bool = True) -> bool:
#         if not OrdersService.initialized:
#             return None

#         confirmed = True

#         if confirm:
#             confirmed = messagebox.askyesno(
#                 title="Clear order history",
#                 message="Are you sure you want to clear the order history?\n\nThis will delete all inactive orders.",
#                 default='no'
#             )

#         if confirmed:
#             DatabaseHandler.delete_from_table(
#                 table_name=REFS.ORDERS_TABLE_NAME,
#                 row_filter=condition
#             )
#         else:
#             print(f"Truncating '{REFS.ORDERS_TABLE_NAME}' table canceled.")
            
#         return confirmed

#     @staticmethod
#     def truncate_table(confirm: bool = True) -> bool:
#         if not OrdersService.initialized:
#             return None

#         confirmed = True

#         if confirm:
#             confirmed = messagebox.askyesno(
#                 title="Clear order history",
#                 message="Are you sure you want to clear the order history?\n\nThis will delete all inactive orders.",
#                 default='no'
#             )

#         if confirmed:
#             DatabaseHandler.truncate_table(table_name=REFS.ORDERS_TABLE_NAME)
#         else:
#             print(f"Truncating '{REFS.ORDERS_TABLE_NAME}' table canceled.")
            
#         return confirmed

#     @staticmethod
#     def get_orders(order_by: str = "", row_filter: str = "") -> []:
#         if not OrdersService.initialized:
#             return None

#         return DatabaseHandler.select_from_table(
#             table_name=REFS.ORDERS_TABLE_NAME,
#             order_by=order_by,
#             row_filter=row_filter
#         )

#     @staticmethod
#     def update_order(order: Order, active: bool = None):
#         if not OrdersService.initialized or order == None:
#             return None

#         # First: get the order's current data
#         result = OrdersService.get_orders(
#             row_filter=f"{REFS.ORDERS_TABLE_ID}={order.id}"
#         )

#         if result == None or len(result) == 0:
#             raise RuntimeError("The given order can not be changed because it's not in the database.")

#         old_order = OrdersService.convert_to_order_object(result[0])

#         # Only if the new and old order state are both OPEN
#         if order.state == old_order.state and order.state == REFS.OPEN:
#             # Check if the order was changed in the form or the meals list
#             if order.form != old_order.form or order.meals != old_order.meals: # TODO: Does this actually work?
#                 # If so: set its state to CHANGED
#                 order.state = REFS.CHANGED

#         columns = [
#             REFS.ORDERS_TABLE_FORM,
#             REFS.ORDERS_TABLE_STATE,
#             REFS.ORDERS_TABLE_MEALS
#         ]

#         meal_codes = REFS.MEAL_CODES_DELIMITER.join(order.meal_codes)

#         values = [
#             order.form,
#             order.state,
#             f"'{meal_codes}'"
#         ]

#         if active != None:
#             active_label = REFS.ORDERS_TABLE_ACTIVE_FALSE

#             if active == True:
#                 active_label = REFS.ORDERS_TABLE_ACTIVE_TRUE

#             columns.append(REFS.ORDERS_TABLE_ACTIVE)
#             values.append(f"'{active_label}'")
        
#         DatabaseHandler.update_table(
#             table_name=REFS.ORDERS_TABLE_NAME,
#             columns=columns,
#             values=values,
#             condition=f"{REFS.ORDERS_TABLE_ID}={order.id}"
#         )

#         if active != False:
#             if order.state == REFS.PREPARED or order.state == REFS.CANCELED:
#                 OrdersService._create_timer(order)
#             else:
#                 OrdersService._stop_timer_if_existant(order)

#     @staticmethod
#     def create_new_order(meals_list: [], order_form: int) -> Order:
#         if not OrdersService.initialized or meals_list == None or order_form == None:
#             return None

#         # Create Order object with the given information
#         #   meals:      given from the arguments of this function
#         #   form:       given from the arguments of this function
#         #   timestamp:  set in the constructor of the order class
#         #   id:         later set after insertion in the db table
#         #   state:      reset in the constructor to value of zero
#         new_order: Order = Order(meals=meals_list, form=order_form)

#         # Defining sql query contents
#         columns = [
#             REFS.ORDERS_TABLE_TIMESTAMP,
#             REFS.ORDERS_TABLE_FORM,
#             REFS.ORDERS_TABLE_PRICE,
#             REFS.ORDERS_TABLE_MEALS
#         ]

#         # Joins the individual meal codes into one string, separated by a pipe symbol
#         meals_code = REFS.MEAL_CODES_DELIMITER.join(new_order.meal_codes)

#         # Defines whether the order is active or not: Y = Yes, it is active, since it's new
#         # active = REFS.ORDERS_TABLE_ACTIVE_TRUE
#         # ACTIVE DEFAULTS TO 'Y' IF NOT SET! -> CAN BE LEFT OUT

#         order_price = new_order.calculate_price()

#         values = [
#             new_order.timestamp,
#             new_order.form,
#             # new_order.state, # -> Defaults to 0 in the database, so not necessary here
#             # f"'{active}'",   # -> Defaults to 'Y' in the database, so not necessary here
#             order_price,
#             f"'{meals_code}'"
#         ]

#         # Insert new order into the database table
#         DatabaseHandler.insert_into_table(REFS.ORDERS_TABLE_NAME, columns, values)

#         # Get the highest id value of database
#         highest_id = DatabaseHandler.select_from_table(
#             table_name=REFS.ORDERS_TABLE_NAME,
#             columns=[f"MAX({REFS.ORDERS_TABLE_ID})"]
#         )

#         # Set the order's internal id property to the id value of the database
#         new_order.id = highest_id

#         # Increment counter of added orders
#         OrdersService.counter = OrdersService.counter + 1

#         # Trigger event to inform others of a change in the orders-list
#         OrdersService.on_order_created_event(new_order)

#         # Return the newly created order object with the updated information
#         return new_order

#     @staticmethod
#     def _create_timer(order):
#         """ Creates and starts a new timer for the given order.
#         """
#         OrderTimerPair(order=order).start_timer()

#     @staticmethod
#     def _stop_timer_if_existant(order):
#         """ Checks if there is a timer running for the given order.
#         If so: stop the timer and delete it from the registry.
#         """
#         pair = OrderTimerPair.get_order_timer_pair(order)

#         if pair == None:
#             return
            
#         pair.stop_timer()


# class OrderTimerPair():
#     TIMER_DELAY_MS = 5000

#     ACTIVE_PAIRS = []

#     def __init__(
#         self,
#         order
#     ):
#         self._order = order
#         self._timer_id = -1

#         OrderTimerPair.ACTIVE_PAIRS.append(self)

#     # def __del__(self):
#     #     self.stop_timer()

#     @property
#     def order(self):
#         return self._order

#     @property
#     def timer_id(self):
#         return self._timer_id

#     @staticmethod
#     def get_order_timer_pair(order):
#         for pair in OrderTimerPair.ACTIVE_PAIRS:
#             if pair.order.id == order.id:
#                 return pair

#         return None
    
#     def _timer_callback(self):
#         OrderTimerPair.ACTIVE_PAIRS.remove(self)

#         print(f"Setting order #{self._order.id} as inactive.")
#         OrdersService.update_order(order=self._order, active=False)
#         OrdersService.on_orders_changed()
    
#     def start_timer(self):
#         self._timer_id = TimerHandler.start_timer(self._timer_callback, OrderTimerPair.TIMER_DELAY_MS)

#     def stop_timer(self):
#         if self._timer_id == -1:
#             return

#         OrderTimerPair.ACTIVE_PAIRS.remove(self)

#         TimerHandler.cancel_timer(self._timer_id)

