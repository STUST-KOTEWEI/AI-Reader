#!/bin/bash

# Development server startup script for Project-HOLO

echo "🚀 Starting Project-HOLO Development Environment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
pip install -r web/backend/requirements.txt

echo -e "${YELLOW}📦 Installing Frontend dependencies...${NC}"
cd web/frontend
npm install
cd "$PROJECT_ROOT"

echo -e "${GREEN}✅ Dependencies installed${NC}"

# Start backend server
echo -e "${YELLOW}🖥️  Starting Backend Server...${NC}"
cd web/backend
API_PORT=${API_PORT:-8000}
python -m uvicorn main:app --reload --port $API_PORT &
BACKEND_PID=$!
cd "$PROJECT_ROOT"

# Wait for backend to start
sleep 3

# Start frontend server
echo -e "${YELLOW}🌐 Starting Frontend Server...${NC}"
cd web/frontend
npm run dev &
FRONTEND_PID=$!
cd "$PROJECT_ROOT"

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Project-HOLO Development Environment Started!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "  Backend API:  ${YELLOW}http://localhost:${API_PORT}${NC}"
echo -e "  Frontend App: ${YELLOW}http://localhost:5173${NC}"
echo -e "  API Docs:     ${YELLOW}http://localhost:${API_PORT}/docs${NC}"
echo ""
echo -e "  Press Ctrl+C to stop all servers"
echo ""

# Handle cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ Servers stopped${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for processes
wait
