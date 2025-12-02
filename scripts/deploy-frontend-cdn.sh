#!/bin/bash

# Deploy frontend to S3 with CloudFront CDN (HTTPS enabled)
# This provides a fast, secure, global CDN for your application

set -e

echo "=== Deploying Frontend with CloudFront CDN ==="

# Configuration
BUCKET_NAME="resume-analyzer-frontend-$(aws sts get-caller-identity --query Account --output text)"
REGION="us-east-1"

# Build the React app
echo "Building React application..."
cd frontend
npm run build

# Create S3 bucket
echo "Setting up S3 bucket: $BUCKET_NAME"
if ! aws s3 ls "s3://$BUCKET_NAME" 2>/dev/null; then
    aws s3 mb "s3://$BUCKET_NAME" --region $REGION
fi

# Upload files
echo "Uploading files to S3..."
aws s3 sync build/ "s3://$BUCKET_NAME" --delete

# Create CloudFront distribution (this will take 15-20 minutes)
echo "Creating CloudFront distribution..."
echo "Note: This process takes 15-20 minutes. Please wait..."

DISTRIBUTION_CONFIG=$(cat <<EOF
{
    "CallerReference": "resume-analyzer-$(date +%s)",
    "DefaultRootObject": "index.html",
    "Origins": {
        "Quantity": 1,
        "Items": [
            {
                "Id": "S3-${BUCKET_NAME}",
                "DomainName": "${BUCKET_NAME}.s3.amazonaws.com",
                "S3OriginConfig": {
                    "OriginAccessIdentity": ""
                }
            }
        ]
    },
    "DefaultCacheBehavior": {
        "TargetOriginId": "S3-${BUCKET_NAME}",
        "ViewerProtocolPolicy": "redirect-to-https",
        "AllowedMethods": {
            "Quantity": 2,
            "Items": ["GET", "HEAD"]
        },
        "ForwardedValues": {
            "QueryString": false,
            "Cookies": {
                "Forward": "none"
            }
        },
        "MinTTL": 0,
        "TrustedSigners": {
            "Enabled": false,
            "Quantity": 0
        }
    },
    "CustomErrorResponses": {
        "Quantity": 1,
        "Items": [
            {
                "ErrorCode": 404,
                "ResponsePagePath": "/index.html",
                "ResponseCode": "200",
                "ErrorCachingMinTTL": 300
            }
        ]
    },
    "Comment": "Resume Analyzer Frontend",
    "Enabled": true
}
EOF
)

# Check if distribution already exists
EXISTING_DIST=$(aws cloudfront list-distributions --query "DistributionList.Items[?Comment=='Resume Analyzer Frontend'].Id" --output text)

if [ -n "$EXISTING_DIST" ]; then
    echo "CloudFront distribution already exists: $EXISTING_DIST"
    DOMAIN=$(aws cloudfront get-distribution --id $EXISTING_DIST --query 'Distribution.DomainName' --output text)
else
    echo "$DISTRIBUTION_CONFIG" > /tmp/cf-config.json
    RESULT=$(aws cloudfront create-distribution --distribution-config file:///tmp/cf-config.json)
    DIST_ID=$(echo $RESULT | jq -r '.Distribution.Id')
    DOMAIN=$(echo $RESULT | jq -r '.Distribution.DomainName')
    
    echo "CloudFront distribution created: $DIST_ID"
fi

echo ""
echo "=== Deployment Initiated ==="
echo ""
echo "⏳ CloudFront distribution is deploying (takes 15-20 minutes)"
echo "📍 Your site will be available at: https://$DOMAIN"
echo ""
echo "You can check the status with:"
echo "aws cloudfront get-distribution --id \$DIST_ID"
echo ""

cd ..
