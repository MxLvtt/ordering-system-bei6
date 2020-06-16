# NETWORK
CASH_DESK_IP = "192.168.2.115"              # set as static ip of raspberry
CASH_DESK_DB_PORT = "8457"                  # port on which to access the database remotely
CASH_DESK_IP_DBG = "127.0.0.1"              # debugging endpoint
CASH_DESK_DB_PORT_DBG = "3306"              # debugging port
CASH_DESK_DB_USER = "ordsysRD"              # user with just read-access
CASH_DESK_DB_PW = "he=h5bY&x#Lb/=$"         # password for above user
CASH_DESK_DB_NAME = "ordsys"                # name of the database

# MEALS
MEALS_TABLE_NAME = "meals"                  # name of the table containing all available meals
MEALS_TABLE_ID_COLUMN = "id"                # name of the 'id' column
MEALS_TABLE_KATEGORIE_COLUMN = "kategorie"  # name of the 'kategorie' column
MEALS_TABLE_NAME_COLUMN = "name"            # name of the 'name' column
MEALS_TABLE_ZUTATEN_COLUMN = "zutaten"      # name of the 'zutaten' column
MEALS_TABLE_ADDONS_COLUMN = "addons"        # name of the 'addons' column
MEALS_TABLE_GROESSEN_COLUMN = "groessen"    # name of the 'groessen' column
LIST_DELIMITER = ";"
CATEGORY_DELIMITER = "/"

# ORDERS # TODO
ORDERS_TABLE_NAME = "orders"
ORDERS_TABLE_ID = "id"
ORDERS_TABLE_NUMBER = "number"
ORDERS_TABLE_TIMESTAMP = "timestamp"
ORDERS_TABLE_FORM = "form"
ORDERS_TABLE_STATE = "state"
ORDERS_TABLE_ACTIVE = "active"
ORDERS_TABLE_ACTIVE_TRUE = "Y"
ORDERS_TABLE_ACTIVE_FALSE = "N"

# COLORS
LIGHT_GRAY = "#D6D6D1"
LIGHT_GREEN = "#BEF291"
LIGHT_YELLOW = "#FFE48C"
LIGHT_RED = "#DD726C"

# TEXTS
ADDORDERVIEW_TITLE = "Neue Bestellung aufnehmen"    # displayed title for the AddOrderView
ACTIVEORDERSVIEW_TITLE = "Aktive Bestellungen"      # displayed title for the ActiveOrdersView
CURRENT_ORDER_TITLE = "Aktuelle Bestellung"         # displayed title for the CurrentOrderView

ORDER_STATES=[                                      # names of the different order states
    "Offen",
    "Fertig",
    "Verändert",
    "Verworfen"
]
OPEN=0                                              # indices for the order states array
PREPARED=1
CHANGED=2
CANCELED=3

ORDER_FORMS=[                                       # names of the different forms of orders
    "Hier essen",
    "Mitnehmen"
]
EAT_IN=0                                            # indices for the order forms array
TAKEAWAY=1
