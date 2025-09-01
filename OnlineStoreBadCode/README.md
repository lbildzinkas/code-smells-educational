# Online Store Bad Code API

This is an intentionally poorly designed .NET 8 Web API created for educational purposes. It demonstrates numerous code smells and anti-patterns that should be refactored using good software engineering practices.

## 🚨 WARNING: DO NOT USE IN PRODUCTION

This code is intentionally bad and contains:
- Security vulnerabilities (SQL injection, hardcoded credentials)
- Poor design patterns
- No proper error handling
- Global state management issues

## Code Smells Included

### 1. **God Controller** (MainController.cs - 900+ lines)
- Single controller handling all operations
- Mixed responsibilities
- No separation of concerns

### 2. **Global State** (GlobalVariables.cs)
- Static mutable variables
- Hardcoded connection strings and API keys
- Shopping cart stored globally

### 3. **SQL Injection Vulnerabilities**
- String concatenation for SQL queries
- No parameterized queries
- Direct user input in SQL

### 4. **Poor Error Handling**
- Generic catch blocks
- Swallowing exceptions
- Exposing internal errors to users

### 5. **Magic Numbers**
- Hardcoded values throughout code
- No constants or configuration
- Business rules scattered

### 6. **Duplicate Code**
- Copy-pasted database connections
- Repeated validation logic
- Similar methods with slight variations

### 7. **Deeply Nested Code**
- Payment processing with 5+ levels of nesting
- Complex if-else chains
- Giant switch statements

### 8. **Poor Naming**
- Variables like `temp`, `data`, `x`, `obj`
- Classes like `Stuff` and `Helper`
- Inconsistent naming conventions

### 9. **Mixed Responsibilities**
- Controllers doing business logic
- Data access in controllers
- UI generation in helpers

### 10. **No Abstraction**
- Direct SQL in controllers
- No interfaces or dependency injection
- Tight coupling everywhere

## How to Run

### Prerequisites
- Docker & Docker Compose
- .NET 8 SDK

### Database Setup (Using Docker)
1. **Start the SQL Server database:**
   ```bash
   docker-compose up -d
   ```
   This will:
   - Start SQL Server 2022 in a Docker container
   - Create the OnlineStore database
   - Initialize tables with sample data
   - Expose the database on localhost:1433

2. **Wait for initialization** (about 30-60 seconds)
   - The database needs time to start and run the initialization script
   - Check logs: `docker-compose logs -f sqlserver`

### API Setup
1. Install .NET 8 SDK
2. Clone this repository
3. Navigate to the project folder
4. Run: `dotnet restore`
5. Run: `dotnet run --urls=http://localhost:5000`
6. Open browser to: http://localhost:5000/swagger

### Sample Data Available
- **Users**: admin@store.com, user@store.com, test@store.com
- **Products**: 10 sample products with IDs 1000-1009
- **Orders**: 3 sample orders with different statuses

### Testing the API
- Use the included `sample-requests.http` file for testing endpoints
- Use Swagger UI at http://localhost:5000/swagger
- Run the test script: `./test-api.sh` (tests working and broken endpoints)

### Known Issues (Intentional Bad Code!)
- Login endpoint fails due to bad dynamic type handling
- Payment processing has similar JSON parsing issues  
- Stats endpoint exposes internal application state
- No proper error handling or validation
- SQL injection vulnerabilities throughout

### Cleanup
```bash
# Stop containers
docker-compose down

# Remove database data (start fresh)
docker-compose down -v
sudo rm -rf ./sqldata
```

## API Endpoints

### Products
- `GET /api/main/GetProduct?id={id}`
- `POST /api/main/AddProduct`
- `PUT /api/main/UpdateProduct?id={id}`
- `DELETE /api/main/DeleteProduct?id={id}`
- `GET /api/main/SearchProducts`

### Orders
- `POST /api/main/CreateOrder`
- `GET /api/main/GetOrder?id={id}`
- `PUT /api/main/UpdateOrderStatus?orderId={id}&newStatus={status}`

### Shopping Cart
- `POST /api/main/AddToCart`
- `GET /api/main/GetCart`
- `DELETE /api/main/RemoveFromCart?index={index}`
- `POST /api/main/ClearCart`

### Payment
- `POST /api/main/ProcessPayment`

### Users
- `POST /api/main/Login`
- `POST /api/main/Logout`
- `POST /api/main/Register`

## Default Credentials
- Admin: `admin@store.com` / `admin123`
- User: `user@store.com` / `user123`

## Database Schema (Intentionally Bad!)

The database schema demonstrates poor design practices:
- No primary keys or foreign keys
- No indexes for performance
- String-based dates instead of datetime
- No constraints or validation
- Mixed data types and responsibilities

See `Database/init.sql` for the complete poorly designed schema.

## Refactoring Opportunities

This codebase is perfect for teaching:
- SOLID principles
- Design patterns (Repository, Unit of Work, etc.)
- Dependency injection
- Clean architecture
- Security best practices
- Error handling strategies
- Code organization
- Testing approaches

## Educational Use

Use this project to:
1. Identify code smells
2. Practice refactoring techniques
3. Implement design patterns
4. Add proper security
5. Introduce testing
6. Apply clean code principles

Remember: This is how NOT to write production code!