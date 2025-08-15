# Claude Code Instructions: Tourism Recommendation Streamlit Frontend

## Project Overview

Create a modern, responsive Streamlit frontend for the Tourism Recommendation API that allows users to get personalized tourism place recommendations in Indonesia.

## Project Structure

```
tourism_frontend/
├── app.py                 # Main Streamlit application
├── components/
│   ├── __init__.py
│   ├── sidebar.py         # User preference input
│   ├── place_cards.py     # Place display components
│   └── charts.py          # Visualization components
├── utils/
│   ├── __init__.py
│   ├── api_client.py      # FastAPI integration
│   ├── data_processing.py # Data formatting utilities
│   └── validators.py      # Input validation
├── assets/
│   └── styles.css         # Custom CSS styling
├── requirements.txt       # Dependencies
├── config.py             # Configuration settings
└── README.md             # Documentation
```

## Core Requirements

### 1. Main Application (app.py)

Create a multi-page Streamlit app with:

- **Home Page**: Welcome screen with system overview
- **Recommendations Page**: Main functionality for getting recommendations
- **Analytics Page**: Model performance metrics and insights
- **About Page**: Information about the recommendation system

Key features:

- Modern, Indonesian tourism-themed UI
- Responsive design that works on mobile/desktop
- Real-time API integration
- Interactive visualizations
- Error handling and loading states

### 2. User Interface Components

#### Sidebar (components/sidebar.py)

Create user preference input form:

```python
# Required inputs:
- user_age: Slider (18-100)
- preferred_category: Selectbox with options like:
  * "Budaya" (Culture)
  * "Taman Hiburan" (Theme Park)
  * "Cagar Alam" (Nature Reserve)
  * "Bahari" (Marine)
  * "Pusat Perbelanjaan" (Shopping Center)
  * "Tempat Ibadah" (Religious Site)
- preferred_city: Selectbox with Indonesian cities
- budget_range: Select (low, medium, high)

# Additional features:
- Form validation
- Clear/Reset button
- Save preferences to session state
```

#### Place Cards (components/place_cards.py)

Design attractive place display cards showing:

- Place name and category
- Location (city)
- Predicted rating with star visualization
- Price information
- Visit duration
- Confidence score as progress bar
- Recommendation rank badge

#### Charts (components/charts.py)

Create visualization components:

- Rating distribution chart
- Price vs Rating scatter plot
- Category preference radar chart
- Model confidence visualization

### 3. API Integration (utils/api_client.py)

Create a robust API client class:

```python
class TourismAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    async def get_health(self):
        # Health check endpoint

    async def get_model_info(self):
        # Model information

    async def predict_ratings(self, user_prefs, places):
        # Main prediction endpoint

    async def get_recommendations(self, user_prefs, places, top_k=5):
        # Recommendations endpoint

    # Include proper error handling, timeouts, retries
```

### 4. Sample Data Integration

Since the API expects place data, create a sample dataset of Indonesian tourism places:

```python
# Include ~50-100 popular Indonesian destinations with:
- place_id
- place_category
- place_city
- place_price (in IDR)
- place_average_rating
- place_visit_duration_minutes
- place_description

# Cities should include: Jakarta, Bali, Yogyakarta, Bandung, Surabaya, etc.
# Categories should match the API expectations
```

### 5. Key Features to Implement

#### User Experience:

- **Progressive Disclosure**: Start simple, reveal more options as needed
- **Real-time Updates**: Show recommendations as user changes preferences
- **Loading States**: Elegant spinners and progress indicators
- **Error Handling**: Graceful degradation when API is unavailable
- **Responsive Design**: Works well on mobile devices

#### Functionality:

- **Personalized Recommendations**: Based on user preferences
- **Filtering & Sorting**: By category, price, rating, location
- **Comparison View**: Side-by-side place comparison
- **Favorites System**: Save preferred places (session-based)
- **Export Results**: Download recommendations as PDF/CSV

#### Analytics Dashboard:

- **Model Performance Metrics**: RMSE, MAE, F1-score display
- **Recommendation Statistics**: Distribution charts
- **User Interaction Analytics**: Most popular categories/cities
- **System Health**: API status, response times

