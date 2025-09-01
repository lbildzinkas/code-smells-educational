# Code smell: Another utility module with mixed responsibilities
import pyodbc
import global_variables
import time
from datetime import datetime

# Bad practice: non-static utility class equivalent (functions that should be methods)
class Helper:
    # Bad practice: class with only static-like methods
    
    @staticmethod
    def get_data(query):
        try:
            results = []
            
            conn = pyodbc.connect(global_variables.CONNECTION_STRING)
            cursor = conn.cursor()
            cursor.execute(query)  # SQL injection risk
            rows = cursor.fetchall()
            
            for row in rows:
                row_dict = {}
                for i, col in enumerate(cursor.description):
                    row_dict[col[0]] = row[i]
                results.append(row_dict)
                
            conn.close()
            
            # Bad practice: returning different types
            if len(results) == 0:
                return None
            elif len(results) == 1:
                return results[0]
            else:
                return results
                
        except Exception as e:
            # Bad practice: returning exception as result
            return str(e)
    
    @staticmethod
    def generate_html(html_type, data):
        html = ""
        
        if html_type == "product":
            # Bad practice: inline HTML generation
            html = f"<div class='product'><h2>{data.get('name', 'N/A')}</h2><p>Price: ${data.get('price', 0)}</p><button onclick='addToCart({data.get('id', 0)})'>Add to Cart</button></div>"
        elif html_type == "order":
            html = f"<div class='order'><h3>Order #{data.get('id', 'N/A')}</h3><p>Total: ${data.get('total', 0)}</p><p>Status: {data.get('status', 'Unknown')}</p></div>"
        elif html_type == "error":
            html = f"<div style='color:red;font-weight:bold;'>ERROR: {data}</div>"
            
        # Bad practice: modifying global state
        global_variables.temp = html
        
        return html
    
    @staticmethod 
    def apply_discount(price, customer_type, is_first_order, quantity):
        discounted_price = price
        
        # Bad practice: complex nested conditions
        if customer_type == "VIP":
            if quantity > 10:
                discounted_price = price * 0.7  # 30% off
            elif quantity > 5:
                discounted_price = price * 0.8  # 20% off
            else:
                discounted_price = price * 0.9  # 10% off
                
            if is_first_order:
                # Additional 5% for first order
                discounted_price = discounted_price * 0.95
        elif customer_type == "Regular":
            if quantity > 20:
                discounted_price = price * 0.95  # 5% off
                
            if is_first_order:
                # Additional 10% for first order
                discounted_price = discounted_price * 0.9
        elif customer_type == "New":
            if is_first_order:
                discounted_price = price * 0.85  # 15% off first order
                
        # Bad practice: magic number
        if discounted_price < 10:
            discounted_price = 10  # minimum price
            
        return discounted_price
    
    @staticmethod
    def log_something(message):
        try:
            # Bad practice: hardcoded file path
            with open("/var/log/store.log", "a") as f:
                f.write(f"{datetime.now()}: {message}\n")
        except:
            # Bad practice: try alternative path without checking OS
            try:
                with open("C:\\logs\\store.log", "a") as f:
                    f.write(f"{datetime.now()}: {message}\n")
            except:
                # Give up silently
                pass
    
    @staticmethod
    def send_email(to, subject, body):
        try:
            # Bad practice: fake email sending
            if not to or "@" not in to:
                return False
                
            # Simulate email sending
            time.sleep(1)
            
            # Bad practice: always return true
            return True
        except:
            return False
    
    @staticmethod
    def process_order(order_id, action):
        result = {}
        
        if action == "calculate":
            # Bad practice: direct database access in helper
            order_data = Helper.get_data(f"SELECT * FROM Orders WHERE OrderId = {order_id}")
            if isinstance(order_data, dict):
                total = float(order_data["Total"])
                tax = total * 0.15
                shipping = 10 if total < 50 else 0
                
                result["subtotal"] = total
                result["tax"] = tax  
                result["shipping"] = shipping
                result["grandTotal"] = total + tax + shipping
        elif action == "ship":
            # Bad practice: mixing concerns
            import random
            tracking_number = f"TRK{random.randint(100000, 999999)}"
            result["tracking"] = tracking_number
            result["carrier"] = "FastShip"
            result["estimatedDays"] = random.randint(3, 10)
            
            # Update database
            Helper.execute_non_query(f"UPDATE Orders SET TrackingNumber = '{tracking_number}' WHERE OrderId = {order_id}")
        elif action == "cancel":
            # Bad practice: no validation
            Helper.execute_non_query(f"UPDATE Orders SET Status = 'cancelled' WHERE OrderId = {order_id}")
            result["cancelled"] = True
            result["refundAmount"] = "pending calculation"
            
        return result
    
    @staticmethod
    def execute_non_query(sql):
        # Bad practice: duplicate database code
        try:
            conn = pyodbc.connect(global_variables.CONNECTION_STRING)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
        except:
            pass  # ignore errors

# Bad practice: functions outside of class doing similar things
def get_random_days():
    import random
    return random.randint(3, 10)

def calculate_tax_amount(amount):
    return amount * global_variables.TAX_RATE

def format_currency(amount, currency="USD"):
    # Bad practice: hardcoded formatting
    if currency == "USD":
        return f"${amount:.2f}"
    elif currency == "EUR":
        return f"€{amount:.2f}"
    else:
        return f"{amount:.2f} {currency}"

# Bad practice: async function mixed with sync code
async def async_process_data(data):
    # This doesn't make sense in this context
    import asyncio
    await asyncio.sleep(0.1)
    return data.upper()

# Bad practice: function that mutates input
def process_list_in_place(items):
    for i in range(len(items)):
        if isinstance(items[i], str):
            items[i] = items[i].upper()
        elif isinstance(items[i], (int, float)):
            items[i] = items[i] * 2
    
    # Also modifies global state
    global_variables.obj = items
    return items

# Bad practice: recursive function without base case protection
def factorial(n, depth=0):
    if depth > 1000:  # Weak protection
        return 1
    if n <= 1:
        return 1
    return n * factorial(n-1, depth+1)

# Bad practice: function with confusing name and behavior
def is_valid_data(data):
    # This function actually fixes data instead of just validating
    if data is None:
        data = {}
    if isinstance(data, str) and data == "":
        data = "default"
    if isinstance(data, list) and len(data) == 0:
        data = ["empty"]
    
    # Modifies global state
    global_variables.data = data
    
    # Always returns True regardless of input
    return True

# Bad practice: function that can fail silently
def safe_convert_to_int(value):
    try:
        return int(value)
    except:
        # Returns random number on failure
        import random
        return random.randint(1, 100)

# Bad practice: function with side effects not mentioned in name
def get_user_name(user_id):
    # Side effect: also logs the access
    global_variables.error_messages.append(f"User {user_id} name accessed")
    
    # Side effect: increments global counter
    global_variables.x += 1
    
    # Actual functionality
    return f"User_{user_id}"

# Bad practice: performance killer function
def slow_operation():
    # Bad practice: busy waiting
    start = time.time()
    while time.time() - start < 2:
        # Waste CPU cycles
        _ = sum(range(1000))
    
    return "Done wasting time"

# Bad practice: function that modifies sys.path
def add_to_python_path(path):
    import sys
    if path not in sys.path:
        sys.path.append(path)
    
    # Bad practice: modifying global variables too
    global_variables.temp = path