#!/bin/bash

# Scholarship Master Quick Start Script

set -e

echo "=================================="
echo "Scholarship Master - Quick Start"
echo "=================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python $(python3 --version) found"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠ .env file created. Please edit it with your configuration:"
    echo "  - GOOGLE_DRIVE_FOLDER_ID"
    echo "  - GOOGLE_SERVICE_ACCOUNT_JSON"
    echo "  - OPENAI_API_KEY (optional)"
    echo ""
    read -p "Press Enter once you've configured .env..."
fi

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your .env file with Google Drive and OpenAI credentials"
echo "2. Set up your Google Drive folder structure"
echo "3. Run the workflow: python main.py"
echo "4. Generate reports: python cli.py report summary"
echo ""
