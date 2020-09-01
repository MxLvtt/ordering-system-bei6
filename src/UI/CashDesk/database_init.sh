#!/bin/bash

echo "Starting initialization of database 'ordsys'...";

mysql -u root "-pYal#8925xNxx" < "database_init.sql";

echo "Done";

exit 0;
