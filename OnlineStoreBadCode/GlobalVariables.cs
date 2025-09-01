namespace OnlineStoreBadCode;

// This class is a code smell: God Object with global state
public static class GlobalVariables
{
    // Bad practice: hardcoded connection string
    public static string connectionString = "Server=localhost;Database=OnlineStore;User Id=sa;Password=MyPass123!;";
    
    // Bad practice: global mutable state
    public static List<object> shoppingCart = new List<object>();
    public static Dictionary<string, object> currentUser = new Dictionary<string, object>();
    public static int cartId = 0;
    public static bool isLoggedIn = false;
    public static string userEmail = "";
    public static decimal totalAmount = 0;
    
    // Bad practice: magic numbers as globals
    public static double taxRate = 0.15; // what does this mean?
    public static int maxItems = 50; // max items for what?
    public static decimal shippingThreshold = 50; // in what currency?
    public static int timeout = 30; // seconds? minutes?
    
    // Bad practice: hardcoded API keys
    public static string paypalApiKey = "pk_test_1234567890abcdef";
    public static string stripeSecretKey = "sk_test_abcdef1234567890";
    public static string emailServiceKey = "key-abc123def456";
    
    // Bad practice: temporary variables as globals
    public static object temp;
    public static string data;
    public static int x;
    public static bool flag;
    public static dynamic obj;
    
    // Bad practice: hardcoded URLs
    public static string apiUrl = "https://api.ourstore.com";
    public static string paymentGateway = "https://payment.gateway.com/api/v1";
    
    // Bad practice: status codes as strings
    public static string ORDER_PENDING = "pending";
    public static string ORDER_PROCESSING = "processing";
    public static string ORDER_SHIPPED = "shipped";
    public static string ORDER_DELIVERED = "delivered";
    public static string ORDER_CANCELLED = "cancelled";
    
    // Bad practice: mixed responsibilities
    public static List<string> errorMessages = new List<string>();
    public static DateTime lastError;
    public static int errorCount = 0;
    
    // Bad practice: hardcoded business rules
    public static decimal creditCardFee = 0.02M; // 2%
    public static decimal paypalFee = 0.03M; // 3%
    public static int bankTransferDays = 5;
    
    // Bad practice: global counters
    public static int productIdCounter = 1000;
    public static int orderIdCounter = 5000;
    public static int userIdCounter = 100;
}