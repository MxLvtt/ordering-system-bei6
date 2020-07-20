from cashdesk_gui import CashDeskGUI
import sys

is_mobile_view = True
is_main_station = True
is_debug = False

def check_arg(arg_name, arg_value, parameter_name, default_value) -> bool:
    if parameter_name in arg_name.lower():
        if arg_value == '0' or arg_value == 'false':
            return False
        elif arg_value == '1' or arg_value == 'true':
            return True

    return default_value

# Step 1: Read command line arguments
# If a VALID argument is given, then dont do Step 2 for that specific argument
for arg in sys.argv:
    if "=" in arg:
        var = arg.split('=')[0]
        val = arg.split('=')[1]

        is_mobile_view = not check_arg(var, val, 'fullscreen', is_mobile_view)
        is_main_station = check_arg(var, val, 'main', is_main_station)
        is_debug = check_arg(var, val, 'debug', is_debug)

# Step 2: Read config file (lower prio than cmd args)
# TODO

print(f"Starting ordering system with following settings:")

if is_mobile_view:
    print(f"View: mobile")
else:
    print(f"View: fullscreen")

if is_main_station:
    print(f"Station: cashdesk")
else:
    print(f"Station: kitchen")

CashDeskGUI(
    mobile_view = is_mobile_view,
    main_station = is_main_station,
    debug = is_debug
)
