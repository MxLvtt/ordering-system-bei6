#!/bin/bash

echo "Starting initialization of database 'ordsys'...";

echo "    Creating database, table and users";

mysql -u root "-pYal#8925xNxx" < "database_init.sql";

echo "    Filling table";

mysql -u root "-pYal#8925xNxx" < "database_fill_table.sql";

echo "Done";

exit 0;
