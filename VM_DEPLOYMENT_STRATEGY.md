# Tourism API - VM Deployment Strategy
=====================================

## 🎯 Deployment Architecture

```
Your VM Infrastructure:
┌─────────────────────────────────────────┐
│             Your VM Server              │
├─────────────────────────────────────────┤
│  🗄️  MLflow Tracking Server             │
│  📊  Model Registry (with your models)   │
│  🗃️  MinIO/S3 (model artifacts)         │
│  🗂️  ClickHouse Database               │
├─────────────────────────────────────────┤
│  🚀  Tourism API (NEW - to deploy)      │
│      ├── FastAPI Application            │
│      ├── Model Loading & Inference      │
│      └── REST Endpoints                 │
└─────────────────────────────────────────┘
```

## 🔧 Why Deploy API on Same VM?

### ✅ **Advantages:**
- **Direct Model Access**: No network latency to MLflow registry
- **Shared Resources**: Same environment, databases, and configurations  
- **Security**: Models stay within your secure environment
- **Cost Effective**: No additional infrastructure needed
- **Performance**: Fastest possible model loading and predictions
- **Simple Management**: Single server to maintain

### 📦 **Architecture Benefits:**
- MLflow models are already available locally
- Same `.env` configuration works for everything
- Database connections already established
- No cross-server communication needed

## 🚀 Deployment Plan

### Step 1: Transfer API Files to VM
You'll need to copy these files to your VM:
- `tourism_api.py` - Main FastAPI application
- `api_requirements.txt` - API dependencies
- `start_api.sh` - Startup script
- `Dockerfile` + `docker-compose.yml` - Container deployment
- `test_api.py` - Testing suite

### Step 2: VM Environment Setup
```bash
# On your VM, install API dependencies
pip install fastapi uvicorn pydantic httpx

# Or use virtual environment
python3 -m venv tourism_api_env
source tourism_api_env/bin/activate
pip install -r api_requirements.txt
```

### Step 3: Configure API on VM
- API will automatically connect to your existing MLflow server
- Uses same `.env` file as your ML pipeline
- Models are already registered and available

### Step 4: Start API Service
```bash
# Start API alongside your existing services
uvicorn tourism_api:app --host 0.0.0.0 --port 8000
```

## 🌐 External Access Configuration

### Option 1: Direct VM Access (Simple)
If your VM has a public IP:
```
http://YOUR_VM_PUBLIC_IP:8000
```

### Option 2: Reverse Proxy (Recommended)
Add nginx configuration to your VM:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or VM IP
    
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 3: Cloud Load Balancer
Route external traffic through cloud load balancer to your VM.

## 🔐 Security Considerations

### Firewall Rules
```bash
# Allow API port (if not using reverse proxy)
sudo ufw allow 8000/tcp

# Or just allow HTTP/HTTPS (if using nginx)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### API Security
- API includes rate limiting (10 req/sec)
- Input validation on all endpoints
- CORS configured appropriately
- No sensitive data exposure

## 📊 Resource Requirements

### Additional VM Resources Needed:
- **CPU**: +1-2 cores for API processing
- **RAM**: +2-4GB for model inference
- **Storage**: +1GB for API code and dependencies
- **Network**: API will use existing bandwidth

### Performance Expectations:
- **Model Loading**: ~10-30 seconds (one-time)
- **Prediction Response**: ~100-500ms per request
- **Concurrent Users**: 50-100 (depending on VM specs)

## 🔄 Service Management

### Systemd Service (Recommended)
Create `/etc/systemd/system/tourism-api.service`:
```ini
[Unit]
Description=Tourism Recommendation API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/api
Environment=PATH=/path/to/venv/bin
ExecStart=/path/to/venv/bin/uvicorn tourism_api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable tourism-api
sudo systemctl start tourism-api
```

### Docker Deployment (Alternative)
```bash
# Build and run API container
docker build -t tourism-api .
docker run -d --name tourism-api -p 8000:8000 --env-file .env tourism-api
```

## 📈 Monitoring & Maintenance

### Health Monitoring
- Health endpoint: `http://vm-ip:8000/health`
- Model status included in health check
- Automatic model reloading capability

### Log Management
```bash
# API logs location
tail -f /var/log/tourism-api.log

# Or using journald
journalctl -u tourism-api -f
```

### Backup Strategy
- API code is stateless (easy to redeploy)
- Models are already backed up in MLflow
- Configuration in `.env` file

## 🎯 Next Steps

1. **Transfer Files**: Copy API files to your VM
2. **Install Dependencies**: Set up Python environment
3. **Configure Service**: Set up as systemd service
4. **Test Deployment**: Verify all endpoints work
5. **Configure Access**: Set up external access method
6. **Share with Friends**: Provide access details

This strategy leverages your existing VM infrastructure while adding powerful API capabilities to your ML models!