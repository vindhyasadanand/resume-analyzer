#!/bin/bash

# Secure CloudFront deployment - bypasses Block Public Access restrictions
# Files stay private in S3, accessible only through CloudFront

set -e

echo "=== Deploying with CloudFront (Secure) ==="

# Configuration
BUCKET_NAME="resume-analyzer-frontend-$(aws sts get-caller-identity --query Account --output text)"
REGION="us-east-1"

# Build the React app
echo "Building React application..."
cd frontend
npm run build

# Create S3 bucket (stays private)
echo "Setting up private S3 bucket: $BUCKET_NAME"
if ! aws s3 ls "s3://$BUCKET_NAME" 2>/dev/null; then
    aws s3 mb "s3://$BUCKET_NAME" --region $REGION
    echo "✓ Bucket created"
else
    echo "✓ Using existing bucket"
fi

# Upload files (bucket remains private - CloudFront will access it)
echo "Uploading files..."
aws s3 sync build/ "s3://$BUCKET_NAME" --delete

# Create Origin Access Identity
echo "Setting up CloudFront access..."
OAI_LIST=$(aws cloudfront list-cloud-front-origin-access-identities --query "CloudFrontOriginAccessIdentityList.Items[?Comment=='resume-analyzer-oai']" --output json)
OAI_COUNT=$(echo $OAI_LIST | jq '. | length')

if [ "$OAI_COUNT" -eq "0" ]; then
    echo "Creating Origin Access Identity..."
    OAI_RESULT=$(aws cloudfront create-cloud-front-origin-access-identity \
        --cloud-front-origin-access-identity-config \
        CallerReference="resume-analyzer-$(date +%s)",Comment="resume-analyzer-oai")
    OAI_ID=$(echo $OAI_RESULT | jq -r '.CloudFrontOriginAccessIdentity.Id')
    echo "✓ Created OAI: $OAI_ID"
else
    OAI_ID=$(echo $OAI_LIST | jq -r '.[0].Id')
    echo "✓ Using existing OAI: $OAI_ID"
fi

# Get OAI Canonical User ID
OAI_CANONICAL=$(aws cloudfront get-cloud-front-origin-access-identity --id $OAI_ID --query 'CloudFrontOriginAccessIdentity.S3CanonicalUserId' --output text)

# Grant CloudFront OAI access to S3 bucket
echo "Granting CloudFront access to bucket..."
POLICY=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "CanonicalUser": "${OAI_CANONICAL}"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::${BUCKET_NAME}/*"
        }
    ]
}
EOF
)

echo "$POLICY" | aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file:///dev/stdin
echo "✓ Bucket policy configured"

# Check for existing distribution
DIST_ID=$(aws cloudfront list-distributions --query "DistributionList.Items[?Comment=='resume-analyzer-frontend'].Id" --output text 2>/dev/null || echo "")

if [ -n "$DIST_ID" ] && [ "$DIST_ID" != "None" ]; then
    echo "✓ Found existing distribution: $DIST_ID"
    DOMAIN=$(aws cloudfront get-distribution --id $DIST_ID --query 'Distribution.DomainName' --output text)
    
    echo "Invalidating cache..."
    aws cloudfront create-invalidation --distribution-id $DIST_ID --paths "/*" --query 'Invalidation.Id' --output text > /dev/null
    echo "✓ Cache invalidated"
else
    echo "Creating CloudFront distribution..."
    
    DIST_CONFIG=$(cat <<EOF
{
    "CallerReference": "resume-analyzer-$(date +%s)",
    "Comment": "resume-analyzer-frontend",
    "DefaultRootObject": "index.html",
    "Enabled": true,
    "Origins": {
        "Quantity": 1,
        "Items": [
            {
                "Id": "S3-resume-analyzer",
                "DomainName": "${BUCKET_NAME}.s3.amazonaws.com",
                "S3OriginConfig": {
                    "OriginAccessIdentity": "origin-access-identity/cloudfront/${OAI_ID}"
                }
            }
        ]
    },
    "DefaultCacheBehavior": {
        "TargetOriginId": "S3-resume-analyzer",
        "ViewerProtocolPolicy": "redirect-to-https",
        "AllowedMethods": {
            "Quantity": 2,
            "Items": ["GET", "HEAD"],
            "CachedMethods": {
                "Quantity": 2,
                "Items": ["GET", "HEAD"]
            }
        },
        "Compress": true,
        "ForwardedValues": {
            "QueryString": false,
            "Cookies": {"Forward": "none"}
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
    }
}
EOF
    )
    
    RESULT=$(aws cloudfront create-distribution --distribution-config "$DIST_CONFIG")
    DIST_ID=$(echo $RESULT | jq -r '.Distribution.Id')
    DOMAIN=$(echo $RESULT | jq -r '.Distribution.DomainName')
    STATUS=$(echo $RESULT | jq -r '.Distribution.Status')
    
    echo "✓ Distribution created: $DIST_ID"
fi

cd ..

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║       🚀 DEPLOYMENT SUCCESSFUL!            ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "🌐 Your site URL: https://$DOMAIN"
echo "📋 Distribution ID: $DIST_ID"
echo ""
echo "⏳ Status: Deploying (takes 15-20 minutes for new distributions)"
echo ""
echo "Check deployment status:"
echo "  aws cloudfront get-distribution --id $DIST_ID --query 'Distribution.Status'"
echo ""
echo "Once status shows 'Deployed', your site will be live!"
echo ""
