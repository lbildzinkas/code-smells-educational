# Code smell: Poorly named module
import global_variables
import threading
import time
import gc

# Bad practice: class with terrible name
class Stuff:
    # Bad practice: public instance variables
    def __init__(self):
        self.temp = None
        self.counter = 0
        self.data = None
        self.flag = False
        
        # Bad practice: side effects in constructor
        global_variables.obj = self
    
    # Bad practice: method name gives no clue what it does
    def process(self, *args, **kwargs):
        # Bad practice: no parameter validation
        if len(args) == 0:
            return None
            
        # Bad practice: type checking with try-catch
        for arg in args:
            try:
                int_val = int(arg)
                self.counter += int_val
            except:
                try:
                    self.temp = str(self.temp) + str(arg)
                except:
                    self.data = arg
                    
        # Bad practice: returning different types based on state
        if self.counter > 0 and self.temp:
            return {"number": self.counter, "text": self.temp}
        elif self.counter > 0:
            return self.counter
        elif self.temp:
            return self.temp
        else:
            return self.data
    
    # Bad practice: method that changes behavior based on global state
    def transform(self, input_data):
        if global_variables.flag:
            return str(input_data).upper()
        elif global_variables.x > 10:
            return str(input_data).lower()  
        elif global_variables.is_logged_in:
            return f"USER: {input_data}"
        else:
            return str(input_data)
    
    # Bad practice: cache implementation without expiration
    _cache = {}
    
    def get_from_cache(self, key):
        if key in self._cache:
            return self._cache[key]
            
        # Bad practice: generating cache value in getter
        if key.startswith("product"):
            value = "Cached Product Data"
        elif key.startswith("user"):
            value = {"id": 1, "name": "Cached User"}
        else:
            value = time.time()  # Bad practice: caching current time
            
        self._cache[key] = value
        return value
    
    # Bad practice: threading without synchronization
    def do_async(self, func):
        # Bad practice: fire and forget
        def wrapper():
            try:
                func()
            except:
                # Bad practice: swallow all exceptions
                pass
                
        thread = threading.Thread(target=wrapper)
        thread.start()
        # No way to wait for completion or get results
    
    # Bad practice: parsing method that modifies input
    def parse(self, input_str):
        # This should not modify the input!
        input_str = input_str.strip().lower()
        
        result = {}
        
        # Bad practice: naive parsing
        parts = input_str.split('&')
        for part in parts:
            kvp = part.split('=')
            if len(kvp) == 2:
                result[kvp[0]] = kvp[1]
            else:
                # Bad practice: using index as key
                result[str(len(result))] = part
                
        # Bad practice: side effect
        self.data = result
        
        return result
    
    # Bad practice: comparison method with side effects
    def compare(self, a, b):
        self.flag = False
        
        try:
            # Bad practice: comparing everything as strings
            str_a = str(a)
            str_b = str(b)
            
            if str_a == str_b:
                self.flag = True
                global_variables.flag = True
                return True
                
            # Bad practice: try numeric comparison
            try:
                num_a = float(a)
                num_b = float(b)
                
                # Bad practice: floating point equality
                if num_a == num_b:
                    self.flag = True
                    return True
            except:
                pass
                
            # Bad practice: case-insensitive fallback
            if str_a.lower() == str_b.lower():
                self.flag = True
                return True
                
            return False
        except:
            # Bad practice: exception means equal?
            return True
    
    # Bad practice: method that can crash other code
    def dangerous_reset(self):
        # This could break other parts of the application
        global_variables.shopping_cart = None
        global_variables.current_user = None
        global_variables.temp = None
        global_variables.data = None
        global_variables.obj = None
        global_variables.flag = False
        global_variables.x = 0
        
        # Force garbage collection (performance impact)
        gc.collect()

