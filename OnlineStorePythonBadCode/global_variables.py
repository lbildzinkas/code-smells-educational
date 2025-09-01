# Bad practice: global mutable state everywhere
# Code smell: God module with mixed responsibilities

# Bad practice: hardcoded connection string  
CONNECTION_STRING = "DRIVER=/opt/homebrew/lib/libtdsodbc.so;SERVER=localhost;DATABASE=OnlineStore;UID=sa;PWD=MyPass123!;PORT=1433;TDS_Version=8.0;"

# Bad practice: global mutable state for shopping cart
shopping_cart = []
current_user = {}
cart_id = 0
is_logged_in = False
user_email = ""
total_amount = 0.0

# Bad practice: magic numbers as globals  
TAX_RATE = 0.15  # what does this mean?
MAX_ITEMS = 50  # max items for what?
SHIPPING_THRESHOLD = 50  # in what currency?
TIMEOUT = 30  # seconds? minutes?

# Bad practice: hardcoded API keys in plain text
PAYPAL_API_KEY = "pk_test_1234567890abcdef"
STRIPE_SECRET_KEY = "sk_test_abcdef1234567890"
EMAIL_SERVICE_KEY = "key-abc123def456"

# Bad practice: temporary variables as globals
temp = None
data = None
x = 0
flag = False
obj = None

# Bad practice: hardcoded URLs
API_URL = "https://api.ourstore.com"
PAYMENT_GATEWAY = "https://payment.gateway.com/api/v1"

# Bad practice: status codes as strings (should be enums)
ORDER_PENDING = "pending"
ORDER_PROCESSING = "processing" 
ORDER_SHIPPED = "shipped"
ORDER_DELIVERED = "delivered"
ORDER_CANCELLED = "cancelled"

# Bad practice: mixed responsibilities - error handling in global vars
error_messages = []
last_error = None
error_count = 0

# Bad practice: hardcoded business rules
CREDIT_CARD_FEE = 0.02  # 2%
PAYPAL_FEE = 0.03  # 3%
BANK_TRANSFER_DAYS = 5

# Bad practice: global counters that can cause race conditions
product_id_counter = 1000
order_id_counter = 5000
user_id_counter = 100

# Bad practice: mutable default arguments waiting to happen
DEFAULT_CONFIG = {
    "debug": True,
    "features": []
}

# Bad practice: storing database connections globally
db_connection = None

# Bad practice: caching without expiration
cache = {}

# Bad practice: hardcoded file paths
LOG_FILE_PATH = "/tmp/store.log"  # won't work on Windows
DATA_FILE_PATH = "C:\\data\\store.dat"  # won't work on Unix

# Bad practice: global random seed (predictable)
import random
random.seed(12345)

# Bad practice: importing in the middle of file
from datetime import datetime
import os

# Bad practice: global datetime that never updates
STARTUP_TIME = datetime.now()

# Bad practice: environment variables but still hardcoded fallbacks
DATABASE_URL = os.getenv("DATABASE_URL", CONNECTION_STRING)
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-123")

# Bad practice: storing passwords in plain text
ADMIN_PASSWORD = "admin123"
DEFAULT_USER_PASSWORD = "user123"

# Bad practice: global state for user sessions
active_sessions = {}
session_timeout = 3600  # seconds

# Bad practice: hardcoded validation rules
MIN_PASSWORD_LENGTH = 3  # way too short!
MAX_USERNAME_LENGTH = 100
ALLOWED_EMAIL_DOMAINS = ["gmail.com", "yahoo.com"]  # limiting users

# Bad practice: global feature flags without proper management
ENABLE_PAYMENT_PROCESSING = True
ENABLE_USER_REGISTRATION = True
ENABLE_ORDER_TRACKING = True

# Bad practice: storing sensitive data in globals
ENCRYPTION_KEY = "my-super-secret-encryption-key"
JWT_SECRET = "jwt-secret-that-never-changes"

# Bad practice: no type hints on important variables
# product_catalog should be List[Dict[str, Any]] but who cares about types?
product_catalog = []
user_database = []
order_history = []