using Microsoft.AspNetCore.Mvc;
using System.Data.SqlClient;

namespace OnlineStoreBadCode.Controllers;

// Code smell: God Controller - does everything
[ApiController]
[Route("api/[controller]")]
public class MainController : ControllerBase
{
    // Bad practice: no dependency injection, direct database access
    
    // ============ PRODUCT METHODS ============
    
    [HttpGet("GetProduct")]
    public IActionResult GetProduct(string id)
    {
        try
        {
            // Bad practice: SQL injection vulnerability
            var sql = "SELECT * FROM Products WHERE ProductId = " + id;
            
            // Bad practice: connection string in code
            using (var conn = new SqlConnection(GlobalVariables.connectionString))
            {
                conn.Open();
                var cmd = new SqlCommand(sql, conn);
                var reader = cmd.ExecuteReader();
                
                // Bad practice: building response manually
                if (reader.Read())
                {
                    var product = new Dictionary<string, object>();
                    product["id"] = reader["ProductId"];
                    product["name"] = reader["ProductName"];
                    product["price"] = reader["Price"];
                    product["stock"] = reader["Stock"];
                    product["description"] = reader["Description"];
                    
                    // Bad practice: magic number
                    if ((decimal)product["price"] > 100)
                    {
                        product["expensive"] = true;
                    }
                    
                    return Ok(product);
                }
                else
                {
                    return NotFound("Product not found");
                }
            }
        }
        catch (Exception ex)
        {
            // Bad practice: exposing internal errors
            return BadRequest(ex.Message);
        }
    }
    
    [HttpPost("AddProduct")]
    public IActionResult AddProduct([FromBody] dynamic product)
    {
        // Bad practice: no validation
        string name = product.name;
        decimal price = product.price;
        int stock = product.stock;
        string description = product.description;
        
        // Bad practice: business logic in controller
        if (price < 0)
        {
            price = 0; // silently fix bad data
        }
        
        if (stock < 0)
        {
            stock = 0;
        }
        
        // Bad practice: duplicate connection code
        try
        {
            using (var conn = new SqlConnection(GlobalVariables.connectionString))
            {
                conn.Open();
                
                // Bad practice: concatenated SQL
                var sql = $"INSERT INTO Products (ProductId, ProductName, Price, Stock, Description) VALUES ({GlobalVariables.productIdCounter++}, '{name}', {price}, {stock}, '{description}')";
                
                var cmd = new SqlCommand(sql, conn);
                cmd.ExecuteNonQuery();
                
                // Bad practice: returning inconsistent data
                return Ok(new { message = "Product added", id = GlobalVariables.productIdCounter - 1 });
            }
        }
        catch
        {
            // Bad practice: generic error handling
            return BadRequest("Error adding product");
        }
    }
    
    [HttpPut("UpdateProduct")]
    public IActionResult UpdateProduct(string id, [FromBody] dynamic product)
    {
        // Bad practice: copy-pasted validation
        string name = product.name;
        decimal price = product.price;
        int stock = product.stock;
        string description = product.description;
        
        if (price < 0)
        {
            price = 0;
        }
        
        if (stock < 0)
        {
            stock = 0;
        }
        
        try
        {
            // Bad practice: duplicate database code
            using (var conn = new SqlConnection(GlobalVariables.connectionString))
            {
                conn.Open();
                
                // Bad practice: SQL injection
                var sql = $"UPDATE Products SET ProductName = '{name}', Price = {price}, Stock = {stock}, Description = '{description}' WHERE ProductId = {id}";
                
                var cmd = new SqlCommand(sql, conn);
                var rows = cmd.ExecuteNonQuery();
                
                if (rows > 0)
                {
                    return Ok("Product updated");
                }
                else
                {
                    return NotFound("Product not found");
                }
            }
        }
        catch (Exception e)
        {
            // Bad practice: inconsistent error handling
            GlobalVariables.errorMessages.Add(e.Message);
            return BadRequest("Update failed");
        }
    }
    
