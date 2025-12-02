#!/bin/bash

# Quick submission package creator
# Creates a clean zip file with source code for submission

set -e

echo "=== Creating Submission Package ==="
echo ""

# Configuration
PROJECT_ROOT="/Users/vindhyahegde/Desktop/cloud_proj"
OUTPUT_DIR="$PROJECT_ROOT/submission"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ZIP_NAME="Resume_Analyzer_SourceCode_${TIMESTAMP}.zip"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "📦 Preparing source code archive..."

# Create temporary directory for clean copy
TEMP_DIR=$(mktemp -d)
PACKAGE_DIR="$TEMP_DIR/Resume_Analyzer_SourceCode"
mkdir -p "$PACKAGE_DIR"

# Copy Lambda functions
echo "  ✓ Copying Lambda functions..."
mkdir -p "$PACKAGE_DIR/lambda"
cp -r "$PROJECT_ROOT/lambda/resume_parser" "$PACKAGE_DIR/lambda/"
cp -r "$PROJECT_ROOT/lambda/score_calculator" "$PACKAGE_DIR/lambda/"
cp -r "$PROJECT_ROOT/lambda/api_handler" "$PACKAGE_DIR/lambda/"

# Remove Python cache files
find "$PACKAGE_DIR/lambda" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR/lambda" -type f -name "*.pyc" -delete 2>/dev/null || true

# Copy frontend source code (excluding node_modules and build)
echo "  ✓ Copying frontend source code..."
mkdir -p "$PACKAGE_DIR/frontend"
cp -r "$PROJECT_ROOT/frontend/src" "$PACKAGE_DIR/frontend/"
cp -r "$PROJECT_ROOT/frontend/public" "$PACKAGE_DIR/frontend/"
cp "$PROJECT_ROOT/frontend/package.json" "$PACKAGE_DIR/frontend/" 2>/dev/null || true
cp "$PROJECT_ROOT/frontend/package-lock.json" "$PACKAGE_DIR/frontend/" 2>/dev/null || true

# Copy infrastructure files
echo "  ✓ Copying infrastructure files..."
cp "$PROJECT_ROOT/template.yaml" "$PACKAGE_DIR/"
cp "$PROJECT_ROOT/README.md" "$PACKAGE_DIR/" 2>/dev/null || true
cp "$PROJECT_ROOT/ARCHITECTURE.md" "$PACKAGE_DIR/" 2>/dev/null || true

# Copy deployment scripts
echo "  ✓ Copying deployment scripts..."
mkdir -p "$PACKAGE_DIR/scripts"
cp "$PROJECT_ROOT/scripts/deploy-secure.sh" "$PACKAGE_DIR/scripts/" 2>/dev/null || true

# Create README for submission
cat > "$PACKAGE_DIR/SUBMISSION_README.txt" << 'EOF'
AI-POWERED RESUME ANALYZER - SOURCE CODE SUBMISSION
===================================================

CONTENTS:
---------
1. lambda/                  - Backend Lambda functions
   - resume_parser/         - PDF parsing and skill extraction
   - score_calculator/      - TF-IDF matching and cover letter generation
   - api_handler/           - API Gateway request handler

2. frontend/                - React frontend application
   - src/                   - React components and logic
   - public/                - Static assets

3. template.yaml            - AWS SAM infrastructure template

4. scripts/                 - Deployment automation scripts

5. Documentation files:
   - README.md              - Project overview
   - ARCHITECTURE.md        - Architecture documentation

SETUP INSTRUCTIONS:
------------------
Backend Deployment:
1. Install AWS SAM CLI: brew install aws-sam-cli
2. Configure AWS credentials: aws configure
3. Deploy: sam build && sam deploy --guided

Frontend Deployment:
1. Install dependencies: cd frontend && npm install
2. Build: npm run build
3. Deploy: Run scripts/deploy-secure.sh

LIVE APPLICATION:
-----------------
Frontend: https://dx8h4r4ocvfti.cloudfront.net
API: https://s0ogqkfqaf.execute-api.us-east-1.amazonaws.com

TECHNOLOGIES USED:
------------------
- AWS Lambda (Python 3.11)
- Amazon S3, DynamoDB, API Gateway, CloudFront
- React 18.2.0
- PyMuPDF for PDF parsing
- NLP with TF-IDF similarity
- Infrastructure as Code with AWS SAM

PROJECT FEATURES:
-----------------
✓ PDF resume parsing and text extraction
✓ Pattern-based NLP skill extraction
✓ ATS compatibility scoring (0-100)
✓ Job description matching with TF-IDF
✓ Personalized cover letter generation
✓ Multi-job comparison with visualization
✓ Secure HTTPS deployment with CloudFront

CONTACT:
--------
[Add your name and email here]
Course: Cloud Computing - Final Project
Institution: UTSA
Date: December 2025
EOF

# Create archive
echo ""
echo "📦 Creating zip archive..."
cd "$TEMP_DIR"
zip -r "$OUTPUT_DIR/$ZIP_NAME" "Resume_Analyzer_SourceCode" -q

# Cleanup
rm -rf "$TEMP_DIR"

# Get file size
FILE_SIZE=$(du -h "$OUTPUT_DIR/$ZIP_NAME" | cut -f1)

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║       ✅ SUBMISSION PACKAGE CREATED!               ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "📦 Package: $ZIP_NAME"
echo "📍 Location: $OUTPUT_DIR/"
echo "📊 Size: $FILE_SIZE"
echo ""
echo "Contents:"
echo "  ✓ Lambda functions (3)"
echo "  ✓ Frontend React source"
echo "  ✓ SAM infrastructure template"
echo "  ✓ Deployment scripts"
echo "  ✓ Documentation"
echo ""
echo "Next steps:"
echo "  1. Extract and verify contents"
echo "  2. Convert FINAL_PROJECT_REPORT.md to IEEE Word format"
echo "  3. Record demo video using Panopto"
echo "  4. Submit all three deliverables"
echo ""
echo "Ready for submission! 🎓"
echo ""

# Open the output directory
open "$OUTPUT_DIR" 2>/dev/null || echo "Package created at: $OUTPUT_DIR"
