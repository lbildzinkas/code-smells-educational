// This module is a code smell: God Object with global state
// Bad practice: exporting mutable global variables

// Bad practice: hardcoded connection configuration
export const connectionConfig = {
    server: 'localhost',
    user: 'sa',
    password: 'MyPass123!',
    database: 'OnlineStore',
    options: {
        encrypt: false,
        trustServerCertificate: true,
        enableArithAbort: true
    }
};

// Bad practice: global mutable state
export var shoppingCart: any[] = [];
export var currentUser: any = {};
export var cartId = 0;
export var isLoggedIn = false;
export var userEmail = "";
export var totalAmount = 0;

// Bad practice: magic numbers as globals
export var taxRate = 0.15; // what does this mean?
export var maxItems = 50; // max items for what?
export var shippingThreshold = 50; // in what currency?
export var timeout = 30; // seconds? minutes?

// Bad practice: hardcoded API keys
export var paypalApiKey = "pk_test_1234567890abcdef";
export var stripeSecretKey = "sk_test_abcdef1234567890";
export var emailServiceKey = "key-abc123def456";

// Bad practice: temporary variables as globals
export var temp: any;
export var data: any;
export var x: number;
export var flag: boolean;
export var obj: any;

// Bad practice: hardcoded URLs
export var apiUrl = "https://api.ourstore.com";
export var paymentGateway = "https://payment.gateway.com/api/v1";

// Bad practice: status codes as strings
export var ORDER_PENDING = "pending";
export var ORDER_PROCESSING = "processing";
export var ORDER_SHIPPED = "shipped";
export var ORDER_DELIVERED = "delivered";
export var ORDER_CANCELLED = "cancelled";

// Bad practice: mixed responsibilities
export var errorMessages: string[] = [];
export var lastError: any;
export var errorCount = 0;

// Bad practice: hardcoded business rules
export var creditCardFee = 0.02; // 2%
export var paypalFee = 0.03; // 3%
export var bankTransferDays = 5;

// Bad practice: global counters
export var productIdCounter = 1000;
export var orderIdCounter = 5000;
export var userIdCounter = 100;

// Bad practice: storing passwords in plain text
export const ADMIN_PASSWORD = "admin123";
export const DEFAULT_USER_PASSWORD = "user123";

// Bad practice: global state for user sessions
export let activeSessions: any = {};
export const sessionTimeout = 3600; // seconds

// Bad practice: hardcoded validation rules
export const MIN_PASSWORD_LENGTH = 3; // way too short!
export const MAX_USERNAME_LENGTH = 100;
export const ALLOWED_EMAIL_DOMAINS = ["gmail.com", "yahoo.com"]; // limiting users

// Bad practice: global feature flags without proper management
export const ENABLE_PAYMENT_PROCESSING = true;
export const ENABLE_USER_REGISTRATION = true;
export const ENABLE_ORDER_TRACKING = true;

// Bad practice: storing sensitive data in globals
export const ENCRYPTION_KEY = "my-super-secret-encryption-key";
export const JWT_SECRET = "jwt-secret-that-never-changes";

// Bad practice: no type safety for important collections
export let productCatalog: any[] = [];
export let userDatabase: any[] = [];
export let orderHistory: any[] = [];

// Bad practice: function to mutate global state
export function resetGlobalState() {
    shoppingCart = [];
    currentUser = {};
    cartId = 0;
    isLoggedIn = false;
    userEmail = "";
    totalAmount = 0;
    errorMessages = [];
    errorCount = 0;
}

// Bad practice: function that modifies multiple globals
export function updateUserState(email: string) {
    isLoggedIn = true;
    userEmail = email;
    currentUser.email = email;
    currentUser.loginTime = new Date();
}

// Bad practice: creating a mutable globals object to bypass TypeScript's safety
export const globals = {
    shoppingCart,
    currentUser,
    cartId,
    isLoggedIn,
    userEmail,
    totalAmount,
    temp,
    data,
    x,
    flag,
    obj,
    errorMessages,
    lastError,
    errorCount,
    productIdCounter,
    orderIdCounter,
    userIdCounter
};

// Bad practice: exposing internal mutation functions
export function mutateGlobals() {
    return globals;
}