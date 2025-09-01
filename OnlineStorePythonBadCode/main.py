# Code smell: God class/module - everything in one file!
# Bad practice: no proper imports organization
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pyodbc
import json
import time
import random
from datetime import datetime
# Bad practice: importing everything from global_variables
from global_variables import *
# Bad practice: star imports
from helpers.utility import *
from helpers.helper import *
from helpers.stuff import *

# Bad practice: global FastAPI instance with no configuration
app = FastAPI()

# Bad practice: startup code in main module
print("Starting Online Store Bad Code Python API...")
error_messages.append(f"Application started at {datetime.now()}")

# ============ PRODUCT ENDPOINTS ============

@app.get("/api/main/GetProduct")
def get_product(id: str):
    # Bad practice: no input validation
    try:
        # Bad practice: SQL injection vulnerability 
        sql = f"SELECT * FROM Products WHERE ProductId = {id}"
        
        # Bad practice: connection in endpoint
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        
        if row:
            # Bad practice: manual dictionary building
            product = {}
            product["id"] = row[0]
            product["name"] = row[1] 
            product["price"] = float(row[2])
            product["stock"] = row[3]
            product["description"] = row[4]
            
            # Bad practice: magic number
            if product["price"] > 100:
                product["expensive"] = True
                
            conn.close()
            return product
        else:
            conn.close()
            return JSONResponse(status_code=404, content="Product not found")
            
    except Exception as e:
        # Bad practice: exposing internal errors
        return JSONResponse(status_code=400, content=str(e))

@app.post("/api/main/AddProduct") 
def add_product(product_data: dict):
    # Bad practice: no validation, using dict instead of Pydantic model
    try:
        name = product_data["name"]
        price = product_data["price"]
        stock = product_data["stock"] 
        description = product_data["description"]
        
        # Bad practice: business logic in endpoint
        if price < 0:
            price = 0  # silently fix bad data
        if stock < 0:
            stock = 0
            
        # Bad practice: global variable mutation
        global product_id_counter
        product_id = product_id_counter
        product_id_counter += 1
        
        # Bad practice: SQL injection
        sql = f"INSERT INTO Products (ProductId, ProductName, Price, Stock, Description) VALUES ({product_id}, '{name}', {price}, {stock}, '{description}')"
        
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        
        return {"message": "Product added", "id": product_id}
        
    except:
        # Bad practice: bare except
        return JSONResponse(status_code=400, content="Error adding product")

@app.put("/api/main/UpdateProduct")
def update_product(id: str, product_data: dict):
    # Bad practice: duplicate validation code
    try:
        name = product_data["name"]
        price = product_data["price"] 
        stock = product_data["stock"]
        description = product_data["description"]
        
        if price < 0:
            price = 0
        if stock < 0:
            stock = 0
            
        # Bad practice: SQL injection
        sql = f"UPDATE Products SET ProductName = '{name}', Price = {price}, Stock = {stock}, Description = '{description}' WHERE ProductId = {id}"
        
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if rows_affected > 0:
            return "Product updated"
        else:
            return JSONResponse(status_code=404, content="Product not found")
            
    except Exception as e:
        # Bad practice: inconsistent error handling
        global error_messages
        error_messages.append(str(e))
        return JSONResponse(status_code=400, content="Update failed")

@app.delete("/api/main/DeleteProduct")
def delete_product(id: str):
    # Bad practice: no authorization check
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        
        # Bad practice: no soft delete
        sql = f"DELETE FROM Products WHERE ProductId = {id}"
        cursor.execute(sql)
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        # Bad practice: magic number
        if rows_affected == 1:
            return "Deleted"
        else:
            return JSONResponse(status_code=400, content="Delete failed")
            
    except:
        return JSONResponse(status_code=500, content="Internal error")

@app.get("/api/main/SearchProducts")
def search_products(query: str = "", sortBy: str = "", filterBy: str = ""):
    # Bad practice: required parameters not properly defined
    try:
        products = []
        
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        
        # Bad practice: complex string concatenation
        sql = "SELECT * FROM Products WHERE 1=1"
        
        if query:
            sql += f" AND (ProductName LIKE '%{query}%' OR Description LIKE '%{query}%')"
            
        # Bad practice: hardcoded filter logic  
        if filterBy == "cheap":
            sql += " AND Price < 50"
        elif filterBy == "expensive":
            sql += " AND Price >= 50" 
        elif filterBy == "instock":
            sql += " AND Stock > 0"
            
        # Bad practice: SQL injection in ORDER BY
        if sortBy:
            sql += f" ORDER BY {sortBy}"
            
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        for row in rows:
            product = {
                "id": row[0],
                "name": row[1], 
                "price": float(row[2]),
                "stock": row[3]
            }
            
            # Bad practice: business logic mixed with data access
            if product["stock"] < 10:
                product["lowStock"] = True
                
            products.append(product)
            
        conn.close()
        # Bad practice: no pagination
        return products
        
    except Exception as e:
        global error_count
        error_count += 1
        return JSONResponse(status_code=400, content="Search failed")

