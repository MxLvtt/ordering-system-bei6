from order_prototype import Order
import mysql.connector

class DBHandler():
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="database_for_order"
        )
        self.cursor = self.db.cursor()

    def create_data_base(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS database_for_order")

    def create_table_for_data_base(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Table_Orders(id INT AUTO_INCREMENT PRIMARY KEY,order_number VARCHAR(255),order_time VARCHAR(255),order_category VARCHAR(255),order_status VARCHAR(255))")

    def add_order_to_db(self, order: Order):
        """ Adds a new entry to the database, based on the information
        given in the 'order' object.
        """
        order_number = order.number
        order_time = order.timestamp
        order_category = order.category
        order_status = order.status
        query = "INSERT INTO Table_Orders(order_number,order_time,order_category,order_status) VALUES(%s,%s,%s,%s)"
        values = (order_number, order_time, order_category, order_status)
        self.cursor.execute(query, values)
        self.db.commit()
        print("Orders Added")

    def get_order_from_db(self,id: int, order_number: int = -1, order_time: str = ""):
        """ Returns an entry from the database, that matches the given conditions/attributes.
        Not all attributes have to be set: If you only want to search with the order_number,
        then only set the order_number parameter in the function call.
        """
        query = "SELECT * FROM Table_Orders WHERE id=%s OR order_number=%s OR order_time=%s"
        values = (id, order_number, order_time)
        self.cursor.execute(query, values)
        order = self.cursor.fetchall()
        return order

db_handler = DBHandler()
db_handler.create_data_base()
db_handler.create_table_for_data_base()
#db_handler.add_order_to_db(Order())
#db_handler.add_order_to_db(Order(185,"25:22:03",0,1))
order1 = db_handler.get_order_from_db(3)
print(order1)

