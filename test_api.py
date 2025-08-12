"""
Tourism API Test Suite
=====================

Comprehensive testing script for the Tourism Recommendation API
including unit tests, integration tests, and performance tests.
"""

import requests
import json
import time
import asyncio
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
API_BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test API health endpoint."""
    logger.info("Testing API health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Health check passed: {data}")
            return True
        else:
            logger.error(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Health check error: {e}")
        return False

def test_model_info():
    """Test model info endpoint."""
    logger.info("Testing model info...")
    try:
        response = requests.get(f"{API_BASE_URL}/model/info")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Model info retrieved: {data}")
            return True
        else:
            logger.error(f"❌ Model info failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Model info error: {e}")
        return False

def test_prediction_endpoint():
    """Test the prediction endpoint with sample data."""
    logger.info("Testing prediction endpoint...")
    
    # Sample prediction request
    sample_request = {
        "user": {
            "user_age": 28,
            "preferred_category": "museum",
            "preferred_city": "Jakarta",
            "budget_range": "medium"
        },
        "places": [
            {
                "place_id": "place_001",
                "place_category": "museum",
                "place_city": "Jakarta",
                "place_price": 25000,
                "place_average_rating": 4.2,
                "place_visit_duration_minutes": 120,
                "place_description": "Historical museum with ancient artifacts"
            },
            {
                "place_id": "place_002",
                "place_category": "park",
                "place_city": "Jakarta",
                "place_price": 10000,
                "place_average_rating": 3.8,
                "place_visit_duration_minutes": 90,
                "place_description": "Beautiful city park with lake views"
            },
            {
                "place_id": "place_003",
                "place_category": "restaurant",
                "place_city": "Jakarta",
                "place_price": 50000,
                "place_average_rating": 4.5,
                "place_visit_duration_minutes": 60,
                "place_description": "Traditional Indonesian cuisine restaurant"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=sample_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Prediction successful!")
            logger.info(f"Model used: {data['model_used']}")
            logger.info(f"Places evaluated: {data['total_places_evaluated']}")
            logger.info(f"Top recommendation: {data['top_recommendation']}")
            
            # Print all predictions
            for pred in data['predictions']:
                logger.info(f"  Place {pred['place_id']}: {pred['predicted_rating']:.2f} (rank {pred['recommendation_rank']})")
            
            return True
        else:
            logger.error(f"❌ Prediction failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        return False

def test_recommendation_endpoint():
    """Test the recommendation endpoint."""
    logger.info("Testing recommendation endpoint...")
    
    sample_request = {
        "user": {
            "user_age": 35,
            "preferred_category": "cultural",
            "preferred_city": "Yogyakarta",
            "budget_range": "high"
        },
        "places": [
            {
                "place_id": "yogya_001",
                "place_category": "temple",
                "place_city": "Yogyakarta",
                "place_price": 30000,
                "place_average_rating": 4.7,
                "place_visit_duration_minutes": 180,
                "place_description": "Ancient Buddhist temple complex"
            },
            {
                "place_id": "yogya_002",
                "place_category": "palace",
                "place_city": "Yogyakarta",
                "place_price": 15000,
                "place_average_rating": 4.3,
                "place_visit_duration_minutes": 150,
                "place_description": "Royal palace with traditional architecture"
            },
            {
                "place_id": "yogya_003",
                "place_category": "market",
                "place_city": "Yogyakarta",
                "place_price": 5000,
                "place_average_rating": 4.0,
                "place_visit_duration_minutes": 120,
                "place_description": "Traditional street market"
            },
            {
                "place_id": "yogya_004",
                "place_category": "museum",
                "place_city": "Yogyakarta",
                "place_price": 20000,
                "place_average_rating": 3.9,
                "place_visit_duration_minutes": 90,
                "place_description": "Cultural heritage museum"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/recommend?top_k=3",
            json=sample_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Recommendation successful!")
            logger.info(f"Top 3 recommendations for user (age {sample_request['user']['user_age']}):")
            
            for rec in data['top_recommendations']:
                logger.info(f"  #{rec['recommendation_rank']}: {rec['place_id']} - Rating: {rec['predicted_rating']:.2f}")
            
            logger.info(f"Recommendation summary: {data['recommendation_summary']}")
            return True
        else:
            logger.error(f"❌ Recommendation failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Recommendation error: {e}")
        return False

def test_input_validation():
    """Test API input validation."""
    logger.info("Testing input validation...")
    
    # Test invalid age
    invalid_request = {
        "user": {
            "user_age": 150,  # Invalid age
            "preferred_category": "museum"
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
            f"{API_BASE_URL}/predict",
            json=invalid_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 422:
            logger.info("✅ Input validation working correctly (rejected invalid age)")
            return True
        else:
            logger.error(f"❌ Input validation failed: expected 422, got {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Validation test error: {e}")
        return False

def performance_test(num_requests: int = 10):
    """Test API performance with multiple requests."""
    logger.info(f"Running performance test with {num_requests} requests...")
    
    sample_request = {
        "user": {
            "user_age": 30,
            "preferred_category": "recreation",
            "budget_range": "medium"
        },
        "places": [
            {
                "place_id": f"perf_test_{i}",
                "place_category": "recreation",
                "place_city": "Bali",
                "place_price": 35000,
                "place_average_rating": 4.1,
                "place_visit_duration_minutes": 120
            } for i in range(5)
        ]
    }
    
    start_time = time.time()
    successful_requests = 0
    
    for i in range(num_requests):
        try:
            response = requests.post(
                f"{API_BASE_URL}/predict",
                json=sample_request,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                successful_requests += 1
            
            if i % 5 == 0:
                logger.info(f"Completed {i + 1}/{num_requests} requests")
                
        except Exception as e:
            logger.error(f"Request {i + 1} failed: {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_response_time = total_time / num_requests
    
    logger.info(f"✅ Performance test completed:")
    logger.info(f"  Total requests: {num_requests}")
    logger.info(f"  Successful requests: {successful_requests}")
    logger.info(f"  Success rate: {(successful_requests/num_requests)*100:.1f}%")
    logger.info(f"  Total time: {total_time:.2f}s")
    logger.info(f"  Average response time: {avg_response_time:.3f}s")
    logger.info(f"  Requests per second: {num_requests/total_time:.2f}")

def run_comprehensive_test():
    """Run all tests in sequence."""
    logger.info("🚀 Starting comprehensive API test suite...")
    logger.info("=" * 60)
    
    tests = [
        ("Health Check", test_api_health),
        ("Model Info", test_model_info),
        ("Prediction Endpoint", test_prediction_endpoint),
        ("Recommendation Endpoint", test_recommendation_endpoint),
        ("Input Validation", test_input_validation)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Running: {test_name}")
        logger.info("-" * 40)
        
        try:
            if test_func():
                passed_tests += 1
                logger.info(f"✅ {test_name}: PASSED")
            else:
                logger.info(f"❌ {test_name}: FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {e}")
        
        time.sleep(1)  # Brief pause between tests
    
    # Run performance test
    logger.info(f"\n🔍 Running: Performance Test")
    logger.info("-" * 40)
    performance_test(10)
    
    # Final summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Tests passed: {passed_tests}/{total_tests}")
    logger.info(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        logger.info("🎉 All tests passed! API is ready for production.")
    else:
        logger.info(f"⚠️  {total_tests - passed_tests} test(s) failed. Please check the logs.")

if __name__ == "__main__":
    run_comprehensive_test()