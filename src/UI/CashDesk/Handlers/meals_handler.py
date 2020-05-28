import mysql.connector as MySQL
import Templates.references as REFS

class MealsHandler:
    def __init__(self):
        self.CONNECTION_READY = False

        print(f"Establishing connection to database '{REFS.CASH_DESK_DB_NAME}' @ {REFS.CASH_DESK_IP}:{REFS.CASH_DESK_DB_PORT} ...", end='')

        self._cursor = None

        # try:
        #     self._connection = MySQL.connect(
        #         host = REFS.CASH_DESK_IP,
        #         port = REFS.CASH_DESK_DB_PORT,
        #         user = REFS.CASH_DESK_DB_USER,
        #         passwd = REFS.CASH_DESK_DB_PW,
        #         database = REFS.CASH_DESK_DB_NAME
        #     )

        #     self._cursor = self._connection.cursor()
        # except MySQL.Error as err:
        #     print("")
        #     if err.errno == MySQL.errorcode.ER_ACCESS_DENIED_ERROR:
        #         print("Something is wrong with your user name or password")
        #     elif err.errno == MySQL.errorcode.ER_BAD_DB_ERROR:
        #         print("Database does not exist")
        #     else:
        #         print(err)
        # else:
        #     self.CONNECTION_READY = True
        #     print(" Done")

        #     self._initialize(self._cursor)

    def __del__(self):
        if self.CONNECTION_READY:
            print("Closing connection to database...")
            # self._connection.close()

    def _initialize(self, cursor):
        print(f"Getting information for table '{REFS.MEALS_TABLE_NAME}'")

        cursor.execute(f"SELECT * FROM {REFS.MEALS_TABLE_NAME} WHERE id = 0")

        self.num_columns = len(cursor.description)
        self.column_names = [i[0] for i in cursor.description]

        cursor.fetchall()

    @property
    def is_connection_ready(self) -> bool:
        return self.CONNECTION_READY

    def get_meal_by_name(self, name: str):
        self._cursor.execute(f"SELECT * FROM {REFS.MEALS_TABLE_NAME} WHERE name = {name}")
        return self._cursor.fetchall()

    def get_meal_by_id(self, id: int):
        self._cursor.execute(f"SELECT * FROM {REFS.MEALS_TABLE_NAME} WHERE id = {id}")
        return self._cursor.fetchall()

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
