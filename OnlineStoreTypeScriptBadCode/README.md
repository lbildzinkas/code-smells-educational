# Online Store Bad Code - TypeScript/Node.js Edition

This is an intentionally bad implementation of an online store API using TypeScript and Node.js. It demonstrates numerous anti-patterns, security vulnerabilities, and poor coding practices for educational purposes.

## ⚠️ WARNING ⚠️
This code is intentionally insecure and poorly written. DO NOT use any of this code in production. It exists solely to demonstrate what NOT to do.

## Bad Practices Demonstrated

### Security Issues
- SQL Injection vulnerabilities
- Plain text password storage
- Hardcoded credentials and API keys
- No authentication/authorization
- Exposed internal state via API
- No input validation or sanitization

### Code Smells
- God Controller (everything in main.ts)
- Global mutable state
- Magic numbers and hardcoded values
- Code duplication
- Deeply nested conditionals
- Mixed responsibilities
- No error handling
- Type safety disabled (`any` everywhere)

### Architecture Issues
- No separation of concerns
- Direct database access in controllers
- No service layer
- No repository pattern
- No dependency injection
- No configuration management

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start SQL Server with Docker:
```bash
docker-compose up -d
```

3. Wait for database to initialize (about 30 seconds)

4. Build TypeScript:
```bash
npm run build
```

5. Start the server:
```bash
npm start
```

Or for development:
```bash
npm run dev
```

## Testing

Run the test script:
```bash
npm test
```

Or use the `sample-requests.http` file with REST Client extension in VS Code.

## API Endpoints

- **Products**: GET/POST/PUT/DELETE `/api/main/*Product`
- **Orders**: POST/GET/PUT `/api/main/*Order*`
- **Cart**: POST/GET/DELETE `/api/main/*Cart`
- **Payment**: POST `/api/main/ProcessPayment`
- **Users**: POST `/api/main/Login`, `/api/main/Register`, `/api/main/Logout`
- **Utility**: GET `/api/main/GetStats`, POST `/api/main/Calculate`

## Default Users
- admin@store.com / admin123
- user@store.com / user123

## Learning Points

Study this code to understand:
1. How NOT to handle user input (SQL injection)
2. Why global state is problematic
3. The importance of proper error handling
4. Why passwords should be hashed
5. The need for input validation
6. How poor architecture leads to unmaintainable code

## Remember
This is an example of BAD code. Always follow security best practices, use proper architecture patterns, and write clean, maintainable code in real projects!