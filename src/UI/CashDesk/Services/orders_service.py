import Templates.references as REFS
from EventHandler.Event import Event
from Templates.order import Order
from Handlers.database_handler import DatabaseHandler


class OrdersService():
    initialized = False
    counter = 0

    # Events
    on_order_created_event: Event = Event()

    def __init__(self):
        # TODO: ?

        OrdersService.initialized = True

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

        # Get the order's id in the database table
        num_active_orders = DatabaseHandler.get_table_row_count(
            table_name=REFS.ORDERS_TABLE_NAME,
            # row_filter=f"{REFS.ORDERS_TABLE_ACTIVE}='{REFS.ORDERS_TABLE_ACTIVE_TRUE}'"
        )

        # Set the order's internal id property to the number of active orders + 1
        new_order.id = num_active_orders + 1

        # Defining sql query contents
        columns = [
            REFS.ORDERS_TABLE_NUMBER,
            REFS.ORDERS_TABLE_TIMESTAMP,
            REFS.ORDERS_TABLE_FORM,
            REFS.ORDERS_TABLE_STATE,
            REFS.ORDERS_TABLE_ACTIVE
        ]

        active = 'Y'

        values = [
            new_order.id,
            new_order.timestamp,
            new_order.form,
            new_order.state,
            f"'{active}'"
        ]

        # Insert new order into the database table
        DatabaseHandler.insert_into_table(REFS.ORDERS_TABLE_NAME, columns, values)

        # Increment counter of added orders
        OrdersService.counter = OrdersService.counter + 1

        # Trigger event to inform others of a change in the orders-list
        OrdersService.on_order_created_event(new_order)

        # Return the newly created order object with the updated information
        return new_order
