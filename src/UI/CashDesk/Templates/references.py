import math

MOBILE = False
MAIN_STATION = True
NEW_VERSION = True

# NETWORK
CASH_DESK_IP = "192.168.2.115"              # set as static ip of raspberry
CASH_DESK_DB_PORT = "8457"                  # port on which to access the database remotely
CASH_DESK_IP_DBG = "127.0.0.1"              # debugging endpoint
CASH_DESK_DB_PORT_DBG = "3306"              # debugging port
CASH_DESK_DB_USER = "ordsysRD"              # user with just read-access
CASH_DESK_DB_PW = "he=h5bY&x#Lb/=$"         # password for above user
CASH_DESK_DB_NAME = "ordsys"                # name of the database

PUBLIC_KEY_16BIT = "(YHJ{5PcL/s-+e6}"

CASHDESK_SERVER_IP = "127.0.0.1" # CASH_DESK_IP
CASHDESK_SERVER_PORT = 1489

KITCHEN_SERVER_IP = "127.0.0.1"
KITCHEN_SERVER_PORT = 1487

MESSAGE_LENGTH = 200                        # Length of a message in bytes
RECEIVE_REFRESH_DELAY = 1000                # Refresh delay in milliseconds

HANDSHAKE_MSG = "ACKNOWLEDGEMENT"

IDENTIFIER_LENGTH = 5
MAX_IDENTIFIER = int(math.pow(10,IDENTIFIER_LENGTH) - 1)
FORMAT_STRING = "{:0" + str(IDENTIFIER_LENGTH) + "d}"
IDENTIFIER_DELIMITER = "#"

# MEALS
MEALS_TABLE_NAME = "meals"                  # name of the table containing all available meals
MEALS_TABLE_ID_COLUMN = "id"                # name of the 'id' column
MEALS_TABLE_KATEGORIE_COLUMN = "kategorie"  # name of the 'kategorie' column
MEALS_TABLE_NAME_COLUMN = "name"            # name of the 'name' column
MEALS_TABLE_ZUTATEN_COLUMN = "zutaten"      # name of the 'zutaten' column
MEALS_TABLE_ADDONS_COLUMN = "addons"        # name of the 'addons' column
MEALS_TABLE_GROESSEN_COLUMN = "groessen"    # name of the 'groessen' column
MEALS_TABLE_PRICE_COLUMN = "price"          # name of the 'price' column
MEALS_AMOUNT_IDENTIFIER = "amount"
LIST_DELIMITER = ";"
CATEGORY_DELIMITER = "/"
MEAL_CODE_DELIMITER = "%"
MEAL_CODES_DELIMITER = "|"
MEAL_PRICE_DELIMITER = "@"

MEALS_BASE_PRICE = "Basispreis"
MEALS_BASE_PRICE_SHORT = "BASIS"
MEALS_TOTAL_PRICE_SHORT = "GESAMT"
MEALS_SINGLE_PRICE_SHORT = "EINZEL"
MEALS_NETTO_PRICE_SHORT = "NETTO"

CURRENCY = "€"

MWST_PROZENT = 19.0
MWST_TEXT_RECEIPT = "davon {0}% MWST"
RECEIPTS_FOLDER_NAME = "__receipts"

INGREDIENTS_LABEL = 'Zutaten'
ADDONS_LABEL = 'Extras'
SIZES_LABEL = 'Größen'
SIZE_LABEL = 'Größe'

# ORDERS # TODO
ORDERS_TABLE_NAME = "orders"
ORDERS_TABLE_ID = "id"
# ORDERS_TABLE_NUMBER = "number"
ORDERS_TABLE_TIMESTAMP = "timestamp"
ORDERS_TABLE_FORM = "form"
ORDERS_TABLE_STATE = "state"
ORDERS_TABLE_ACTIVE = "active"
ORDERS_TABLE_ACTIVE_TRUE = "Y"
ORDERS_TABLE_ACTIVE_FALSE = "N"
ORDERS_TABLE_PRICE = "price"
ORDERS_TABLE_MEALS = "meals"

