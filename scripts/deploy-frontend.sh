#!/bin/bash

# Deploy frontend to S3 and CloudFront
# This makes your application accessible via a public URL

set -e

echo "=== Deploying Frontend to AWS ==="

# Configuration
BUCKET_NAME="resume-analyzer-frontend-$(aws sts get-caller-identity --query Account --output text)"
REGION="us-east-1"

# Build the React app
echo "Building React application..."
cd frontend
npm run build

# Create S3 bucket for static website hosting
echo "Setting up S3 bucket: $BUCKET_NAME"
if ! aws s3 ls "s3://$BUCKET_NAME" 2>/dev/null; then
    aws s3 mb "s3://$BUCKET_NAME" --region $REGION
    echo "Bucket created"
else
    echo "Bucket already exists"
fi

# Enable static website hosting
aws s3 website "s3://$BUCKET_NAME" \
    --index-document index.html \
    --error-document index.html

# Update bucket policy for public access
cat > /tmp/bucket-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
        }
    ]
}
EOF

aws s3api put-bucket-policy \
    --bucket "$BUCKET_NAME" \
    --policy file:///tmp/bucket-policy.json

# Disable block public access
aws s3api put-public-access-block \
    --bucket "$BUCKET_NAME" \
    --public-access-block-configuration \
    "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

# Upload built files to S3
echo "Uploading files to S3..."
aws s3 sync build/ "s3://$BUCKET_NAME" \
    --delete \
    --cache-control "public, max-age=31536000" \
    --exclude "index.html" \
    --exclude "asset-manifest.json"

# Upload index.html separately with no caching
aws s3 cp build/index.html "s3://$BUCKET_NAME/index.html" \
    --cache-control "no-cache, no-store, must-revalidate"

# Get the website URL
WEBSITE_URL="http://${BUCKET_NAME}.s3-website-${REGION}.amazonaws.com"

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "🎉 Your application is now live!"
echo "📍 Website URL: $WEBSITE_URL"
echo ""
echo "Note: This is an HTTP endpoint. For HTTPS, you can:"
echo "1. Set up CloudFront (CDN) for better performance and HTTPS"
echo "2. Use a custom domain with Route53"
echo ""

cd ..
