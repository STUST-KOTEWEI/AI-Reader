#!/bin/bash

# Run all tests for Project-HOLO

echo "🧪 Running Project-HOLO Tests..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Track overall status
FAILED=0

# Run Python backend tests
echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  Running Backend Tests (Python/Pytest)${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo ""

if python -m pytest tests/ -v --tb=short; then
    echo -e "${GREEN}✅ Backend tests passed${NC}"
else
    echo -e "${RED}❌ Backend tests failed${NC}"
    FAILED=1
fi

# Run Frontend tests
echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  Running Frontend Tests (Vitest)${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo ""

cd web/frontend
if npm test -- --run; then
    echo -e "${GREEN}✅ Frontend tests passed${NC}"
else
    echo -e "${RED}❌ Frontend tests failed${NC}"
    FAILED=1
fi
cd "$PROJECT_ROOT"

# Summary
echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  Test Summary${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
