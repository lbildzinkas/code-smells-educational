// Bad practice: test file with no proper test framework
import axios from 'axios';

const BASE_URL = 'http://localhost:3001';

// Bad practice: no proper test structure
async function runTests() {
    console.log('Starting bad API tests...\n');
    
    try {
        // Test 1: Login
        console.log('Test 1: Login as admin');
        const loginResponse = await axios.post(`${BASE_URL}/api/main/Login`, {
            email: 'admin@store.com',
            password: 'admin123'
        });
        console.log('Login successful:', loginResponse.data);
        
        // Test 2: Get Product
        console.log('\nTest 2: Get Product');
        const productResponse = await axios.get(`${BASE_URL}/api/main/GetProduct?id=1000`);
        console.log('Product:', productResponse.data);
        
        // Test 3: Add to Cart
        console.log('\nTest 3: Add to Cart');
        const cartResponse = await axios.post(`${BASE_URL}/api/main/AddToCart`, {
            id: 1000,
            name: 'Gaming Laptop',
            price: 1299.99,
            quantity: 1,
            category: 'electronics'
        });
        console.log('Cart response:', cartResponse.data);
        
        // Test 4: Get Cart
        console.log('\nTest 4: Get Cart');
        const getCartResponse = await axios.get(`${BASE_URL}/api/main/GetCart`);
        console.log('Cart contents:', getCartResponse.data);
        
        // Test 5: Create Order
        console.log('\nTest 5: Create Order');
        const orderResponse = await axios.post(`${BASE_URL}/api/main/CreateOrder`, {
            paymentMethod: 'credit_card'
        });
        console.log('Order created:', orderResponse.data);
        
        // Test 6: Get Stats (exposing internal state!)
        console.log('\nTest 6: Get Stats');
        const statsResponse = await axios.get(`${BASE_URL}/api/main/GetStats`);
        console.log('Internal stats:', statsResponse.data);
        
        // Test 7: Search Products
        console.log('\nTest 7: Search Products');
        const searchResponse = await axios.get(`${BASE_URL}/api/main/SearchProducts?query=laptop`);
        console.log('Search results:', searchResponse.data.length, 'products found');
        
        // Test 8: SQL Injection attempt (educational purpose only!)
        console.log('\nTest 8: SQL Injection vulnerability test');
        try {
            const sqlInjectionTest = await axios.get(`${BASE_URL}/api/main/GetProduct?id=1000 OR 1=1`);
            console.log('SQL Injection worked! This is bad!');
        } catch (err) {
            console.log('SQL Injection failed (which is actually good)');
        }
        
        console.log('\nAll tests completed!');
        
    } catch (error: any) {
        // Bad practice: generic error handling
        console.error('Test failed:', error.message);
    }
}

// Bad practice: running tests immediately
runTests();

// Bad practice: no test assertions
// Bad practice: no cleanup after tests
// Bad practice: no test isolation