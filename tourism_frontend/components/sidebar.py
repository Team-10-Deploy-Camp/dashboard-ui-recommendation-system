"""
Sidebar component for user preference input
"""

import streamlit as st
from typing import Dict, Any
from config import TOURISM_CATEGORIES, INDONESIAN_CITIES, BUDGET_RANGES, COLORS

def render_user_preferences_form() -> Dict[str, Any]:
    """Render user preferences form in sidebar using native Streamlit."""
    
    # Header using native Streamlit
    st.sidebar.markdown("# 🎯 Your Preferences")
    st.sidebar.markdown("*Tell us what you're looking for*")
    st.sidebar.write("")
    
    with st.sidebar.form("user_preferences"):
        # Personal Section
        st.markdown("### 👤 Personal Details")
        
        user_age = st.slider(
            "Your Age",
            min_value=18,
            max_value=100,
            value=28,
            help="Your age helps us recommend age-appropriate activities"
        )
        
        # Travel Preferences Section
        st.write("")
        st.markdown("### 🎯 Travel Preferences")
        
        preferred_category = st.selectbox(
            "What interests you most?",
            options=["All Categories"] + TOURISM_CATEGORIES,
            index=0,
            help="Choose the type of places you'd like to explore"
        )
        
        preferred_city = st.selectbox(
            "Which city to explore?",
            options=["All Cities"] + INDONESIAN_CITIES,
            index=0,
            help="Select your preferred destination city"
        )
        
        budget_range = st.selectbox(
            "Your budget range",
            options=BUDGET_RANGES,
            index=1,  # Default to Medium
            help="Low: <50K IDR • Medium: 50K-200K IDR • High: >200K IDR"
        )
        
        # Advanced Filters Section
        st.write("")
        st.markdown("### ⚙️ Advanced Filters")
        
        col1, col2 = st.columns(2)
        with col1:
            top_k = st.selectbox(
                "Recommendations",
                options=[3, 5, 8, 10],
                index=1,  # Default to 5
                help="Number of places to recommend"
            )
        
        with col2:
            min_rating = st.selectbox(
                "Min Rating",
                options=[1.0, 2.0, 3.0, 4.0, 4.5],
                index=2,  # Default to 3.0
                help="Minimum rating filter"
            )
        
        max_price = st.selectbox(
            "Max Price (IDR)",
            options=[50000, 100000, 200000, 500000, 1000000],
            index=2,  # Default to 200K
            help="Maximum price you're willing to spend"
        )
        
        # Action Buttons
        st.write("")
        
        submitted = st.form_submit_button(
            "🚀 Get My Recommendations",
            use_container_width=True,
            help="Generate personalized recommendations based on your preferences"
        )
        
        if st.form_submit_button("🔄 Reset All", use_container_width=True, help="Clear all preferences and start over"):
            st.session_state.clear()
            st.rerun()
    
    # Store preferences in session state
    preferences = {
        'user_age': user_age,
        'preferred_category': preferred_category if preferred_category not in ["All Categories", "All"] else None,
        'preferred_city': preferred_city if preferred_city not in ["All Cities", "All"] else None,
        'budget_range': budget_range,
        'top_k': top_k,
        'min_rating': min_rating,
        'max_price': max_price,
        'submitted': submitted
    }
    
    # Update session state
    for key, value in preferences.items():
        st.session_state[f'pref_{key}'] = value
    
    return preferences

def render_preference_summary(preferences: Dict[str, Any]) -> None:
    """Render a summary of current preferences."""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Current Preferences")
    
    # Create preference summary
    summary_items = []
    
    if preferences.get('preferred_category'):
        summary_items.append(f"**Category:** {preferences['preferred_category']}")
    
    if preferences.get('preferred_city'):
        summary_items.append(f"**City:** {preferences['preferred_city']}")
    
    summary_items.append(f"**Age:** {preferences['user_age']}")
    summary_items.append(f"**Budget:** {preferences['budget_range']}")
    summary_items.append(f"**Min Rating:** {preferences['min_rating']:.1f}⭐")
    summary_items.append(f"**Max Price:** Rp {preferences['max_price']:,}")
    
    for item in summary_items:
        st.sidebar.markdown(f"• {item}")

def render_tips_and_info() -> None:
    """Render tips and information in sidebar."""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Tips")
    
    tips = [
        "🎯 **Be specific** about your preferences for better recommendations",
        "💰 **Budget ranges**: Low (<50K), Medium (50K-200K), High (>200K)",
        "⭐ **Higher ratings** mean more popular places",
        "🏛️ **Cultural sites** often have entrance fees",
        "🏖️ **Beach areas** may have additional activity costs"
    ]
    
    for tip in tips:
        st.sidebar.markdown(f"• {tip}")

def render_api_status() -> None:
    """Render API connection status in sidebar."""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔌 API Status")
    
    # Import here to avoid circular import
    from utils.api_client import cached_get_health
    
    try:
        health = cached_get_health()
        if health.get('status') == 'healthy':
            st.sidebar.success("✅ API Connected")
            if health.get('model_name'):
                st.sidebar.info(f"🤖 Model: {health['model_name']}")
        else:
            st.sidebar.warning("⚠️ API Issues")
    except Exception:
        st.sidebar.error("❌ API Offline")
        st.sidebar.info("Using demo mode")

def render_sidebar() -> Dict[str, Any]:
    """Main function to render complete sidebar."""
    
    # Render user preferences form
    preferences = render_user_preferences_form()
    
    # Render preference summary if preferences are set
    if any(preferences.values()):
        render_preference_summary(preferences)
    
    # Render tips and info
    render_tips_and_info()
    
    # Render API status
    render_api_status()
    
    return preferences