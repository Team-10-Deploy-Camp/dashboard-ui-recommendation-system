"""
Tourism Indonesia - AI Recommendations
Main Streamlit Application
"""

import streamlit as st
import sys
import os

# Add current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from config import APP_TITLE, PAGE_ICON, LAYOUT, COLORS
from components.sidebar import render_sidebar
from components.place_cards import render_places_with_tabs
# Removed analytics dashboard import
from components.maps import render_interactive_map_selector, render_map_summary_stats
from utils.data_processing import (
    load_sample_places, filter_places, calculate_statistics, 
    prepare_api_payload
)
from utils.api_client import (
    get_api_client, cached_get_health,
    get_recommendations_with_progress
)

# CSS loading removed - using native Streamlit components only

# Configure Streamlit page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

def render_home_page():
    """Render the home page."""
    
    # Hero section using native Streamlit
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🏝️ Tourism Indonesia")
        st.markdown("### *AI-Powered Recommendations*")
        st.write("")
        st.markdown("""
        Discover amazing places across Indonesia tailored to your preferences using advanced machine learning. 
        From ancient temples to pristine beaches, find your perfect Indonesian adventure.
        """)
        st.write("")
    
    # Features using columns
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("### 🤖 AI Powered")
        st.write("Smart Recommendations")
        
    with feature_col2:
        st.markdown("### 🎯 Personalized") 
        st.write("Based on Your Preferences")
        
    with feature_col3:
        st.markdown("### 🏛️ 50+ Places")
        st.write("Across Indonesia")
    
    st.write("")
    st.write("")
    
    # Features section with native Streamlit
    detail_col1, detail_col2, detail_col3 = st.columns(3)
    
    with detail_col1:
        st.markdown("#### 🎯 Personalized Experience")
        st.write("Get recommendations tailored to your age, interests, budget, and travel preferences using advanced AI algorithms.")
    
    with detail_col2:
        st.markdown("#### 🤖 AI-Powered Intelligence")
        st.write("Advanced machine learning models analyze patterns to predict your perfect rating for each destination.")
    
    with detail_col3:
        st.markdown("#### 🏛️ Comprehensive Coverage")
        st.write("Explore cultural heritage sites, pristine nature reserves, beautiful beaches, and vibrant cities across Indonesia.")
    
    # Quick stats
    st.markdown("---")
    st.subheader("📊 Platform Overview")
    
    places = load_sample_places()
    stats = calculate_statistics(places)
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Places", stats['total_places'])
        
        with col2:
            st.metric("Average Rating", f"{stats['avg_rating']:.1f}⭐")
        
        with col3:
            st.metric("Categories", len(stats['categories']))
        
        with col4:
            st.metric("Cities", len(stats['cities']))
    
    # Getting started
    st.markdown("---")
    st.subheader("🚀 Getting Started")
    
    st.markdown("""
    1. **Set Your Preferences** - Use the sidebar to specify your age, preferred category, city, and budget
    2. **Get Recommendations** - Click "Get Recommendations" to receive personalized suggestions
    3. **Explore Results** - View detailed place cards with ratings, prices, and descriptions
    4. **Find Locations** - Use the Maps tab to view places on Google Maps and get directions
    """)
    
    # System Status
    st.markdown("---")
    st.subheader("🔌 System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**API Status:**")
        try:
            health = cached_get_health()
            
            if health.get('status') == 'healthy':
                st.success("✅ AI API: Connected")
                if health.get('model_name'):
                    st.info(f"🤖 Model: {health.get('model_name', 'Unknown')}")
            else:
                st.warning("⚠️ AI API: Issues detected")
                    
        except Exception as e:
            st.error(f"❌ AI API: Offline ({str(e)})")
    
    with col2:
        st.markdown("**Data Source:**")
        try:
            from utils.clickhouse_loader import test_clickhouse_connection
            clickhouse_status = test_clickhouse_connection()
            
            if clickhouse_status['status'] == 'connected':
                st.success("✅ ClickHouse: Connected")
                st.info(f"🗄️ Database: {clickhouse_status['database']}")
            else:
                st.warning("⚠️ ClickHouse: Using sample data")
                st.info("📁 Fallback: JSON file")
                
        except Exception as e:
            st.warning("⚠️ Database: Using sample data")
            st.info("📁 Fallback: JSON file")

