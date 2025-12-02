# Resume Analyzer - Quick Start Guide

## For Team Members: Keyur, Naveen, Vindhya

### Quick Setup (10 minutes)

#### 1. Prerequisites Check
```bash
# Check if you have these installed:
python3 --version   # Should be 3.11+
node --version      # Should be 18+
aws --version       # AWS CLI
sam --version       # SAM CLI

# If missing, install from:
# Python: https://www.python.org/downloads/
# Node.js: https://nodejs.org/
# AWS CLI: https://aws.amazon.com/cli/
# SAM CLI: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
```

#### 2. Configure AWS
```bash
aws configure
# Enter your AWS credentials
# Access Key ID: [your-key]
# Secret Access Key: [your-secret]
# Default region: us-east-1
# Output format: json
```

#### 3. Deploy to AWS
```bash
cd /Users/vindhyahegde/Desktop/cloud_proj

# Make script executable
chmod +x infrastructure/deploy.sh

# Deploy (takes ~5 minutes)
./infrastructure/deploy.sh

# Note the API endpoint from output!
```

#### 4. Setup Frontend
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_ENDPOINT=YOUR_API_URL_HERE" > .env
# Replace YOUR_API_URL_HERE with the URL from step 3

# Start development server
npm start
```

### Testing the Application

1. **Open Browser**: http://localhost:3000

2. **Test Flow**:
   - Upload a sample PDF resume
   - Paste a job description
   - Click "Analyze Resume"
   - View results!

### Sample Job Description for Testing
```
Software Engineer

We are seeking a Software Engineer with 3+ years of experience in Python, 
JavaScript, and cloud technologies. The ideal candidate will have:

Required Skills:
- Python, JavaScript, React
- AWS (Lambda, S3, DynamoDB)
- RESTful API development
- Git version control

Qualifications:
- Bachelor's degree in Computer Science
- Strong problem-solving skills
- Experience with serverless architectures

Responsibilities:
- Design and develop scalable applications
- Write clean, maintainable code
- Collaborate with cross-functional teams
```

### Troubleshooting

**Problem**: Lambda deployment fails
```bash
# Solution: Check if you have enough permissions
aws iam get-user
```

**Problem**: Frontend can't connect to API
```bash
# Solution: Check CORS and API endpoint
# Make sure .env has correct API URL
cat frontend/.env
```

**Problem**: PDF parsing not working
```bash
# Solution: Check PyMuPDF layer
cd cloud_proj
mkdir -p layers/pymupdf/python
pip install PyMuPDF -t layers/pymupdf/python/
```

### Project Demo Checklist

- [ ] Deploy backend to AWS
- [ ] Configure frontend with API endpoint
- [ ] Test with sample resume and job description
- [ ] Show compatibility score
- [ ] Demonstrate skill matching
- [ ] Show feedback sections
- [ ] Check CloudWatch logs
- [ ] View DynamoDB entries

### Architecture Diagram for Presentation

```
User Interface (React)
        ↓
    API Gateway
        ↓
    Lambda Functions
    ├── Resume Parser (NLP)
    ├── Score Calculator (TF-IDF)
    └── API Handler
        ↓
    ┌─────────┬──────────────┐
    ↓         ↓              ↓
   S3     DynamoDB    CloudWatch
(Storage) (Database)  (Monitoring)
```

### Key Features to Highlight

1. **Fully Serverless** - No servers to manage
2. **Scalable** - Handles 1 or 1000 requests
3. **Cost-Effective** - Pay per use (~$4/month for 1000 analyses)
4. **Real NLP** - TF-IDF and cosine similarity
5. **Modern Stack** - Python, React, AWS

### AWS Resources Created

- S3 Bucket: `resume-analyzer-{account-id}-dev`
- DynamoDB Table: `ResumeAnalysisResults-dev`
- Lambda Functions: 3 (parser, scorer, api-handler)
- API Gateway: REST API with CORS
- CloudWatch: Logs and monitoring
- IAM Roles: Least privilege access

### Cleanup (After Demo)

```bash
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name resume-analyzer-stack

# Delete S3 bucket (if needed)
aws s3 rb s3://resume-analyzer-{account-id}-dev --force

# Delete deployment bucket
aws s3 rb s3://resume-analyzer-deployment-{account-id} --force
```

### Presentation Tips

1. Start with architecture diagram
2. Demo the live application
3. Show AWS Console (Lambda, S3, DynamoDB)
4. Explain TF-IDF algorithm
5. Highlight serverless benefits
6. Discuss cost and scalability

Good luck with your presentation! 🚀
