#!/bin/bash
# Tourism Frontend Deployment Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

case "$1" in
    start)
        echo "Starting Tourism Frontend..."
        screen -dmS tourism_frontend bash -c "source .venv/bin/activate && source $HOME/.local/bin/env && streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
        sleep 3
        if screen -list | grep -q "tourism_frontend"; then
            echo "✅ Frontend started successfully!"
            echo "🌐 Access at: http://$(curl -s ifconfig.me):8501"
        else
            echo "❌ Failed to start frontend"
            exit 1
        fi
        ;;
    stop)
        echo "Stopping Tourism Frontend..."
        screen -S tourism_frontend -X quit
        echo "✅ Frontend stopped"
        ;;
    restart)
        echo "Restarting Tourism Frontend..."
        screen -S tourism_frontend -X quit 2>/dev/null
        sleep 2
        screen -dmS tourism_frontend bash -c "source .venv/bin/activate && source $HOME/.local/bin/env && streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
        sleep 3
        if screen -list | grep -q "tourism_frontend"; then
            echo "✅ Frontend restarted successfully!"
            echo "🌐 Access at: http://$(curl -s ifconfig.me):8501"
        else
            echo "❌ Failed to restart frontend"
            exit 1
        fi
        ;;
    status)
        echo "Checking Frontend Status..."
        if screen -list | grep -q "tourism_frontend"; then
            echo "✅ Frontend is running"
            echo "📊 Screen session:"
            screen -list | grep tourism_frontend
            echo "🌐 Access at: http://$(curl -s ifconfig.me):8501"
            echo "🔍 Port status:"
            ss -tlnp | grep :8501 || echo "Port 8501 not listening"
        else
            echo "❌ Frontend is not running"
        fi
        ;;
    logs)
        echo "Showing Frontend logs (press Ctrl+C to exit)..."
        screen -r tourism_frontend
        ;;
    *)
        echo "Tourism Frontend Deployment Manager"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the frontend application"
        echo "  stop    - Stop the frontend application"
        echo "  restart - Restart the frontend application"
        echo "  status  - Check application status"
        echo "  logs    - View application logs (interactive)"
        echo ""
        exit 1
        ;;
esac