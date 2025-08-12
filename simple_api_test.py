#!/usr/bin/env python3
"""
Simple API Test Script
====================

Quick test to verify the API is working
"""

import requests
import json
import time

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
    except Exception as e:
        print(f"Health check failed: {e}")
    return False

def test_root():
    """Test the root endpoint"""
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        print(f"Root Endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
    except Exception as e:
        print(f"Root test failed: {e}")
    return False

def test_prediction():
    """Test prediction with simple data"""
    sample_request = {
        "user": {
            "user_age": 30
        },
        "places": [
            {
                "place_id": "test_001",
                "place_category": "museum",
                "place_city": "Jakarta",
                "place_price": 25000,
                "place_average_rating": 4.2,
                "place_visit_duration_minutes": 120
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=sample_request,
            timeout=30
        )
        print(f"Prediction Test: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Prediction: {data['predictions'][0]['predicted_rating']}")
            return True
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Prediction test failed: {e}")
    return False

if __name__ == "__main__":
    print("Testing Tourism Recommendation API...")
    print("====================================")
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("Prediction", test_prediction)
    ]
    
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        if test_func():
            print(f"✅ {name}: PASSED")
        else:
            print(f"❌ {name}: FAILED")
        time.sleep(1)