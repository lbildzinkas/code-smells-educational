# Code smell: Utility module with random unrelated methods
# Bad practice: no proper imports
import global_variables
import random
import string

# Bad practice: method names that don't describe what they do
def do_stuff(input_data):
    if input_data is None:
        return None
        
    # Bad practice: type checking with strings
    if "product" in str(input_data):
        return f"PROD_{str(input_data).upper()}"
    elif "order" in str(input_data):
        return f"ORD_{str(input_data).upper()}"
    else:
        return input_data

# Bad practice: method that does too many things
def process_data(data, type_num, flag):
    result = ""
    
    # Bad practice: magic numbers
    if type_num == 1:
        result = data.upper()
        if flag:
            result = result.replace(" ", "_")
    elif type_num == 2:
        result = data.lower() 
        if flag:
            result = result.replace("_", " ")
    elif type_num == 3:
        # Bad practice: complex string manipulation
        for i, char in enumerate(data):
            if i % 2 == 0:
                result += char.upper()
            else:
                result += char.lower()
    else:
        # Bad practice: returning input when type is unknown
        result = data
        
    # Bad practice: side effect
    global_variables.data = result
    
    return result

# Bad practice: method that should be in a Math class
def calculate_something(a, b, operation):
    result = 0.0
    
    # Bad practice: string comparison for operations
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        # Bad practice: no zero check
        result = a / b
    elif operation == "percentage":
        result = (a / b) * 100
    elif operation == "tax":
        # Bad practice: hardcoded tax rate
        result = a * 1.15
        
    # Bad practice: global state mutation
    global_variables.x = int(result)
    
    return result

# Bad practice: SQL generation in utility module
def build_query(table, conditions):
    sql = f"SELECT * FROM {table} WHERE 1=1"
    
    # Bad practice: SQL injection vulnerability
    for key, value in conditions.items():
        if isinstance(value, str):
            sql += f" AND {key} = '{value}'"
        elif isinstance(value, (int, float)):
            sql += f" AND {key} = {value}"
        elif isinstance(value, bool):
            sql += f" AND {key} = {1 if value else 0}"
            
    return sql

# Bad practice: date manipulation with strings
def format_date(date_obj, format_type):
    # Bad practice: no type checking
    try:
        if format_type == 1:
            return date_obj.strftime("%m/%d/%Y")
        elif format_type == 2:
            return date_obj.strftime("%d/%m/%Y")
        elif format_type == 3:
            return date_obj.strftime("%Y-%m-%d")
        elif format_type == 4:
            return date_obj.strftime("%b %d, %Y")
        elif format_type == 5:
            # Bad practice: custom format
            return f"{date_obj.day} of {date_obj.strftime('%B')}, {date_obj.year}"
        else:
            return str(date_obj)
    except:
        # Bad practice: swallow all exceptions
        return "Invalid Date"

# Bad practice: validation method that's too generic
def validate(value, validation_type):
    try:
        if validation_type == "email":
            # Bad practice: weak email validation
            return "@" in str(value)
        elif validation_type == "phone":
            # Bad practice: US-only phone validation
            return len(str(value)) == 10
        elif validation_type == "creditcard":
            # Bad practice: only checks length
            return len(str(value)) == 16
        elif validation_type == "positive":
            return float(value) > 0
        elif validation_type == "notempty":
            return len(str(value)) > 0
        else:
            # Bad practice: default to true
            return True
    except:
        # Bad practice: swallow exceptions
        return False

# Bad practice: random number generator with side effects
def get_random_number(min_val, max_val):
    # Bad practice: no seed management
    result = random.randint(min_val, max_val)
    
    # Bad practice: logging in utility method
    global_variables.error_messages.append(f"Generated random number: {result}")
    
    return result

# Bad practice: file operations without proper error handling  
def write_to_file(filename, content):
    try:
        # Bad practice: hardcoded file path
        with open(f"/tmp/{filename}", "w") as f:
            f.write(content)
        return True
    except:
        # Bad practice: try alternative path without checking OS
        try:
            with open(f"C:\\temp\\{filename}", "w") as f:
                f.write(content)
            return True
        except:
            # Give up silently
            return False

# Bad practice: crypto operations in utility
def hash_password(password):
    # Bad practice: weak hashing
    hash_val = 0
    for char in password:
        hash_val += ord(char)
        
    # Bad practice: predictable hash
    return f"HASH_{hash_val}_{len(password)}"

# Bad practice: method that returns different types
def get_data_from_somewhere(data_type):
    if data_type == "list":
        return [1, 2, 3]
    elif data_type == "dict":
        return {"key": "value"}
    elif data_type == "string":
        return "some string"
    elif data_type == "number":
        return 42
    elif data_type == "none":
        return None
    else:
        # Bad practice: returning boolean for unknown type
        return False

# Bad practice: function with mutable default argument
def add_to_list(item, target_list=[]):
    target_list.append(item)
    return target_list

# Bad practice: function that modifies global state unexpectedly
def process_item(item):
    # Bad practice: modifying global list
    global_variables.product_catalog.append(item)
    
    # Bad practice: side effects
    global_variables.flag = True
    global_variables.temp = item
    
    return "processed"

# Bad practice: inconsistent naming and no docstrings
def CALCULATE_TAX(amt):
    return amt * global_variables.TAX_RATE

def calculateShipping(amount):
    if amount < global_variables.SHIPPING_THRESHOLD:
        return 10.0
    return 0.0

def calc_discount(amt, code):
    # Bad practice: hardcoded discount logic
    discounts = {
        "SAVE10": 0.1,
        "SAVE20": 0.2,
        "SAVE50": 0.5
    }
    return amt * discounts.get(code, 0)

# Bad practice: debugging functions left in production code
def debug_print(msg):
    print(f"DEBUG: {msg}")
    global_variables.error_messages.append(f"DEBUG: {msg}")

def dump_globals():
    print("=== GLOBAL STATE DUMP ===")
    print(f"Shopping cart: {global_variables.shopping_cart}")
    print(f"Current user: {global_variables.current_user}")
    print(f"Is logged in: {global_variables.is_logged_in}")
    print("========================")

# Bad practice: monkey patching built-in functions
def evil_print(*args, **kwargs):
    # Intercept all print statements
    global_variables.error_messages.append(" ".join(str(arg) for arg in args))
    print(*args, **kwargs)

# Bad practice: function that can crash the entire application
def dangerous_operation():
    # This could bring down the whole API
    global_variables.shopping_cart = None
    global_variables.current_user = None
    return "Oops!"