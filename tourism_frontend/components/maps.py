"""
Google Maps components for tourism recommendations
"""

import streamlit as st
from typing import List, Dict, Any
from utils.maps import get_place_maps_data
from config import ENABLE_GOOGLE_MAPS

def render_place_map_links(place: Dict[str, Any]) -> None:
    """
    Render Google Maps links for a single place (no embedded maps).
    
    Args:
        place: Place data dictionary
    """
    maps_data = get_place_maps_data(place)
    place_name = place['place_id'].replace('_', ' ').title()
    
    st.markdown(f"### 🗺️ Map: {place_name}")
    
    # Add location info
    col1, col2 = st.columns(2)
    with col1:
        if st.link_button("📍 Open in Google Maps", maps_data['view_url']):
            pass
    with col2:
        if st.link_button("🧭 Get Directions", maps_data['directions_url']):
            pass
    
    # Show coordinates if available
    if maps_data['coordinates']:
        lat, lng = maps_data['coordinates']
        st.caption(f"📍 Coordinates: {lat:.4f}, {lng:.4f}")

def render_places_map_grid(places: List[Dict[str, Any]], max_places: int = 6) -> None:
    """
    Render a grid of map links for multiple places.
    
    Args:
        places: List of place data dictionaries
        max_places: Maximum number of places to show maps for
    """
    st.markdown("### 🗺️ View Places on Maps")
    
    for i, place in enumerate(places[:max_places]):
        maps_data = get_place_maps_data(place)
        place_name = place['place_id'].replace('_', ' ').title()
        city = place['place_city']
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{place_name}** - {city}")
            if maps_data['coordinates']:
                lat, lng = maps_data['coordinates']
                st.caption(f"📍 {lat:.4f}, {lng:.4f}")
        with col2:
            if st.link_button("📍 View", maps_data['view_url'], key=f"view_{i}"):
                pass
        with col3:
            if st.link_button("🧭 Directions", maps_data['directions_url'], key=f"dir_{i}"):
                pass

def render_interactive_map_selector(places: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Render an interactive map selector interface.
    
    Args:
        places: List of place data dictionaries
        
    Returns:
        Selected place data or None
    """
    st.markdown("### 🗺️ Explore Places on Map")
    
    # Place selector
    place_names = [p['place_id'].replace('_', ' ').title() for p in places]
    selected_index = st.selectbox(
        "Choose a place to view on map:",
        range(len(places)),
        format_func=lambda i: f"{place_names[i]} ({places[i]['place_city']})"
    )
    
    selected_place = places[selected_index]
    
    # Show map links for selected place
    render_place_map_links(selected_place)
    
    return selected_place

def render_map_summary_stats(places: List[Dict[str, Any]]) -> None:
    """
    Render summary statistics about places with map data.
    
    Args:
        places: List of place data dictionaries
    """
    from utils.maps import get_place_coordinates
    
    # Count places with coordinates
    places_with_coords = sum(1 for place in places if get_place_coordinates(place['place_id']))
    
    # Count cities
    cities = set(place['place_city'] for place in places)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Places with Maps", places_with_coords)
    
    with col2:
        st.metric("Cities Covered", len(cities))
        
    with col3:
        st.metric("Google Maps", "✅ Enabled")