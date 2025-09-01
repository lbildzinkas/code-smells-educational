#!/bin/bash

# Bad practice: no error handling in shell script
# Bad practice: hardcoded wait time

# Wait for SQL Server to start
echo "Waiting for SQL Server to start..."
sleep 30

# Bad practice: password in command line
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P MyPass123! -d master -i /docker-entrypoint-initdb.d/init.sql

echo "Database initialization complete!"