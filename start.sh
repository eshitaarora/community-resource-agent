#!/bin/bash
# Quick Start Script - Community Resource Navigation AI Agent

echo "🚀 Starting Community Resource Navigation AI Agent"
echo "=================================================="
echo ""

# Set environment
export PATH="$HOME/.local/node/bin:$PATH"
PROJECT_DIR="/private/tmp/community-resource-agent"

# Check if backends already running
if pgrep -f "uvicorn app.main" > /dev/null; then
    echo "ℹ️  Backend is already running on port 8000"
else
    echo "📦 Starting backend server..."
    cd "$PROJECT_DIR/backend"
    source venv/bin/activate
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
    echo "✅ Backend started (http://localhost:8000)"
fi

echo ""

# Start frontend
if pgrep -f "npm run dev" > /dev/null; then
    echo "ℹ️  Frontend is already running on port 3000"
else
    echo "📦 Starting frontend server..."
    cd "$PROJECT_DIR/frontend"
    npm run dev > /tmp/frontend.log 2>&1 &
    echo "✅ Frontend started (http://localhost:3000)"
fi

echo ""
echo "=================================================="
echo "🎉 Application is ready!"
echo ""
echo "📍 Open your browser:"
echo "   http://localhost:3000"
echo ""
echo "📚 API Documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "🔍 Health Check:"
echo "   curl http://localhost:8000/health"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f /tmp/backend.log"
echo "   Frontend: tail -f /tmp/frontend.log"
echo ""
echo "💡 To stop servers: pkill -f 'uvicorn\|npm run dev'"
echo ""
