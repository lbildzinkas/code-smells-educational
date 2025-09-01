#!/usr/bin/env python3
"""
Test script for the Bad Code Online Store Python API

This script demonstrates the same terrible practices as the API itself!
"""

import requests
import json
import sys

# Bad practice: hardcoded API URL
API_URL = "http://localhost:8000"

# Bad practice: no error handling classes
def test_api():
    print("🐍 Testing Online Store Bad Code Python API...")
    print("")
    
    # Bad practice: no validation of API availability
    try:
        response = requests.get(f"{API_URL}/api/main/GetStats")
    except:
        print("❌ API is not running on", API_URL)
        print("Start it with: python main.py")
        sys.exit(1)
        
    print("✅ Python API is running")
    print("")
    
    # Test 1: Get Stats (Working - exposes internal state)
    print("📊 Testing Stats (exposes internal state - bad practice!)...")
    try:
        response = requests.get(f"{API_URL}/api/main/GetStats")
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)
    print("")
    
    # Test 2: Add to Cart (Working)
    print("🛒 Testing Add to Cart...")
    try:
        cart_data = {
            "id": 1000,
            "name": "Gaming Laptop", 
            "price": 1299.99,
            "quantity": 1,
            "category": "electronics"
        }
        response = requests.post(f"{API_URL}/api/main/AddToCart", json=cart_data)
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)
    print("")
    
    # Test 3: Get Cart (Working)
    print("🛍️ Testing Get Cart...")
    try:
        response = requests.get(f"{API_URL}/api/main/GetCart")
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)
    print("")
    
    # Test 4: Login (Working in Python version!)
    print("🔐 Testing Login...")
    try:
        login_data = {
            "email": "admin@store.com",
            "password": "admin123"
        }
        response = requests.post(f"{API_URL}/api/main/Login", json=login_data)
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)
    print("")
    
    # Test 5: Payment Processing (Working with bad practices!)
    print("💳 Testing Payment Processing...")
    try:
        payment_data = {
            "method": "credit_card",
            "amount": 1299.99,
            "cardNumber": "1234567890123456",
            "cvv": "123", 
            "expiry": "12/25"
        }
        response = requests.post(f"{API_URL}/api/main/ProcessPayment", json=payment_data)
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)
    print("")
    
    # Test 6: Get Product from Database (May fail due to ODBC setup)
    print("📦 Testing Product Retrieval from Database...")
    try:
        response = requests.get(f"{API_URL}/api/main/GetProduct?id=1000")
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Database Error (expected on some systems):", response.json())
    except Exception as e:
        print("Error:", e)
    print("")
    
    # Test 7: Calculate Utility (Working)
    print("🧮 Testing Calculate Utility...")
    try:
        calc_data = {
            "subtotal": 100.00,
            "type": "tax"
        }
        response = requests.post(f"{API_URL}/api/main/Calculate", json=calc_data)
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)
    print("")
    
    # Test 8: Logout (Working)
    print("🚪 Testing Logout...")
    try:
        response = requests.post(f"{API_URL}/api/main/Logout")
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)
    print("")
    
    print("✅ Python API Testing Complete!")
    print("")
    print("🎯 Summary:")
    print("   - Cart operations work (global state)")
    print("   - Login works (hardcoded credentials)")
    print("   - Payment processing works (fake implementation)")
    print("   - Stats endpoint exposes internal state") 
    print("   - Calculation utilities work")
    print("   - Database operations may fail (ODBC setup dependent)")
    print("")
    print("Perfect for demonstrating Python code smells and refactoring opportunities!")
    print("Compare with C# version - some things work better, some worse!")

# Bad practice: no if __name__ == "__main__" guard
test_api()