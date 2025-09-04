#!/bin/bash

# Bad practice: no error checking
# Bad practice: hardcoded passwords

echo "Waiting for SQL Server to start..."
sleep 30

echo "Running database initialization script..."
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P MyPass123! -d master -i /scripts/init.sql

echo "Database initialization complete!"

# Bad practice: no verification of success