### 6. Styling and Theme

Use Indonesian tourism-inspired design:

```css
/* Color Palette */
--primary: #C8102E;      /* Indonesian Red */
--secondary: #FFFFFF;     /* White */
--accent: #FFD700;        /* Gold */
--nature: #228B22;        /* Forest Green */
--ocean: #006994;         /* Ocean Blue */

/* Typography */
- Primary font: Modern sans-serif (Inter, Poppins)
- Headers: Bold, clean
- Body: Readable, accessible

/* Visual Elements */
- Indonesian cultural patterns as subtle backgrounds
- Tourism-related icons (temples, beaches, mountains)
- Card-based layout with shadows and hover effects
- Gradient backgrounds for hero sections
```

### 7. Technical Specifications

#### Dependencies (requirements.txt):

```
streamlit>=1.28.0
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
altair>=5.0.0
Pillow>=10.0.0
asyncio
aiohttp>=3.8.0
python-dotenv>=1.0.0
```

#### Configuration (config.py):

```python
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# App Configuration
APP_TITLE = "Tourism Indonesia - AI Recommendations"
PAGE_ICON = "🏝️"
LAYOUT = "wide"

# Sample Data Configuration
SAMPLE_DATA_PATH = "data/sample_places.json"
DEFAULT_TOP_K = 5
MAX_PLACES_TO_EVALUATE = 50
```

### 8. Error Handling Strategy

Implement comprehensive error handling:

- **API Connection Errors**: Show offline mode with cached data
- **Invalid Input**: Real-time validation with helpful messages
- **Server Errors**: Graceful degradation to basic recommendations
- **Network Timeouts**: Retry mechanism with user feedback
- **Data Validation**: Ensure API responses match expected format

### 9. Performance Optimization

- **Caching**: Use st.cache_data for expensive operations
- **Async Operations**: Non-blocking API calls
- **Lazy Loading**: Load place images on demand
- **Session State**: Persist user preferences and recommendations
- **Batch Processing**: Group API calls efficiently

### 10. Accessibility Features

- **Keyboard Navigation**: Full app usable without mouse
- **Screen Reader Support**: Proper ARIA labels
- **Color Contrast**: WCAG compliant color combinations
- **Text Scaling**: Responsive typography
- **Alternative Text**: All images have descriptive alt text

## Implementation Priority

### Phase 1 (MVP):

1. Basic Streamlit app structure
2. User preference input form
3. API client integration
4. Simple recommendations display
5. Basic error handling

### Phase 2 (Enhanced):

1. Advanced visualizations
2. Place comparison features
3. Filtering and sorting
4. Custom styling and themes
5. Mobile responsiveness

### Phase 3 (Advanced):

1. Analytics dashboard
2. Favorites system
3. Export functionality
4. Performance optimizations
5. Accessibility improvements

## Success Criteria

The completed application should:

1. ✅ Connect successfully to the FastAPI backend
2. ✅ Provide intuitive user preference input
3. ✅ Display personalized recommendations attractively
4. ✅ Handle errors gracefully
5. ✅ Work responsively on different screen sizes
6. ✅ Show model performance metrics
7. ✅ Include Indonesian cultural design elements
8. ✅ Load and perform well under normal usage
9. ✅ Be accessible to users with disabilities
10. ✅ Include comprehensive documentation

## Development Notes

- Use async/await for API calls to keep UI responsive
- Implement proper logging for debugging
- Add environment variable support for different deployment stages
- Include unit tests for critical functions
- Follow Python PEP 8 style guidelines
- Use type hints throughout the codebase
- Include comprehensive docstrings
- Handle Indonesian language text properly (UTF-8)

## Deployment Considerations

- Ensure compatibility with Streamlit Cloud
- Include proper environment variable management
- Add health checks and monitoring
- Optimize for production performance
- Include backup data in case API is unavailable

Create this as a modern, production-ready application that showcases the ML model capabilities while providing an excellent user experience for discovering Indonesian tourism destinations.