# Bad practice: functions outside class with similar functionality
def process_stuff(data, mode="default"):
    # Bad practice: mutable default argument would be worse, but this is still bad
    if mode == "upper":
        return str(data).upper()
    elif mode == "lower":
        return str(data).lower()
    elif mode == "reverse":
        return str(data)[::-1]
    else:
        return data

# Bad practice: global variables in module
global_counter = 0
global_data = []
global_state = {"initialized": False}

def increment_global():
    global global_counter
    global_counter += 1
    return global_counter

def add_to_global_data(item):
    global_data.append(item)
    global_variables.temp = global_data
    return len(global_data)

# Bad practice: function that modifies sys.modules
def monkey_patch_builtins():
    import builtins
    import sys
    
    # This is extremely dangerous!
    original_print = builtins.print
    
    def evil_print(*args, **kwargs):
        global_variables.error_messages.append(" ".join(str(arg) for arg in args))
        original_print("[INTERCEPTED]", *args, **kwargs)
    
    builtins.print = evil_print

# Bad practice: recursive function without proper termination
def fibonacci_bad(n, memo={}):
    # Mutable default argument + poor recursion
    if n in memo:
        return memo[n]
    
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        memo[n] = fibonacci_bad(n-1, memo) + fibonacci_bad(n-2, memo)
        return memo[n]

# Bad practice: function that imports in the middle
def dynamic_import_function(module_name):
    try:
        exec(f"import {module_name}")
        return True
    except:
        return False

# Bad practice: function with confusing control flow
def confusing_function(x):
    for i in range(10):
        if i == x:
            continue
        if i > x:
            break
        else:
            if i % 2:
                return i * 2
            else:
                pass
    else:
        return x
    
    return -1  # This line might never be reached

# Bad practice: function that uses eval/exec
def execute_user_code(code_string):
    # EXTREMELY DANGEROUS!
    try:
        result = eval(code_string)
        global_variables.temp = result
        return result
    except:
        try:
            exec(code_string)
            return "Executed"
        except:
            return "Failed"

# Bad practice: context manager that doesn't properly clean up
class BadContextManager:
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.resource = None
    
    def __enter__(self):
        self.resource = f"Resource_{self.resource_name}"
        global_variables.temp = self.resource
        return self.resource
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Bad practice: not actually cleaning up
        # self.resource should be cleaned up here
        pass

# Bad practice: generator that modifies global state
def bad_generator(items):
    for item in items:
        global_variables.x += 1
        global_data.append(item)
        yield item * 2

# Bad practice: decorator that modifies function behavior unpredictably
def unpredictable_decorator(func):
    def wrapper(*args, **kwargs):
        # Sometimes works, sometimes doesn't
        if global_variables.x % 2 == 0:
            return func(*args, **kwargs)
        else:
            return "Decorator says no!"
    return wrapper

# Bad practice: exception class that's too generic
class BadException(Exception):
    def __init__(self, message="Something bad happened"):
        super().__init__(message)
        # Side effect in exception constructor
        global_variables.error_count += 1
        global_variables.error_messages.append(message)

# Bad practice: metaclass that does unexpected things
class BadMeta(type):
    def __new__(cls, name, bases, attrs):
        # Modify all methods to log their calls
        for key, value in attrs.items():
            if callable(value) and not key.startswith('__'):
                def logged_method(original_method):
                    def wrapper(*args, **kwargs):
                        global_variables.error_messages.append(f"Called {original_method.__name__}")
                        return original_method(*args, **kwargs)
                    return wrapper
                attrs[key] = logged_method(value)
        
        return super().__new__(cls, name, bases, attrs)

class BadClass(metaclass=BadMeta):
    def some_method(self):
        return "This call will be logged"

# Bad practice: module-level code that runs on import
print("Stuff module imported!")  # This will execute on import
global_variables.error_messages.append("Stuff module imported")

# Bad practice: changing working directory on import
import os
try:
    os.chdir("/tmp")  # This could break other code
except:
    pass

# Bad practice: setting environment variables
os.environ["BAD_STUFF_MODULE"] = "loaded"