    [HttpDelete("DeleteProduct")]
    public IActionResult DeleteProduct(string id)
    {
        // Bad practice: no authorization check
        
        try
        {
            using (var conn = new SqlConnection(GlobalVariables.connectionString))
            {
                conn.Open();
                
                // Bad practice: no soft delete
                var sql = "DELETE FROM Products WHERE ProductId = " + id;
                
                var cmd = new SqlCommand(sql, conn);
                var rows = cmd.ExecuteNonQuery();
                
                // Bad practice: magic number
                if (rows == 1)
                {
                    return Ok("Deleted");
                }
                else
                {
                    return BadRequest("Delete failed");
                }
            }
        }
        catch
        {
            return StatusCode(500);
        }
    }
    
    [HttpGet("SearchProducts")]
    public IActionResult SearchProducts(string query, string sortBy, string filterBy)
    {
        try
        {
            var products = new List<Dictionary<string, object>>();
            
            using (var conn = new SqlConnection(GlobalVariables.connectionString))
            {
                conn.Open();
                
                // Bad practice: complex string concatenation
                var sql = "SELECT * FROM Products WHERE 1=1";
                
                if (!string.IsNullOrEmpty(query))
                {
                    sql += $" AND (ProductName LIKE '%{query}%' OR Description LIKE '%{query}%')";
                }
                
                // Bad practice: hardcoded filter logic
                if (filterBy == "cheap")
                {
                    sql += " AND Price < 50";
                }
                else if (filterBy == "expensive")
                {
                    sql += " AND Price >= 50";
                }
                else if (filterBy == "instock")
                {
                    sql += " AND Stock > 0";
                }
                
                // Bad practice: SQL injection in ORDER BY
                if (!string.IsNullOrEmpty(sortBy))
                {
                    sql += " ORDER BY " + sortBy;
                }
                
                var cmd = new SqlCommand(sql, conn);
                var reader = cmd.ExecuteReader();
                
                while (reader.Read())
                {
                    var product = new Dictionary<string, object>();
                    product["id"] = reader["ProductId"];
                    product["name"] = reader["ProductName"];
                    product["price"] = reader["Price"];
                    product["stock"] = reader["Stock"];
                    
                    // Bad practice: business logic mixed with data access
                    if ((int)product["stock"] < 10)
                    {
                        product["lowStock"] = true;
                    }
                    
                    products.Add(product);
                }
            }
            
            // Bad practice: no pagination
            return Ok(products);
        }
        catch (Exception ex)
        {
            GlobalVariables.errorCount++;
            return BadRequest("Search failed");
        }
    }
    
    // ============ ORDER METHODS ============
    
    [HttpPost("CreateOrder")]
    public IActionResult CreateOrder([FromBody] dynamic orderData)
    {
        // Bad practice: deeply nested code
        if (GlobalVariables.isLoggedIn)
        {
            if (GlobalVariables.shoppingCart.Count > 0)
            {
                try
                {
                    var orderId = GlobalVariables.orderIdCounter++;
                    decimal total = 0;
                    
                    // Bad practice: no transaction
                    using (var conn = new SqlConnection(GlobalVariables.connectionString))
                    {
                        conn.Open();
                        
                        // Bad practice: manual calculation
                        foreach (dynamic item in GlobalVariables.shoppingCart)
                        {
                            decimal price = 0;
                            int quantity = 1;
                            
                            // Bad practice: type confusion
                            try
                            {
                                price = Convert.ToDecimal(item.price);
                                quantity = Convert.ToInt32(item.quantity);
                            }
                            catch
                            {
                                // silently continue
                                continue;
                            }
                            
                            total += price * quantity;
                            
                            // Bad practice: hardcoded tax calculation
                            if (item.category == "electronics")
                            {
                                total += price * quantity * 0.15m; // electronics tax
                            }
                            else if (item.category == "food")
                            {
                                total += price * quantity * 0.08m; // food tax
                            }
                            else
                            {
                                total += price * quantity * 0.10m; // general tax
                            }
                        }
                        
                        // Bad practice: shipping calculation
                        if (total < GlobalVariables.shippingThreshold)
                        {
                            total += 10; // shipping cost
                        }
                        
                        // Bad practice: payment method fees
                        string paymentMethod = orderData.paymentMethod;
                        if (paymentMethod == "credit_card")
                        {
                            total += total * GlobalVariables.creditCardFee;
                        }
                        else if (paymentMethod == "paypal")
                        {
                            total += total * GlobalVariables.paypalFee;
                        }
                        
                        // Bad practice: date handling
                        var orderDate = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
                        
                        // Bad practice: SQL injection
                        var sql = $"INSERT INTO Orders (OrderId, UserId, Total, Status, PaymentMethod, OrderDate) VALUES ({orderId}, '{GlobalVariables.userEmail}', {total}, '{GlobalVariables.ORDER_PENDING}', '{paymentMethod}', '{orderDate}')";
                        
                        var cmd = new SqlCommand(sql, conn);
                        cmd.ExecuteNonQuery();
                        
                        // Bad practice: clear global state
                        GlobalVariables.shoppingCart.Clear();
                        GlobalVariables.totalAmount = 0;
                        
                        return Ok(new { orderId = orderId, total = total });
                    }
                }
                catch (Exception ex)
                {
                    // Bad practice: generic error
                    return BadRequest("Order creation failed");
                }
            }
            else
            {
                return BadRequest("Cart is empty");
            }
        }
        else
        {
            return Unauthorized("Please login first");
        }
    }
    
