#!/usr/bin/env python3
"""
Full Integration Test for Tourism Recommendation System
Tests both API and Frontend components
"""

import requests
import json
import sys
import time

def test_api_health():
    """Test API health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        data = response.json()
        print(f"✅ API Health: {data['status']}")
        print(f"✅ Model: {data['model_name']}")
        return True
    except Exception as e:
        print(f"❌ API Health Check Failed: {e}")
        return False

def test_api_model_info():
    """Test API model info endpoint"""
    try:
        response = requests.get("http://localhost:8000/model/info", timeout=5)
        data = response.json()
        print(f"✅ Model Info: {data['model_name']} v{data['model_version']}")
        print(f"✅ Features: {data['feature_count']}")
        return True
    except Exception as e:
        print(f"❌ Model Info Failed: {e}")
        return False

def test_api_recommendations():
    """Test API recommendations endpoint"""
    try:
        # Sample request payload
        payload = {
            "user": {
                "user_age": 30,
                "preferred_category": "Budaya",
                "preferred_city": "Yogyakarta",
                "budget_range": "Medium"
            },
            "places": [
                {
                    "place_id": "borobudur_001",
                    "place_category": "Budaya",
                    "place_city": "Yogyakarta",
                    "place_price": 50000,
                    "place_average_rating": 4.8,
                    "place_visit_duration_minutes": 180,
                    "place_description": "Ancient Buddhist temple"
                },
                {
                    "place_id": "prambanan_013",
                    "place_category": "Budaya", 
                    "place_city": "Yogyakarta",
                    "place_price": 50000,
                    "place_average_rating": 4.6,
                    "place_visit_duration_minutes": 150,
                    "place_description": "Hindu temple complex"
                }
            ]
        }
        
        response = requests.post(
            "http://localhost:8000/recommend?top_k=2",
            json=payload,
            timeout=10
        )
        data = response.json()
        
        print(f"✅ Recommendations: {len(data['top_recommendations'])}")
        top_rec = data['top_recommendations'][0]
        print(f"✅ Top: {top_rec['place_id']} (Rating: {top_rec['predicted_rating']:.2f}, Confidence: {top_rec['confidence_score']:.1%})")
        
        return True
    except Exception as e:
        print(f"❌ Recommendations Failed: {e}")
        return False

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200 and "Streamlit" in response.text:
            print("✅ Frontend: Accessible")
            return True
        else:
            print("❌ Frontend: Not accessible")
            return False
    except Exception as e:
        print(f"❌ Frontend Accessibility Failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🧪 Tourism Recommendation System - Integration Test")
    print("=" * 60)
    
    tests = [
        ("API Health Check", test_api_health),
        ("API Model Info", test_api_model_info), 
        ("API Recommendations", test_api_recommendations),
        ("Frontend Accessibility", test_frontend_accessibility)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        print("-" * 40)
        if test_func():
            passed += 1
        else:
            print("⚠️ Test failed")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is fully operational.")
        print("\n🌐 Access URLs:")
        print("   • API Documentation: http://localhost:8000/docs")
        print("   • Frontend Application: http://localhost:8501")
        print("   • API Health: http://localhost:8000/health")
        return True
    else:
        print("❌ Some tests failed. Please check the system.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)