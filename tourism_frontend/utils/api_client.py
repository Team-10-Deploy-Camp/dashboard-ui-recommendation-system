"""
Tourism API Client for Streamlit Frontend
"""

import asyncio
import aiohttp
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import streamlit as st
from config import API_BASE_URL, API_TIMEOUT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TourismAPIClient:
    """Client for interacting with the Tourism Recommendation API."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.timeout = API_TIMEOUT
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make a synchronous HTTP request."""
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault('timeout', self.timeout)
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def get_health(self) -> Dict[str, Any]:
        """Check API health status."""
        try:
            response = self._make_request('GET', '/health')
            return response.json()
        except Exception as e:
            return {
                "status": "unhealthy",
                "model_loaded": False,
                "model_name": "unknown",
                "api_version": "unknown",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        try:
            response = self._make_request('GET', '/model/info')
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            return {
                "model_name": "unknown",
                "model_version": "unknown", 
                "model_stage": "unknown",
                "model_metrics": {},
                "feature_count": 0,
                "last_updated": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def predict_ratings(self, user_prefs: Dict[str, Any], places: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get rating predictions for places."""
        try:
            payload = {
                "user": user_prefs,
                "places": places
            }
            
            response = self._make_request('POST', '/predict', json=payload)
            return response.json()
        except Exception as e:
            logger.error(f"Prediction request failed: {e}")
            raise
    
    def get_recommendations(self, user_prefs: Dict[str, Any], places: List[Dict[str, Any]], top_k: int = 5) -> Dict[str, Any]:
        """Get top-K recommendations for a user."""
        try:
            # Format user preferences according to API spec
            user_data = {
                "user_age": user_prefs.get('user_age', 25)
            }
            
            # Add optional user preferences if available
            if 'preferred_category' in user_prefs and user_prefs['preferred_category']:
                user_data["preferred_category"] = user_prefs['preferred_category']
            if 'preferred_city' in user_prefs and user_prefs['preferred_city']:
                user_data["preferred_city"] = user_prefs['preferred_city']
            if 'budget_range' in user_prefs and user_prefs['budget_range']:
                user_data["budget_range"] = user_prefs['budget_range']
            
            # Format places according to API spec
            places_data = []
            for place in places:
                place_data = {
                    "place_id": str(place.get('place_id', 0)),  # API expects string
                    "place_category": place.get('place_category', 'Unknown'),
                    "place_city": place.get('place_city', 'Unknown'),
                    "place_price": float(place.get('place_price') or 0),
                    "place_average_rating": float(place.get('place_average_rating') or 0),
                    "place_visit_duration_minutes": max(30, int(place.get('place_visit_duration_minutes') or 30))  # API requires >= 30
                }
                places_data.append(place_data)
            
            # Create the request payload in the correct format
            payload = {
                "user": user_data,
                "places": places_data
            }
            
            # Add top_k as query parameter
            params = {"top_k": top_k} if top_k != 5 else {}
            
            # Use recommendation endpoint
            response = self._make_request('POST', '/recommend', json=payload, params=params)
            result = response.json()
            
            # The API already returns top recommendations sorted by rating
            # Return in the expected format for the frontend
            return {
                "top_recommendations": result.get("top_recommendations", [])
            }
        except Exception as e:
            logger.error(f"Recommendation request failed: {e}")
            raise
    
    def reload_model(self) -> Dict[str, Any]:
        """Trigger model reload."""
        try:
            response = self._make_request('POST', '/model/reload')
            return response.json()
        except Exception as e:
            logger.error(f"Model reload failed: {e}")
            return {"message": "Model reload failed", "status": "error", "error": str(e)}

# Cached API client instance
@st.cache_resource
def get_api_client() -> TourismAPIClient:
    """Get cached API client instance."""
    return TourismAPIClient()

# Helper functions with caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def cached_get_health() -> Dict[str, Any]:
    """Get cached health status."""
    client = get_api_client()
    return client.get_health()

@st.cache_data(ttl=3600)  # Cache for 1 hour  
def cached_get_model_info() -> Dict[str, Any]:
    """Get cached model information."""
    client = get_api_client()
    return client.get_model_info()

def get_recommendations_with_progress(user_prefs: Dict[str, Any], places: List[Dict[str, Any]], top_k: int = 5) -> Dict[str, Any]:
    """Get recommendations with progress indicator and enhanced error handling."""
    client = get_api_client()
    
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Validate inputs
        status_text.text("🔍 Validating inputs...")
        progress_bar.progress(20)
        
        if not user_prefs:
            raise ValueError("User preferences are required")
        if not places:
            raise ValueError("Places data is required")
        if top_k < 1 or top_k > 20:
            raise ValueError("top_k must be between 1 and 20")
        
        # Step 2: Prepare API request
        status_text.text("📦 Preparing API request...")
        progress_bar.progress(40)
        
        # Step 3: Send API request
        status_text.text("🚀 Sending request to AI model...")
        progress_bar.progress(60)
        
        result = client.get_recommendations(user_prefs, places, top_k)
        
        # Step 4: Process results
        status_text.text("🔄 Processing recommendations...")
        progress_bar.progress(80)
        
        if not result or 'top_recommendations' not in result:
            raise ValueError("Invalid response from recommendation API")
        
        # Step 5: Complete
        status_text.text("✅ Recommendations ready!")
        progress_bar.progress(100)
        
        # Clean up progress indicators
        import time
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        st.success(f"✅ Generated {len(result.get('top_recommendations', []))} recommendations successfully!")
        return result
        
    except requests.exceptions.ConnectionError:
        progress_bar.empty()
        status_text.empty()
        st.error("❌ **Connection Error**: Cannot connect to the recommendation API. The service may be offline.")
        st.info("💡 **Tip**: Check if the API server is running at the configured URL.")
        raise
        
    except requests.exceptions.Timeout:
        progress_bar.empty()
        status_text.empty()
        st.error("⏱️ **Timeout Error**: The API request took too long to complete.")
        st.info("💡 **Tip**: Try reducing the number of places or check your internet connection.")
        raise
        
    except requests.exceptions.HTTPError as e:
        progress_bar.empty()
        status_text.empty()
        if e.response.status_code == 503:
            st.error("🤖 **Service Unavailable**: The AI model is not loaded or unavailable.")
            st.info("💡 **Tip**: Wait a few moments and try again, or contact the system administrator.")
        elif e.response.status_code == 422:
            try:
                error_detail = e.response.json()
                if "Failed to enforce schema" in str(error_detail):
                    st.error("🤖 **Model Processing Error**: The ML model is having issues with data processing.")
                    st.info("💡 **Status**: The API is receiving data correctly, but the model has an internal tensor processing issue.")
                    st.info("🔧 **For developers**: Model expects tensor input but received list format - this is an API-side issue.")
                else:
                    st.error("📝 **Validation Error**: The input data format is incorrect.")
                    st.info("💡 **Tip**: Check your preferences and try again.")
            except:
                st.error("📝 **Validation Error**: The input data format is incorrect.")
                st.info("💡 **Tip**: Check your preferences and try again.")
        else:
            st.error(f"🌐 **HTTP Error**: Server returned status code {e.response.status_code}")
        raise
        
    except ValueError as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"⚠️ **Input Error**: {str(e)}")
        st.info("💡 **Tip**: Please check your input values and try again.")
        raise
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ **Unexpected Error**: {str(e)}")
        st.info("💡 **Tip**: Please try again or contact support if the problem persists.")
        raise