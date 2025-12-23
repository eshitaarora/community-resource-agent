#!/bin/bash

# Community Resource Agent Setup Script
# This script sets up the complete development environment

echo "🚀 Community Resource Agent - Setup Script"
echo "==========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed."
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"
echo ""

# Setup Backend
echo -e "${BLUE}Setting up Backend...${NC}"
cd /private/tmp/community-resource-agent/backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python -m app.db.seed_data

echo -e "${GREEN}✓ Backend setup complete!${NC}"
echo ""

# Setup Frontend (instructions)
echo -e "${BLUE}Frontend Setup Instructions:${NC}"
echo "=============================="
echo ""
echo "Node.js is not installed on this system."
echo "To set up the frontend, you need to install Node.js:"
echo ""
echo "Option 1: Using curl (easiest)"
echo "  curl -fsSL https://fnm.io/install | bash"
echo "  fnm use --install-if-missing 18"
echo ""
echo "Option 2: Download from https://nodejs.org/ (LTS)"
echo ""
echo "After installing Node.js, run:"
echo "  cd /private/tmp/community-resource-agent/frontend"
echo "  npm install"
echo ""

# Summary
echo -e "${YELLOW}Setup Summary:${NC}"
echo "=============="
echo "✓ Python backend configured"
echo "✗ Node.js frontend (requires separate installation)"
echo ""
echo -e "${BLUE}To start the backend:${NC}"
echo "  cd /private/tmp/community-resource-agent/backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "The backend will run at: http://localhost:8000"
echo "API documentation: http://localhost:8000/docs"
echo ""
