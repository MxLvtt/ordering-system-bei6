from order_prototype import Order

class DBHandler():
    def __init__(self):
        pass

    def add_order_to_db(self, order: Order):
        """ Adds a new entry to the database, based on the information
        given in the 'order' object.
        """
        order_number = order.number
        order_time = order.timestamp
        order_category = order.category
        order_status = order.status
        pass

    def get_order_from_db(self, order_number: int = -1, timestamp: str = ""):
        """ Returns an entry from the database, that matches the given conditions/attributes.
        Not all attributes have to be set: If you only want to search with the order_number, 
        then only set the order_number parameter in the function call.
        """
        pass

db_handler = DBHandler()
db_handler.add_order_to_db(Order())
db_handler.add_order_to_db(Order(
    182,
    "20:21:03",
    0,
    1
))
