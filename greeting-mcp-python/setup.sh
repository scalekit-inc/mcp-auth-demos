#!/bin/bash

# Python MCP Server Setup Script

echo "🐍 Setting up Python MCP Server..."

# Check if Python 3.11+ is available
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
else
    echo "❌ Error: Python 3.11+ is required but not found"
    echo "Please install Python 3.11 or 3.12"
    exit 1
fi

echo "✅ Using $PYTHON_CMD"

# Create virtual environment
echo "📦 Creating virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run the server:"
echo "  python main.py"
echo ""
echo "To deactivate:"
echo "  deactivate"
