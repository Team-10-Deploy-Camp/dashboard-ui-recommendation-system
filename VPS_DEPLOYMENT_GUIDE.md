# 🚀 VPS Deployment Guide - Tourism Frontend

## Prerequisites

- ✅ VPS server (Ubuntu/Debian recommended)
- ✅ Custom domain pointing to your VPS IP
- ✅ SSH access to your server

## Step-by-Step Deployment

### Step 1: Prepare Your Code for Deployment

**On your local machine:**

```bash
cd /home/hasbi/deploycamp/tourism_frontend

# Create requirements.txt
echo "streamlit==1.48.1
pandas==2.3.1
plotly==6.3.0
requests==2.32.4
python-dotenv==1.0.0" > requirements.txt

# Update config for production
```

**Edit `config.py` for production:**

```python
# tourism_frontend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")  # Keep localhost if API is on same server
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# App Configuration
APP_TITLE = "Tourism Indonesia - AI Recommendations"
PAGE_ICON = "🏝️"
LAYOUT = "wide"
```

### Step 2: Upload Code to Your VPS

**Option A: Using git (recommended)**

```bash
# On your local machine - push to GitHub/GitLab first
git add .
git commit -m "Ready for production deployment"
git push origin main

# On your VPS
sudo mkdir -p /opt/tourism-frontend
cd /opt/tourism-frontend
sudo git clone https://github.com/yourusername/yourrepo.git .
# OR if private repo: sudo git clone https://username:token@github.com/user/repo.git .
```

**Option B: Using scp**

```bash
# On your local machine
scp -r /home/hasbi/deploycamp/tourism_frontend/ user@your-server-ip:/opt/tourism-frontend/
```

### Step 3: Server Setup

**SSH into your VPS:**

```bash
ssh user@your-server-ip
```

**Install dependencies:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and nginx
sudo apt install python3 python3-pip python3-venv nginx git -y

# Create application directory
sudo mkdir -p /opt/tourism-frontend
sudo chown $USER:$USER /opt/tourism-frontend
```

### Step 4: Setup Python Environment

```bash
cd /opt/tourism-frontend

# If you used git clone, navigate to the frontend directory
cd tourism_frontend  # or wherever your app.py is located

# Create virtual environment
python3 -m venv venv

# Activate and install requirements
source venv/bin/activate
pip install -r requirements.txt

# Test that the app works
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
# Ctrl+C to stop after testing
```

### Step 5: Create Environment File

```bash
# Create production environment file
nano /opt/tourism-frontend/tourism_frontend/.env
```

**Add your production settings:**

```env
# Production Environment
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30
DEBUG=False
```

### Step 6: Create Systemd Service

```bash
sudo nano /etc/systemd/system/tourism-frontend.service
```

**Service configuration:**

```ini
[Unit]
Description=Tourism Indonesia Frontend
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/tourism-frontend/tourism_frontend
Environment=PATH=/opt/tourism-frontend/tourism_frontend/venv/bin
ExecStart=/opt/tourism-frontend/tourism_frontend/venv/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1 --server.headless=true
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Set permissions and start service:**

```bash
# Set correct ownership
sudo chown -R www-data:www-data /opt/tourism-frontend

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable tourism-frontend
sudo systemctl start tourism-frontend

# Check status
sudo systemctl status tourism-frontend
```

### Step 7: Configure Nginx

**Create nginx configuration:**

```bash
sudo nano /etc/nginx/sites-available/tourism-frontend
```

**Nginx config (replace `your-domain.com`):**

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # Optional: Serve static files directly
    location /_stcore/static {
        proxy_pass http://127.0.0.1:8501/_stcore/static;
    }
}
```

**Enable the site:**

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/tourism-frontend /etc/nginx/sites-enabled/

# Test nginx config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### Step 8: Setup SSL Certificate (Free with Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### Step 9: Firewall Configuration

```bash
# Enable firewall
sudo ufw enable

# Allow SSH, HTTP, and HTTPS
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Check status
sudo ufw status
```

## 🔧 Management Commands

### Check Application Status

```bash
# Service status
sudo systemctl status tourism-frontend

# View logs
sudo journalctl -u tourism-frontend -f

# Restart service
sudo systemctl restart tourism-frontend
```

### Update Application

```bash
cd /opt/tourism-frontend
sudo git pull origin main
sudo systemctl restart tourism-frontend
```

### Monitor Performance

```bash
# Check memory usage
htop

# Check nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 🚀 Final Steps

1. **Test your deployment:**

   - Visit: `https://your-domain.com`
   - Test all functionality: Home, Recommendations, Maps, About

2. **Monitor the application:**

   ```bash
   sudo systemctl status tourism-frontend
   ```

3. **Check logs if issues:**
   ```bash
   sudo journalctl -u tourism-frontend -n 50
   ```

## 🔒 Security Hardening (Optional)

### Basic Security

```bash
# Update system regularly
sudo apt update && sudo apt upgrade

# Install fail2ban
sudo apt install fail2ban

# Configure firewall to only allow necessary ports
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
```

### Backup Strategy

```bash
# Create backup script
sudo nano /opt/backup-tourism.sh
```

```bash
#!/bin/bash
cd /opt/tourism-frontend
tar -czf /opt/backups/tourism-$(date +%Y%m%d).tar.gz .
```

## 🎯 Performance Tips for Small Users

Since you have small user amount, this setup will handle:

- ✅ **50-100 concurrent users easily**
- ✅ **Fast response times**
- ✅ **Automatic restarts if app crashes**
- ✅ **SSL encryption**
- ✅ **Easy updates via git pull**

## 🆘 Troubleshooting

**Common issues:**

1. **Service won't start:**

   ```bash
   sudo journalctl -u tourism-frontend -n 20
   ```

2. **Nginx 502 error:**

   ```bash
   # Check if streamlit is running
   sudo systemctl status tourism-frontend
   # Check port 8501
   sudo netstat -tlnp | grep 8501
   ```

3. **Domain not working:**
   - Check DNS settings point to your VPS IP
   - Verify nginx config: `sudo nginx -t`

**Your Tourism Frontend will be live at: `https://your-domain.com`** 🎉
