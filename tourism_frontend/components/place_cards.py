"""
Place cards component for displaying tourism recommendations
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from utils.data_processing import format_currency, format_duration
from utils.maps import get_place_maps_data
from config import COLORS

def render_star_rating(rating: float) -> str:
    """Generate star rating HTML."""
    full_stars = int(rating)
    half_star = 1 if (rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "⭐" * full_stars
    if half_star:
        stars += "⭐"  # Using full star for simplicity
    stars += "☆" * empty_stars
    
    return f"{stars} ({rating:.1f})"

def render_confidence_bar(confidence: float) -> str:
    """Generate confidence score progress bar."""
    percentage = int(confidence * 100)
    color = COLORS["nature"] if confidence >= 0.8 else COLORS["accent"] if confidence >= 0.6 else COLORS["primary"]
    
    return f"""
    <div style="background-color: #e0e0e0; border-radius: 10px; overflow: hidden; margin: 5px 0;">
        <div style="width: {percentage}%; background-color: {color}; height: 8px; border-radius: 10px;"></div>
    </div>
    <small style="color: #666;">Confidence: {percentage}%</small>
    """

def render_place_card(place: Dict[str, Any], prediction: Dict[str, Any] = None) -> None:
    """Render a single place card using native Streamlit components."""
    
    # Extract data
    place_name = place['place_id'].replace('_', ' ').title()
    category = place['place_category']
    city = place['place_city']
    price = place['place_price']
    rating = place['place_average_rating']
    duration = place['place_visit_duration_minutes']
    description = place.get('place_description', 'No description available')
    
    # Prediction data if available
    predicted_rating = prediction.get('predicted_rating') if prediction else None
    confidence = prediction.get('confidence_score') if prediction else None
    rank = prediction.get('recommendation_rank') if prediction else None
    
    # Icon mapping for categories
    category_icons = {
        "Budaya": "🏛️",
        "Taman Hiburan": "🎢", 
        "Cagar Alam": "🌿",
        "Bahari": "🌊",
        "Pusat Perbelanjaan": "🛍️",
        "Tempat Ibadah": "🕌"
    }
    
    category_icon = category_icons.get(category, "📍")
    
    # Create card using native Streamlit container
    with st.container():
        # Add border using markdown
        st.markdown("---")
        
        # Rank badge if available
        if rank:
            st.markdown(f"**#{rank} Recommendation**")
        
        # Header with icon and title
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"## {category_icon}")
        with col2:
            st.markdown(f"### {place_name}")
            st.markdown(f"📍 {city} • 🎯 {category}")
        
        # Description
        st.write(description)
        
        # Price and Duration in columns
        price_col, duration_col = st.columns(2)
        with price_col:
            st.metric("Price", format_currency(price))
        with duration_col:
            st.metric("Duration", format_duration(duration))
        
        # Ratings
        st.write(f"**Original Rating:** {render_star_rating(rating)}")
        
        if predicted_rating:
            st.success(f"**AI Predicted Rating:** {render_star_rating(predicted_rating)}")
        
        if confidence:
            st.write(f"**Confidence Score:** {confidence:.1%}")
            st.progress(confidence, text=f"Confidence: {confidence:.1%}")
        
        # Google Maps integration
        maps_data = get_place_maps_data(place)
        
        # Maps links section
        st.write("")
        st.markdown("#### 🗺️ Location & Maps")
        
        maps_col1, maps_col2 = st.columns(2)
        
        with maps_col1:
            # View on Google Maps button
            if st.link_button(
                "📍 View on Google Maps", 
                maps_data['view_url'],
                help=f"Open {place_name} on Google Maps"
            ):
                pass
                
        with maps_col2:
            # Get Directions button
            if st.link_button(
                "🧭 Get Directions",
                maps_data['directions_url'], 
                help=f"Get directions to {place_name}"
            ):
                pass
        
        # Show coordinates if available
        if maps_data['coordinates']:
            lat, lng = maps_data['coordinates']
            st.caption(f"📍 Coordinates: {lat:.4f}, {lng:.4f}")
        
        st.markdown("---")

def render_places_grid(places: List[Dict[str, Any]], predictions: List[Dict[str, Any]] = None) -> None:
    """Render places in a grid layout."""
    
    if not places:
        st.info("No places to display. Try adjusting your filters.")
        return
    
    # Create prediction lookup if available
    prediction_lookup = {}
    if predictions:
        prediction_lookup = {pred['place_id']: pred for pred in predictions}
    
    # Display places in columns
    cols_per_row = 2
    for i in range(0, len(places), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j in range(cols_per_row):
            if i + j < len(places):
                place = places[i + j]
                prediction = prediction_lookup.get(place['place_id'])
                
                with cols[j]:
                    render_place_card(place, prediction)

def render_recommendations_summary(predictions: List[Dict[str, Any]]) -> None:
    """Render summary of recommendations."""
    
    if not predictions:
        return
    
    avg_predicted_rating = sum(p['predicted_rating'] for p in predictions) / len(predictions)
    avg_confidence = sum(p['confidence_score'] for p in predictions) / len(predictions)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Average Predicted Rating",
            f"{avg_predicted_rating:.1f}⭐",
            delta=None
        )
    
    with col2:
        st.metric(
            "Average Confidence",
            f"{avg_confidence:.1%}",
            delta=None
        )
    
    with col3:
        st.metric(
            "Total Recommendations",
            len(predictions),
            delta=None
        )

def render_comparison_table(places: List[Dict[str, Any]], predictions: List[Dict[str, Any]] = None) -> None:
    """Render places comparison table."""
    
    if not places:
        return
    
    # Create DataFrame
    df_data = []
    prediction_lookup = {}
    if predictions:
        prediction_lookup = {pred['place_id']: pred for pred in predictions}
    
    for place in places:
        prediction = prediction_lookup.get(place['place_id'])
        
        row = {
            'Place': place['place_id'].replace('_', ' ').title(),
            'Category': place['place_category'],
            'City': place['place_city'],
            'Price (IDR)': format_currency(place['place_price']),
            'Original Rating': place['place_average_rating'],
            'Duration': format_duration(place['place_visit_duration_minutes'])
        }
        
        if prediction:
            row['Predicted Rating'] = prediction['predicted_rating']
            row['Confidence'] = f"{prediction['confidence_score']:.1%}"
            row['Rank'] = prediction['recommendation_rank']
        
        df_data.append(row)
    
    df = pd.DataFrame(df_data)
    
    # Sort by rank if available
    if 'Rank' in df.columns:
        df = df.sort_values('Rank')
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Original Rating': st.column_config.NumberColumn(
                format="%.1f ⭐"
            ),
            'Predicted Rating': st.column_config.NumberColumn(
                format="%.1f ⭐"
            ) if 'Predicted Rating' in df.columns else None
        }
    )

def render_places_with_tabs(places: List[Dict[str, Any]], predictions: List[Dict[str, Any]] = None) -> None:
    """Render places with different view options in tabs."""
    
    tab1, tab2 = st.tabs(["🎴 Card View", "📊 Table View"])
    
    with tab1:
        if predictions:
            render_recommendations_summary(predictions)
            st.markdown("---")
        render_places_grid(places, predictions)
    
    with tab2:
        render_comparison_table(places, predictions)