def render_recommendations_page():
    """Render the recommendations page."""
    
    # Header using native Streamlit
    st.markdown("# 🎯 Get Your Recommendations")
    st.markdown("*Personalized tourism suggestions based on your preferences*")
    st.write("")
    
    # Load places data
    places = load_sample_places()
    if not places:
        st.error("Unable to load places data. Please check the data files.")
        return
    
    # Get user preferences from sidebar
    preferences = st.session_state.get('sidebar_preferences', {})
    
    # Apply basic filters
    filtered_places = filter_places(
        places,
        category=preferences.get('preferred_category'),
        city=preferences.get('preferred_city'),
        max_price=preferences.get('max_price'),
        min_rating=preferences.get('min_rating')
    )
    
    if not filtered_places:
        st.warning("No places match your current filters. Try adjusting your preferences in the sidebar.")
        return
    
    # Limit places for API call
    max_places = min(len(filtered_places), preferences.get('max_places_to_evaluate', 20))
    places_for_api = filtered_places[:max_places]
    
    st.info(f"Found {len(filtered_places)} places matching your filters. Analyzing top {len(places_for_api)} places.")
    
    # Get recommendations if user clicked submit
    if preferences.get('submitted', False):
        # Validate preferences before making API call
        from utils.validators import validate_user_preferences, display_validation_errors, sanitize_user_input
        
        validation_errors = validate_user_preferences(preferences)
        
        if validation_errors:
            st.error("❌ **Input Validation Failed**")
            display_validation_errors(validation_errors, "Please correct the following issues:")
            st.info("💡 **Tip**: Check your preferences in the sidebar and try again.")
        else:
            try:
                # Sanitize inputs
                clean_preferences = sanitize_user_input(preferences)
                
                # Prepare API payload
                api_payload = prepare_api_payload(clean_preferences, places_for_api)
                
                # Show user what we're doing
                with st.expander("🔍 Request Details", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.json(api_payload['user'])
                    with col2:
                        st.write(f"Analyzing {len(api_payload['places'])} places")
                        st.write(f"Requesting top {clean_preferences.get('top_k', 5)} recommendations")
                
                # Get recommendations from API
                recommendations = get_recommendations_with_progress(
                    api_payload['user'], 
                    api_payload['places'], 
                    clean_preferences.get('top_k', 5)
                )
                
                if recommendations and 'top_recommendations' in recommendations:
                    # Create lookup for predictions
                    predictions = recommendations['top_recommendations']
                    
                    # Get recommended places in order
                    # Create a mapping from numeric place_id back to original places
                    place_id_map = {}
                    for place in places_for_api:
                        # Calculate the same numeric ID as in prepare_api_payload
                        place_id = place.get('place_id')
                        if isinstance(place_id, str):
                            numeric_place_id = abs(hash(place_id)) % 1000000
                        else:
                            numeric_place_id = int(place_id) if place_id is not None else 0
                        place_id_map[numeric_place_id] = place
                    
                    recommended_places = []
                    for pred in predictions:
                        # API returns place_id as string, convert to int for lookup
                        place_id_int = int(pred['place_id'])
                        place = place_id_map.get(place_id_int)
                        if place:
                            recommended_places.append(place)
                    
                    if recommended_places:
                        # Show summary statistics
                        avg_rating = sum(p['predicted_rating'] for p in predictions) / len(predictions)
                        avg_confidence = sum(p['confidence_score'] for p in predictions) / len(predictions)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Recommendations", len(predictions))
                        with col2:
                            st.metric("Avg Predicted Rating", f"{avg_rating:.1f}⭐")
                        with col3:
                            st.metric("Avg Confidence", f"{avg_confidence:.1%}")
                        
                        # Render recommendations
                        render_places_with_tabs(recommended_places, predictions)
                        
                        # Store in session state 
                        st.session_state['last_recommendations'] = recommendations
                        st.session_state['last_places'] = recommended_places
                    else:
                        st.warning("⚠️ No matching places found for your preferences.")
                        st.info("💡 **Tip**: Try adjusting your filters or preferences.")
                else:
                    st.error("❌ Failed to get valid recommendations from the API.")
                    st.info("💡 **Tip**: The API may be experiencing issues. Try again later.")
                    
            except Exception as e:
                st.error("❌ **Recommendation Error**")
                error_type = type(e).__name__
                st.error(f"**Error Type**: {error_type}")
                st.error(f"**Details**: {str(e)}")
                
                # Provide fallback functionality
                st.info("🔄 **Fallback Mode**: Showing places without AI recommendations")
                
                # Show places without predictions
                fallback_places = places_for_api[:preferences.get('top_k', 5)]
                render_places_with_tabs(fallback_places)
                
                # Provide debugging info
                with st.expander("🐛 Debug Information", expanded=False):
                    st.write("**User Preferences:**")
                    st.json(preferences)
                    st.write("**Places Count:**", len(places_for_api))
                    try:
                        api_client = get_api_client()
                        st.write("**API Base URL:**", api_client.base_url)
                    except:
                        st.write("**API Base URL:**", "Could not determine")
    else:
        st.info("👈 Set your preferences in the sidebar and click 'Get Recommendations' to start!")
        st.markdown("### Preview: Available Places")
        
        # Show preview of available places
        preview_places = places_for_api[:6]  # Show first 6 places as preview
        render_places_with_tabs(preview_places)

# Analytics page removed - focusing on core recommendation and maps functionality

def render_about_page():
    """Render the about page."""
    
    # Header using native Streamlit
    st.markdown("# ℹ️ About Tourism Indonesia")
    st.markdown("*Learn more about our AI-powered recommendation system*")
    st.write("")
    
    # About the system
    st.subheader("🤖 How It Works")
    st.markdown("""
    Our tourism recommendation system uses advanced machine learning algorithms to provide personalized suggestions:
    
    1. **Feature Engineering** - We analyze user preferences, place characteristics, and historical rating patterns
    2. **Hybrid Models** - Combines collaborative filtering with content-based recommendations
    3. **Advanced ML** - Uses ensemble methods including Gradient Boosting and Neural Networks
    4. **Real-time Predictions** - Provides instant recommendations based on your preferences
    """)
    
    # System information
    st.subheader("📊 System Details")
    
    try:
        health = cached_get_health()
        
        if health.get('status') == 'healthy':
            st.markdown("**System Status:**")
            st.success("✅ Recommendation API is online and healthy")
            if health.get('model_name'):
                st.info(f"🤖 Active Model: {health['model_name']}")
        else:
            st.warning("⚠️ System may be experiencing issues")
    
    except Exception as e:
        st.error(f"Unable to connect to recommendation system: {e}")
        st.info("The system may be offline or starting up.")
    
    # Data sources
    st.subheader("🗂️ Data Sources")
    st.markdown("""
    Our recommendations are based on:
    
    - **50+ Popular Indonesian Destinations** across major cities
    - **6 Tourism Categories**: Cultural sites, theme parks, nature reserves, marine areas, shopping centers, religious sites
    - **Comprehensive Place Information**: Ratings, prices, duration, descriptions
    - **User Preference Modeling**: Age, category preferences, budget, location preferences
    """)
    
    # Categories
    st.subheader("🎯 Tourism Categories")
    
    categories_info = {
        "Budaya": "Cultural and historical sites including temples, museums, and heritage locations",
        "Taman Hiburan": "Theme parks, amusement parks, and family entertainment venues",
        "Cagar Alam": "Nature reserves, national parks, and natural attractions",
        "Bahari": "Marine and coastal attractions including beaches and diving spots",
        "Pusat Perbelanjaan": "Shopping centers, markets, and retail destinations",
        "Tempat Ibadah": "Religious and spiritual sites including mosques, temples, and churches"
    }
    
    for category, description in categories_info.items():
        st.markdown(f"**{category}:** {description}")
    
    # Technical details
    st.subheader("⚙️ Technical Implementation")
    
    with st.expander("System Architecture"):
        st.markdown("""
        - **Frontend:** Streamlit with responsive design
        - **Backend API:** FastAPI with automatic documentation
        - **ML Framework:** MLflow for model management and versioning
        - **Model Types:** Gradient Boosting, Neural Networks, Ensemble methods
        - **Data Processing:** Pandas, NumPy for feature engineering
        - **Visualization:** Plotly for interactive charts and analytics
        """)
    
    with st.expander("Model Features"):
        st.markdown("""
        The recommendation model uses 22+ features including:
        
        - **User Features:** Age, historical preferences, rating patterns
        - **Place Features:** Category, city, price, duration, rating
        - **Interaction Features:** User-place compatibility scores
        - **Global Features:** Population statistics and trends
        - **Contextual Features:** Price ratios, rating deviations
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("**Built with ❤️ for Indonesian Tourism • Powered by AI & Machine Learning**")
    st.markdown("🏝️ Discover the beauty of Indonesia with personalized recommendations")

def render_maps_page():
    """Render the maps page."""
    
    # Header using native Streamlit
    st.markdown("# 🗺️ Explore Places on Maps")
    st.markdown("*Interactive maps and location information for all destinations*")
    st.write("")
    
    # Load places data
    places = load_sample_places()
    if not places:
        st.error("Unable to load places data. Please check the data files.")
        return
    
    # Map summary stats
    render_map_summary_stats(places)
    
    st.write("")
    st.write("")
    
    # Interactive map selector
    selected_place = render_interactive_map_selector(places)
    
    # Show place details
    if selected_place:
        st.write("")
        st.markdown("---")
        st.markdown("### 📍 Selected Place Details")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write(f"**Name:** {selected_place.get('place_name', selected_place['place_id'].replace('_', ' ').title())}")
            st.write(f"**Category:** {selected_place['place_category']}")
            st.write(f"**City:** {selected_place['place_city']}")
            
        with col2:
            from utils.data_processing import format_currency, format_duration
            st.write(f"**Price:** {format_currency(selected_place['place_price'])}")
            st.write(f"**Rating:** {selected_place['place_average_rating']:.1f}⭐")
            st.write(f"**Duration:** {format_duration(selected_place['place_visit_duration_minutes'])}")
        
        st.write(f"**Description:** {selected_place.get('place_description', 'No description available')}")
    
    # Additional tips
    st.write("")
    st.markdown("---")
    st.markdown("### 💡 Maps Integration Tips")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **🗺️ View on Google Maps:**
        - Click "📍 View on Google Maps" to open the location in a new tab
        - Perfect for getting detailed information and street view
        """)
        
    with tips_col2:
        st.markdown("""
        **🧭 Get Directions:**
        - Click "Get Directions" for turn-by-turn navigation
        - Opens Google Maps with route planning from your location
        """)

def main():
    """Main application function."""
    
    # Render sidebar
    sidebar_preferences = render_sidebar()
    st.session_state['sidebar_preferences'] = sidebar_preferences
    
    # Check if form was submitted and switch to Recommendations
    if sidebar_preferences.get('submitted', False):
        st.session_state.active_tab_index = 1  # Recommendations tab
    
    # Initialize active tab if not set
    if 'active_tab_index' not in st.session_state:
        st.session_state.active_tab_index = 0
    
    # Create custom tab interface with buttons
    tab_names = ["🏠 Home", "🎯 Recommendations", "🗺️ Maps", "ℹ️ About"]
    
    # Create columns for tab buttons
    cols = st.columns(len(tab_names))
    
    for i, (col, tab_name) in enumerate(zip(cols, tab_names)):
        with col:
            # Highlight active tab
            if i == st.session_state.active_tab_index:
                if st.button(tab_name, key=f"tab_{i}", use_container_width=True, type="primary"):
                    st.session_state.active_tab_index = i
                    st.rerun()
            else:
                if st.button(tab_name, key=f"tab_{i}", use_container_width=True):
                    st.session_state.active_tab_index = i
                    st.rerun()
    
    st.divider()
    
    # Render content based on active tab
    if st.session_state.active_tab_index == 0:
        st.session_state.current_page = 'Home'
        render_home_page()
    elif st.session_state.active_tab_index == 1:
        st.session_state.current_page = 'Recommendations'
        # User submitted recommendations, content will be displayed below
        render_recommendations_page()
    elif st.session_state.active_tab_index == 2:
        st.session_state.current_page = 'Maps'
        render_maps_page()
    elif st.session_state.active_tab_index == 3:
        st.session_state.current_page = 'About'
        render_about_page()

if __name__ == "__main__":
    main()