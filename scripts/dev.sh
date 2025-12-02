#!/bin/bash
# Local development and testing script

echo "=== Resume Analyzer Local Development ==="
echo ""

# Check prerequisites
check_prerequisites() {
    echo "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 not found. Please install Python 3.11+"
        exit 1
    fi
    echo "✅ Python $(python3 --version)"
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js not found. Please install Node.js 18+"
        exit 1
    fi
    echo "✅ Node.js $(node --version)"
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        echo "❌ AWS CLI not found. Please install AWS CLI"
        exit 1
    fi
    echo "✅ AWS CLI $(aws --version)"
    
    # Check SAM CLI
    if ! command -v sam &> /dev/null; then
        echo "❌ SAM CLI not found. Please install AWS SAM CLI"
        exit 1
    fi
    echo "✅ SAM CLI $(sam --version)"
    
    echo ""
}

# Install Lambda dependencies
install_lambda_deps() {
    echo "Installing Lambda dependencies..."
    
    for lambda_dir in lambda/*/; do
        if [ -f "${lambda_dir}requirements.txt" ]; then
            echo "📦 Installing for ${lambda_dir}"
            pip3 install -r "${lambda_dir}requirements.txt" -t "${lambda_dir}" --upgrade
        fi
    done
    
    echo "✅ Lambda dependencies installed"
    echo ""
}

# Install frontend dependencies
install_frontend_deps() {
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
    echo "✅ Frontend dependencies installed"
    echo ""
}

# Run tests
run_tests() {
    echo "Running tests..."
    
    # Test Python imports
    python3 -c "import boto3; print('✅ boto3 imported successfully')"
    
    # You can add more tests here
    echo ""
}

# Start local API
start_local_api() {
    echo "Starting local SAM API..."
    echo "API will be available at http://127.0.0.1:3001"
    echo "Press Ctrl+C to stop"
    echo ""
    sam local start-api --port 3001
}

# Start frontend dev server
start_frontend() {
    echo "Starting React development server..."
    cd frontend
    npm start
}

# Main menu
show_menu() {
    echo "What would you like to do?"
    echo "1) Check prerequisites"
    echo "2) Install all dependencies"
    echo "3) Install Lambda dependencies only"
    echo "4) Install frontend dependencies only"
    echo "5) Run local SAM API"
    echo "6) Start frontend dev server"
    echo "7) Run tests"
    echo "8) Exit"
    echo ""
    read -p "Enter choice [1-8]: " choice
    
    case $choice in
        1) check_prerequisites ;;
        2) install_lambda_deps && install_frontend_deps ;;
        3) install_lambda_deps ;;
        4) install_frontend_deps ;;
        5) start_local_api ;;
        6) start_frontend ;;
        7) run_tests ;;
        8) exit 0 ;;
        *) echo "Invalid choice"; show_menu ;;
    esac
}

# Run
show_menu
