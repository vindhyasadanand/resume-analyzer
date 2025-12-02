# Serverless Resume Analyzer

A cloud-based resume analysis system built entirely on AWS serverless components that compares resumes against job descriptions and produces compatibility scores using NLP techniques.

## Team Members
- **Keyur Nareshkumar Modi**
- **Naveen John**
- **Vindhya Sadanand Hegde**

**Project Group:** 20

## 🎯 Project Overview

This serverless application analyzes resumes against job descriptions to provide:
- **Compatibility Score**: Overall match percentage using TF-IDF and cosine similarity
- **Skill Match Analysis**: Percentage of required skills found in the resume
- **Detailed Feedback**: Strengths, improvements, and missing keywords

### Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │─────▶│  API Gateway │─────▶│   Lambda    │
│  Frontend   │      │              │      │  Functions  │
└─────────────┘      └──────────────┘      └─────────────┘
                                                   │
                                                   ▼
                      ┌──────────────────────────────────┐
                      │                                  │
                  ┌───▼────┐    ┌──────────┐    ┌──────▼────┐
                  │   S3   │    │ DynamoDB │    │CloudWatch │
                  │ Bucket │    │  Table   │    │   Logs    │
                  └────────┘    └──────────┘    └───────────┘
```

## 🚀 Features

1. **Resume Upload**: Drag & drop interface for PDF and TXT files
2. **NLP Parsing**: Extracts skills, education, and experience from resumes
3. **Smart Analysis**: TF-IDF and cosine similarity algorithms for scoring
4. **Real-time Results**: Instant feedback with detailed recommendations
5. **Scalable**: Fully serverless architecture handles any load
6. **Cost-Effective**: Pay only for what you use

## 🛠️ Tech Stack

### AWS Services
- **S3**: Resume file storage with lifecycle policies
- **Lambda**: Three functions for parsing, scoring, and API handling
- **DynamoDB**: NoSQL database for analysis results
- **API Gateway**: REST API endpoints
- **CloudWatch**: Monitoring and logging
- **SAM**: Infrastructure as Code

### Programming & Libraries
- **Backend**: Python 3.11
  - `boto3`: AWS SDK
  - `PyMuPDF`: PDF text extraction
  - `scikit-learn concepts`: TF-IDF, cosine similarity (custom implementation)
- **Frontend**: React 18
  - `axios`: HTTP client
  - `react-dropzone`: File upload
  
## 📁 Project Structure

```
cloud_proj/
├── lambda/
│   ├── resume_parser/          # Extracts text and skills from resumes
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   ├── score_calculator/       # Calculates compatibility scores
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   └── api_handler/           # REST API endpoints
│       ├── lambda_function.py
│       └── requirements.txt
├── frontend/                   # React web application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js
│   │   │   ├── JobDescriptionInput.js
│   │   │   └── Results.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── infrastructure/
│   └── deploy.sh              # Deployment script
├── template.yaml              # AWS SAM template
└── README.md
```

## 🔧 Setup & Deployment

### Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials
3. **AWS SAM CLI** installed
4. **Python 3.11**
5. **Node.js 18+** and npm

### Installation Steps

#### 1. Clone and Navigate to Project

```bash
cd /Users/vindhyahegde/Desktop/cloud_proj
```

#### 2. Configure AWS Credentials

```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and default region
```

#### 3. Deploy Backend (AWS SAM)

```bash
# Make deployment script executable
chmod +x infrastructure/deploy.sh

# Run deployment
./infrastructure/deploy.sh
```

This script will:
- Create S3 deployment bucket
- Install Lambda dependencies
- Build PyMuPDF layer
- Package and deploy SAM application
- Output API endpoint URL

#### 4. Configure Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file with your API endpoint
echo "REACT_APP_API_ENDPOINT=YOUR_API_GATEWAY_URL" > .env
# Replace YOUR_API_GATEWAY_URL with the URL from SAM deployment output
```

#### 5. Run Frontend Locally

```bash
npm start
# Opens http://localhost:3000
```

#### 6. Build for Production (Optional)

```bash
npm run build
# Creates optimized production build in build/

# Deploy to S3 static website hosting
aws s3 sync build/ s3://your-frontend-bucket --acl public-read
```

## 📝 Usage

### 1. Upload Resume
- Drag and drop a PDF or TXT resume file
- Or click to browse and select a file

### 2. Enter Job Description
- Paste the complete job description
- Include skills, qualifications, and responsibilities

### 3. View Results
- **Compatibility Score**: Overall match percentage
- **Skill Match**: Percentage of skills aligned
- **Strengths**: What matches well
- **Improvements**: Areas to enhance
- **Missing Keywords**: Important terms to add

## 🧪 Testing

### Test Lambda Functions Locally

```bash
# Test Resume Parser
sam local invoke ResumeParserFunction -e test/events/parser_event.json

# Test Score Calculator
sam local invoke ScoreCalculatorFunction -e test/events/scorer_event.json
```

### Create Test Events

Create `test/events/parser_event.json`:
```json
{
  "body": "{\"bucket\": \"your-bucket\", \"key\": \"resumes/test.pdf\"}"
}
```

## 🔍 Algorithm Details

### Resume Parsing
- Extracts skills using pattern matching against skill database
- Identifies education with degree and institution patterns
- Parses experience using job title recognition

### Scoring Algorithm

1. **Tokenization**: Convert text to lowercase, remove stop words
2. **TF-IDF Calculation**:
   - TF (Term Frequency): `count(word) / total_words`
   - IDF (Inverse Document Frequency): `log(n_docs / (1 + docs_with_word))`
   - TF-IDF: `TF × IDF`
3. **Cosine Similarity**: 
   ```
   similarity = (vec1 · vec2) / (||vec1|| × ||vec2||)
   ```
4. **Final Score**: 
   ```
   score = (similarity × 0.6 + skill_match × 0.4) × 100
   ```

## 💰 Cost Estimation

For 1000 resume analyses per month:
- **Lambda**: ~$0.20 (with free tier)
- **S3**: ~$0.05 
- **DynamoDB**: ~$0.25 (on-demand)
- **API Gateway**: ~$3.50
- **Total**: ~$4.00/month

## 🔐 Security Features

- S3 bucket encryption at rest
- Private S3 bucket with presigned URLs
- IAM roles with least privilege
- CORS configured for frontend domain
- API Gateway request validation

## 📊 Monitoring

CloudWatch automatically tracks:
- Lambda invocation counts and duration
- API Gateway requests and latency
- DynamoDB read/write capacity
- Error rates and logs

Access logs:
```bash
aws logs tail /aws/lambda/resume-parser-dev --follow
```

## 🐛 Troubleshooting

### Lambda Timeout
- Increase timeout in `template.yaml` (default: 300s)
- Optimize PDF parsing for large files

### Deployment Fails
- Check AWS credentials: `aws sts get-caller-identity`
- Verify SAM CLI: `sam --version`
- Ensure unique S3 bucket names

### CORS Errors
- Update API endpoint in frontend `.env` file
- Check API Gateway CORS configuration

## 🚧 Future Enhancements

- [ ] Support for DOCX files
- [ ] Multi-language resume support
- [ ] ATS keyword optimization
- [ ] Resume formatting suggestions
- [ ] Historical analysis tracking
- [ ] Email notifications
- [ ] Integration with job boards

## 📚 References

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [TF-IDF Algorithm](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)

## 📄 License

This project is created for educational purposes as part of a cloud computing course.

## 👥 Contact

For questions or issues:
- Keyur Modi
- Naveen John  
- Vindhya Hegde

---

**Built with ❤️ using AWS Serverless Technologies**
