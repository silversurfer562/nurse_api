#!/bin/bash

# Development startup script for Nurse AI Assistant API

echo "Starting Nurse AI Assistant API in development mode..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your API keys and configuration"
fi

# Run tests
echo "Running tests..."
python -m pytest tests/ -v

if [ $? -eq 0 ]; then
    echo "Tests passed! Starting the API server..."
    echo "API will be available at: http://localhost:8000"
    echo "API documentation: http://localhost:8000/docs"
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    # Start the server
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Tests failed! Please fix the issues before starting the server."
    exit 1
fi