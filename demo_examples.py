#!/usr/bin/env python3
"""
Tourism API Demo Examples
========================

Simple examples to demonstrate the Tourism Recommendation API
Perfect for sharing with friends and showcasing the capabilities!
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://YOUR-VM-IP:8000"  # Replace with your actual VM IP
TIMEOUT = 30

class TourismAPIDemo:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')
        
    def test_connection(self) -> bool:
        """Test if API is accessible"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API is online! Status: {data['status']}")
                print(f"   Model loaded: {data['model_name']}")
                return True
            else:
                print(f"❌ API returned status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to API: {e}")
            print(f"   Make sure API is running at: {self.base_url}")
            return False

    def demo_jakarta_recommendations(self):
        """Demo: Get recommendations for Jakarta places"""
        print("\n🏙️ JAKARTA TOURISM RECOMMENDATIONS")
        print("=" * 50)
        
        request_data = {
            "user": {
                "user_age": 28,
                "preferred_category": "cultural",
                "budget_range": "medium"
            },
            "places": [
                {
                    "place_id": "jakarta_national_museum",
                    "place_category": "museum",
                    "place_city": "Jakarta",
                    "place_price": 20000,
                    "place_average_rating": 4.1,
                    "place_visit_duration_minutes": 150,
                    "place_description": "National museum with Indonesian historical artifacts"
                },
                {
                    "place_id": "jakarta_old_town",
                    "place_category": "historical",
                    "place_city": "Jakarta", 
                    "place_price": 15000,
                    "place_average_rating": 4.3,
                    "place_visit_duration_minutes": 120,
                    "place_description": "Historic colonial area with Dutch architecture"
                },
                {
                    "place_id": "jakarta_grand_mosque",
                    "place_category": "religious",
                    "place_city": "Jakarta",
                    "place_price": 0,
                    "place_average_rating": 4.6,
                    "place_visit_duration_minutes": 90,
                    "place_description": "Beautiful Islamic mosque with modern architecture"
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/recommend?top_k=3",
                json=request_data,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"🎯 Top recommendations for {request_data['user']['user_age']}-year-old cultural enthusiast:")
                print()
                
                for rec in data['top_recommendations']:
                    rating = rec['predicted_rating']
                    confidence = rec['confidence_score']
                    rank = rec['recommendation_rank']
                    
                    # Get place details from original request
                    place_details = next((p for p in request_data['places'] if p['place_id'] == rec['place_id']), {})
                    place_name = place_details.get('place_description', rec['place_id'])
                    price = place_details.get('place_price', 0)
                    
                    print(f"   #{rank}. {place_name}")
                    print(f"       Predicted Rating: {rating:.2f}/5.0")
                    print(f"       Confidence: {confidence:.1%}")
                    print(f"       Price: Rp {price:,}")
                    print()
                
                avg_rating = data['recommendation_summary']['average_predicted_rating']
                print(f"📊 Average predicted rating: {avg_rating}/5.0")
                
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")

    def demo_yogyakarta_cultural_trip(self):
        """Demo: Cultural trip to Yogyakarta"""
        print("\n🏛️ YOGYAKARTA CULTURAL TRIP PLANNER")
        print("=" * 50)
        
        request_data = {
            "user": {
                "user_age": 35,
                "preferred_category": "cultural",
                "budget_range": "high"
            },
            "places": [
                {
                    "place_id": "borobudur_temple",
                    "place_category": "temple",
                    "place_city": "Yogyakarta",
                    "place_price": 30000,
                    "place_average_rating": 4.8,
                    "place_visit_duration_minutes": 240,
                    "place_description": "UNESCO World Heritage Buddhist temple complex"
                },
                {
                    "place_id": "sultan_palace",
                    "place_category": "palace", 
                    "place_city": "Yogyakarta",
                    "place_price": 15000,
                    "place_average_rating": 4.5,
                    "place_visit_duration_minutes": 150,
                    "place_description": "Traditional Javanese royal palace (Keraton)"
                },
                {
                    "place_id": "prambanan_temple",
                    "place_category": "temple",
                    "place_city": "Yogyakarta", 
                    "place_price": 25000,
                    "place_average_rating": 4.7,
                    "place_visit_duration_minutes": 180,
                    "place_description": "Hindu temple complex with intricate stone carvings"
                },
                {
                    "place_id": "malioboro_street",
                    "place_category": "shopping",
                    "place_city": "Yogyakarta",
                    "place_price": 10000,
                    "place_average_rating": 4.2,
                    "place_visit_duration_minutes": 120,
                    "place_description": "Famous pedestrian shopping street"
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json=request_data,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"🎯 Cultural trip predictions for {request_data['user']['user_age']}-year-old traveler:")
                print()
                
                # Sort by predicted rating
                predictions = sorted(data['predictions'], key=lambda x: x['predicted_rating'], reverse=True)
                
                total_cost = 0
                total_time = 0
                
                for pred in predictions:
                    rating = pred['predicted_rating']
                    confidence = pred['confidence_score']
                    
                    # Get place details
                    place_details = next((p for p in request_data['places'] if p['place_id'] == pred['place_id']), {})
                    place_name = place_details.get('place_description', pred['place_id'])
                    price = place_details.get('place_price', 0)
                    duration = place_details.get('place_visit_duration_minutes', 0)
                    
                    total_cost += price
                    total_time += duration
                    
                    # Rating visualization
                    stars = "⭐" * int(rating)
                    
                    print(f"   {stars} {place_name}")
                    print(f"      Predicted Rating: {rating:.2f}/5.0 ({confidence:.1%} confidence)")
                    print(f"      Cost: Rp {price:,} | Duration: {duration} minutes")
                    print()
                
                print("📋 TRIP SUMMARY")
                print(f"   Total estimated cost: Rp {total_cost:,}")
                print(f"   Total time needed: {total_time//60}h {total_time%60}m")
                print(f"   Places to visit: {len(predictions)}")
                
            else:
                print(f"❌ Request failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")

    def demo_budget_recommendations(self):
        """Demo: Budget-friendly recommendations"""
        print("\n💰 BUDGET-FRIENDLY RECOMMENDATIONS")
        print("=" * 50)
        
        request_data = {
            "user": {
                "user_age": 22,
                "preferred_category": "nature",
                "budget_range": "low"
            },
            "places": [
                {
                    "place_id": "taman_mini",
                    "place_category": "park",
                    "place_city": "Jakarta",
                    "place_price": 8000,
                    "place_average_rating": 4.0,
                    "place_visit_duration_minutes": 180,
                    "place_description": "Cultural park showcasing Indonesian diversity"
                },
                {
                    "place_id": "ancol_beach",
                    "place_category": "beach",
                    "place_city": "Jakarta",
                    "place_price": 12000,
                    "place_average_rating": 3.8,
                    "place_visit_duration_minutes": 240,
                    "place_description": "Beach recreation area with various activities"
                },
                {
                    "place_id": "ragunan_zoo",
                    "place_category": "zoo",
                    "place_city": "Jakarta", 
                    "place_price": 6000,
                    "place_average_rating": 4.1,
                    "place_visit_duration_minutes": 200,
                    "place_description": "Large zoo with diverse Indonesian wildlife"
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/recommend?top_k=3",
                json=request_data,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"🎯 Budget recommendations for student (age {request_data['user']['user_age']}):")
                print()
                
                total_budget = 0
                for rec in data['top_recommendations']:
                    rating = rec['predicted_rating']
                    rank = rec['recommendation_rank']
                    
                    place_details = next((p for p in request_data['places'] if p['place_id'] == rec['place_id']), {})
                    place_name = place_details.get('place_description', rec['place_id'])
                    price = place_details.get('place_price', 0)
                    
                    total_budget += price
                    
                    print(f"   #{rank}. {place_name}")
                    print(f"       Expected enjoyment: {rating:.2f}/5.0")
                    print(f"       Cost: Rp {price:,}")
                    print()
                
                print(f"💳 Total budget needed: Rp {total_budget:,}")
                print(f"💡 Perfect for students and budget-conscious travelers!")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")

    def demo_model_info(self):
        """Demo: Show model information"""
        print("\n🧠 AI MODEL INFORMATION")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.base_url}/model/info", timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                print(f"🤖 Model Name: {data['model_name']}")
                print(f"📊 Version: {data['model_version']}")
                print(f"🎯 Stage: {data['model_stage']}")
                print(f"🔢 Features: {data['feature_count']} engineered features")
                print(f"📅 Last Updated: {data['last_updated']}")
                print()
                print("📈 Performance Metrics:")
                for metric, value in data['model_metrics'].items():
                    print(f"   {metric.upper()}: {value:.3f}")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot retrieve model info: {e}")

def main():
    """Run all demo examples"""
    print("🎉 TOURISM RECOMMENDATION API - DEMO")
    print("=" * 60)
    print("This demo showcases the AI-powered tourism recommendation system!")
    print()
    
    # Initialize demo
    demo = TourismAPIDemo()
    
    # Test connection first
    if not demo.test_connection():
        print("\n❌ Cannot connect to API. Please check:")
        print("   1. API is running on your VM")
        print("   2. Replace 'YOUR-VM-IP' with actual IP address")
        print("   3. Port 8000 is accessible")
        return
    
    # Run demo examples
    demos = [
        ("Jakarta Cultural Tour", demo.demo_jakarta_recommendations),
        ("Yogyakarta Temple Tour", demo.demo_yogyakarta_cultural_trip), 
        ("Budget-Friendly Options", demo.demo_budget_recommendations),
        ("AI Model Details", demo.demo_model_info)
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
            time.sleep(2)  # Pause between demos
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Demo '{demo_name}' failed: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("🎯 DEMO COMPLETED!")
    print("=" * 60)
    print()
    print("💡 Want to try your own queries?")
    print(f"   Visit: {API_BASE_URL}/docs")
    print()
    print("🚀 Ready to build something amazing?")
    print("   Use these examples as a starting point!")

if __name__ == "__main__":
    main()