# ============ ORDER ENDPOINTS ============

@app.post("/api/main/CreateOrder")
def create_order(order_data: dict):
    # Bad practice: deeply nested code
    global is_logged_in, shopping_cart, order_id_counter, total_amount
    
    if is_logged_in:
        if len(shopping_cart) > 0:
            try:
                order_id = order_id_counter
                order_id_counter += 1
                total = 0.0
                
                # Bad practice: no transaction
                conn = pyodbc.connect(CONNECTION_STRING)
                cursor = conn.cursor()
                
                # Bad practice: manual calculation
                for item in shopping_cart:
                    try:
                        price = float(item["price"])
                        quantity = int(item["quantity"])
                    except:
                        continue  # silently skip bad data
                        
                    total += price * quantity
                    
                    # Bad practice: hardcoded tax calculation
                    if item.get("category") == "electronics":
                        total += price * quantity * 0.15  # electronics tax
                    elif item.get("category") == "food":
                        total += price * quantity * 0.08  # food tax
                    else:
                        total += price * quantity * 0.10  # general tax
                        
                # Bad practice: shipping calculation
                if total < SHIPPING_THRESHOLD:
                    total += 10  # shipping cost
                    
                # Bad practice: payment method fees
                payment_method = order_data["paymentMethod"]
                if payment_method == "credit_card":
                    total += total * CREDIT_CARD_FEE
                elif payment_method == "paypal":
                    total += total * PAYPAL_FEE
                    
                # Bad practice: date handling as string
                order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Bad practice: SQL injection
                sql = f"INSERT INTO Orders (OrderId, UserId, Total, Status, PaymentMethod, OrderDate) VALUES ({order_id}, '{user_email}', {total}, '{ORDER_PENDING}', '{payment_method}', '{order_date}')"
                
                cursor.execute(sql)
                conn.commit()
                conn.close()
                
                # Bad practice: clear global state
                shopping_cart = []
                total_amount = 0
                
                return {"orderId": order_id, "total": total}
                
            except Exception as e:
                return JSONResponse(status_code=400, content="Order creation failed")
        else:
            return JSONResponse(status_code=400, content="Cart is empty")
    else:
        return JSONResponse(status_code=401, content="Please login first")

@app.get("/api/main/GetOrder")
def get_order(id: int):
    # Bad practice: no authorization check
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        
        sql = f"SELECT * FROM Orders WHERE OrderId = {id}"
        cursor.execute(sql)
        row = cursor.fetchone()
        
        if row:
            order = {
                "orderId": row[0],
                "userId": row[1],
                "total": float(row[2]), 
                "status": row[3],
                "paymentMethod": row[4],
                "orderDate": row[5]
            }
            conn.close()
            return order
        else:
            conn.close()
            return JSONResponse(status_code=404, content="Order not found")
            
    except:
        return JSONResponse(status_code=500, content="Internal error")

@app.put("/api/main/UpdateOrderStatus") 
def update_order_status(orderId: int, newStatus: str):
    # Bad practice: giant if-elif chain instead of switch
    global temp, data, obj
    
    status_lower = newStatus.lower()
    if status_lower == "pending":
        newStatus = ORDER_PENDING
    elif status_lower == "processing":
        newStatus = ORDER_PROCESSING
        # Bad practice: side effects
        temp = f"Processing order {orderId}"
    elif status_lower == "shipped":
        newStatus = ORDER_SHIPPED
        # Bad practice: hardcoded email logic
        try:
            # Pretend to send email
            data = f"Email sent for order {orderId}"
        except:
            pass  # ignore email errors
    elif status_lower == "delivered":
        newStatus = ORDER_DELIVERED
    elif status_lower == "cancelled":
        newStatus = ORDER_CANCELLED
        # Bad practice: refund logic in status update
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            sql = f"SELECT Total, PaymentMethod FROM Orders WHERE OrderId = {orderId}"
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                refund_amount = float(row[0])
                payment_method = row[1]
                
                # Bad practice: nested if for refund logic
                if payment_method == "credit_card":
                    refund_amount = refund_amount * 0.98  # 2% fee not refunded
                elif payment_method == "paypal":
                    refund_amount = refund_amount * 0.97  # 3% fee not refunded
                    
                obj = {"refund": refund_amount}
            conn.close()
        except:
            pass  # ignore refund errors
    else:
        return JSONResponse(status_code=400, content="Invalid status")
        
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        sql = f"UPDATE Orders SET Status = '{newStatus}' WHERE OrderId = {orderId}"
        cursor.execute(sql)
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if rows_affected > 0:
            return "Status updated"
        else:
            return JSONResponse(status_code=404, content="Order not found")
            
    except:
        return JSONResponse(status_code=400, content="Update failed")

