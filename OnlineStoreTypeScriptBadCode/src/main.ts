// Code smell: God class/module - everything in one file!
// Bad practice: no proper imports organization
import express from 'express';
import bodyParser from 'body-parser';
import * as sql from 'mssql';
import cors from 'cors';
import * as globalVars from './globalVariables';
// Bad practice: importing helpers that don't exist yet
// import * as helper from './helpers/helper';
// import * as utility from './helpers/utility';
// import * as stuff from './helpers/stuff';

// Bad practice: destructuring all globals for easier access
const { 
    connectionConfig, taxRate, shippingThreshold, creditCardFee, paypalFee, 
    bankTransferDays, ORDER_PENDING, ORDER_PROCESSING, ORDER_SHIPPED, 
    ORDER_DELIVERED, ORDER_CANCELLED, globals 
} = globalVars;

// Bad practice: global Express instance with no configuration
const app = express();
app.use(bodyParser.json());
app.use(cors()); // Bad practice: allowing all origins

// Bad practice: startup code in main module
console.log("Starting Online Store Bad Code TypeScript API...");
globals.errorMessages.push(`Application started at ${new Date()}`);

// ============ PRODUCT ENDPOINTS ============

app.get("/api/main/GetProduct", async (req: any, res: any) => {
    // Bad practice: no input validation
    const id = req.query.id;
    
    try {
        // Bad practice: SQL injection vulnerability
        const query = `SELECT * FROM Products WHERE ProductId = ${id}`;
        
        // Bad practice: connection in endpoint
        const pool = await sql.connect(connectionConfig);
        const result = await pool.request().query(query);
        
        if (result.recordset.length > 0) {
            const row = result.recordset[0];
            // Bad practice: manual dictionary building
            const product: any = {};
            product.id = row.ProductId;
            product.name = row.ProductName;
            product.price = parseFloat(row.Price);
            product.stock = row.Stock;
            product.description = row.Description;
            
            // Bad practice: magic number
            if (product.price > 100) {
                product.expensive = true;
            }
            
            pool.close();
            res.json(product);
        } else {
            pool.close();
            res.status(404).send("Product not found");
        }
    } catch (ex: any) {
        // Bad practice: exposing internal errors
        res.status(400).send(ex.message);
    }
});

app.post("/api/main/AddProduct", async (req: any, res: any) => {
    // Bad practice: no validation, using any instead of proper types
    const name = req.body.name;
    let price = req.body.price;
    let stock = req.body.stock;
    const description = req.body.description;
    
    // Bad practice: business logic in endpoint
    if (price < 0) {
        price = 0; // silently fix bad data
    }
    if (stock < 0) {
        stock = 0;
    }
    
    try {
        const pool = await sql.connect(connectionConfig);
        
        // Bad practice: SQL injection
        const query = `INSERT INTO Products (ProductId, ProductName, Price, Stock, Description) VALUES (${globals.productIdCounter++}, '${name}', ${price}, ${stock}, '${description}')`;
        
        await pool.request().query(query);
        pool.close();
        
        // Bad practice: returning inconsistent data
        res.json({ message: "Product added", id: globals.productIdCounter - 1 });
    } catch {
        // Bad practice: generic error handling
        res.status(400).send("Error adding product");
    }
});

app.put("/api/main/UpdateProduct", async (req: any, res: any) => {
    // Bad practice: copy-pasted validation
    const id = req.query.id;
    const name = req.body.name;
    let price = req.body.price;
    let stock = req.body.stock;
    const description = req.body.description;
    
    if (price < 0) {
        price = 0;
    }
    if (stock < 0) {
        stock = 0;
    }
    
    try {
        // Bad practice: duplicate database code
        const pool = await sql.connect(connectionConfig);
        
        // Bad practice: SQL injection
        const query = `UPDATE Products SET ProductName = '${name}', Price = ${price}, Stock = ${stock}, Description = '${description}' WHERE ProductId = ${id}`;
        
        const result = await pool.request().query(query);
        pool.close();
        
        if (result.rowsAffected[0] > 0) {
            res.send("Product updated");
        } else {
            res.status(404).send("Product not found");
        }
    } catch (e: any) {
        // Bad practice: inconsistent error handling
        globals.errorMessages.push(e.message);
        res.status(400).send("Update failed");
    }
});

