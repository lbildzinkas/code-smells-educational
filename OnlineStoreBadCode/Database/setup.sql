-- Bad practice: SQL script mixed with project files
-- Bad practice: no proper schema design
-- Bad practice: no foreign keys or constraints

CREATE TABLE Products (
    ProductId int,
    ProductName varchar(255),
    Price decimal(10,2),
    Stock int,
    Description text,
    Category varchar(50) -- Bad practice: should be a separate table
);

CREATE TABLE Orders (
    OrderId int,
    UserId varchar(255), -- Bad practice: storing email as user ID
    Total decimal(10,2),
    Status varchar(50),
    PaymentMethod varchar(50),
    OrderDate varchar(50), -- Bad practice: date as string
    TrackingNumber varchar(100)
);

CREATE TABLE Users (
    UserId int,
    Email varchar(255),
    Password varchar(255), -- Bad practice: plain text passwords
    Name varchar(255)
);

-- Bad practice: no indexes
-- Bad practice: no primary keys defined
-- Bad practice: no audit columns (created_at, updated_at)
-- Bad practice: no soft delete support