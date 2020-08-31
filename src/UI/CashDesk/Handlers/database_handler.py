import mysql.connector as MySQL
import Templates.references as REFS
from tkinter import messagebox


class DatabaseHandler:
    CONNECTION_READY = False
    CONNECTION = None
    CURSOR = None

    DEBUG = False

    def __init__(self, debug: bool = False):
        self._cursor = None

        DatabaseHandler.DEBUG = debug

        # try:
        #     if not debug:
        #         print(
        #             f"Establishing connection to database '{REFS.CASH_DESK_DB_NAME}' @ {REFS.CASH_DESK_IP}:{REFS.CASH_DESK_DB_PORT} ...", end='')

        #         self._connection = MySQL.connect(
        #             host=REFS.CASH_DESK_IP,
        #             port=REFS.CASH_DESK_DB_PORT,
        #             user=REFS.CASH_DESK_DB_USER,
        #             passwd=REFS.CASH_DESK_DB_PW,
        #             database=REFS.CASH_DESK_DB_NAME
        #         )
        #     else:
        #         print(
        #             f"Establishing connection to database '{REFS.CASH_DESK_DB_NAME}' @ {REFS.CASH_DESK_IP_DBG}:{REFS.CASH_DESK_DB_PORT_DBG} ...", end='')

        #         self._connection = MySQL.connect(
        #             host=REFS.CASH_DESK_IP_DBG,
        #             port=REFS.CASH_DESK_DB_PORT_DBG,
        #             user=REFS.CASH_DESK_DB_USER,
        #             passwd=REFS.CASH_DESK_DB_PW,
        #             database=REFS.CASH_DESK_DB_NAME,
        #             auth_plugin='mysql_native_password'
        #         )

        #     self._cursor = self._connection.cursor()
        #     DatabaseHandler.CURSOR = self._cursor
        #     DatabaseHandler.CONNECTION = self._connection
        # except MySQL.Error as err:
        #     print("")
        #     if err.errno == MySQL.errorcode.ER_ACCESS_DENIED_ERROR:
        #         print("Something is wrong with your user name or password")
        #     elif err.errno == MySQL.errorcode.ER_BAD_DB_ERROR:
        #         print("Database does not exist")
        #     else:
        #         print(err)

        #     messagebox.showerror("Database Connection Error", str(
        #         err) + "\n\nMake sure, the database is running/reachable and restart the software.")
        # else:
        #     DatabaseHandler.CONNECTION_READY = True
        #     print(" Done")

        DatabaseHandler.CONNECTION_READY = True

    def __del__(self):
        DatabaseHandler.disconnect()


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


    @staticmethod
    def connect():
        """ Establishes a new connection to the database.

        Returns the connection and cursor object: (conn, cur)
        """
        if DatabaseHandler.CURSOR != None:
            DatabaseHandler.CURSOR.close()
        if DatabaseHandler.CONNECTION != None:
            DatabaseHandler.CONNECTION.close()

        if not DatabaseHandler.DEBUG:
            if REFS.MAIN_STATION:
                _connection = MySQL.connect(
                    host=REFS.RW_USER_HOST,
                    port=REFS.CASH_DESK_DB_PORT,
                    user=REFS.RW_USER_NAME,
                    passwd=REFS.RW_USER_PASSWORD,
                    database=REFS.CASH_DESK_DB_NAME
                )            
            else:
                _connection = MySQL.connect(
                    host=REFS.CASH_DESK_IP,
                    port=REFS.CASH_DESK_DB_PORT,
                    user=REFS.CASH_DESK_DB_USER,
                    passwd=REFS.CASH_DESK_DB_PW,
                    database=REFS.CASH_DESK_DB_NAME
                )
        else:
            _connection = MySQL.connect(
                host=REFS.CASH_DESK_IP_DBG,
                port=REFS.CASH_DESK_DB_PORT_DBG,
                user=REFS.CASH_DESK_DB_USER,
                passwd=REFS.CASH_DESK_DB_PW,
                database=REFS.CASH_DESK_DB_NAME,
                auth_plugin='mysql_native_password'
            )

        _cursor = _connection.cursor()

        DatabaseHandler.CURSOR = _cursor
        DatabaseHandler.CONNECTION = _connection

        DatabaseHandler.CONNECTION_READY = True

        return (_connection, _cursor)


    @staticmethod
    def disconnect():
        """ Closes the connection to the database.
        """
        if DatabaseHandler.CURSOR != None:
            DatabaseHandler.CURSOR.close()
        if DatabaseHandler.CONNECTION != None:
            DatabaseHandler.CONNECTION.close()


    ######### SPECIFIC METHODS


    @staticmethod
    def get_table_row_count(table_name: str, row_filter: str = "") -> int:
        result = DatabaseHandler.select_from_table(
            table_name, columns=["COUNT(*)"], row_filter=row_filter, disconnect=False)

        if result == None or len(result) < 1 or result[0] == None or len(result[0]) < 1:
            raise RuntimeError(
                f"Result ({result}) of SQL command is empty or Nonetype.")

        DatabaseHandler.disconnect()

        return result[0][0]

    @staticmethod
    def get_table_information(table_name: str) -> (int, []):
        # Dummy-command to get table information, ignore fetched results
        DatabaseHandler.select_from_table(table_name, row_filter="id = 0", disconnect=False)

        num_columns = len(DatabaseHandler.CURSOR.description)
        column_names = [i[0] for i in DatabaseHandler.CURSOR.description]

        DatabaseHandler.disconnect()

        return (num_columns, column_names)


    ######### GENERAL METHODS


    @staticmethod
    def update_table(table_name: str, columns: [], values: [], condition: str):
        DatabaseHandler.connect()

        if DatabaseHandler.CURSOR == None:
            raise RuntimeError(f"DatabaseHandler's cursor is not set.")

        if columns == None or values == None or len(columns) != len(values) or len(columns) == 0 or condition == None or condition == "":
            raise ValueError(
                "The provided arguments do not fit the requirements.")

        # Prepare setter arguments for the command
        setter_arg = f"{columns[0]}={values[0]}"
        for idx, col in enumerate(columns):
            if idx != 0:
                val = values[idx]
                setter_arg = f"{setter_arg},{col}={val}"

        def send_command():
            DatabaseHandler.CURSOR.execute(
                f"UPDATE {table_name} SET {setter_arg} WHERE {condition}"
            )
            DatabaseHandler.CONNECTION.commit()

        # Run the previous method surrounded by try and catch
        DatabaseHandler._surround_by_try_catch(func=send_command)
        
        DatabaseHandler.disconnect()

    @staticmethod
    def delete_from_table(table_name: str, row_filter: str = ""):
        DatabaseHandler.connect()

        if DatabaseHandler.CURSOR == None:
            raise RuntimeError(f"DatabaseHandler's cursor is not set.")

        condition = ""

        if row_filter != "" and row_filter != None:
            condition = f" WHERE {row_filter}"

        def send_command():
            DatabaseHandler.CURSOR.execute(f"DELETE FROM {table_name}{condition}")
            DatabaseHandler.CONNECTION.commit()

        # Run the previous method surrounded by try and catch
        DatabaseHandler._surround_by_try_catch(func=send_command)
        
        DatabaseHandler.disconnect()

    @staticmethod
    def truncate_table(table_name: str):
        DatabaseHandler.connect()

        if DatabaseHandler.CURSOR == None:
            raise RuntimeError(f"DatabaseHandler's cursor is not set.")

        def send_command():
            DatabaseHandler.CURSOR.execute(f"TRUNCATE TABLE {table_name}")
            DatabaseHandler.CONNECTION.commit()

        # Run the previous method surrounded by try and catch
        DatabaseHandler._surround_by_try_catch(func=send_command)
        
        DatabaseHandler.disconnect()

    @staticmethod
    def insert_into_table(table_name: str, columns: [], values: []):
        """ Sends the following sql command to the database:

        INSERT INTO {table_name} ({columns[0]},{columns[1]},...) VALUES ({values[0]},{values[1]},...)
        """
        DatabaseHandler.connect()

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
        
        DatabaseHandler.disconnect()

    @staticmethod
    def select_from_table(table_name: str, columns: [] = [], row_filter: str = "", order_by: str = "", disconnect: bool = True):
        """ Sends the following sql command to the database:

        SELECT {columns[0]},{columns[1]},... FROM {table_name} [WHERE {row_filter}] [ORDER BY {order_by}]

        If columns is [] (default), the column identifier will be "*".
        The condition is only used, if the row_filter parameter is set.
        Sorting is only used, if the order_by parameter is set.

        order_by: "col1 ASC, col2 DESC"
        """
        DatabaseHandler.connect()

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
        sorting = ""

        if row_filter != "" and row_filter != None:
            condition = f" WHERE {row_filter}"

        if order_by != "" and order_by != None:
            sorting = f" ORDER BY {order_by}"

        def send_command():
            DatabaseHandler.CURSOR.execute(
                f"SELECT {cols_identifier} FROM {table_name}{condition}{sorting}"
            )
            return DatabaseHandler.CURSOR.fetchall()

        # Run the previous method surrounded by try and catch
        results = DatabaseHandler._surround_by_try_catch(func=send_command)
        
        if disconnect:
            DatabaseHandler.disconnect()

        return results