app.delete("/api/main/DeleteProduct", async (req: any, res: any) => {
    // Bad practice: no authorization check
    const id = req.query.id;
    
    try {
        const pool = await sql.connect(connectionConfig);
        
        // Bad practice: no soft delete
        const query = `DELETE FROM Products WHERE ProductId = ${id}`;
        
        const result = await pool.request().query(query);
        pool.close();
        
        // Bad practice: magic number
        if (result.rowsAffected[0] == 1) {
            res.send("Deleted");
        } else {
            res.status(400).send("Delete failed");
        }
    } catch {
        res.status(500).send();
    }
});

app.get("/api/main/SearchProducts", async (req: any, res: any) => {
    const query = req.query.query || "";
    const sortBy = req.query.sortBy || "";
    const filterBy = req.query.filterBy || "";
    
    try {
        const products: any[] = [];
        
        const pool = await sql.connect(connectionConfig);
        
        // Bad practice: complex string concatenation
        let sqlQuery = "SELECT * FROM Products WHERE 1=1";
        
        if (query) {
            sqlQuery += ` AND (ProductName LIKE '%${query}%' OR Description LIKE '%${query}%')`;
        }
        
        // Bad practice: hardcoded filter logic
        if (filterBy == "cheap") {
            sqlQuery += " AND Price < 50";
        } else if (filterBy == "expensive") {
            sqlQuery += " AND Price >= 50";
        } else if (filterBy == "instock") {
            sqlQuery += " AND Stock > 0";
        }
        
        // Bad practice: SQL injection in ORDER BY
        if (sortBy) {
            sqlQuery += " ORDER BY " + sortBy;
        }
        
        const result = await pool.request().query(sqlQuery);
        
        result.recordset.forEach((row: any) => {
            const product: any = {};
            product.id = row.ProductId;
            product.name = row.ProductName;
            product.price = parseFloat(row.Price);
            product.stock = row.Stock;
            
            // Bad practice: business logic mixed with data access
            if (product.stock < 10) {
                product.lowStock = true;
            }
            
            products.push(product);
        });
        
        pool.close();
        // Bad practice: no pagination
        res.json(products);
    } catch (ex: any) {
        globals.errorCount++;
        res.status(400).send("Search failed");
    }
});

// ============ ORDER ENDPOINTS ============

app.post("/api/main/CreateOrder", async (req: any, res: any) => {
    // Bad practice: deeply nested code
    if (globals.isLoggedIn) {
        if (globals.shoppingCart.length > 0) {
            try {
                const orderId = globals.orderIdCounter++;
                let total = 0;
                
                // Bad practice: no transaction
                const pool = await sql.connect(connectionConfig);
                
                // Bad practice: manual calculation
                for (const item of globals.shoppingCart) {
                    let price = 0;
                    let quantity = 1;
                    
                    // Bad practice: type confusion
                    try {
                        price = parseFloat(item.price);
                        quantity = parseInt(item.quantity);
                    } catch {
                        // silently continue
                        continue;
                    }
                    
                    total += price * quantity;
                    
                    // Bad practice: hardcoded tax calculation
                    if (item.category == "electronics") {
                        total += price * quantity * 0.15; // electronics tax
                    } else if (item.category == "food") {
                        total += price * quantity * 0.08; // food tax
                    } else {
                        total += price * quantity * 0.10; // general tax
                    }
                }
                
                // Bad practice: shipping calculation
                if (total < shippingThreshold) {
                    total += 10; // shipping cost
                }
                
                // Bad practice: payment method fees
                const paymentMethod = req.body.paymentMethod;
                if (paymentMethod == "credit_card") {
                    total += total * creditCardFee;
                } else if (paymentMethod == "paypal") {
                    total += total * paypalFee;
                }
                
                // Bad practice: date handling
                const orderDate = new Date().toISOString().slice(0, 19).replace('T', ' ');
                
                // Bad practice: SQL injection
                const query = `INSERT INTO Orders (OrderId, UserId, Total, Status, PaymentMethod, OrderDate) VALUES (${orderId}, '${globals.userEmail}', ${total}, '${ORDER_PENDING}', '${paymentMethod}', '${orderDate}')`;
                
                await pool.request().query(query);
                pool.close();
                
                // Bad practice: clear global state
                globals.shoppingCart = [];
                globals.totalAmount = 0;
                
                res.json({ orderId: orderId, total: total });
            } catch (ex: any) {
                // Bad practice: generic error
                res.status(400).send("Order creation failed");
            }
        } else {
            res.status(400).send("Cart is empty");
        }
    } else {
        res.status(401).send("Please login first");
    }
});

