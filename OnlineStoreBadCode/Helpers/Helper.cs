using System.Data.SqlClient;

namespace OnlineStoreBadCode.Helpers;

// Code smell: Another utility class with mixed responsibilities
public class Helper
{
    // Bad practice: non-static utility class
    
    // Bad practice: database operations in helper class
    public object GetData(string query)
    {
        try
        {
            var results = new List<Dictionary<string, object>>();
            
            using (var conn = new SqlConnection(GlobalVariables.connectionString))
            {
                conn.Open();
                var cmd = new SqlCommand(query, conn); // SQL injection risk
                var reader = cmd.ExecuteReader();
                
                while (reader.Read())
                {
                    var row = new Dictionary<string, object>();
                    for (int i = 0; i < reader.FieldCount; i++)
                    {
                        row[reader.GetName(i)] = reader.GetValue(i);
                    }
                    results.Add(row);
                }
            }
            
            // Bad practice: returning different types
            if (results.Count == 0)
            {
                return null;
            }
            else if (results.Count == 1)
            {
                return results[0];
            }
            else
            {
                return results;
            }
        }
        catch (Exception ex)
        {
            // Bad practice: returning exception as result
            return ex.Message;
        }
    }
    
    // Bad practice: HTML generation in helper
    public string GenerateHtml(string type, object data)
    {
        string html = "";
        
        if (type == "product")
        {
            // Bad practice: inline HTML
            dynamic product = data;
            html = $"<div class='product'><h2>{product.name}</h2><p>Price: ${product.price}</p><button onclick='addToCart({product.id})'>Add to Cart</button></div>";
        }
        else if (type == "order")
        {
            dynamic order = data;
            html = $"<div class='order'><h3>Order #{order.id}</h3><p>Total: ${order.total}</p><p>Status: {order.status}</p></div>";
        }
        else if (type == "error")
        {
            html = $"<div style='color:red;font-weight:bold;'>ERROR: {data}</div>";
        }
        
        // Bad practice: modifying global state
        GlobalVariables.temp = html;
        
        return html;
    }
    
    // Bad practice: business logic in helper
    public decimal ApplyDiscount(decimal price, string customerType, bool isFirstOrder, int quantity)
    {
        decimal discountedPrice = price;
        
        // Bad practice: complex nested conditions
        if (customerType == "VIP")
        {
            if (quantity > 10)
            {
                discountedPrice = price * 0.7m; // 30% off
            }
            else if (quantity > 5)
            {
                discountedPrice = price * 0.8m; // 20% off
            }
            else
            {
                discountedPrice = price * 0.9m; // 10% off
            }
            
            if (isFirstOrder)
            {
                // Additional 5% for first order
                discountedPrice = discountedPrice * 0.95m;
            }
        }
        else if (customerType == "Regular")
        {
            if (quantity > 20)
            {
                discountedPrice = price * 0.95m; // 5% off
            }
            
            if (isFirstOrder)
            {
                // Additional 10% for first order
                discountedPrice = discountedPrice * 0.9m;
            }
        }
        else if (customerType == "New")
        {
            if (isFirstOrder)
            {
                discountedPrice = price * 0.85m; // 15% off first order
            }
        }
        
        // Bad practice: magic number
        if (discountedPrice < 10)
        {
            discountedPrice = 10; // minimum price
        }
        
        return discountedPrice;
    }
    
    // Bad practice: file operations without proper error handling
    public void LogSomething(string message)
    {
        try
        {
            // Bad practice: hardcoded file path
            System.IO.File.AppendAllText("C:\\logs\\store.log", DateTime.Now + ": " + message + Environment.NewLine);
        }
        catch
        {
            // Bad practice: try alternative path without checking OS
            try
            {
                System.IO.File.AppendAllText("/tmp/store.log", DateTime.Now + ": " + message + Environment.NewLine);
            }
            catch
            {
                // Give up silently
            }
        }
    }
    
    // Bad practice: crypto operations in helper
    public string HashPassword(string password)
    {
        // Bad practice: weak hashing
        int hash = 0;
        foreach (char c in password)
        {
            hash += (int)c;
        }
        
        // Bad practice: predictable hash
        return "HASH_" + hash.ToString() + "_" + password.Length;
    }
    
    // Bad practice: email sending in helper
    public bool SendEmail(string to, string subject, string body)
    {
        try
        {
            // Bad practice: fake email sending
            if (string.IsNullOrEmpty(to) || !to.Contains("@"))
            {
                return false;
            }
            
            // Simulate email sending
            System.Threading.Thread.Sleep(1000);
            
            // Bad practice: always return true
            return true;
        }
        catch
        {
            return false;
        }
    }
    
    // Bad practice: method that does multiple unrelated things
    public Dictionary<string, object> ProcessOrder(int orderId, string action)
    {
        var result = new Dictionary<string, object>();
        
        if (action == "calculate")
        {
            // Bad practice: direct database access
            var orderData = GetData($"SELECT * FROM Orders WHERE OrderId = {orderId}");
            if (orderData is Dictionary<string, object> order)
            {
                decimal total = Convert.ToDecimal(order["Total"]);
                decimal tax = total * 0.15m;
                decimal shipping = total < 50 ? 10 : 0;
                
                result["subtotal"] = total;
                result["tax"] = tax;
                result["shipping"] = shipping;
                result["grandTotal"] = total + tax + shipping;
            }
        }
        else if (action == "ship")
        {
            // Bad practice: mixing concerns
            var trackingNumber = "TRK" + DateTime.Now.Ticks;
            result["tracking"] = trackingNumber;
            result["carrier"] = "FastShip";
            result["estimatedDays"] = Helper.GetRandomDays();
            
            // Update database
            ExecuteNonQuery($"UPDATE Orders SET TrackingNumber = '{trackingNumber}' WHERE OrderId = {orderId}");
        }
        else if (action == "cancel")
        {
            // Bad practice: no validation
            ExecuteNonQuery($"UPDATE Orders SET Status = 'cancelled' WHERE OrderId = {orderId}");
            result["cancelled"] = true;
            result["refundAmount"] = "pending calculation";
        }
        
        return result;
    }
    
    // Bad practice: static method in non-static class
    public static int GetRandomDays()
    {
        return new Random().Next(3, 10);
    }
    
    // Bad practice: duplicate database code
    private void ExecuteNonQuery(string sql)
    {
        using (var conn = new SqlConnection(GlobalVariables.connectionString))
        {
            conn.Open();
            var cmd = new SqlCommand(sql, conn);
            cmd.ExecuteNonQuery();
        }
    }
}