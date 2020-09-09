#!/bin/bash

echo "Starting initialization of database 'ordsys' ...";
echo "Make sure to ..";
echo "    .. start this script with 'sudo'";
echo "    .. set the 'root' user's password to 'M9KN;2j.@T7e#E'";

echo "    Creating database, table and users";

mysql -u root "-pM9KN;2j.@T7e#E" < "database_init.sql";

echo "    Filling table";

mysql -u root "-pM9KN;2j.@T7e#E" < "database_fill_table.sql";

echo "Done";

exit 0;
