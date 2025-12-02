# Serverless Resume Analyzer
# CloudFormation deployment script

#!/bin/bash

# Configuration
STACK_NAME="resume-analyzer-stack"
ENVIRONMENT="dev"
REGION="us-east-1"
S3_DEPLOYMENT_BUCKET="resume-analyzer-deployment-$(aws sts get-caller-identity --query Account --output text)"

echo "=== Serverless Resume Analyzer Deployment ==="
echo "Stack Name: $STACK_NAME"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo ""

# Create deployment bucket if it doesn't exist
echo "Checking deployment bucket..."
if ! aws s3 ls "s3://$S3_DEPLOYMENT_BUCKET" 2>/dev/null; then
    echo "Creating deployment bucket: $S3_DEPLOYMENT_BUCKET"
    aws s3 mb "s3://$S3_DEPLOYMENT_BUCKET" --region $REGION
fi

# Install Lambda dependencies
echo ""
echo "Installing Lambda dependencies..."

for lambda_dir in lambda/*/; do
    if [ -f "${lambda_dir}requirements.txt" ]; then
        echo "Installing dependencies for ${lambda_dir}"
        pip install -r "${lambda_dir}requirements.txt" -t "${lambda_dir}" --upgrade
    fi
done

# Build Lambda layer for PyMuPDF
echo ""
echo "Building PyMuPDF layer..."
mkdir -p layers/pymupdf/python
pip install PyMuPDF==1.23.8 -t layers/pymupdf/python/ --upgrade

# Package SAM application
echo ""
echo "Packaging SAM application..."
sam package \
    --template-file template.yaml \
    --s3-bucket $S3_DEPLOYMENT_BUCKET \
    --output-template-file packaged.yaml \
    --region $REGION

# Deploy SAM application
echo ""
echo "Deploying SAM application..."
sam deploy \
    --template-file packaged.yaml \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides Environment=$ENVIRONMENT \
    --region $REGION \
    --no-fail-on-empty-changeset

# Get outputs
echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Stack Outputs:"
aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output table

echo ""
echo "API Endpoint:"
aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
    --output text