    [HttpGet("GetOrder")]
    public IActionResult GetOrder(int id)
    {
        // Bad practice: no authorization check
        try
        {
            using (var conn = new SqlConnection(GlobalVariables.connectionString))
            {
                conn.Open();
                
                var sql = "SELECT * FROM Orders WHERE OrderId = " + id;
                var cmd = new SqlCommand(sql, conn);
                var reader = cmd.ExecuteReader();
                
                if (reader.Read())
                {
                    // Bad practice: manual mapping
                    var order = new
                    {
                        orderId = reader["OrderId"],
                        userId = reader["UserId"],
                        total = reader["Total"],
                        status = reader["Status"],
                        paymentMethod = reader["PaymentMethod"],
                        orderDate = reader["OrderDate"]
                    };
                    
                    return Ok(order);
                }
                else
                {
                    return NotFound();
                }
            }
        }
        catch
        {
            return StatusCode(500);
        }
    }
    
    [HttpPut("UpdateOrderStatus")]
    public IActionResult UpdateOrderStatus(int orderId, string newStatus)
    {
        // Bad practice: giant switch statement
        switch (newStatus.ToLower())
        {
            case "pending":
                newStatus = GlobalVariables.ORDER_PENDING;
                break;
            case "processing":
                newStatus = GlobalVariables.ORDER_PROCESSING;
                // Bad practice: side effects in switch
                GlobalVariables.temp = "Processing order " + orderId;
                break;
            case "shipped":
                newStatus = GlobalVariables.ORDER_SHIPPED;
                // Bad practice: hardcoded email logic
                try
                {
                    // Pretend to send email
                    GlobalVariables.data = "Email sent for order " + orderId;
                }
                catch
                {
                    // ignore email errors
                }
                break;
            case "delivered":
                newStatus = GlobalVariables.ORDER_DELIVERED;
                break;
            case "cancelled":
                newStatus = GlobalVariables.ORDER_CANCELLED;
                // Bad practice: refund logic in status update
                try
                {
                    using (var conn = new SqlConnection(GlobalVariables.connectionString))
                    {
                        conn.Open();
                        var sql = "SELECT Total, PaymentMethod FROM Orders WHERE OrderId = " + orderId;
                        var cmd = new SqlCommand(sql, conn);
                        var reader = cmd.ExecuteReader();
                        if (reader.Read())
                        {
                            decimal refundAmount = (decimal)reader["Total"];
                            string paymentMethod = (string)reader["PaymentMethod"];
                            
                            // Bad practice: nested if for refund logic
                            if (paymentMethod == "credit_card")
                            {
                                refundAmount = refundAmount * 0.98m; // 2% fee not refunded
                            }
                            else if (paymentMethod == "paypal")
                            {
                                refundAmount = refundAmount * 0.97m; // 3% fee not refunded
                            }
                            
                            GlobalVariables.obj = new { refund = refundAmount };
                        }
                    }
                }
                catch
                {
                    // ignore refund errors
                }
                break;
            default:
                return BadRequest("Invalid status");
        }
        
        try
        {
            using (var conn = new SqlConnection(GlobalVariables.connectionString))
            {
                conn.Open();
                var sql = $"UPDATE Orders SET Status = '{newStatus}' WHERE OrderId = {orderId}";
                var cmd = new SqlCommand(sql, conn);
                var rows = cmd.ExecuteNonQuery();
                
                if (rows > 0)
                {
                    return Ok("Status updated");
                }
                else
                {
                    return NotFound();
                }
            }
        }
        catch
        {
            return BadRequest("Update failed");
        }
    }
    
