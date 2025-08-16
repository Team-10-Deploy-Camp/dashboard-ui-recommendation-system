# Tourism Indonesia - AI Recommendations Frontend 🏝️

A modern, responsive Streamlit frontend application for discovering Indonesian tourism destinations with AI-powered personalized recommendations. Built with native Streamlit components and featuring an Indonesian cultural design theme.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io/)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-Database-yellow.svg)](https://clickhouse.com/)

## ✨ Features

- **🎯 Personalized Recommendations**: AI-powered tourism suggestions based on user preferences
- **🎨 Indonesian Cultural Design**: Modern UI with traditional Indonesian color schemes and themes
- **📱 Responsive Interface**: Multi-page layout with interactive maps and visualizations
- **🗺️ Interactive Maps**: Google Maps integration for location discovery
- **📊 Analytics Dashboard**: Real-time insights and recommendation analytics
- **🏖️ 50+ Destinations**: Curated Indonesian tourism places across multiple categories
- **⚡ Real-time Processing**: Fast API integration with comprehensive error handling

## 🏗️ Application Architecture

```
┌─────────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Streamlit Frontend │────│  Tourism API     │────│  ClickHouse DB  │
│  (Port 8501)        │    │  (Port 8000)     │    │  (Port 9000)    │
└─────────────────────┘    └──────────────────┘    └─────────────────┘
         │                          │                        │
    ┌────────────┐        ┌─────────────────┐      ┌─────────────────┐
    │ UI Components      │  ML Models      │      │  Tourism Data   │
    │ & Analytics│        │  (Predictions)  │      │  (Live from DB) │
    └────────────┘        └─────────────────┘      └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- ClickHouse database (running)
- Tourism API backend (optional for offline mode)

### 1. Installation

```bash
# Navigate to the tourism frontend directory
cd tourism_frontend

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the root directory:

```env
# API Configuration
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30

# ClickHouse Database Configuration
clickhouse_host=localhost
clickhouse_port=8123
clickhouse_user=default
clickhouse_password=
clickhouse_database=default
clickhouse_table=mart_ratings_per_user
```

### 3. Run the Application

```bash
# Start the Streamlit app
streamlit run tourism_frontend/app.py

# Or using the deploy script
bash tourism_frontend/deploy.sh
```

### 4. Access the App

Open your browser to: `http://localhost:8501`

## 🎯 How to Use

### Getting Recommendations

1. **Set Your Preferences** (in sidebar):
   - Age (18-100)
   - Preferred category (Budaya, Taman Hiburan, Cagar Alam, etc.)
   - Preferred city (Jakarta, Bali, Yogyakarta, etc.)
   - Budget range (Low, Medium, High)
   - Number of recommendations (1-10)

2. **Apply Filters**:
   - Minimum rating threshold
   - Maximum price limit
   - Specific categories or cities

3. **Get Results**: Click "🔍 Get Recommendations" to receive personalized suggestions

### Viewing Results

- **Card View**: Visual cards with place images and details
- **Table View**: Comprehensive data table with all metrics
- **Analytics**: Charts and insights about recommendations

## 📊 Available Pages

### 🏠 Home
- Welcome interface with app overview
- Quick navigation to main features
- Indonesian tourism highlights

### 🎯 Recommendations 
- Main recommendation engine
- User preference settings
- Personalized tourism suggestions
- Filtering and sorting options

### 📊 Analytics (Coming Soon)
- Recommendation performance metrics
- User preference analysis
- Popular destinations insights
- Rating distribution charts

### ℹ️ About
- Application information
- Technology stack details
- Indonesian tourism overview

## 📁 Project Structure

```
tourism_frontend/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── requirements.txt       # Python dependencies
├── deploy.sh             # Deployment script
├── components/           # UI components
│   ├── __init__.py
│   ├── sidebar.py         # User preference sidebar
│   ├── place_cards.py     # Place display components  
│   ├── charts.py          # Data visualization
│   └── maps.py            # Map components
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── api_client.py      # API integration
│   ├── data_processing.py # Data processing
│   ├── clickhouse_loader.py # ClickHouse integration
│   └── validators.py      # Input validation
├── data/               # Sample data
│   └── sample_places.json
└── assets/             # Static assets
    └── styles.css         # Custom CSS
```

## 🌏 Indonesian Tourism Categories

### 🏠 Budaya (Culture)
- Historical sites and museums
- Traditional villages and heritage
- Cultural performances and exhibitions

### 🎠 Taman Hiburan (Theme Parks)
- Amusement parks and entertainment
- Water parks and recreational facilities
- Family-friendly attractions

### 🌳 Cagar Alam (Nature Reserves) 
- National parks and natural reserves
- Wildlife sanctuaries and conservation areas
- Eco-tourism destinations

### 🏖️ Bahari (Marine)
- Beaches and coastal areas
- Diving and snorkeling spots
- Island destinations

### 🛒 Pusat Perbelanjaan (Shopping)
- Shopping malls and centers
- Traditional markets and bazaars
- Retail and commercial areas

### 🕕 Tempat Ibadah (Religious Sites)
- Mosques, temples, and churches
- Pilgrimage destinations
- Spiritual and religious landmarks

## ⚙️ Configuration Options

### App Settings (config.py)

```python
# API Configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30

# Indonesian Tourism Categories
TOURISM_CATEGORIES = [
    "Budaya", "Taman Hiburan", "Cagar Alam", 
    "Bahari", "Pusat Perbelanjaan", "Tempat Ibadah"
]

# Indonesian Cities
INDONESIAN_CITIES = [
    "Jakarta", "Bali", "Yogyakarta", "Bandung",
    "Surabaya", "Medan", "Semarang", "Palembang"
]

# UI Colors (Indonesian Theme)
COLORS = {
    "primary": "#DC2626",      # Indonesian Red
    "accent": "#F59E0B",       # Gold
    "success": "#10B981",     # Nature Green
    "info": "#3B82F6"         # Ocean Blue
}
```

### ClickHouse Integration

- Live data loading from tourism database
- Dynamic place information and ratings
- Real-time recommendation scoring
- Analytics data for insights

## 🔍 Features Overview

### 🎯 Smart Recommendations
- Personalized suggestions based on user profile
- Multi-factor filtering (age, budget, preferences)
- Confidence scoring for each recommendation
- Real-time data from ClickHouse database

### 🎨 Indonesian Design Theme
- Traditional Indonesian color palette
- Cultural design elements and patterns  
- Modern responsive layout
- Native Streamlit components

### 📊 Analytics & Insights
- Recommendation performance metrics
- User preference analysis
- Tourism trends and patterns
- Interactive data visualizations

### 🚀 Performance
- Fast loading with caching
- Efficient API integration
- Real-time data processing
- Responsive user interface

## 🚀 Deployment

### Development Mode
```bash
cd tourism_frontend
streamlit run app.py
```

### Production Mode
```bash
# Using the deployment script
bash tourism_frontend/deploy.sh

# Or with custom settings
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Running in Background
```bash
# Use screen session (current setup)
screen -dmS tourism_frontend bash -c "source .venv/bin/activate && streamlit run app.py --server.port 8501 --server.address 0.0.0.0"

# Check running sessions
screen -ls

# Attach to session
screen -r tourism_frontend
```

## 🔍 Troubleshooting

### Common Issues

#### API Connection Failed
```bash
# Check if API is running
curl http://localhost:8000/health

# Verify configuration
grep API_BASE_URL .env
```

#### ClickHouse Connection Issues
```bash
# Test ClickHouse connectivity
telnet localhost 8123

# Check ClickHouse container
docker ps | grep clickhouse
```

#### No Recommendations Shown
- Check user preferences are valid
- Verify filter settings aren't too restrictive
- Ensure ClickHouse has tourism data
- Try broadening search criteria

#### Performance Issues
- Clear Streamlit cache: Delete `.streamlit` folder
- Check available memory and CPU
- Verify ClickHouse query performance

## 📝 Dependencies

### Core Requirements
```
streamlit>=1.28.0      # Web framework
pandas>=1.5.0          # Data manipulation
plotly>=5.0.0          # Interactive charts
requests>=2.25.0       # API client
clickhouse-connect>=0.5.0  # Database connectivity
python-dotenv>=0.19.0  # Environment management
```

### Optional Features
```
numpy>=1.21.0          # Numerical computing
scikit-learn>=1.1.0    # ML utilities (if needed)
pillow>=8.0.0          # Image processing
```

## 🏁 Performance Metrics

### Application Performance
| Metric | Target | Typical |
|--------|--------|---------|
| Page Load Time | < 3s | 1-2s |
| API Response | < 500ms | 200-300ms |
| Database Query | < 1s | 300-500ms |
| Recommendation Generation | < 2s | 1s |

### Resource Usage
- **Memory**: ~200-400MB (typical)
- **CPU**: Low usage, spikes during data processing
- **Storage**: ~50MB app + data cache
- **Network**: Minimal, API calls only

## 🤝 Contributing

### Development Setup
```bash
# Clone and setup
git clone <repository-url>
cd tourism_frontend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run app.py
```

### Code Structure Guidelines
- Follow Streamlit best practices
- Use native components when possible
- Keep Indonesian cultural theme consistent
- Add comprehensive error handling
- Document all functions and components

### Contribution Areas
- UI/UX improvements
- New visualization components
- Performance optimizations
- Additional tourism categories
- Enhanced filtering options

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for the excellent web framework
- **ClickHouse** for high-performance analytics database
- **Plotly** for interactive data visualizations
- **Indonesian Tourism Ministry** for inspiration
- **Open Source Community** for tools and libraries

---

**🏝️ Discover Indonesia with AI-Powered Recommendations! 🎯**