app.get("/api/main/GetOrder", async (req: any, res: any) => {
    // Bad practice: no authorization check
    const id = req.query.id;
    
    try {
        const pool = await sql.connect(connectionConfig);
        
        const query = `SELECT * FROM Orders WHERE OrderId = ${id}`;
        const result = await pool.request().query(query);
        
        if (result.recordset.length > 0) {
            const row = result.recordset[0];
            // Bad practice: manual mapping
            const order = {
                orderId: row.OrderId,
                userId: row.UserId,
                total: row.Total,
                status: row.Status,
                paymentMethod: row.PaymentMethod,
                orderDate: row.OrderDate
            };
            
            pool.close();
            res.json(order);
        } else {
            pool.close();
            res.status(404).send();
        }
    } catch {
        res.status(500).send();
    }
});

app.put("/api/main/UpdateOrderStatus", async (req: any, res: any) => {
    const orderId = req.query.orderId;
    let newStatus = req.query.newStatus;
    
    // Bad practice: giant switch statement
    switch (newStatus.toLowerCase()) {
        case "pending":
            newStatus = ORDER_PENDING;
            break;
        case "processing":
            newStatus = ORDER_PROCESSING;
            // Bad practice: side effects in switch
            globals.temp = "Processing order " + orderId;
            break;
        case "shipped":
            newStatus = ORDER_SHIPPED;
            // Bad practice: hardcoded email logic
            try {
                // Pretend to send email
                globals.data = "Email sent for order " + orderId;
            } catch {
                // ignore email errors
            }
            break;
        case "delivered":
            newStatus = ORDER_DELIVERED;
            break;
        case "cancelled":
            newStatus = ORDER_CANCELLED;
            // Bad practice: refund logic in status update
            try {
                const pool = await sql.connect(connectionConfig);
                const query = `SELECT Total, PaymentMethod FROM Orders WHERE OrderId = ${orderId}`;
                const result = await pool.request().query(query);
                if (result.recordset.length > 0) {
                    let refundAmount = parseFloat(result.recordset[0].Total);
                    const paymentMethod = result.recordset[0].PaymentMethod;
                    
                    // Bad practice: nested if for refund logic
                    if (paymentMethod == "credit_card") {
                        refundAmount = refundAmount * 0.98; // 2% fee not refunded
                    } else if (paymentMethod == "paypal") {
                        refundAmount = refundAmount * 0.97; // 3% fee not refunded
                    }
                    
                    globals.obj = { refund: refundAmount };
                }
                pool.close();
            } catch {
                // ignore refund errors
            }
            break;
        default:
            res.status(400).send("Invalid status");
            return;
    }
    
    try {
        const pool = await sql.connect(connectionConfig);
        const query = `UPDATE Orders SET Status = '${newStatus}' WHERE OrderId = ${orderId}`;
        const result = await pool.request().query(query);
        pool.close();
        
        if (result.rowsAffected[0] > 0) {
            res.send("Status updated");
        } else {
            res.status(404).send();
        }
    } catch {
        res.status(400).send("Update failed");
    }
});

// ============ SHOPPING CART ENDPOINTS ============

app.post("/api/main/AddToCart", (req: any, res: any) => {
    // Bad practice: no validation
    globals.shoppingCart.push(req.body);
    
    // Bad practice: manual total calculation
    try {
        globals.totalAmount += parseFloat(req.body.price) * parseInt(req.body.quantity);
    } catch {
        // ignore calculation errors
    }
    
    globals.cartId++;
    
    res.json({ cartSize: globals.shoppingCart.length });
});

app.get("/api/main/GetCart", (req: any, res: any) => {
    // Bad practice: returning global state directly
    res.json({
        items: globals.shoppingCart,
        total: globals.totalAmount,
        itemCount: globals.shoppingCart.length
    });
});

