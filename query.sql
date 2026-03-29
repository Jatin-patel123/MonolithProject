CREATE DATABASE StoreDB;
USE StoreDB;

-- USERS
CREATE TABLE Users (
    id INT PRIMARY KEY IDENTITY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(10)
);

-- PRODUCTS
CREATE TABLE Products (
    id INT PRIMARY KEY IDENTITY,
    name VARCHAR(100),
    buying_price FLOAT,
    selling_price FLOAT,
    quantity INT,
    qty_alert INT
);

-- BILLING
CREATE TABLE BillItems (
    id INT PRIMARY KEY IDENTITY,
    bill_id INT,
    product_id INT,
    quantity INT,
    price FLOAT,
    created_at DATETIME DEFAULT GETDATE()
);

-- RETURNS
CREATE TABLE Returns (
    id INT PRIMARY KEY IDENTITY,
    product_id INT,
    quantity INT,
    refund_amount FLOAT,
    created_at DATETIME DEFAULT GETDATE()
);

SELECT * FROM Users;
SELECT * FROM Products;
SELECT * FROM BillItems;
SELECT * FROM Returns;