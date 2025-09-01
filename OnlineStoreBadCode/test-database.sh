#!/bin/bash

# Bad practice: no error handling in script
# Test script to verify database is working

echo "🧪 Testing Database Connection..."

# Check if container is running
if ! docker ps | grep -q "onlinestore-sqlserver"; then
    echo "❌ SQL Server container is not running!"
    echo "Run: docker-compose up -d"
    exit 1
fi

echo "✅ Container is running"

# Test database connection
echo "🔌 Testing database connection..."

# Bad practice: password in command
docker exec onlinestore-sqlserver /opt/mssql-tools/bin/sqlcmd \
    -S localhost -U sa -P MyPass123! \
    -Q "SELECT COUNT(*) as ProductCount FROM OnlineStore.dbo.Products; SELECT COUNT(*) as UserCount FROM OnlineStore.dbo.Users;"

if [ $? -eq 0 ]; then
    echo "✅ Database connection successful!"
    echo "✅ Sample data is available"
    echo ""
    echo "🚀 You can now start the API with: dotnet run --urls=http://localhost:5000"
else
    echo "❌ Database connection failed!"
    echo "Wait a bit longer for initialization or check logs:"
    echo "docker-compose logs sqlserver"
fi