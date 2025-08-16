"""
ClickHouse data loader for tourism frontend
"""

import clickhouse_connect
import streamlit as st
from typing import List, Dict, Any, Optional
from config import (
    CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, 
    CLICKHOUSE_PASSWORD, CLICKHOUSE_DATABASE, CLICKHOUSE_TABLE
)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_places_from_clickhouse() -> List[Dict[str, Any]]:
    """Load tourism places data from ClickHouse."""
    try:
        # Connect to ClickHouse
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE
        )
        
        # Query to get unique places with aggregated data
        query = f"""
        SELECT 
            place_id,
            place_name,
            place_description,
            place_category,
            place_city,
            place_price,
            place_average_rating,
            place_visit_duration_minutes,
            place_latitude,
            place_longitude,
            COUNT(*) as rating_count,
            AVG(user_rating) as avg_user_rating
        FROM {CLICKHOUSE_TABLE}
        GROUP BY 
            place_id, place_name, place_description, place_category,
            place_city, place_price, place_average_rating, 
            place_visit_duration_minutes, place_latitude, place_longitude
        ORDER BY rating_count DESC, place_average_rating DESC
        """
        
        result = client.query(query)
        
        # Convert to the same format as sample_places.json
        places = []
        for row in result.result_rows:
            place = {
                "place_id": f"place_{row[0]}",  # Convert to string format like sample data
                "place_name": row[1],
                "place_description": row[2],
                "place_category": row[3],
                "place_city": row[4],
                "place_price": float(row[5]),
                "place_average_rating": float(row[6]),
                "place_visit_duration_minutes": int(row[7]),
                "place_latitude": float(row[8]) if row[8] is not None else 0.0,
                "place_longitude": float(row[9]) if row[9] is not None else 0.0,
                "rating_count": int(row[10]),
                "avg_user_rating": float(row[11]) if row[11] is not None else 0.0
            }
            places.append(place)
        
        st.success("✅ Sistem rekomendasi siap digunakan")
        return places
        
    except Exception as e:
        st.warning(f"⚠️ ClickHouse connection failed: {str(e)}")
        st.info("🔄 Falling back to sample data...")
        raise e

@st.cache_data(ttl=300)
def get_clickhouse_stats() -> Dict[str, Any]:
    """Get database statistics from ClickHouse."""
    try:
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE
        )
        
        stats_query = f"""
        SELECT 
            COUNT(DISTINCT place_id) as total_places,
            COUNT(DISTINCT place_category) as total_categories,
            COUNT(DISTINCT place_city) as total_cities,
            COUNT(*) as total_ratings,
            AVG(place_average_rating) as avg_rating,
            MAX(loaded_at) as last_updated
        FROM {CLICKHOUSE_TABLE}
        """
        
        result = client.query(stats_query)
        row = result.result_rows[0]
        
        return {
            "total_places": int(row[0]),
            "total_categories": int(row[1]),
            "total_cities": int(row[2]),
            "total_ratings": int(row[3]),
            "avg_rating": float(row[4]),
            "last_updated": row[5],
            "data_source": "ClickHouse Database"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "data_source": "ClickHouse (Failed)"
        }

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_cities_from_clickhouse() -> List[str]:
    """Get unique cities from ClickHouse database."""
    try:
        # Connect to ClickHouse
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE
        )
        
        # Query to get unique cities
        query = f"""
        SELECT DISTINCT place_city
        FROM {CLICKHOUSE_TABLE}
        WHERE place_city IS NOT NULL AND place_city != ''
        ORDER BY place_city
        """
        
        result = client.query(query)
        cities = [row[0] for row in result.result_rows if row[0]]
        
        return cities
        
    except Exception as e:
        st.warning(f"⚠️ Failed to load cities from ClickHouse: {str(e)}")
        # Fallback to hardcoded cities from config
        from config import INDONESIAN_CITIES
        return INDONESIAN_CITIES

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_categories_from_clickhouse() -> List[str]:
    """Get unique categories from ClickHouse database."""
    try:
        # Connect to ClickHouse
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE
        )
        
        # Query to get unique categories
        query = f"""
        SELECT DISTINCT place_category
        FROM {CLICKHOUSE_TABLE}
        WHERE place_category IS NOT NULL AND place_category != ''
        ORDER BY place_category
        """
        
        result = client.query(query)
        categories = [row[0] for row in result.result_rows if row[0]]
        
        return categories
        
    except Exception as e:
        st.warning(f"⚠️ Failed to load categories from ClickHouse: {str(e)}")
        # Fallback to hardcoded categories from config
        from config import TOURISM_CATEGORIES
        return TOURISM_CATEGORIES

def test_clickhouse_connection() -> Dict[str, Any]:
    """Test ClickHouse connection and return status."""
    try:
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE
        )
        
        # Simple test query
        result = client.query("SELECT 1")
        
        return {
            "status": "connected",
            "host": CLICKHOUSE_HOST,
            "port": CLICKHOUSE_PORT,
            "database": CLICKHOUSE_DATABASE,
            "table": CLICKHOUSE_TABLE,
            "message": "✅ ClickHouse connection successful"
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "host": CLICKHOUSE_HOST,
            "port": CLICKHOUSE_PORT,
            "database": CLICKHOUSE_DATABASE,
            "table": CLICKHOUSE_TABLE,
            "error": str(e),
            "message": f"❌ ClickHouse connection failed: {str(e)}"
        }