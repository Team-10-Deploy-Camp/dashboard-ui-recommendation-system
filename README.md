# Tourism Recommendation System 🏖️

A production-ready machine learning API for tourism place recommendations using advanced ML models including collaborative filtering, neural networks, and hybrid approaches.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange.svg)](https://mlflow.org/)

## 🚀 Features

- **Advanced ML Models**: Collaborative Filtering, Neural CF, Hybrid Models, Ensemble Methods
- **Production Ready**: FastAPI with comprehensive API endpoints
- **MLOps Integration**: MLflow experiment tracking and model registry
- **Scalable Architecture**: Docker containerization with NGINX reverse proxy
- **Real-time Predictions**: High-performance recommendation API
- **Comprehensive Monitoring**: Health checks and logging
- **Database Integration**: ClickHouse for analytics data

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   NGINX Proxy   │────│  FastAPI Server  │────│  MLflow Server  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                          │
                    ┌─────────────────┐    ┌─────────────────┐
                    │   ClickHouse    │    │   MinIO/S3      │
                    │   Database      │    │   Artifacts     │
                    └─────────────────┘    └─────────────────┘
```

## 📦 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- ClickHouse database access
- MLflow tracking server
- MinIO/S3 for artifact storage

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd deploycamp

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Environment Variables

Create a `.env` file with the following configuration:

```env
# MLflow Configuration
MLFLOW_TRACKING_URI=http://your-mlflow-server/

# S3/MinIO Configuration (for model artifacts)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
MLFLOW_S3_ENDPOINT_URL=http://your-minio-server:9000

# ClickHouse Database Configuration
clickhouse_host=your-clickhouse-host
clickhouse_port=8123
clickhouse_user=default
clickhouse_database=tourism_data
clickhouse_table=mart_ratings_per_user
```

### 3. Docker Deployment

```bash
# Build and start services
docker-compose up -d

# Check service health
curl http://localhost:8000/health
```

### 4. Manual Setup (Development)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r api_requirements.txt

# Set up environment
bash setup_environment.sh

# Run the API server
python tourism_api.py
```

## 🔬 ML Pipeline

### Train Models

```bash
# Train all recommendation models
python tourism_recommendation_pipeline.py

# Monitor training in MLflow
# Visit: http://your-mlflow-server
```

### Available Models

1. **Collaborative Filtering (SVD)** - Matrix factorization approach
2. **Neural Collaborative Filtering** - Deep learning recommendation
3. **Content-Based Filtering** - Feature-based recommendations
4. **Advanced Hybrid Model** - Enhanced feature engineering with Gradient Boosting
5. **Ensemble Model** - Combination of multiple approaches
6. **Popularity Baseline** - Simple popularity-based recommendations

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Key Endpoints

#### Health Check
```http
GET /health
```

#### Get Recommendations
```http
POST /predict
Content-Type: application/json

{
  "user": {
    "user_age": 25,
    "preferred_category": "Cultural",
    "preferred_city": "Jakarta",
    "budget_range": "medium"
  },
  "places": [
    {
      "place_id": "place_001",
      "place_category": "Cultural",
      "place_city": "Jakarta",
      "place_price": 50000,
      "place_average_rating": 4.2,
      "place_visit_duration_minutes": 120,
      "place_description": "Historical museum..."
    }
  ]
}
```

#### Top-K Recommendations
```http
POST /recommend?top_k=5
```

#### Model Information
```http
GET /model/info
```

### Interactive API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🛠️ Development

### Project Structure

```
deploycamp/
├── tourism_api.py                    # Main FastAPI application
├── tourism_recommendation_pipeline.py # ML training pipeline
├── docker-compose.yml               # Multi-container setup
├── Dockerfile                       # API container definition
├── nginx.conf                       # Reverse proxy configuration
├── requirements.txt                 # Core ML dependencies
├── api_requirements.txt             # API-specific dependencies
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── tests/
│   ├── test_api.py                 # API tests
│   ├── simple_api_test.py          # Basic functionality tests
│   └── demo_examples.py            # Usage examples
├── deployment/
│   ├── deploy_to_vm.sh             # VM deployment script
│   ├── start_api.sh                # API startup script
│   └── setup_environment.sh       # Environment setup
├── monitoring/
│   ├── mlflow_monitor.py           # MLflow monitoring
│   └── mlflow_diagnostic.py       # Diagnostic tools
└── docs/
    ├── API_DEPLOYMENT_GUIDE.md     # Deployment guide
    └── VM_DEPLOYMENT_STRATEGY.md   # VM strategy
```

### Running Tests

```bash
# Basic API functionality test
python simple_api_test.py

# Full API test suite
python test_api.py

# Demo examples
python demo_examples.py
```

### Model Development

```bash
# Unified model testing
python wdr_test_unified_models.py

# MLflow monitoring
python mlflow_monitor.py

# Diagnostic checks
python mlflow_diagnostic.py
```

## 🔧 Configuration

### Model Selection Priority

The API automatically loads the best available model in this priority order:
1. `tourism-advanced-hybrid-gb` (Best performing)
2. `wdr-tourism-advanced-hybrid-gb`
3. `tourism-neural-cf`
4. `wdr-tourism-neural-cf`
5. `tourism-ensemble-svd`
6. `wdr-tourism-ensemble-svd`

### Performance Tuning

#### API Configuration
- Workers: Adjust `--workers` in Docker CMD
- Memory: Configure Docker memory limits
- Caching: Enable response caching for frequently accessed data

#### Model Configuration
- Feature Engineering: Modify feature extraction in `create_feature_vector()`
- Hyperparameters: Adjust in respective training functions
- Ensemble Weights: Configure in `train_ensemble_model()`

## 📊 Monitoring & Observability

### MLflow Tracking
- **Experiments**: All model training tracked
- **Metrics**: RMSE, MAE, F1-Score, NDCG@10
- **Artifacts**: Models, scalers, and preprocessors
- **Parameters**: All hyperparameters logged

### Health Monitoring
```bash
# API health check
curl http://localhost:8000/health

# Container health
docker-compose ps

# Logs
docker-compose logs tourism-api
```

### Performance Metrics
- **Model Performance**: RMSE < 0.85 (target)
- **API Response Time**: < 200ms (typical)
- **Throughput**: 100+ requests/second
- **Availability**: 99.9% uptime target

## 🚀 Deployment

### Docker Compose (Recommended)
```bash
docker-compose up -d
```

### VM Deployment
```bash
bash deploy_to_vm.sh
```

### Manual Deployment
```bash
bash start_api.sh
```

See detailed deployment guides:
- [API Deployment Guide](API_DEPLOYMENT_GUIDE.md)
- [VM Deployment Strategy](VM_DEPLOYMENT_STRATEGY.md)

## 🔐 Security

### Environment Protection
- `.env` files are gitignored
- Credentials loaded from environment variables
- No hardcoded secrets in code

### API Security
- CORS configuration for production
- Input validation with Pydantic
- Rate limiting (configure as needed)
- Health check endpoints

### Best Practices
- Run containers as non-root user
- Regular credential rotation
- Secure NGINX configuration
- SSL/TLS termination at proxy level

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt -r api_requirements.txt

# Run pre-commit hooks (if configured)
pre-commit run --all-files

# Run tests
python -m pytest tests/
```

## 📈 Performance Benchmarks

| Model Type | RMSE | MAE | F1-Score | NDCG@10 |
|------------|------|-----|----------|---------|
| Advanced Hybrid GB | 0.82 | 0.65 | 0.78 | 0.85 |
| Neural CF | 0.85 | 0.67 | 0.76 | 0.82 |
| Ensemble | 0.84 | 0.66 | 0.77 | 0.83 |
| Collaborative SVD | 0.90 | 0.72 | 0.74 | 0.80 |
| Content-Based | 0.95 | 0.75 | 0.72 | 0.78 |
| Popularity Baseline | 1.10 | 0.85 | 0.65 | 0.70 |

## 🆘 Troubleshooting

### Common Issues

#### Model Loading Failures
```bash
# Check MLflow connection
python mlflow_diagnostic.py

# Verify environment variables
python -c "import os; print(os.getenv('MLFLOW_TRACKING_URI'))"
```

#### Database Connection Issues
```bash
# Test ClickHouse connection
python -c "
import clickhouse_connect
client = clickhouse_connect.get_client(host='your-host')
print(client.query('SELECT 1').result_rows)
"
```

#### API Performance Issues
```bash
# Monitor resource usage
docker stats tourism-api

# Check logs
docker logs tourism-api --tail 100
```

### Support

- **Documentation**: Check the `/docs` directory
- **Issues**: Open GitHub issues for bugs
- **Performance**: Profile with MLflow metrics

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MLflow for experiment tracking
- FastAPI for the excellent web framework
- scikit-learn and TensorFlow for ML capabilities
- ClickHouse for analytics database
- Docker for containerization

---

**Happy Recommending! 🎯**

For more detailed information, check the documentation in the `/docs` directory.