app.delete("/api/main/RemoveFromCart", (req: any, res: any) => {
    // Bad practice: no bounds checking
    const index = parseInt(req.query.index);
    
    try {
        globals.shoppingCart.splice(index, 1);
        
        // Bad practice: recalculate total from scratch
        globals.totalAmount = 0;
        for (const item of globals.shoppingCart) {
            try {
                globals.totalAmount += parseFloat(item.price) * parseInt(item.quantity);
            } catch {
                continue;
            }
        }
        
        res.send("Item removed");
    } catch {
        res.status(400).send("Invalid index");
    }
});

app.post("/api/main/ClearCart", (req: any, res: any) => {
    globals.shoppingCart = [];
    globals.totalAmount = 0;
    globals.cartId = 0;
    
    res.send("Cart cleared");
});

// ============ PAYMENT ENDPOINTS ============

app.post("/api/main/ProcessPayment", (req: any, res: any) => {
    const method = req.body.method;
    const amount = req.body.amount;
    
    // Bad practice: deeply nested payment processing
    if (method == "credit_card") {
        const cardNumber = req.body.cardNumber;
        const cvv = req.body.cvv;
        const expiry = req.body.expiry;
        
        // Bad practice: credit card validation
        if (cardNumber) {
            if (cardNumber.length == 16) {
                if (cvv) {
                    if (cvv.length == 3 || cvv.length == 4) {
                        if (expiry) {
                            // Bad practice: fake processing
                            setTimeout(() => {}, 2000); // simulate API call
                            
                            // Bad practice: random success/failure
                            if (Math.random() * 10 > 1) { // 90% success rate
                                // Bad practice: logging sensitive data
                                globals.data = `Payment processed for card ending in ${cardNumber.substr(12)}`;
                                
                                // Apply fee
                                const totalWithFee = amount + (amount * creditCardFee);
                                
                                res.json({ 
                                    success: true, 
                                    transactionId: Math.random().toString(36).substr(2, 9), 
                                    charged: totalWithFee 
                                });
                            } else {
                                res.status(400).send("Payment declined");
                            }
                        } else {
                            res.status(400).send("Invalid expiry date");
                        }
                    } else {
                        res.status(400).send("Invalid CVV");
                    }
                } else {
                    res.status(400).send("CVV required");
                }
            } else {
                res.status(400).send("Invalid card number");
            }
        } else {
            res.status(400).send("Card number required");
        }
    } else if (method == "paypal") {
        const email = req.body.email;
        const password = req.body.password; // Bad practice: asking for PayPal password
        
        if (email) {
            if (email.includes("@")) {
                // Bad practice: fake PayPal processing
                setTimeout(() => {}, 3000); // simulate API call
                
                // Apply fee
                const totalWithFee = amount + (amount * paypalFee);
                
                // Bad practice: hardcoded response
                res.json({ 
                    success: true, 
                    paypalTransactionId: "PP-" + Math.floor(Math.random() * 900000 + 100000), 
                    charged: totalWithFee 
                });
            } else {
                res.status(400).send("Invalid email");
            }
        } else {
            res.status(400).send("Email required for PayPal");
        }
    } else if (method == "bank_transfer") {
        const accountNumber = req.body.accountNumber;
        const routingNumber = req.body.routingNumber;
        
        if (accountNumber && routingNumber) {
            // Bad practice: no real validation
            if (accountNumber.length > 5 && routingNumber.length == 9) {
                // No fee for bank transfer
                res.json({ 
                    success: true, 
                    message: `Bank transfer initiated. Will be processed in ${bankTransferDays} business days`,
                    referenceNumber: "BT-" + Date.now()
                });
            } else {
                res.status(400).send("Invalid account details");
            }
        } else {
            res.status(400).send("Account details required");
        }
    } else {
        res.status(400).send("Unsupported payment method");
    }
});

// ============ USER ENDPOINTS ============

app.post("/api/main/Login", async (req: any, res: any) => {
    const email = req.body.email;
    const password = req.body.password;
    
    // Bad practice: hardcoded users
    if (email == "admin@store.com" && password == "admin123") {
        globals.isLoggedIn = true;
        globals.userEmail = email;
        globals.currentUser["role"] = "admin";
        globals.currentUser["loginTime"] = new Date();
        
        res.json({ success: true, user: "admin" });
    } else if (email == "user@store.com" && password == "user123") {
        globals.isLoggedIn = true;
        globals.userEmail = email;
        globals.currentUser["role"] = "user";
        globals.currentUser["loginTime"] = new Date();
        
        res.json({ success: true, user: "user" });
    } else {
        // Bad practice: user enumeration
        try {
            const pool = await sql.connect(connectionConfig);
            // Bad practice: plain text password comparison
            const query = `SELECT * FROM Users WHERE Email = '${email}' AND Password = '${password}'`;
            const result = await pool.request().query(query);
            
            if (result.recordset.length > 0) {
                globals.isLoggedIn = true;
                globals.userEmail = email;
                globals.currentUser["id"] = result.recordset[0].UserId;
                
                pool.close();
                res.json({ success: true });
            } else {
                pool.close();
                res.status(400).send("Invalid credentials");
            }
        } catch {
            res.status(400).send("Login failed");
        }
    }
});