    // ============ SHOPPING CART METHODS ============
    
    [HttpPost("AddToCart")]
    public IActionResult AddToCart([FromBody] dynamic item)
    {
        // Bad practice: no validation
        GlobalVariables.shoppingCart.Add(item);
        
        // Bad practice: manual total calculation
        try
        {
            GlobalVariables.totalAmount += Convert.ToDecimal(item.price) * Convert.ToInt32(item.quantity);
        }
        catch
        {
            // ignore calculation errors
        }
        
        GlobalVariables.cartId++;
        
        return Ok(new { cartSize = GlobalVariables.shoppingCart.Count });
    }
    
    [HttpGet("GetCart")]
    public IActionResult GetCart()
    {
        // Bad practice: returning global state directly
        return Ok(new
        {
            items = GlobalVariables.shoppingCart,
            total = GlobalVariables.totalAmount,
            itemCount = GlobalVariables.shoppingCart.Count
        });
    }
    
    [HttpDelete("RemoveFromCart")]
    public IActionResult RemoveFromCart(int index)
    {
        // Bad practice: no bounds checking
        try
        {
            GlobalVariables.shoppingCart.RemoveAt(index);
            
            // Bad practice: recalculate total from scratch
            GlobalVariables.totalAmount = 0;
            foreach (dynamic item in GlobalVariables.shoppingCart)
            {
                try
                {
                    GlobalVariables.totalAmount += Convert.ToDecimal(item.price) * Convert.ToInt32(item.quantity);
                }
                catch
                {
                    continue;
                }
            }
            
            return Ok("Item removed");
        }
        catch
        {
            return BadRequest("Invalid index");
        }
    }
    
    [HttpPost("ClearCart")]
    public IActionResult ClearCart()
    {
        GlobalVariables.shoppingCart.Clear();
        GlobalVariables.totalAmount = 0;
        GlobalVariables.cartId = 0;
        
        return Ok("Cart cleared");
    }
    
    // ============ PAYMENT METHODS ============
    
