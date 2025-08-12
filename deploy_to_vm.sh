#!/bin/bash

# Tourism API - VM Deployment Script
# ==================================

set -e

echo "🚀 Tourism API - VM Deployment Script"
echo "======================================"

# Configuration
VM_USER="your-vm-user"          # Replace with your VM username
VM_HOST="your-vm-ip"            # Replace with your VM IP address  
VM_PATH="/opt/tourism-api"      # Path on VM where API will be deployed
API_PORT="8000"                 # Port for the API

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if required files exist
echo "📋 Checking required files..."
required_files=(
    "tourism_api.py"
    "api_requirements.txt"
    "start_api.sh"
    "test_api.py"
    "Dockerfile"
    "docker-compose.yml"
    ".env"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "$file exists"
    else
        print_error "$file not found!"
        echo "Please ensure all required files are present before deployment."
        exit 1
    fi
done

# Get VM connection details from user
echo ""
echo "🔧 VM Configuration"
echo "==================="
read -p "Enter VM username: " VM_USER
read -p "Enter VM IP address: " VM_HOST
read -p "Enter deployment path (/opt/tourism-api): " input_path
VM_PATH=${input_path:-/opt/tourism-api}

echo ""
echo "📦 Preparing deployment package..."

# Create temporary deployment directory
TEMP_DIR=$(mktemp -d)
DEPLOY_DIR="$TEMP_DIR/tourism-api-deployment"
mkdir -p "$DEPLOY_DIR"

# Copy all necessary files
cp tourism_api.py "$DEPLOY_DIR/"
cp api_requirements.txt "$DEPLOY_DIR/"
cp start_api.sh "$DEPLOY_DIR/"
cp test_api.py "$DEPLOY_DIR/"
cp simple_api_test.py "$DEPLOY_DIR/"
cp Dockerfile "$DEPLOY_DIR/"
cp docker-compose.yml "$DEPLOY_DIR/"
cp nginx.conf "$DEPLOY_DIR/"
cp .env "$DEPLOY_DIR/"
cp VM_DEPLOYMENT_STRATEGY.md "$DEPLOY_DIR/"
cp API_DEPLOYMENT_GUIDE.md "$DEPLOY_DIR/"

# Create VM-specific installation script
cat > "$DEPLOY_DIR/install_on_vm.sh" << 'EOF'
#!/bin/bash

echo "🔧 Installing Tourism API on VM..."
echo "=================================="

# Update system packages
sudo apt update

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv curl nginx

# Create API user (optional, for security)
sudo useradd -r -s /bin/false -d /opt/tourism-api tourism-api || true

# Create application directory
sudo mkdir -p /opt/tourism-api
sudo chown $USER:$USER /opt/tourism-api

# Copy files to application directory
cp -r . /opt/tourism-api/
cd /opt/tourism-api

# Create virtual environment
python3 -m venv tourism_api_env
source tourism_api_env/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r api_requirements.txt

# Make scripts executable
chmod +x start_api.sh
chmod +x test_api.py

# Create systemd service file
sudo tee /etc/systemd/system/tourism-api.service > /dev/null << SERVICEEOF
[Unit]
Description=Tourism Recommendation API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/tourism-api
Environment=PATH=/opt/tourism-api/tourism_api_env/bin
ExecStart=/opt/tourism-api/tourism_api_env/bin/uvicorn tourism_api:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICEEOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable tourism-api

echo ""
echo "✅ Installation completed!"
echo "🚀 To start the API service:"
echo "   sudo systemctl start tourism-api"
echo ""
echo "📊 To check service status:"
echo "   sudo systemctl status tourism-api"
echo ""
echo "🔍 To test the API:"
echo "   python3 test_api.py"
echo ""
echo "🌐 API will be available at:"
echo "   http://$(curl -s ifconfig.me):8000"
echo "   http://localhost:8000 (from VM)"
EOF

chmod +x "$DEPLOY_DIR/install_on_vm.sh"

# Create quick start script
cat > "$DEPLOY_DIR/quick_start.sh" << 'EOF'
#!/bin/bash
echo "🚀 Quick Start - Tourism API"
echo "============================"

# Start the API service
sudo systemctl start tourism-api

# Wait for service to start
echo "Waiting for API to start..."
sleep 5

# Check if API is running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API is running successfully!"
    echo "🌐 Access your API at:"
    echo "   http://$(curl -s ifconfig.me):8000"
    echo "📚 Documentation: http://$(curl -s ifconfig.me):8000/docs"
else
    echo "❌ API failed to start. Check logs:"
    echo "   sudo journalctl -u tourism-api -f"
fi
EOF

chmod +x "$DEPLOY_DIR/quick_start.sh"

print_status "Deployment package prepared in $DEPLOY_DIR"

# Create deployment archive
cd "$TEMP_DIR"
tar -czf tourism-api-deployment.tar.gz tourism-api-deployment/
print_status "Created deployment archive: tourism-api-deployment.tar.gz"

echo ""
echo "📤 Deploying to VM..."
echo "===================="

# Test SSH connection
if ! ssh -o ConnectTimeout=5 "$VM_USER@$VM_HOST" "echo 'SSH connection successful'" > /dev/null 2>&1; then
    print_error "Cannot connect to $VM_USER@$VM_HOST"
    echo "Please check:"
    echo "- VM IP address is correct"
    echo "- SSH key is configured"
    echo "- VM is running and accessible"
    echo ""
    echo "Manual deployment option:"
    echo "1. Copy the archive: scp $TEMP_DIR/tourism-api-deployment.tar.gz $VM_USER@$VM_HOST:~/"
    echo "2. On VM: tar -xzf tourism-api-deployment.tar.gz"
    echo "3. On VM: cd tourism-api-deployment && ./install_on_vm.sh"
    exit 1
fi

# Copy deployment archive to VM
scp "$TEMP_DIR/tourism-api-deployment.tar.gz" "$VM_USER@$VM_HOST:~/"
print_status "Copied deployment archive to VM"

# Extract and install on VM
ssh "$VM_USER@$VM_HOST" << REMOTE_COMMANDS
    echo "📦 Extracting deployment archive..."
    tar -xzf tourism-api-deployment.tar.gz
    cd tourism-api-deployment
    
    echo "🔧 Installing Tourism API..."
    ./install_on_vm.sh
    
    echo "🚀 Starting API service..."
    sudo systemctl start tourism-api
    
    # Wait for service to start
    sleep 10
    
    echo "🔍 Checking API status..."
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ API deployed and running successfully!"
        VM_IP=\$(curl -s ifconfig.me)
        echo ""
        echo "🌐 Your API is now live at:"
        echo "   http://\$VM_IP:8000"
        echo "📚 Documentation: http://\$VM_IP:8000/docs"
        echo "🔍 Health Check: http://\$VM_IP:8000/health"
        echo ""
        echo "🎉 Deployment completed successfully!"
    else
        echo "❌ API deployment failed. Checking logs..."
        sudo journalctl -u tourism-api --no-pager -n 20
    fi
REMOTE_COMMANDS

# Clean up temporary files
rm -rf "$TEMP_DIR"
print_status "Cleaned up temporary files"

echo ""
echo "🎉 Deployment script completed!"
echo "==============================="
echo ""
echo "📋 Next Steps:"
echo "1. Test your API: ssh $VM_USER@$VM_HOST 'cd tourism-api-deployment && python3 test_api.py'"
echo "2. Check service status: ssh $VM_USER@$VM_HOST 'sudo systemctl status tourism-api'"
echo "3. View logs: ssh $VM_USER@$VM_HOST 'sudo journalctl -u tourism-api -f'"
echo "4. Share API details with your friends using the provided documentation"