# Online Store Bad Code API (Python Version)

This is an intentionally poorly designed Python FastAPI created for educational purposes. It demonstrates numerous code smells and anti-patterns that should be refactored using good software engineering practices.

## 🚨 WARNING: DO NOT USE IN PRODUCTION

This code is intentionally bad and contains:
- Security vulnerabilities (SQL injection, hardcoded credentials)
- Poor design patterns
- No proper error handling
- Global state management issues
- Python-specific anti-patterns

## Python-Specific Code Smells Included

### 1. **God Module** (main.py - 500+ lines)
- Single module handling all operations
- Mixed responsibilities
- No separation of concerns

### 2. **Global State** (global_variables.py)
- Module-level mutable variables
- Hardcoded connection strings and API keys
- Shopping cart stored globally

### 3. **SQL Injection Vulnerabilities**
- String formatting for SQL queries
- No parameterized queries
- Direct user input in SQL

### 4. **Poor Error Handling**
- Bare except clauses
- Swallowing exceptions
- Exposing internal errors to users

### 5. **Import Chaos**
- Star imports (`from module import *`)
- Imports in the middle of files
- Circular import potential

### 6. **No Type Hints**
- Missing or inconsistent type annotations
- Using `dict` instead of Pydantic models
- Dynamic typing everywhere

### 7. **Mutable Defaults**
- Functions with mutable default arguments
- Global state modification
- Side effects in functions

### 8. **Mixed Async/Sync**
- Sync database calls in async framework
- No proper async/await usage
- Blocking operations

### 9. **String Formatting Inconsistency**
- Mix of %, .format(), and f-strings
- SQL injection through formatting
- No validation

### 10. **Poor Resource Management**
- No connection pooling
- Manual connection handling
- Resource leaks

## How to Run

### Prerequisites
- Python 3.8+ (but we don't specify this properly!)
- Docker & Docker Compose (for database)
- ODBC Driver 17 for SQL Server

### Database Setup
The Python version uses the same SQL Server database as the C# version:

1. **If not already running, start the SQL Server database:**
   ```bash
   cd ../OnlineStoreBadCode
   docker compose up -d
   ```

2. **Wait for database initialization** (about 30-60 seconds)

### Python API Setup
1. **Install dependencies (bad practice - no virtual environment!):**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Better practice (but we don't document this properly):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start the Python API:**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Open browser to:** http://localhost:8000/docs

### Sample Data Available
- **Users**: admin@store.com, user@store.com, test@store.com (same as C# version)
- **Products**: 10 sample products with IDs 1000-1009
- **Orders**: 3 sample orders with different statuses

### Testing the API
- Use the included `sample-requests.http` file for testing endpoints
- Use FastAPI's automatic docs at http://localhost:8000/docs  
- Run the test script: `python test-api.py`

### Known Issues (Intentional Bad Code!)
- Login endpoint works but uses terrible practices
- Payment processing has poor validation
- Stats endpoint exposes internal application state
- No proper error handling or validation
- SQL injection vulnerabilities throughout
- Global state causes race conditions
- No proper async/await usage

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

### Utilities
- `GET /api/main/GetStats`
- `POST /api/main/Calculate`

## Default Credentials
- Admin: `admin@store.com` / `admin123`
- User: `user@store.com` / `user123`

## Database Schema (Intentionally Bad!)

Uses the same poorly designed database as the C# version:
- No primary keys or foreign keys
- No indexes for performance
- String-based dates instead of datetime
- No constraints or validation

## Comparison with C# Version

| Aspect | C# Version | Python Version |
|--------|------------|----------------|
| Framework | ASP.NET Core | FastAPI |
| Database | SQL Server (pyodbc) | SQL Server (System.Data.SqlClient) |
| Global State | Static classes | Module-level variables |
| Type Safety | Dynamic types | No type hints |
| Error Handling | Generic catches | Bare except clauses |
| Code Organization | God Controller | God Module |

## Refactoring Opportunities

This Python codebase is perfect for teaching:
- SOLID principles
- Design patterns (Repository, Unit of Work, etc.)
- Proper async/await usage
- Type hints and Pydantic models
- Dependency injection with FastAPI
- Proper error handling
- Database connection pooling
- Security best practices

## Educational Use

Use this project to:
1. Identify Python-specific code smells
2. Practice refactoring techniques
3. Implement proper FastAPI patterns
4. Add proper async/await
5. Introduce proper type hints
6. Apply clean code principles

Remember: This is how NOT to write Python production code!

## Environment Setup Issues (Intentional)
- No virtual environment documentation
- No Python version specification
- Mixed development and production dependencies
- Hardcoded database drivers
- No proper logging configuration
- No health checks or monitoring

Perfect for teaching proper Python project setup and best practices!