    [HttpPost("ProcessPayment")]
    public IActionResult ProcessPayment([FromBody] dynamic paymentData)
    {
        string method = paymentData.method;
        decimal amount = paymentData.amount;
        
        // Bad practice: deeply nested payment processing
        if (method == "credit_card")
        {
            string cardNumber = paymentData.cardNumber;
            string cvv = paymentData.cvv;
            string expiry = paymentData.expiry;
            
            // Bad practice: credit card validation
            if (!string.IsNullOrEmpty(cardNumber))
            {
                if (cardNumber.Length == 16)
                {
                    if (!string.IsNullOrEmpty(cvv))
                    {
                        if (cvv.Length == 3 || cvv.Length == 4)
                        {
                            if (!string.IsNullOrEmpty(expiry))
                            {
                                // Bad practice: fake processing
                                System.Threading.Thread.Sleep(2000); // simulate API call
                                
                                // Bad practice: random success/failure
                                if (new Random().Next(10) > 1) // 90% success rate
                                {
                                    // Bad practice: logging sensitive data
                                    GlobalVariables.data = $"Payment processed for card ending in {cardNumber.Substring(12)}";
                                    
                                    // Apply fee
                                    decimal totalWithFee = amount + (amount * GlobalVariables.creditCardFee);
                                    
                                    return Ok(new { success = true, transactionId = Guid.NewGuid().ToString(), charged = totalWithFee });
                                }
                                else
                                {
                                    return BadRequest("Payment declined");
                                }
                            }
                            else
                            {
                                return BadRequest("Invalid expiry date");
                            }
                        }
                        else
                        {
                            return BadRequest("Invalid CVV");
                        }
                    }
                    else
                    {
                        return BadRequest("CVV required");
                    }
                }
                else
                {
                    return BadRequest("Invalid card number");
                }
            }
            else
            {
                return BadRequest("Card number required");
            }
        }
        else if (method == "paypal")
        {
            string email = paymentData.email;
            string password = paymentData.password; // Bad practice: asking for PayPal password
            
            if (!string.IsNullOrEmpty(email))
            {
                if (email.Contains("@"))
                {
                    // Bad practice: fake PayPal processing
                    System.Threading.Thread.Sleep(3000); // simulate API call
                    
                    // Apply fee
                    decimal totalWithFee = amount + (amount * GlobalVariables.paypalFee);
                    
                    // Bad practice: hardcoded response
                    return Ok(new { success = true, paypalTransactionId = "PP-" + new Random().Next(100000, 999999), charged = totalWithFee });
                }
                else
                {
                    return BadRequest("Invalid email");
                }
            }
            else
            {
                return BadRequest("Email required for PayPal");
            }
        }
        else if (method == "bank_transfer")
        {
            string accountNumber = paymentData.accountNumber;
            string routingNumber = paymentData.routingNumber;
            
            if (!string.IsNullOrEmpty(accountNumber) && !string.IsNullOrEmpty(routingNumber))
            {
                // Bad practice: no real validation
                if (accountNumber.Length > 5 && routingNumber.Length == 9)
                {
                    // No fee for bank transfer
                    return Ok(new 
                    { 
                        success = true, 
                        message = $"Bank transfer initiated. Will be processed in {GlobalVariables.bankTransferDays} business days",
                        referenceNumber = "BT-" + DateTime.Now.Ticks
                    });
                }
                else
                {
                    return BadRequest("Invalid account details");
                }
            }
            else
            {
                return BadRequest("Account details required");
            }
        }
        else
        {
            return BadRequest("Unsupported payment method");
        }
    }
    
    // ============ USER METHODS ============
    
    [HttpPost("Login")]
    public IActionResult Login([FromBody] dynamic credentials)
    {
        string email = credentials.email;
        string password = credentials.password;
        
        // Bad practice: hardcoded users
        if (email == "admin@store.com" && password == "admin123")
        {
            GlobalVariables.isLoggedIn = true;
            GlobalVariables.userEmail = email;
            GlobalVariables.currentUser["role"] = "admin";
            GlobalVariables.currentUser["loginTime"] = DateTime.Now;
            
            return Ok(new { success = true, user = "admin" });
        }
        else if (email == "user@store.com" && password == "user123")
        {
            GlobalVariables.isLoggedIn = true;
            GlobalVariables.userEmail = email;
            GlobalVariables.currentUser["role"] = "user";
            GlobalVariables.currentUser["loginTime"] = DateTime.Now;
            
            return Ok(new { success = true, user = "user" });
        }
        else
        {
            // Bad practice: user enumeration
            using (var conn = new SqlConnection(GlobalVariables.connectionString))
            {
                try
                {
                    conn.Open();
                    // Bad practice: plain text password comparison
                    var sql = $"SELECT * FROM Users WHERE Email = '{email}' AND Password = '{password}'";
                    var cmd = new SqlCommand(sql, conn);
                    var reader = cmd.ExecuteReader();
                    
                    if (reader.Read())
                    {
                        GlobalVariables.isLoggedIn = true;
                        GlobalVariables.userEmail = email;
                        GlobalVariables.currentUser["id"] = reader["UserId"];
                        
                        return Ok(new { success = true });
                    }
                    else
                    {
                        return BadRequest("Invalid credentials");
                    }
                }
                catch
                {
                    return BadRequest("Login failed");
                }
            }
        }
    }
    
