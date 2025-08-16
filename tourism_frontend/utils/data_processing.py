"""
Data processing utilities for tourism frontend
"""

import json
import pandas as pd
import streamlit as st
from typing import List, Dict, Any
import os
from config import SAMPLE_DATA_PATH, TOURISM_CATEGORIES, INDONESIAN_CITIES

@st.cache_data
def load_sample_places_fallback() -> List[Dict[str, Any]]:
    """Load sample tourism places data as fallback."""
    try:
        # Get the absolute path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(os.path.dirname(current_dir), SAMPLE_DATA_PATH)
        
        with open(data_path, 'r', encoding='utf-8') as f:
            places = json.load(f)
        st.info("📁 Using sample data (ClickHouse unavailable)")
        return places
    except Exception as e:
        st.error(f"Failed to load sample data: {e}")
        return []

@st.cache_data
def load_sample_places() -> List[Dict[str, Any]]:
    """Load tourism places data from ClickHouse with fallback to sample data."""
    try:
        # Try to load from ClickHouse first
        from utils.clickhouse_loader import load_places_from_clickhouse
        return load_places_from_clickhouse()
    except Exception as e:
        # Fallback to sample data
        st.warning("🔄 ClickHouse unavailable, using sample data as fallback")
        return load_sample_places_fallback()

@st.cache_data
def get_places_dataframe() -> pd.DataFrame:
    """Get places data as pandas DataFrame."""
    places = load_sample_places()
    if not places:
        return pd.DataFrame()
    
    df = pd.DataFrame(places)
    return df

def filter_places(places: List[Dict[str, Any]], 
                 category: str = None, 
                 city: str = None, 
                 max_price: float = None,
                 min_rating: float = None) -> List[Dict[str, Any]]:
    """Filter places based on criteria."""
    filtered = places.copy()
    
    if category and category != "All":
        filtered = [p for p in filtered if p['place_category'] == category]
    
    if city and city != "All":
        filtered = [p for p in filtered if p['place_city'] == city]
    
    if max_price is not None:
        filtered = [p for p in filtered if p['place_price'] <= max_price]
    
    if min_rating is not None:
        filtered = [p for p in filtered if p['place_average_rating'] >= min_rating]
    
    return filtered

def format_currency(amount: float) -> str:
    """Format Indonesian Rupiah currency."""
    if amount == 0:
        return "Free"
    elif amount < 1000:
        return f"Rp {amount:,.0f}"
    elif amount < 1000000:
        return f"Rp {amount/1000:,.0f}K"
    else:
        return f"Rp {amount/1000000:,.1f}M"

def format_duration(minutes: int) -> str:
    """Format visit duration."""
    if minutes < 60:
        return f"{minutes} minutes"
    elif minutes < 1440:  # Less than 24 hours
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            return f"{hours}h {remaining_minutes}m"
    else:
        days = minutes // 1440
        return f"{days} day{'s' if days > 1 else ''}"

def get_price_range_label(price: float) -> str:
    """Get price range label for a place."""
    if price == 0:
        return "Free"
    elif price <= 50000:
        return "Low"
    elif price <= 200000:
        return "Medium"
    else:
        return "High"

def calculate_statistics(places: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate statistics from places data."""
    if not places:
        return {}
    
    # Try to get enhanced stats from ClickHouse first
    try:
        from utils.clickhouse_loader import get_clickhouse_stats
        clickhouse_stats = get_clickhouse_stats()
        if 'error' not in clickhouse_stats:
            # Use ClickHouse stats if available
            df = pd.DataFrame(places)
            enhanced_stats = clickhouse_stats.copy()
            enhanced_stats.update({
                'categories': df['place_category'].value_counts().to_dict(),
                'cities': df['place_city'].value_counts().to_dict(),
                'price_ranges': df['place_price'].apply(get_price_range_label).value_counts().to_dict(),
                'avg_price': df['place_price'].mean(),
                'avg_duration': df['place_visit_duration_minutes'].mean()
            })
            return enhanced_stats
    except Exception:
        pass  # Fall back to basic calculation
    
    # Fallback to basic calculation from loaded places
    df = pd.DataFrame(places)
    
    stats = {
        'total_places': len(places),
        'avg_rating': df['place_average_rating'].mean(),
        'avg_price': df['place_price'].mean(),
        'avg_duration': df['place_visit_duration_minutes'].mean(),
        'categories': df['place_category'].value_counts().to_dict(),
        'cities': df['place_city'].value_counts().to_dict(),
        'price_ranges': df['place_price'].apply(get_price_range_label).value_counts().to_dict(),
        'data_source': 'Sample Data'
    }
    
    return stats

def validate_user_preferences(user_prefs: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean user preferences."""
    validated = user_prefs.copy()
    
    # Validate age
    if 'user_age' in validated:
        validated['user_age'] = max(18, min(100, int(validated['user_age'])))
    
    # Validate category
    if 'preferred_category' in validated:
        if validated['preferred_category'] not in TOURISM_CATEGORIES + ["All", None]:
            validated['preferred_category'] = None
    
    # Validate city
    if 'preferred_city' in validated:
        if validated['preferred_city'] not in INDONESIAN_CITIES + ["All", None]:
            validated['preferred_city'] = None
    
    # Validate budget range
    if 'budget_range' in validated:
        if validated['budget_range'] not in ["Low", "Medium", "High", None]:
            validated['budget_range'] = None
    
    return validated

def prepare_api_payload(user_prefs: Dict[str, Any], places: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Prepare payload for API request."""
    # Clean user preferences
    cleaned_prefs = validate_user_preferences(user_prefs)
    
    # Prepare user preferences without user_id (not needed for recommendations)
    api_prefs = {
        'user_age': cleaned_prefs.get('user_age', 25),
        'preferred_category': cleaned_prefs.get('preferred_category'),
        'preferred_city': cleaned_prefs.get('preferred_city'),
        'budget_range': cleaned_prefs.get('budget_range')
    }
    
    # Clean places data - ensure all required fields and convert place_id to numeric
    api_places = []
    for i, place in enumerate(places):
        # Convert string place_id to numeric by hashing or using index
        place_id = place.get('place_id')
        if isinstance(place_id, str):
            # Create a numeric ID from string by using a simple hash or index
            numeric_place_id = abs(hash(place_id)) % 1000000  # Keep it reasonable
        else:
            numeric_place_id = int(place_id) if place_id is not None else i + 1
            
        api_place = {
            'place_id': numeric_place_id,
            'place_category': place['place_category'],
            'place_city': place['place_city'],
            'place_price': float(place['place_price']),
            'place_average_rating': float(place['place_average_rating']),
            'place_visit_duration_minutes': int(place['place_visit_duration_minutes']),
            'place_description': place.get('place_description', ''),
            # Store original place_id for reference
            'original_place_id': place.get('place_id')
        }
        api_places.append(api_place)
    
    return {
        'user': api_prefs,
        'places': api_places
    }