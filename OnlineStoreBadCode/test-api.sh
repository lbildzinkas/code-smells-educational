#!/bin/bash

# Test script for the Bad Code Online Store API

echo "🧪 Testing Online Store Bad Code API..."
echo ""

API_URL="http://localhost:5000"

# Check if API is running
if ! curl -s "$API_URL/api/main/GetStats" > /dev/null 2>&1; then
    echo "❌ API is not running on $API_URL"
    echo "Start it with: dotnet run --urls=http://localhost:5000"
    exit 1
fi

echo "✅ API is running"
echo ""

# Test 1: Get Product (Working)
echo "📦 Testing Product Retrieval..."
PRODUCT_RESPONSE=$(curl -s "$API_URL/api/main/GetProduct?id=1000")
echo "Response: $PRODUCT_RESPONSE"
echo ""

# Test 2: Search Products (Working)  
echo "🔍 Testing Product Search..."
SEARCH_RESPONSE=$(curl -s "$API_URL/api/main/SearchProducts?query=laptop&sortBy=Price&filterBy=expensive")
echo "Response: $SEARCH_RESPONSE"
echo ""

# Test 3: Add to Cart (Working)
echo "🛒 Testing Add to Cart..."
CART_RESPONSE=$(curl -s -X POST "$API_URL/api/main/AddToCart" \
  -H "Content-Type: application/json" \
  -d '{"id": 1000, "name": "Gaming Laptop", "price": 1299.99, "quantity": 1, "category": "electronics"}')
echo "Response: $CART_RESPONSE"
echo ""

# Test 4: Get Cart (Working)
echo "🛍️ Testing Get Cart..."
GET_CART_RESPONSE=$(curl -s "$API_URL/api/main/GetCart")
echo "Response: $GET_CART_RESPONSE"
echo ""

# Test 5: Get Order from Database (Working)
echo "📋 Testing Get Order from Database..."
ORDER_RESPONSE=$(curl -s "$API_URL/api/main/GetOrder?id=5000")
echo "Response: $ORDER_RESPONSE"
echo ""

# Test 6: Login (Shows Error - Bad Code!)
echo "🔐 Testing Login (This will show an error - that's intentional bad code!)..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/api/main/Login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@store.com", "password": "admin123"}' 2>&1)
echo "Response: $LOGIN_RESPONSE" | head -5
echo "... (truncated error output)"
echo ""

# Test 7: Stats Endpoint (Exposes Internal State - Bad!)
echo "📊 Testing Stats (Exposes internal state - bad practice!)..."
STATS_RESPONSE=$(curl -s "$API_URL/api/main/GetStats")
echo "Response: $STATS_RESPONSE"
echo ""

echo "✅ API Testing Complete!"
echo ""
echo "🎯 Summary:"
echo "   - Product operations work (with database)"
echo "   - Cart operations work (global state)" 
echo "   - Order retrieval works (database)"
echo "   - Login fails (bad dynamic type handling)"
echo "   - Stats endpoint exposes internal state"
echo ""
echo "Perfect for demonstrating code smells and refactoring opportunities!"