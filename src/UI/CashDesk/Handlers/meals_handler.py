import mysql.connector as MySQL
import Templates.references as REFS
from Templates.category import Category
from tkinter import messagebox
from EventHandler.Event import Event

class MealsHandler:
    CONNECTION_READY = False
    CURSOR = None

    COLUMN_NAMES = []
    NUM_COLUMNS = 0

    def __init__(self, connection_ready_event: Event):
        print(f"Establishing connection to database '{REFS.CASH_DESK_DB_NAME}' @ {REFS.CASH_DESK_IP}:{REFS.CASH_DESK_DB_PORT} ...", end='')

        self._cursor = None

        try:
            self._connection = MySQL.connect(
                host = REFS.CASH_DESK_IP,
                port = REFS.CASH_DESK_DB_PORT,
                user = REFS.CASH_DESK_DB_USER,
                passwd = REFS.CASH_DESK_DB_PW,
                database = REFS.CASH_DESK_DB_NAME
            )

            self._cursor = self._connection.cursor()
            MealsHandler.CURSOR = self._cursor
        except MySQL.Error as err:
            print("")
            if err.errno == MySQL.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == MySQL.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

            messagebox.showerror("Database Connection Error", str(err) + "\n\nMake sure, the database is running/reachable and restart the software.")
        else:
            MealsHandler.CONNECTION_READY = True
            print(" Done")
            
            self._initialize(self._cursor)

            # Sending the Event to trigger all related methods
            connection_ready_event()

    def __del__(self):
        if MealsHandler.CONNECTION_READY:
            print("Closing connection to database...")
            # self._connection.close()

    def _initialize(self, cursor):
        print(f"Getting information for table '{REFS.MEALS_TABLE_NAME}'")

        cursor.execute(f"SELECT * FROM {REFS.MEALS_TABLE_NAME} WHERE id = 0")

        self.NUM_COLUMNS = len(cursor.description)
        self.COLUMN_NAMES = [i[0] for i in cursor.description]

        cursor.fetchall()

    @property
    def is_connection_ready(self) -> bool:
        return MealsHandler.CONNECTION_READY

    def get_meal_by_name(self, name: str):
        self._cursor.execute(f"SELECT * FROM {REFS.MEALS_TABLE_NAME} WHERE name = {name}")
        return self._cursor.fetchall()

    def get_meal_by_id(self, id: int):
        self._cursor.execute(f"SELECT * FROM {REFS.MEALS_TABLE_NAME} WHERE id = {id}")
        return self._cursor.fetchall()

    @staticmethod
    def get_raw_meals():
        """ Returns an array of all meals in the database in their raw form.
        """
        if MealsHandler.CONNECTION_READY:
            MealsHandler.CURSOR.execute(f"SELECT * FROM {REFS.MEALS_TABLE_NAME}")
            return MealsHandler.CURSOR.fetchall()
        else:
            return []

    @staticmethod
    def split_meals_by_categories(meals) -> Category:
        """ Splits the given list of meals (in raw format) up into their categories
        and return the root category
        """
        root: Category = Category("root")
        
        # Create Category-Tree by adding subcategories to root and so on
        for meal in meals:
            category_value = meal[1]
            name_value = meal[2]

            # TODO: CHECK IF THE CATEGORIES CONTENT IS VALID AND NOT NULL!
            # TODO: IF NULL, THEN THE FOR-LOOP IN THE MIDDLE SHOULD BE SKIPPED! -> only add meal-cat and meal-object

            # Extract subcategories and split up into a separate array -> ['Getraenke', 'Kalt', 'Alkoholfrei']
            subcats_arr = category_value.split('/')
            prev_cat = root

            # For every category in subcategories
            for subcat in subcats_arr:
                # Add the subcategory to the previous category (ignore if existant)
                # And set the previous category to the current subcategory
                prev_cat = prev_cat.add(subcat)
            
            # Create object of class Meal with the data given from the database (-> 'meal')
            meal_object: Meal = Meal(meal)

            # Create on last subcategory named like the meal itself
            # And add the meal object to this new subcategory
            prev_cat.add(name_value).insert_meal(meal_object)
        
        return root


class Meal(object):
    def __init__(self, database_content):
        # TODO: generate object of class meal from the given meal database-data
        pass

# connection = MySQL.connect(
#     host="192.168.2.116",
#     port="8457",
#     user="marcel",
#     passwd="3482657ml",
#     database="meals"
# )

# cursor = connection.cursor()

# cursor.execute("SELECT * FROM mains")

# result = cursor.fetchall()

# for line in result:
#     print(line)
