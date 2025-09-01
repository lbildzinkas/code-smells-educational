-- Bad practice: no error handling
-- Bad practice: no transaction management

-- Create database
CREATE DATABASE OnlineStore;
GO

USE OnlineStore;
GO

-- Create tables (bad schema from setup.sql)
CREATE TABLE Products (
    ProductId int,
    ProductName varchar(255),
    Price decimal(10,2),
    Stock int,
    Description text,
    Category varchar(50)
);
GO

CREATE TABLE Orders (
    OrderId int,
    UserId varchar(255),
    Total decimal(10,2),
    Status varchar(50),
    PaymentMethod varchar(50),
    OrderDate varchar(50),
    TrackingNumber varchar(100)
);
GO

CREATE TABLE Users (
    UserId int,
    Email varchar(255),
    Password varchar(255),
    Name varchar(255)
);
GO

-- Bad practice: inserting test data with hardcoded values
-- Bad practice: plain text passwords
INSERT INTO Users (UserId, Email, Password, Name) VALUES 
(1, 'admin@store.com', 'admin123', 'Admin User'),
(2, 'user@store.com', 'user123', 'Regular User'),
(3, 'test@store.com', 'test123', 'Test User');
GO

-- Bad practice: no validation on insert
INSERT INTO Products (ProductId, ProductName, Price, Stock, Description, Category) VALUES 
(1000, 'Gaming Laptop', 1299.99, 5, 'High-end gaming laptop with RTX 4070', 'electronics'),
(1001, 'Wireless Mouse', 49.99, 50, 'Ergonomic wireless mouse', 'electronics'),
(1002, 'Mechanical Keyboard', 129.99, 20, 'RGB mechanical keyboard', 'electronics'),
(1003, 'Office Chair', 299.99, 10, 'Ergonomic office chair', 'furniture'),
(1004, 'Standing Desk', 499.99, 8, 'Electric standing desk', 'furniture'),
(1005, 'Coffee Maker', 89.99, 15, 'Automatic coffee maker', 'appliances'),
(1006, 'Headphones', 199.99, 25, 'Noise-cancelling headphones', 'electronics'),
(1007, 'Monitor 27"', 399.99, 12, '4K IPS Monitor', 'electronics'),
(1008, 'Webcam', 79.99, 30, '1080p HD Webcam', 'electronics'),
(1009, 'USB Hub', 29.99, 100, '7-port USB 3.0 Hub', 'electronics');
GO

-- Bad practice: sample orders with string dates
INSERT INTO Orders (OrderId, UserId, Total, Status, PaymentMethod, OrderDate, TrackingNumber) VALUES 
(5000, 'user@store.com', 1379.98, 'delivered', 'credit_card', '2024-01-15 10:30:00', 'TRK123456789'),
(5001, 'test@store.com', 329.98, 'shipped', 'paypal', '2024-01-20 14:45:00', 'TRK987654321'),
(5002, 'user@store.com', 89.99, 'processing', 'bank_transfer', '2024-01-25 09:15:00', NULL);
GO

-- Bad practice: no indexes created
-- Bad practice: no constraints or foreign keys
-- Bad practice: no stored procedures (everything inline in code)