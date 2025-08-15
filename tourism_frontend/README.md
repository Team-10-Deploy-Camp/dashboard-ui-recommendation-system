# Tourism Indonesia - AI Recommendations Frontend

A modern, responsive Streamlit frontend for the Tourism Recommendation API that provides personalized tourism place recommendations in Indonesia using advanced machine learning.

## 🏝️ Features

- **Personalized Recommendations**: Get AI-powered suggestions based on your preferences
- **Multi-page Interface**: Home, Recommendations, Analytics, and About pages
- **Interactive Visualizations**: Charts and analytics dashboard with Plotly
- **Indonesian-themed Design**: Cultural design elements and color scheme
- **Responsive Layout**: Works on desktop and mobile devices
- **Real-time API Integration**: Connects to FastAPI backend
- **Error Handling**: Comprehensive error handling with fallback modes
- **Sample Data**: 50+ Indonesian tourism destinations included

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Access to the Tourism Recommendation API (running on localhost:8000 by default)

### Installation

1. Navigate to the frontend directory:
```bash
cd tourism_frontend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## 🎯 Usage

### Getting Recommendations

1. **Set Preferences**: Use the sidebar to specify:
   - Age (18-100)
   - Preferred category (Culture, Theme Parks, Nature, etc.)
   - Preferred city
   - Budget range (Low, Medium, High)
   - Number of recommendations (1-10)
   - Minimum rating filter
   - Maximum price filter

2. **Get Results**: Click "🔍 Get Recommendations" to receive personalized suggestions

3. **Explore**: View results in card or table format with:
   - Predicted ratings
   - Confidence scores
   - Place details and descriptions
   - Pricing and duration information

### Analytics Dashboard

Access detailed analytics including:
- Model performance metrics
- Rating distributions
- Price vs rating analysis
- Category preferences radar chart
- Confidence score visualizations

## 📁 Project Structure

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
├── data/
│   └── sample_places.json # Sample tourism places
├── requirements.txt       # Dependencies
├── config.py             # Configuration settings
└── README.md             # This file
```

## 🎨 Design Features

### Indonesian Cultural Theme

- **Colors**: Indonesian red (#C8102E), gold (#FFD700), ocean blue (#006994), nature green (#228B22)
- **Typography**: Modern sans-serif fonts with cultural hierarchy
- **Visual Elements**: Batik-inspired patterns and cultural icons
- **Layout**: Card-based design with shadows and hover effects

### User Experience

- **Progressive Disclosure**: Start simple, reveal more options as needed
- **Real-time Updates**: Live filtering and recommendation updates
- **Loading States**: Elegant progress bars and spinners
- **Error Handling**: Graceful degradation with helpful error messages
- **Responsive Design**: Mobile-friendly interface

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30
```

### Configuration Options

Edit `config.py` to customize:

- API endpoints and timeouts
- App title and branding
- Tourism categories and cities
- Color scheme and styling
- Sample data paths

## 🤖 API Integration

The frontend integrates with the Tourism Recommendation FastAPI backend:

### Endpoints Used

- `GET /health` - API health check
- `GET /model/info` - Model information
- `POST /predict` - Rating predictions
- `POST /recommend` - Top-K recommendations

### Error Handling

- **Connection Errors**: Graceful offline mode
- **Timeout Errors**: Retry mechanisms
- **Validation Errors**: Real-time input validation
- **Server Errors**: Fallback to basic recommendations

## 📊 Sample Data

Includes 50+ Indonesian tourism destinations:

### Categories
- **Budaya** (Culture): Temples, museums, heritage sites
- **Taman Hiburan** (Theme Parks): Amusement parks, entertainment
- **Cagar Alam** (Nature Reserves): National parks, natural attractions
- **Bahari** (Marine): Beaches, diving spots, coastal areas
- **Pusat Perbelanjaan** (Shopping): Malls, markets, retail
- **Tempat Ibadah** (Religious Sites): Mosques, temples, churches

### Cities Covered
Jakarta, Bali, Yogyakarta, Bandung, Surabaya, Medan, and more

## 🔍 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check if the FastAPI server is running
   - Verify the API_BASE_URL in config
   - Check network connectivity

2. **No Recommendations Returned**
   - Verify input preferences are valid
   - Check if places match your filters
   - Try broadening your criteria

3. **Styling Issues**
   - Ensure CSS file is loaded properly
   - Check browser compatibility
   - Clear browser cache

### Debug Mode

Enable debug information:
1. Set Streamlit to debug mode: `streamlit run app.py --logger.level=debug`
2. Use the "Debug Information" expander in the UI
3. Check browser developer console for errors

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Set environment variables in dashboard
4. Deploy with one click

### Local Production

```bash
# Install production dependencies
pip install -r requirements.txt

# Run with optimized settings
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is part of the Tourism Recommendation System. See the main project documentation for licensing information.

## 🏝️ About

Built with ❤️ for Indonesian Tourism • Powered by AI & Machine Learning

Discover the beauty of Indonesia with personalized recommendations!