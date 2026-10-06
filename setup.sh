#!/bin/bash

# Multi-Agent Gemma System - Setup Script

echo "=================================="
echo "Multi-Agent Gemma System Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Error: Python 3 not found"; exit 1; }

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys"
else
    echo ""
    echo "✓ .env file already exists"
fi

# Create results directory
mkdir -p results

echo ""
echo "=================================="
echo "✓ Setup complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GOOGLE_API_KEY or HF_TOKEN"
echo "2. Run the web interface: streamlit run app.py"
echo "3. Or run evaluation: python evaluation.py"
echo ""
