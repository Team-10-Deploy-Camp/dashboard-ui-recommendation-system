# Tourism Recommendation API - Deployment Guide
===============================================

## 🎉 Successfully Deployed FastAPI Application

Your tourism recommendation API is now successfully deployed and running! Here's everything you need to know:

## 📋 What Was Built

### 1. **FastAPI Application** (`tourism_api.py`)
- Production-ready API with comprehensive error handling
- Automatic model loading from MLflow registry
- Input validation using Pydantic models
- CORS support for web applications
- Comprehensive logging and monitoring

### 2. **API Endpoints**

#### Core Endpoints:
- **GET** `/` - Root endpoint with API information
- **GET** `/health` - Health check and model status
- **GET** `/model/info` - Detailed model information
- **POST** `/predict` - Get rating predictions for places
- **POST** `/recommend` - Get top-K recommendations
- **GET** `/model/reload` - Reload model (admin endpoint)

#### Interactive Documentation:
- **GET** `/docs` - Swagger UI documentation
- **GET** `/redoc` - ReDoc documentation

### 3. **Model Integration**
- Automatically loads the best performing model: `tourism-advanced-hybrid-gb`
- Fallback to baseline model if MLflow models unavailable
- Real-time predictions with confidence scores
- Feature engineering pipeline integrated

### 4. **Deployment Files**
- `Dockerfile` - Container deployment
- `docker-compose.yml` - Multi-service orchestration
- `nginx.conf` - Production reverse proxy setup
- `start_api.sh` - Simple startup script

## 🚀 Current Status

✅ **API Server**: Running on http://localhost:8000
✅ **Model Loaded**: tourism-advanced-hybrid-gb (Advanced Hybrid Model)
✅ **Health Check**: Passing
✅ **Predictions**: Working correctly

## 📖 API Usage Examples

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Get Model Information
```bash
curl http://localhost:8000/model/info
```

### 3. Make Predictions
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "user": {
         "user_age": 28,
         "preferred_category": "museum",
         "budget_range": "medium"
       },
       "places": [
         {
           "place_id": "jakarta_001",
           "place_category": "museum",
           "place_city": "Jakarta",
           "place_price": 25000,
           "place_average_rating": 4.2,
           "place_visit_duration_minutes": 120,
           "place_description": "National history museum"
         }
       ]
     }'
```

### 4. Get Top Recommendations
```bash
curl -X POST "http://localhost:8000/recommend?top_k=3" \
     -H "Content-Type: application/json" \
     -d '{
       "user": {"user_age": 30},
       "places": [
         {
           "place_id": "place_001",
           "place_category": "temple",
           "place_city": "Yogyakarta",
           "place_price": 30000,
           "place_average_rating": 4.7,
           "place_visit_duration_minutes": 180
         },
         {
           "place_id": "place_002",
           "place_category": "museum",
           "place_city": "Yogyakarta", 
           "place_price": 20000,
           "place_average_rating": 4.3,
           "place_visit_duration_minutes": 120
         }
       ]
     }'
```

## 🛠️ Deployment Options

### Option 1: Direct Python Execution
```bash
# Start the API server
./start_api.sh

# Or manually:
source env/bin/activate
python3 tourism_api.py
```

### Option 2: Docker Deployment
```bash
# Build and run with Docker
docker build -t tourism-api .
docker run -p 8000:8000 --env-file .env tourism-api
```

### Option 3: Docker Compose (Production)
```bash
# Full production setup with nginx
docker-compose up -d
```

### Option 4: Uvicorn Server
```bash
# Production WSGI server
uvicorn tourism_api:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📊 Model Performance

The API automatically loads the **Advanced Hybrid Model** which showed the best performance:
- **Model Type**: Gradient Boosting with Enhanced Features
- **Features**: 22 engineered features including user preferences, place characteristics, and interaction features
- **Performance**: Optimized for recommendation accuracy

## 🔧 Configuration

### Environment Variables (.env)
```env
MLFLOW_TRACKING_URI=your_mlflow_server
AWS_ACCESS_KEY_ID=your_minio_access_key
AWS_SECRET_ACCESS_KEY=your_minio_secret_key
MLFLOW_S3_ENDPOINT_URL=your_minio_endpoint
```

### API Features
- **Rate Limiting**: 10 requests/second with burst capacity
- **CORS**: Configured for cross-origin requests
- **Input Validation**: Automatic request validation
- **Error Handling**: Comprehensive error responses
- **Health Monitoring**: Built-in health checks

## 🧪 Testing

### Automated Testing
```bash
# Run comprehensive test suite
source env/bin/activate
python3 test_api.py

# Or simple tests
python3 simple_api_test.py
```

### Manual Testing
- Visit http://localhost:8000/docs for interactive API documentation
- Use the built-in Swagger UI to test endpoints
- Monitor logs for debugging information

## 📈 Production Considerations

### Scaling
- Use multiple uvicorn workers for production
- Deploy behind a reverse proxy (nginx included)
- Consider horizontal scaling with load balancers

### Monitoring
- Health checks available at `/health`
- Detailed logging throughout the application
- Model performance metrics tracked

### Security
- Input validation with Pydantic models
- Rate limiting configured
- Environment variable configuration
- Non-root user in Docker container

## 🔍 API Response Examples

### Prediction Response
```json
{
  "predictions": [
    {
      "place_id": "jakarta_001",
      "predicted_rating": 4.12,
      "confidence_score": 0.847,
      "recommendation_rank": 1
    }
  ],
  "model_used": "tourism-advanced-hybrid-gb",
  "prediction_timestamp": "2025-08-13T00:05:43.123456",
  "total_places_evaluated": 1,
  "top_recommendation": {
    "place_id": "jakarta_001",
    "predicted_rating": 4.12,
    "confidence_score": 0.847,
    "recommendation_rank": 1
  }
}
```

## 🎯 Next Steps

1. **Production Deployment**: Deploy to cloud platform (AWS, GCP, Azure)
2. **Database Integration**: Connect to production database for real-time data
3. **Authentication**: Add user authentication if needed
4. **Caching**: Implement Redis for response caching
5. **Monitoring**: Set up application performance monitoring
6. **CI/CD**: Configure automated deployment pipeline

## 📞 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/model/info` | Model details |
| POST | `/predict` | Rating predictions |
| POST | `/recommend` | Top-K recommendations |
| GET | `/docs` | Interactive documentation |
| GET | `/redoc` | ReDoc documentation |

## ✨ Features Highlights

- **Best Model Loaded**: Automatically uses your best performing model
- **Production Ready**: Full error handling, logging, and validation
- **Interactive Docs**: Built-in Swagger UI for testing
- **Docker Support**: Complete containerization setup
- **Load Balancing**: Nginx configuration included
- **Performance**: Optimized for high-throughput predictions

Your Tourism Recommendation API is now ready for production use! 🎉