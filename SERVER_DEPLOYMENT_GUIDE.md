# 🚀 Tourism Frontend Server Deployment Guide

## Deployment Options

### Option 1: 🌟 **Streamlit Cloud (Recommended - Free)**

**Best for:** Quick deployment, free hosting, GitHub integration

#### Steps:

1. **Push your code to GitHub:**

   ```bash
   cd /home/hasbi/deploycamp
   git add .
   git commit -m "Tourism frontend ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**

   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set app path: `tourism_frontend/app.py`
   - Click "Deploy"

3. **Configure Environment:**
   - In Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add your environment variables:
   ```toml
   API_BASE_URL = "https://your-api-server.com"
   API_TIMEOUT = "30"
   ```

---

### Option 2: 🐳 **Docker (VPS/Cloud Server)**

**Best for:** Full control, any cloud provider, production deployment

#### Step 1: Create Dockerfile

```dockerfile
# Create this file: /home/hasbi/deploycamp/tourism_frontend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Step 2: Create requirements.txt

```bash
cd /home/hasbi/deploycamp/tourism_frontend
pip freeze > requirements.txt
```

#### Step 3: Build and run

```bash
docker build -t tourism-frontend .
docker run -p 8501:8501 tourism-frontend
```

---

### Option 3: 🖥️ **VPS with systemd (Linux Server)**

**Best for:** Your own VPS, full control, custom domain

#### Step 1: Server Setup

```bash
# On your server
sudo apt update
sudo apt install python3 python3-pip python3-venv git nginx
```

#### Step 2: Deploy Code

```bash
# On your server
cd /opt
sudo git clone https://github.com/yourusername/your-repo.git tourism-frontend
cd tourism-frontend/tourism_frontend
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt
```

#### Step 3: Create systemd service

```bash
# Create: /etc/systemd/system/tourism-frontend.service
sudo nano /etc/systemd/system/tourism-frontend.service
```

```ini
[Unit]
Description=Tourism Frontend Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/tourism-frontend/tourism_frontend
Environment=PATH=/opt/tourism-frontend/tourism_frontend/venv/bin
ExecStart=/opt/tourism-frontend/tourism_frontend/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable tourism-frontend
sudo systemctl start tourism-frontend
```

#### Step 4: Nginx Reverse Proxy

```bash
# Create: /etc/nginx/sites-available/tourism-frontend
sudo nano /etc/nginx/sites-available/tourism-frontend
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/tourism-frontend /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

### Option 4: ☁️ **Cloud Platforms**

#### **4a. Heroku**

1. **Install Heroku CLI**
2. **Create files:**

   ```bash
   # Procfile
   echo "web: streamlit run tourism_frontend/app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

   # runtime.txt
   echo "python-3.9.19" > runtime.txt
   ```

3. **Deploy:**
   ```bash
   heroku create your-tourism-app
   git push heroku main
   ```

#### **4b. Railway**

1. Go to https://railway.app/
2. Connect GitHub repository
3. Auto-deploys with zero configuration

#### **4c. Render**

1. Go to https://render.com/
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run tourism_frontend/app.py --server.port=$PORT --server.address=0.0.0.0`

---

## 🔧 **Deployment Preparation**

### Step 1: Create requirements.txt

```bash
cd /home/hasbi/deploycamp/tourism_frontend
echo "streamlit==1.48.1
pandas==2.3.1
plotly==6.3.0
requests==2.32.4
python-dotenv==1.0.0" > requirements.txt
```

### Step 2: Update config for production

```python
# Edit tourism_frontend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration - Updated for production
API_BASE_URL = os.getenv("API_BASE_URL", "https://your-api-domain.com")  # Change this!
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
```

### Step 3: Environment Variables

Create `.env` file for production:

```env
API_BASE_URL=https://your-ml-api-server.com
API_TIMEOUT=30
```

## 🌐 **Recommended Approach**

**For beginners:** Start with **Streamlit Cloud** (free, easy)
**For production:** Use **Docker + VPS** or **Cloud Platform**

### Quick Streamlit Cloud Deployment:

1. Push to GitHub
2. Connect at share.streamlit.io
3. Deploy in 2 clicks
4. Get public URL: `https://yourapp.streamlit.app`

## 🔒 **Security Considerations**

1. **Environment Variables:** Never commit API keys
2. **HTTPS:** Use SSL certificates (Let's Encrypt for free)
3. **Firewall:** Only open necessary ports
4. **Updates:** Keep dependencies updated

## 📊 **Monitoring**

After deployment, monitor:

- **App health:** Check if Streamlit is running
- **API connectivity:** Ensure your ML API is accessible
- **Performance:** Response times and resource usage

## 🆘 **Need Help?**

Choose your deployment method and I'll provide detailed step-by-step instructions for that specific option!

**Most Popular Options:**

1. **Streamlit Cloud** - Easiest, free
2. **Docker + DigitalOcean/AWS** - Most flexible
3. **Railway/Render** - Good middle ground