    [HttpPost("Logout")]
    public IActionResult Logout()
    {
        // Bad practice: clearing global state
        GlobalVariables.isLoggedIn = false;
        GlobalVariables.userEmail = "";
        GlobalVariables.currentUser.Clear();
        GlobalVariables.shoppingCart.Clear();
        GlobalVariables.totalAmount = 0;
        
        return Ok("Logged out");
    }
    
    [HttpPost("Register")]
    public IActionResult Register([FromBody] dynamic userData)
    {
        string email = userData.email;
        string password = userData.password;
        string name = userData.name;
        
        // Bad practice: weak validation
        if (string.IsNullOrEmpty(email) || string.IsNullOrEmpty(password))
        {
            return BadRequest("Email and password required");
        }
        
        if (password.Length < 3) // Bad practice: weak password requirement
        {
            return BadRequest("Password too short");
        }
        
        try
        {
            using (var conn = new SqlConnection(GlobalVariables.connectionString))
            {
                conn.Open();
                
                // Bad practice: check if user exists with concatenated SQL
                var checkSql = $"SELECT COUNT(*) FROM Users WHERE Email = '{email}'";
                var checkCmd = new SqlCommand(checkSql, conn);
                var count = (int)checkCmd.ExecuteScalar();
                
                if (count > 0)
                {
                    return BadRequest("User already exists");
                }
                
                // Bad practice: plain text password storage
                var userId = GlobalVariables.userIdCounter++;
                var sql = $"INSERT INTO Users (UserId, Email, Password, Name) VALUES ({userId}, '{email}', '{password}', '{name}')";
                var cmd = new SqlCommand(sql, conn);
                cmd.ExecuteNonQuery();
                
                // Bad practice: auto-login after registration
                GlobalVariables.isLoggedIn = true;
                GlobalVariables.userEmail = email;
                
                return Ok(new { success = true, userId = userId });
            }
        }
        catch (Exception ex)
        {
            GlobalVariables.errorMessages.Add(ex.Message);
            return BadRequest("Registration failed");
        }
    }
    
    // ============ UTILITY METHODS ============
    
    [HttpGet("GetStats")]
    public IActionResult GetStats()
    {
        // Bad practice: exposing internal state
        return Ok(new
        {
            errorCount = GlobalVariables.errorCount,
            lastError = GlobalVariables.lastError,
            errorMessages = GlobalVariables.errorMessages,
            currentUser = GlobalVariables.currentUser,
            isLoggedIn = GlobalVariables.isLoggedIn,
            cartSize = GlobalVariables.shoppingCart.Count,
            totalAmount = GlobalVariables.totalAmount,
            productIdCounter = GlobalVariables.productIdCounter,
            orderIdCounter = GlobalVariables.orderIdCounter,
            userIdCounter = GlobalVariables.userIdCounter,
            temp = GlobalVariables.temp,
            data = GlobalVariables.data,
            obj = GlobalVariables.obj
        });
    }
    
    [HttpPost("Calculate")]
    public IActionResult Calculate([FromBody] dynamic data)
    {
        // Bad practice: random utility method in main controller
        try
        {
            decimal subtotal = data.subtotal;
            string type = data.type;
            
            decimal result = 0;
            
            // Bad practice: business logic scattered
            if (type == "tax")
            {
                result = subtotal * (decimal)GlobalVariables.taxRate;
            }
            else if (type == "shipping")
            {
                if (subtotal < GlobalVariables.shippingThreshold)
                {
                    result = 10;
                }
                else
                {
                    result = 0;
                }
            }
            else if (type == "discount")
            {
                string code = data.code;
                // Bad practice: hardcoded discount codes
                if (code == "SAVE10")
                {
                    result = subtotal * 0.1m;
                }
                else if (code == "SAVE20")
                {
                    result = subtotal * 0.2m;
                }
                else if (code == "FREESHIP")
                {
                    result = 0; // free shipping, not a discount
                    GlobalVariables.flag = true; // what does this mean?
                }
            }
            
            return Ok(new { calculated = result });
        }
        catch
        {
            return BadRequest("Calculation error");
        }
    }
}