app.post("/api/main/Logout", (req: any, res: any) => {
    // Bad practice: clearing global state
    globals.isLoggedIn = false;
    globals.userEmail = "";
    globals.currentUser = {};
    globals.shoppingCart = [];
    globals.totalAmount = 0;
    
    res.send("Logged out");
});

app.post("/api/main/Register", async (req: any, res: any) => {
    const email = req.body.email;
    const password = req.body.password;
    const name = req.body.name;
    
    // Bad practice: weak validation
    if (!email || !password) {
        res.status(400).send("Email and password required");
        return;
    }
    
    if (password.length < 3) { // Bad practice: weak password requirement
        res.status(400).send("Password too short");
        return;
    }
    
    try {
        const pool = await sql.connect(connectionConfig);
        
        // Bad practice: check if user exists with concatenated SQL
        const checkQuery = `SELECT COUNT(*) as count FROM Users WHERE Email = '${email}'`;
        const checkResult = await pool.request().query(checkQuery);
        
        if (checkResult.recordset[0].count > 0) {
            pool.close();
            res.status(400).send("User already exists");
            return;
        }
        
        // Bad practice: plain text password storage
        const userId = globals.userIdCounter++;
        const insertQuery = `INSERT INTO Users (UserId, Email, Password, Name) VALUES (${userId}, '${email}', '${password}', '${name}')`;
        await pool.request().query(insertQuery);
        pool.close();
        
        // Bad practice: auto-login after registration
        globals.isLoggedIn = true;
        globals.userEmail = email;
        
        res.json({ success: true, userId: userId });
    } catch (ex: any) {
        globals.errorMessages.push(ex.message);
        res.status(400).send("Registration failed");
    }
});

// ============ UTILITY ENDPOINTS ============

app.get("/api/main/GetStats", (req: any, res: any) => {
    // Bad practice: exposing internal state
    res.json({
        errorCount: globals.errorCount,
        lastError: globals.lastError,
        errorMessages: globals.errorMessages,
        currentUser: globals.currentUser,
        isLoggedIn: globals.isLoggedIn,
        cartSize: globals.shoppingCart.length,
        totalAmount: globals.totalAmount,
        productIdCounter: globals.productIdCounter,
        orderIdCounter: globals.orderIdCounter,
        userIdCounter: globals.userIdCounter,
        temp: globals.temp,
        data: globals.data,
        obj: globals.obj
    });
});

app.post("/api/main/Calculate", (req: any, res: any) => {
    // Bad practice: random utility method in main controller
    try {
        const subtotal = req.body.subtotal;
        const type = req.body.type;
        
        let result = 0;
        
        // Bad practice: business logic scattered
        if (type == "tax") {
            result = subtotal * taxRate;
        } else if (type == "shipping") {
            if (subtotal < shippingThreshold) {
                result = 10;
            } else {
                result = 0;
            }
        } else if (type == "discount") {
            const code = req.body.code;
            // Bad practice: hardcoded discount codes
            if (code == "SAVE10") {
                result = subtotal * 0.1;
            } else if (code == "SAVE20") {
                result = subtotal * 0.2;
            } else if (code == "FREESHIP") {
                result = 0; // free shipping, not a discount
                globals.flag = true; // what does this mean?
            }
        }
        
        res.json({ calculated: result });
    } catch {
        res.status(400).send("Calculation error");
    }
});

// Bad practice: no proper error handling middleware
// Bad practice: no proper startup/shutdown events
// Bad practice: hardcoded port

const PORT = 3001;
app.listen(PORT, () => {
    console.log(`Bad code API running on http://localhost:${PORT}`);
    console.log("This is an example of what NOT to do!");
});