# ============ SHOPPING CART ENDPOINTS ============

@app.post("/api/main/AddToCart")
def add_to_cart(item: dict):
    # Bad practice: no validation
    global shopping_cart, total_amount, cart_id
    
    shopping_cart.append(item)
    
    # Bad practice: manual total calculation with exception swallowing
    try:
        total_amount += float(item["price"]) * int(item["quantity"])
    except:
        pass  # ignore calculation errors
        
    cart_id += 1
    
    return {"cartSize": len(shopping_cart)}

@app.get("/api/main/GetCart")
def get_cart():
    # Bad practice: returning global state directly
    return {
        "items": shopping_cart,
        "total": total_amount,
        "itemCount": len(shopping_cart)
    }

@app.delete("/api/main/RemoveFromCart")
def remove_from_cart(index: int):
    # Bad practice: no bounds checking
    global shopping_cart, total_amount
    
    try:
        shopping_cart.pop(index)
        
        # Bad practice: recalculate total from scratch
        total_amount = 0
        for item in shopping_cart:
            try:
                total_amount += float(item["price"]) * int(item["quantity"])
            except:
                continue
                
        return "Item removed"
    except:
        return JSONResponse(status_code=400, content="Invalid index")

@app.post("/api/main/ClearCart")
def clear_cart():
    global shopping_cart, total_amount, cart_id
    
    shopping_cart = []
    total_amount = 0
    cart_id = 0
    
    return "Cart cleared"

# ============ PAYMENT ENDPOINTS ============

@app.post("/api/main/ProcessPayment")
def process_payment(payment_data: dict):
    method = payment_data["method"]
    amount = float(payment_data["amount"])
    
    # Bad practice: deeply nested payment processing
    if method == "credit_card":
        card_number = payment_data["cardNumber"]
        cvv = payment_data["cvv"]
        expiry = payment_data["expiry"]
        
        # Bad practice: credit card validation
        if card_number:
            if len(card_number) == 16:
                if cvv:
                    if len(cvv) in [3, 4]:
                        if expiry:
                            # Bad practice: fake processing
                            time.sleep(2)  # simulate API call
                            
                            # Bad practice: random success/failure
                            if random.randint(1, 10) > 1:  # 90% success rate
                                # Bad practice: logging sensitive data
                                global data
                                data = f"Payment processed for card ending in {card_number[-4:]}"
                                
                                # Apply fee
                                total_with_fee = amount + (amount * CREDIT_CARD_FEE)
                                
                                return {
                                    "success": True,
                                    "transactionId": f"TXN{random.randint(100000, 999999)}",
                                    "charged": total_with_fee
                                }
                            else:
                                return JSONResponse(status_code=400, content="Payment declined")
                        else:
                            return JSONResponse(status_code=400, content="Invalid expiry date")
                    else:
                        return JSONResponse(status_code=400, content="Invalid CVV")
                else:
                    return JSONResponse(status_code=400, content="CVV required")
            else:
                return JSONResponse(status_code=400, content="Invalid card number")
        else:
            return JSONResponse(status_code=400, content="Card number required")
    elif method == "paypal":
        email = payment_data["email"]
        password = payment_data.get("password", "")  # Bad practice: asking for PayPal password
        
        if email:
            if "@" in email:
                # Bad practice: fake PayPal processing
                time.sleep(3)  # simulate API call
                
                # Apply fee
                total_with_fee = amount + (amount * PAYPAL_FEE)
                
                return {
                    "success": True,
                    "paypalTransactionId": f"PP-{random.randint(100000, 999999)}",
                    "charged": total_with_fee
                }
            else:
                return JSONResponse(status_code=400, content="Invalid email")
        else:
            return JSONResponse(status_code=400, content="Email required for PayPal")
    elif method == "bank_transfer":
        account_number = payment_data["accountNumber"]
        routing_number = payment_data["routingNumber"]
        
        if account_number and routing_number:
            # Bad practice: no real validation
            if len(account_number) > 5 and len(routing_number) == 9:
                # No fee for bank transfer
                return {
                    "success": True,
                    "message": f"Bank transfer initiated. Will be processed in {BANK_TRANSFER_DAYS} business days",
                    "referenceNumber": f"BT-{int(time.time())}"
                }
            else:
                return JSONResponse(status_code=400, content="Invalid account details")
        else:
            return JSONResponse(status_code=400, content="Account details required")
    else:
        return JSONResponse(status_code=400, content="Unsupported payment method")

