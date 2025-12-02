# ⚡ Quick Reference Card - Resume Analyzer

## 🚀 Quick Deploy Commands

```bash
# Deploy Backend
cd /Users/vindhyahegde/Desktop/cloud_proj
./infrastructure/deploy.sh

# Setup Frontend
cd frontend
npm install
echo "REACT_APP_API_ENDPOINT=YOUR_API_URL" > .env
npm start
```

## 📍 Important URLs

| Resource | URL |
|----------|-----|
| Frontend | http://localhost:3000 |
| API Gateway | https://{api-id}.execute-api.us-east-1.amazonaws.com/dev |
| AWS Console Lambda | https://console.aws.amazon.com/lambda |
| AWS Console S3 | https://console.aws.amazon.com/s3 |
| AWS Console DynamoDB | https://console.aws.amazon.com/dynamodb |
| CloudWatch Logs | https://console.aws.amazon.com/cloudwatch |

## 🛠️ Common Commands

### AWS CLI
```bash
# Get API endpoint
aws cloudformation describe-stacks --stack-name resume-analyzer-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' --output text

# View Lambda logs
aws logs tail /aws/lambda/resume-parser-dev --follow

# List S3 buckets
aws s3 ls

# Query DynamoDB
aws dynamodb scan --table-name ResumeAnalysisResults-dev

# Check identity
aws sts get-caller-identity
```

### SAM CLI
```bash
# Validate template
sam validate

# Build application
sam build

# Deploy
sam deploy --guided

# Delete stack
sam delete
```

### Frontend
```bash
# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm run build

# Check for issues
npm audit
```

## 📂 Project Structure

```
cloud_proj/
├── lambda/               # Backend functions
│   ├── resume_parser/
│   ├── score_calculator/
│   └── api_handler/
├── frontend/            # React app
│   ├── src/
│   └── public/
├── template.yaml        # Infrastructure
└── docs/               # Documentation
```

## 🔧 Environment Variables

### Backend (Lambda)
```bash
DYNAMODB_TABLE=ResumeAnalysisResults-dev
S3_BUCKET=resume-analyzer-{account-id}-dev
PARSER_FUNCTION=resume-parser-dev
SCORER_FUNCTION=score-calculator-dev
```

### Frontend (React)
```bash
REACT_APP_API_ENDPOINT=https://xxx.execute-api.us-east-1.amazonaws.com/dev
```

## 📊 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /upload | Get presigned S3 URL |
| POST | /analyze | Analyze resume |
| GET | /results/{id} | Get results |
| OPTIONS | /* | CORS preflight |

## 🔍 Testing Endpoints

```bash
# Test upload endpoint
curl -X POST $API_URL/upload \
  -H "Content-Type: application/json" \
  -d '{"filename": "resume.pdf"}'

# Test analyze endpoint
curl -X POST $API_URL/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_key": "resumes/2024/11/30/resume.pdf",
    "job_description": "Software Engineer..."
  }'

# Test results endpoint
curl -X GET $API_URL/results/{analysis_id}
```

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Deployment fails | Check `aws sts get-caller-identity` |
| CORS errors | Update API endpoint in .env |
| Lambda timeout | Increase timeout in template.yaml |
| PDF parsing fails | Check PyMuPDF layer |
| DynamoDB errors | Verify table name and permissions |

## 💰 Cost Reference

| Service | Cost (1000 analyses/month) |
|---------|---------------------------|
| Lambda | $0.20 |
| S3 | $0.05 |
| DynamoDB | $0.25 |
| API Gateway | $3.50 |
| **Total** | **~$4.00** |

## 📝 Sample Job Description

```text
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

## 🔐 Security Checklist

- [x] S3 bucket encrypted
- [x] Private S3 access
- [x] HTTPS only API
- [x] IAM least privilege
- [x] DynamoDB encrypted
- [x] CloudWatch logging

## 🎯 Demo Script

1. **Show Architecture** (1 min)
   - Explain diagram
   - Highlight serverless

2. **Live Demo** (3 min)
   - Upload resume
   - Enter job description
   - Show results

3. **AWS Console** (2 min)
   - Lambda functions
   - S3 bucket
   - DynamoDB table
   - CloudWatch logs

4. **Q&A** (4 min)
   - Answer questions
   - Show code if asked

## 📞 Quick Help

### Documentation Files
- `README.md` - Main documentation
- `QUICKSTART.md` - Setup guide
- `CHECKLIST.md` - Deployment checklist
- `docs/ARCHITECTURE.md` - Architecture details
- `docs/API.md` - API documentation
- `docs/PRESENTATION_NOTES.md` - Demo guide

### AWS Resources Created
- S3: `resume-analyzer-{account-id}-dev`
- DynamoDB: `ResumeAnalysisResults-dev`
- Lambda: `resume-parser-dev`, `score-calculator-dev`, `api-handler-dev`
- API Gateway: `resume-analyzer-api-dev`

### Key Files
- `template.yaml` - Infrastructure definition
- `lambda/*/lambda_function.py` - Lambda code
- `frontend/src/App.js` - Main React app
- `infrastructure/deploy.sh` - Deployment script

## 🧹 Cleanup Commands

```bash
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name resume-analyzer-stack

# Delete S3 buckets
aws s3 rb s3://resume-analyzer-{account-id}-dev --force
aws s3 rb s3://resume-analyzer-deployment-{account-id} --force

# Verify deletion
aws cloudformation describe-stacks --stack-name resume-analyzer-stack
```

## 🎓 Team Info

**Project**: Serverless Resume Analyzer  
**Team**: Group 20  
**Members**: Keyur Modi, Naveen John, Vindhya Hegde  
**Tech Stack**: AWS (S3, Lambda, DynamoDB), Python, React  

---

**Keep this handy during development and demo! 🚀**
