from tkinter import messagebox
import threading
import Templates.references as REFS
from EventHandler.Event import Event
from Templates.order import Order
from Templates.meals import Meal
from Handlers.database_handler import DatabaseHandler
from Handlers.timer_handler import TimerHandler
from datetime import datetime


class OrdersService():
    TIMESTAMP_FORMAT="%H:%M:%S"
    TIMESTAMP_FORMAT_EXTENDED="%d.%m.%Y, %H:%M:%S"

    COLUMN_NAMES=None

    initialized = False
    counter = 0

    # Events
    on_order_created_event: Event = Event()
    on_orders_changed: Event = Event()

    def __init__(self):
        # TODO: ?
        OrdersService.initialized = True

    @staticmethod
    def convert_form(form: int) -> str:
        if form < 0 or form >= len(REFS.ORDER_FORMS):
            raise RuntimeError(f"Form index {form} is invalid for an order")

        return REFS.ORDER_FORMS[form]

    @staticmethod
    def convert_status(state: int) -> str:
        if state < 0 or state >= len(REFS.ORDER_STATES):
            raise RuntimeError(f"State index {state} is invalid for an order")

        return REFS.ORDER_STATES[state]

    @staticmethod
    def convert_active(active: str) -> str:
        if active != REFS.ORDERS_TABLE_ACTIVE_TRUE and active != REFS.ORDERS_TABLE_ACTIVE_FALSE:
            raise RuntimeError(f"Active character is invalid, must be {REFS.ORDERS_TABLE_ACTIVE_TRUE} or {REFS.ORDERS_TABLE_ACTIVE_FALSE}")

        if active == REFS.ORDERS_TABLE_ACTIVE_TRUE:
            return REFS.ORDERS_TABLE_ACTIVE_TRUE_GER
        elif active == REFS.ORDERS_TABLE_ACTIVE_FALSE:
            return REFS.ORDERS_TABLE_ACTIVE_FALSE_GER

    @staticmethod
    def convert_timestamp(timestamp: int, extended: bool = False) -> str:
        dateTimeObj = datetime.fromtimestamp(timestamp)

        tformat = OrdersService.TIMESTAMP_FORMAT
        if extended:
            tformat = OrdersService.TIMESTAMP_FORMAT_EXTENDED
        
        return dateTimeObj.strftime(tformat)

    @staticmethod
    def get_column_names() -> []:
        if OrdersService.COLUMN_NAMES == None:
            OrdersService.COLUMN_NAMES = DatabaseHandler.get_table_information(table_name=REFS.ORDERS_TABLE_NAME)[1]
            
        return OrdersService.COLUMN_NAMES

    @staticmethod
    def convert_to_order_object(db_content: []) -> Order:
        """ Converts the db content array to an order object
        """
        col_names = OrdersService.get_column_names()

        id_i = col_names.index(REFS.ORDERS_TABLE_ID)
        id_db = db_content[id_i]

        time_i = col_names.index(REFS.ORDERS_TABLE_TIMESTAMP)
        time_db = db_content[time_i]

        form_i = col_names.index(REFS.ORDERS_TABLE_FORM)
        form_db = db_content[form_i]

        state_i = col_names.index(REFS.ORDERS_TABLE_STATE)
        state_db = db_content[state_i]

        price_i = col_names.index(REFS.ORDERS_TABLE_PRICE)
        price_db = db_content[price_i]

        meals_i = col_names.index(REFS.ORDERS_TABLE_MEALS)
        meals_db = db_content[meals_i]
        meals_list = []
        for meal_code in meals_db.split(REFS.MEAL_CODES_DELIMITER):
            meals_list.append(Meal.get_meal_from_code(meal_code))

        order = Order(
            meals=meals_list,
            form=form_db,
            timestamp=time_db,
            id=id_db,
            state=state_db,
            price=price_db
        )

        return order

    @staticmethod
    def delete_from_table(condition: str = "", confirm: bool = True) -> bool:
        if not OrdersService.initialized:
            return None

        confirmed = True

        if confirm:
            confirmed = messagebox.askyesno(
                title="Clear order history",
                message="Are you sure you want to clear the order history? This will delete all inactive orders.\n\nNOTE: This will not reset the counter for the order number!",
                default='no'
            )

        if confirmed:
            DatabaseHandler.delete_from_table(
                table_name=REFS.ORDERS_TABLE_NAME,
                row_filter=condition
            )
        else:
            print(f"Truncating '{REFS.ORDERS_TABLE_NAME}' table canceled.")
            
        return confirmed

    @staticmethod
    def truncate_table(confirm: bool = True) -> bool:
        if not OrdersService.initialized:
            return None

        confirmed = True

        if confirm:
            confirmed = messagebox.askyesno(
                title="Clear order history",
                message="Are you sure you want to clear the whole order history?\n\nThis will delete every order from the database and reset the order counter for the order nubmer.",
                default='no'
            )

        if confirmed:
            DatabaseHandler.truncate_table(table_name=REFS.ORDERS_TABLE_NAME)
        else:
            print(f"Truncating '{REFS.ORDERS_TABLE_NAME}' table canceled.")
            
        return confirmed

    @staticmethod
    def get_orders(order_by: str = "", row_filter: str = "", columns: [] = []) -> []:
        if not OrdersService.initialized:
            return None

        return DatabaseHandler.select_from_table(
            table_name=REFS.ORDERS_TABLE_NAME,
            order_by=order_by,
            row_filter=row_filter,
            columns=columns
        )

    @staticmethod
    def update_order(order: Order, active: bool = None):
        if not OrdersService.initialized or order == None:
            return None

        # First: get the order's current data
        result = OrdersService.get_orders(
            row_filter=f"{REFS.ORDERS_TABLE_ID}={order.id}"
        )

        if result == None or len(result) == 0:
            raise RuntimeError("The given order can not be changed because it's not in the database.")

        old_order = OrdersService.convert_to_order_object(result[0])

        # Only if the new and old order state are both OPEN
        if order.state == old_order.state and order.state == REFS.OPEN:
            # Check if the order was changed in the form or the meals list
            if order.form != old_order.form or order.meals != old_order.meals: # TODO: Does this actually work?
                # If so: set its state to CHANGED
                order.state = REFS.CHANGED

        columns = [
            REFS.ORDERS_TABLE_FORM,
            REFS.ORDERS_TABLE_STATE,
            REFS.ORDERS_TABLE_MEALS
        ]

        meal_codes = REFS.MEAL_CODES_DELIMITER.join(order.meal_codes)

        values = [
            order.form,
            order.state,
            f"'{meal_codes}'"
        ]

        if active != None:
            active_label = REFS.ORDERS_TABLE_ACTIVE_FALSE

            if active == True:
                active_label = REFS.ORDERS_TABLE_ACTIVE_TRUE

            columns.append(REFS.ORDERS_TABLE_ACTIVE)
            values.append(f"'{active_label}'")
        
        DatabaseHandler.update_table(
            table_name=REFS.ORDERS_TABLE_NAME,
            columns=columns,
            values=values,
            condition=f"{REFS.ORDERS_TABLE_ID}={order.id}"
        )

        print("##### UPDATED DATABASE WITH ORDER CHANGE, order state, id = ", order.state, order.id)

        if active != False:
            OrdersService.handle_timer(order)

    @staticmethod
    def handle_timer(order):
        if order.state == REFS.PREPARED or order.state == REFS.CANCELED:
            print("## Creating timer")
            OrdersService._create_timer(order)
        else:
            print("## Stopping timer if existant")
            OrdersService._stop_timer_if_existant(order)

    @staticmethod
    def create_new_order(meals_list: [], order_form: int) -> Order:
        if not OrdersService.initialized or meals_list == None or order_form == None:
            return None

        # Create Order object with the given information
        #   meals:      given from the arguments of this function
        #   form:       given from the arguments of this function
        #   timestamp:  set in the constructor of the order class
        #   id:         later set after insertion in the db table
        #   state:      reset in the constructor to value of zero
        new_order: Order = Order(meals=meals_list, form=order_form)

        # Defining sql query contents
        columns = [
            REFS.ORDERS_TABLE_TIMESTAMP,
            REFS.ORDERS_TABLE_FORM,
            REFS.ORDERS_TABLE_PRICE,
            REFS.ORDERS_TABLE_MEALS
        ]

        # Joins the individual meal codes into one string, separated by a pipe symbol
        meals_code = REFS.MEAL_CODES_DELIMITER.join(new_order.meal_codes)

        # Defines whether the order is active or not: Y = Yes, it is active, since it's new
        # active = REFS.ORDERS_TABLE_ACTIVE_TRUE
        # ACTIVE DEFAULTS TO 'Y' IF NOT SET! -> CAN BE LEFT OUT

        order_price = new_order.calculate_price()

        values = [
            new_order.timestamp,
            new_order.form,
            # new_order.state, # -> Defaults to 0 in the database, so not necessary here
            # f"'{active}'",   # -> Defaults to 'Y' in the database, so not necessary here
            order_price,
            f"'{meals_code}'"
        ]

        # Insert new order into the database table
        DatabaseHandler.insert_into_table(REFS.ORDERS_TABLE_NAME, columns, values)

        # Get the highest id value of database
        highest_id = DatabaseHandler.select_from_table(
            table_name=REFS.ORDERS_TABLE_NAME,
            columns=[f"MAX({REFS.ORDERS_TABLE_ID})"]
        )

        # Set the order's internal id property to the id value of the database
        new_order.id = int(highest_id[0][0])

        # Increment counter of added orders
        OrdersService.counter = OrdersService.counter + 1

        # Trigger event to inform others of a change in the orders-list
        OrdersService.on_order_created_event(new_order)

        # Return the newly created order object with the updated information
        return new_order

    @staticmethod
    def _create_timer(order):
        """ Creates and starts a new timer for the given order.
        """
        OrderTimerPair(order=order).start_timer()

    @staticmethod
    def _stop_timer_if_existant(order):
        """ Checks if there is a timer running for the given order.
        If so: stop the timer and delete it from the registry.
        """
        pair = OrderTimerPair.get_order_timer_pair(order)

        if pair == None:
            return
            
        pair.stop_timer()


class OrderTimerPair():
    TIMER_DELAY_MS = 5000

    ACTIVE_PAIRS = []

    def __init__(
        self,
        order
    ):
        self._order = order
        self._timer_id = -1

        OrderTimerPair.ACTIVE_PAIRS.append(self)

    # def __del__(self):
    #     self.stop_timer()

    @property
    def order(self):
        return self._order

    @property
    def timer_id(self):
        return self._timer_id

    @staticmethod
    def get_order_timer_pair(order):
        for pair in OrderTimerPair.ACTIVE_PAIRS:
            if pair.order.id == order.id:
                return pair

        return None
    
    def _timer_callback(self):
        OrderTimerPair.ACTIVE_PAIRS.remove(self)

        print(f"Setting order #{self._order.id} as inactive.")
        OrdersService.update_order(order=self._order, active=False)
        
        OrdersService.on_orders_changed()
    
    def start_timer(self):
        self._timer_id = TimerHandler.start_timer(self._timer_callback, OrderTimerPair.TIMER_DELAY_MS)

    def stop_timer(self):
        if self._timer_id == -1:
            return

        OrderTimerPair.ACTIVE_PAIRS.remove(self)

        TimerHandler.cancel_timer(self._timer_id)