# ============ USER ENDPOINTS ============

@app.post("/api/main/Login")
def login(credentials: dict):
    global is_logged_in, user_email, current_user
    
    email = credentials["email"]
    password = credentials["password"]
    
    # Bad practice: hardcoded users
    if email == "admin@store.com" and password == "admin123":
        is_logged_in = True
        user_email = email
        current_user["role"] = "admin"
        current_user["loginTime"] = datetime.now()
        
        return {"success": True, "user": "admin"}
    elif email == "user@store.com" and password == "user123":
        is_logged_in = True
        user_email = email
        current_user["role"] = "user"
        current_user["loginTime"] = datetime.now()
        
        return {"success": True, "user": "user"}
    else:
        # Bad practice: user enumeration
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            # Bad practice: plain text password comparison
            sql = f"SELECT * FROM Users WHERE Email = '{email}' AND Password = '{password}'"
            cursor.execute(sql)
            row = cursor.fetchone()
            
            if row:
                is_logged_in = True
                user_email = email
                current_user["id"] = row[0]
                conn.close()
                return {"success": True}
            else:
                conn.close()
                return JSONResponse(status_code=400, content="Invalid credentials")
        except:
            return JSONResponse(status_code=400, content="Login failed")

@app.post("/api/main/Logout")
def logout():
    # Bad practice: clearing global state
    global is_logged_in, user_email, current_user, shopping_cart, total_amount
    
    is_logged_in = False
    user_email = ""
    current_user = {}
    shopping_cart = []
    total_amount = 0
    
    return "Logged out"

@app.post("/api/main/Register") 
def register(user_data: dict):
    global user_id_counter, is_logged_in, user_email
    
    email = user_data["email"]
    password = user_data["password"]
    name = user_data["name"]
    
    # Bad practice: weak validation
    if not email or not password:
        return JSONResponse(status_code=400, content="Email and password required")
        
    if len(password) < 3:  # Bad practice: weak password requirement
        return JSONResponse(status_code=400, content="Password too short")
        
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        
        # Bad practice: check if user exists with concatenated SQL
        check_sql = f"SELECT COUNT(*) FROM Users WHERE Email = '{email}'"
        cursor.execute(check_sql)
        count = cursor.fetchone()[0]
        
        if count > 0:
            conn.close()
            return JSONResponse(status_code=400, content="User already exists")
            
        # Bad practice: plain text password storage
        user_id = user_id_counter
        user_id_counter += 1
        sql = f"INSERT INTO Users (UserId, Email, Password, Name) VALUES ({user_id}, '{email}', '{password}', '{name}')"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        
        # Bad practice: auto-login after registration
        is_logged_in = True
        user_email = email
        
        return {"success": True, "userId": user_id}
        
    except Exception as e:
        error_messages.append(str(e))
        return JSONResponse(status_code=400, content="Registration failed")

# ============ UTILITY ENDPOINTS ============

@app.get("/api/main/GetStats")
def get_stats():
    # Bad practice: exposing internal state
    return {
        "errorCount": error_count,
        "lastError": last_error,
        "errorMessages": error_messages,
        "currentUser": current_user,
        "isLoggedIn": is_logged_in,
        "cartSize": len(shopping_cart),
        "totalAmount": total_amount,
        "productIdCounter": product_id_counter,
        "orderIdCounter": order_id_counter,
        "userIdCounter": user_id_counter,
        "temp": temp,
        "data": data,
        "obj": obj
    }

@app.post("/api/main/Calculate")
def calculate(calc_data: dict):
    # Bad practice: random utility method in main controller
    global x, flag
    
    try:
        subtotal = float(calc_data["subtotal"])
        calc_type = calc_data["type"]
        
        result = 0.0
        
        # Bad practice: business logic scattered
        if calc_type == "tax":
            result = subtotal * TAX_RATE
        elif calc_type == "shipping":
            if subtotal < SHIPPING_THRESHOLD:
                result = 10
            else:
                result = 0
        elif calc_type == "discount":
            code = calc_data["code"]
            # Bad practice: hardcoded discount codes
            if code == "SAVE10":
                result = subtotal * 0.1
            elif code == "SAVE20": 
                result = subtotal * 0.2
            elif code == "FREESHIP":
                result = 0  # free shipping, not a discount
                flag = True  # what does this mean?
                
        x = int(result)  # Bad practice: global state mutation
        
        return {"calculated": result}
        
    except:
        return JSONResponse(status_code=400, content="Calculation error")

# Bad practice: no proper error handling middleware
# Bad practice: no proper startup/shutdown events
# Bad practice: running in debug mode in production

if __name__ == "__main__":
    import uvicorn
    # Bad practice: hardcoded host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)