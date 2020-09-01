#!/bin/bash

echo "Filling table 'meals' with content ...";
echo "Make sure to ..";
echo "    .. start this script with 'sudo'";
echo "    .. set the 'root' user's password to 'M9KN;2j.@T7e#E'";

mysql -u root "-pM9KN;2j.@T7e#E" < "database_fill_table.sql";

echo "Done";

exit 0;
