import mysql.connector as MySQL
import Templates.references as REFS
from tkinter import messagebox


class DatabaseHandler:
    CONNECTION_READY = False
    CONNECTION = None
    CURSOR = None

    def __init__(self, debug: bool = False):
        self._cursor = None

        try:
            if not debug:
                print(
                    f"Establishing connection to database '{REFS.CASH_DESK_DB_NAME}' @ {REFS.CASH_DESK_IP}:{REFS.CASH_DESK_DB_PORT} ...", end='')

                self._connection = MySQL.connect(
                    host=REFS.CASH_DESK_IP,
                    port=REFS.CASH_DESK_DB_PORT,
                    user=REFS.CASH_DESK_DB_USER,
                    passwd=REFS.CASH_DESK_DB_PW,
                    database=REFS.CASH_DESK_DB_NAME
                )
            else:
                print(
                    f"Establishing connection to database '{REFS.CASH_DESK_DB_NAME}' @ {REFS.CASH_DESK_IP_DBG}:{REFS.CASH_DESK_DB_PORT_DBG} ...", end='')

                self._connection = MySQL.connect(
                    host=REFS.CASH_DESK_IP_DBG,
                    port=REFS.CASH_DESK_DB_PORT_DBG,
                    user=REFS.CASH_DESK_DB_USER,
                    passwd=REFS.CASH_DESK_DB_PW,
                    database=REFS.CASH_DESK_DB_NAME,
                    auth_plugin='mysql_native_password'
                )

            self._cursor = self._connection.cursor()
            DatabaseHandler.CURSOR = self._cursor
            DatabaseHandler.CONNECTION = self._connection
        except MySQL.Error as err:
            print("")
            if err.errno == MySQL.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == MySQL.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

            messagebox.showerror("Database Connection Error", str(
                err) + "\n\nMake sure, the database is running/reachable and restart the software.")
        else:
            DatabaseHandler.CONNECTION_READY = True
            print(" Done")

    def __del__(self):
        if DatabaseHandler.CONNECTION_READY:
            print("Closing connection to database...")
            self._connection.close()


    ######### PROPERTIES


    @property
    def is_connection_ready(self) -> bool:
        return DatabaseHandler.CONNECTION_READY


    ######### PRIVATE METHODS 


    @staticmethod
    def _surround_by_try_catch(func):
        if func == None or not callable(func):
            raise RuntimeError("The given function is of Nonetype.")

        try:
            if DatabaseHandler.CONNECTION_READY:
                return func()
            else:
                raise RuntimeError("The database connection is not ready yet.")
        except MySQL.Error as err:
            print("")
            if err.errno == MySQL.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == MySQL.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

            messagebox.showerror("Database Connection Error", str(err))

        raise RuntimeError("Reached the end of the function.")


    ######### SPECIFIC METHODS


    @staticmethod
    def get_table_row_count(table_name: str, row_filter: str = "") -> int:
        if DatabaseHandler.CURSOR == None:
            print(f"DatabaseHandler's cursor is not set.")
            return 0

        result = DatabaseHandler.select_from_table(
            table_name, columns=["COUNT(*)"], row_filter=row_filter)

        if result == None or len(result) < 1 or result[0] == None or len(result[0]) < 1:
            raise RuntimeError(
                f"Result ({result}) of SQL command is empty or Nonetype.")

        return result[0][0]

    @staticmethod
    def get_table_information(table_name: str) -> (int, []):
        if DatabaseHandler.CURSOR == None:
            print(f"DatabaseHandler's cursor is not set.")
            return (0, [])

        # Dummy-command to get table information, ignore fetched results
        DatabaseHandler.select_from_table(table_name, row_filter="id = 0")

        num_columns = len(DatabaseHandler.CURSOR.description)
        column_names = [i[0] for i in DatabaseHandler.CURSOR.description]

        return (num_columns, column_names)


    ######### GENERAL METHODS


    @staticmethod
    def truncate_table(table_name: str):
        if DatabaseHandler.CURSOR == None:
            raise RuntimeError(f"DatabaseHandler's cursor is not set.")

        def send_command():
            DatabaseHandler.CURSOR.execute(f"TRUNCATE TABLE {table_name}")
            DatabaseHandler.CONNECTION.commit()

        # Run the previous method surrounded by try and catch
        DatabaseHandler._surround_by_try_catch(func=send_command)

    @staticmethod
    def insert_into_table(table_name: str, columns: [], values: []):
        """ Sends the following sql command to the database:

        INSERT INTO {table_name} ({columns[0]},{columns[1]},...) VALUES ({values[0]},{values[1]},...)
        """

        if DatabaseHandler.CURSOR == None:
            raise RuntimeError(f"DatabaseHandler's cursor is not set.")

        if columns == None or values == None or len(columns) != len(values) or len(columns) == 0:
            raise ValueError(
                "The provided arguments do not fit the requirements.")

        # Prepare column arguments for the command
        columns_arg = f"{columns[0]}"
        for idx, col in enumerate(columns):
            if idx != 0:
                columns_arg = f"{columns_arg},{col}"

        # Prepare value arguments for the command
        values_arg = f"{values[0]}"
        for idx, val in enumerate(values):
            if idx != 0:
                values_arg = f"{values_arg},{val}"

        def send_command():
            DatabaseHandler.CURSOR.execute(
                f"INSERT INTO {table_name} ({columns_arg}) VALUES ({values_arg})"
            )
            DatabaseHandler.CONNECTION.commit()

        # Run the previous method surrounded by try and catch
        DatabaseHandler._surround_by_try_catch(func=send_command)

    # TODO: Test select_from_table

    @staticmethod
    def select_from_table(table_name: str, columns: [] = [], row_filter: str = ""):
        """ Sends the following sql command to the database:

        SELECT {columns[0]},{columns[1]},... FROM {table_name} [WHERE {row_filter}]

        The condition is only used, if the row_filter parameter is set.
        """

        if DatabaseHandler.CURSOR == None:
            raise RuntimeError(f"DatabaseHandler's cursor is not set.")

        if columns == None:
            raise ValueError(
                "The provided argument does not fit the requirements.")

        cols_identifier = ""

        if len(columns) > 0:
            cols_identifier = f"{columns[0]}"
            for idx, col in enumerate(columns):
                if idx != 0:
                    cols_identifier = f"{cols_identifier},{col}"
        else:
            cols_identifier = "*"

        condition = ""

        if row_filter != "" and row_filter != None:
            condition = f" WHERE {row_filter}"

        def send_command():
            DatabaseHandler.CURSOR.execute(
                f"SELECT {cols_identifier} FROM {table_name}{condition}"
            )
            return DatabaseHandler.CURSOR.fetchall()

        # Run the previous method surrounded by try and catch
        return DatabaseHandler._surround_by_try_catch(func=send_command)