# GERMAN
ORDERS_TABLE_NAME_GER = "Bestellungen"
ORDERS_TABLE_ID_GER = "Nummer"
# ORDERS_TABLE_NUMBER_GER = "Nummer"
ORDERS_TABLE_TIMESTAMP_GER = "Zeitstempel"
ORDERS_TABLE_FORM_GER = "Art"
ORDERS_TABLE_STATE_GER = "Status"
ORDERS_TABLE_ACTIVE_GER = "Aktiv?"
ORDERS_TABLE_ACTIVE_TRUE_GER = "Ja"
ORDERS_TABLE_ACTIVE_FALSE_GER = "Nein"
ORDERS_TABLE_PRICE_GER = "Preis"
ORDERS_TABLE_MEALS_GER = "Gerichte"

HISTORY_TABLE_EDIT = "Bearbeiten"
HISTORY_TABLE_EXPAND = ""

# COLORS
LIGHT_GRAY = "#D6D6D1"
LIGHT_GREEN = "#BEF291"
LIGHT_YELLOW = "#FFE48C"
LIGHT_RED = "#DD726C"
LIGHT_CYAN = "#B7EDFF"

DARK_GRAY = "#666663"

LIGHTER_GRAY = "#B7B7B7"
LIGHTER_GREEN = "#C1D3B1"
LIGHTER_YELLOW = "#DDD3B3"
LIGHTER_RED = "#DBB5B3"

LIGHTEST_RED = "#FF9B9B"
LIGHTEST_GREEN = "#BBFF9E"

# TEXTS
ADDORDERVIEW_TITLE = "Neue Bestellung aufnehmen"    # displayed title for the AddOrderView
ACTIVEORDERSVIEW_TITLE = "Aktive Bestellungen"      # displayed title for the ActiveOrdersView
CURRENT_ORDER_TITLE = "Aktuelle Bestellung"         # displayed title for the CurrentOrderView
RECEIPT_TITLE = "Kassenzettel"                      # displayed title for the ReceiptView
SETTINGSVIEW_TITLE = "Einstellungen"                # displayed title for the SettingsView
HISTORYVIEW_TITLE = "Bestellverlauf"                # displayed title for the HistoryView

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

ORDER_STATE_COLORS=[
    LIGHT_GRAY,
    LIGHT_GREEN,
    LIGHT_YELLOW,
    LIGHT_RED
]

ORDER_STATE_COLORS_BGD=[
    LIGHTER_GRAY,
    LIGHTER_GREEN,
    LIGHTER_YELLOW,
    LIGHTER_RED
]

ORDER_FORMS=[                                       # names of the different forms of orders
    "Im Haus", # "Hier essen",
    "To Go"    # "Mitnehmen"
]
EAT_IN=0                                            # indices for the order forms array
TAKEAWAY=1

DEFAULT_FORM = EAT_IN

# RECEIPT
RESTAURANT_NAME = "RestaurantXYZ"
EMPLOYEE_NAME = "MitarbeiterABC"

# MESSAGE PREFIXES

DB_CHANGED_PREFIX = "C"
SILENT_PREFIX = "S"
ORDER_CREATED_PREFIX = "N"
ORDER_CHANGED_PREFIX = "M"

# TOAST NOTIFICATIONS

ORDER_CREATED_TOAST = (
    "Neue Bestellung",
    "Bestellnummer: {0}\nZeitstempel: {1}"
)

ORDER_CHANGED_TOAST = (
    "Bestellung geändert",
    "Bestellnummer: {0}\nZeitstempel: {1}\nÄnderung: {2}"
)

ORDER_SUMMARY_TOAST = (
    "Bestellung erstellt",
    "Bestellnummer: {0}\nMahlzeit: {1}\nPreis: {2}"
)
