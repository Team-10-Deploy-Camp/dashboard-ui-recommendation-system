"""
Visualization components for tourism recommendations
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict, Any
import numpy as np
from config import COLORS

def create_rating_distribution_chart(places: List[Dict[str, Any]], predictions: List[Dict[str, Any]] = None) -> go.Figure:
    """Create rating distribution chart."""
    
    fig = make_subplots(
        rows=1, cols=2 if predictions else 1,
        subplot_titles=["Original Ratings"] + (["Predicted Ratings"] if predictions else []),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]] if predictions else [[{"secondary_y": False}]]
    )
    
    # Original ratings
    original_ratings = [place['place_average_rating'] for place in places]
    
    fig.add_trace(
        go.Histogram(
            x=original_ratings,
            nbinsx=20,
            name="Original Ratings",
            marker_color=COLORS["primary"],
            opacity=0.7
        ),
        row=1, col=1
    )
    
    # Predicted ratings if available
    if predictions:
        predicted_ratings = [pred['predicted_rating'] for pred in predictions]
        
        fig.add_trace(
            go.Histogram(
                x=predicted_ratings,
                nbinsx=20,
                name="Predicted Ratings",
                marker_color=COLORS["nature"],
                opacity=0.7
            ),
            row=1, col=2
        )
    
    fig.update_layout(
        title="Rating Distribution",
        showlegend=True,
        height=400,
        title_font_color=COLORS["primary"]
    )
    
    return fig

def create_price_vs_rating_scatter(places: List[Dict[str, Any]], predictions: List[Dict[str, Any]] = None) -> go.Figure:
    """Create price vs rating scatter plot."""
    
    # Prepare data
    df_data = []
    prediction_lookup = {}
    if predictions:
        prediction_lookup = {pred['place_id']: pred for pred in predictions}
    
    for place in places:
        prediction = prediction_lookup.get(place['place_id'])
        
        row = {
            'place_name': place['place_id'].replace('_', ' ').title(),
            'price': place['place_price'],
            'original_rating': place['place_average_rating'],
            'category': place['place_category'],
            'city': place['place_city']
        }
        
        if prediction:
            row['predicted_rating'] = prediction['predicted_rating']
            row['confidence'] = prediction['confidence_score']
            row['rank'] = prediction['recommendation_rank']
        
        df_data.append(row)
    
    df = pd.DataFrame(df_data)
    
    fig = go.Figure()
    
    # Original ratings scatter
    fig.add_trace(
        go.Scatter(
            x=df['price'],
            y=df['original_rating'],
            mode='markers',
            name='Original Ratings',
            marker=dict(
                color=COLORS["primary"],
                size=10,
                opacity=0.7
            ),
            text=df['place_name'],
            hovertemplate='<b>%{text}</b><br>Price: Rp %{x:,.0f}<br>Rating: %{y:.1f}<extra></extra>'
        )
    )
    
    # Predicted ratings if available
    if 'predicted_rating' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['price'],
                y=df['predicted_rating'],
                mode='markers',
                name='Predicted Ratings',
                marker=dict(
                    color=COLORS["nature"],
                    size=12,
                    opacity=0.8,
                    symbol='diamond'
                ),
                text=df['place_name'],
                hovertemplate='<b>%{text}</b><br>Price: Rp %{x:,.0f}<br>Predicted Rating: %{y:.1f}<extra></extra>'
            )
        )
    
    fig.update_layout(
        title="Price vs Rating Analysis",
        xaxis_title="Price (IDR)",
        yaxis_title="Rating",
        height=500,
        title_font_color=COLORS["primary"]
    )
    
    return fig

def create_category_radar_chart(places: List[Dict[str, Any]], user_prefs: Dict[str, Any] = None) -> go.Figure:
    """Create category preference radar chart."""
    
    # Calculate category statistics
    df = pd.DataFrame(places)
    category_stats = df.groupby('place_category').agg({
        'place_average_rating': 'mean',
        'place_price': 'mean',
        'place_visit_duration_minutes': 'mean'
    }).reset_index()
    
    # Normalize values for radar chart (0-5 scale)
    category_stats['rating_norm'] = category_stats['place_average_rating']
    category_stats['price_norm'] = 5 - (category_stats['place_price'] / category_stats['place_price'].max() * 5)  # Inverse for price
    category_stats['duration_norm'] = category_stats['place_visit_duration_minutes'] / category_stats['place_visit_duration_minutes'].max() * 5
    
    fig = go.Figure()
    
    # Add trace for each metric
    fig.add_trace(go.Scatterpolar(
        r=category_stats['rating_norm'].tolist() + [category_stats['rating_norm'].iloc[0]],
        theta=category_stats['place_category'].tolist() + [category_stats['place_category'].iloc[0]],
        fill='toself',
        name='Average Rating',
        marker_color=COLORS["primary"]
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=category_stats['price_norm'].tolist() + [category_stats['price_norm'].iloc[0]],
        theta=category_stats['place_category'].tolist() + [category_stats['place_category'].iloc[0]],
        fill='toself',
        name='Value for Money',
        marker_color=COLORS["nature"]
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        title="Category Analysis",
        height=500,
        title_font_color=COLORS["primary"]
    )
    
    return fig

def create_confidence_visualization(predictions: List[Dict[str, Any]]) -> go.Figure:
    """Create model confidence visualization."""
    
    if not predictions:
        return go.Figure()
    
    df = pd.DataFrame(predictions)
    df['place_name'] = df['place_id'].str.replace('_', ' ').str.title()
    
    fig = go.Figure()
    
    # Create confidence bars
    fig.add_trace(
        go.Bar(
            x=df['place_name'],
            y=df['confidence_score'],
            marker_color=[COLORS["nature"] if conf >= 0.8 else COLORS["accent"] if conf >= 0.6 else COLORS["primary"] 
                         for conf in df['confidence_score']],
            text=[f"{conf:.1%}" for conf in df['confidence_score']],
            textposition='auto',
            name='Confidence Score'
        )
    )
    
    fig.update_layout(
        title="Model Confidence by Recommendation",
        xaxis_title="Places",
        yaxis_title="Confidence Score",
        xaxis_tickangle=-45,
        height=400,
        title_font_color=COLORS["primary"]
    )
    
    return fig

def create_model_metrics_dashboard(model_info: Dict[str, Any]) -> go.Figure:
    """Create model performance metrics dashboard."""
    
    metrics = model_info.get('model_metrics', {})
    if not metrics:
        # Default metrics for demo
        metrics = {'rmse': 0.85, 'mae': 0.65, 'f1_score': 0.78}
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=list(metrics.keys()),
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
    )
    
    colors = [COLORS["primary"], COLORS["nature"], COLORS["accent"]]
    
    for i, (metric, value) in enumerate(metrics.items()):
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': metric.upper()},
                gauge={
                    'axis': {'range': [None, 1]},
                    'bar': {'color': colors[i]},
                    'steps': [
                        {'range': [0, 0.5], 'color': "lightgray"},
                        {'range': [0.5, 0.75], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.9
                    }
                }
            ),
            row=1, col=i+1
        )
    
    fig.update_layout(
        title="Model Performance Metrics",
        height=300,
        title_font_color=COLORS["primary"]
    )
    
    return fig

def create_city_popularity_chart(places: List[Dict[str, Any]]) -> go.Figure:
    """Create city popularity chart."""
    
    df = pd.DataFrame(places)
    city_stats = df.groupby('place_city').agg({
        'place_id': 'count',
        'place_average_rating': 'mean',
        'place_price': 'mean'
    }).reset_index()
    city_stats.columns = ['city', 'place_count', 'avg_rating', 'avg_price']
    city_stats = city_stats.sort_values('place_count', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            y=city_stats['city'],
            x=city_stats['place_count'],
            orientation='h',
            marker_color=COLORS["ocean"],
            text=city_stats['place_count'],
            textposition='auto',
            name='Number of Places'
        )
    )
    
    fig.update_layout(
        title="Places by City",
        xaxis_title="Number of Places",
        yaxis_title="City",
        height=400,
        title_font_color=COLORS["primary"]
    )
    
    return fig

def render_analytics_dashboard(places: List[Dict[str, Any]], 
                              predictions: List[Dict[str, Any]] = None,
                              model_info: Dict[str, Any] = None,
                              user_prefs: Dict[str, Any] = None) -> None:
    """Render complete analytics dashboard."""
    
    # Header using native Streamlit
    st.markdown("# 📊 Analytics Dashboard")
    st.markdown("*Insights from your tourism recommendations*")
    st.write("")
    
    # Model Performance Section
    if model_info:
        st.subheader("🤖 Model Performance")
        fig_metrics = create_model_metrics_dashboard(model_info)
        st.plotly_chart(fig_metrics, use_container_width=True)
    
    # Recommendations Analysis
    if predictions:
        st.subheader("🎯 Recommendation Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            fig_confidence = create_confidence_visualization(predictions)
            st.plotly_chart(fig_confidence, use_container_width=True)
        
        with col2:
            fig_ratings = create_rating_distribution_chart(places, predictions)
            st.plotly_chart(fig_ratings, use_container_width=True)
    
    # Place Analysis
    st.subheader("🏛️ Place Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        fig_price_rating = create_price_vs_rating_scatter(places, predictions)
        st.plotly_chart(fig_price_rating, use_container_width=True)
    
    with col2:
        fig_city = create_city_popularity_chart(places)
        st.plotly_chart(fig_city, use_container_width=True)
    
    # Category Analysis
    st.subheader("🎯 Category Analysis")
    fig_radar = create_category_radar_chart(places, user_prefs)
    st.plotly_chart(fig_radar, use_container_width=True)