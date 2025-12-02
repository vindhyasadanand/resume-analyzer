# Architecture Documentation

## System Architecture

### High-Level Overview

The Resume Analyzer is built using AWS serverless architecture, consisting of three main layers:

1. **Presentation Layer**: React-based web application
2. **API Layer**: API Gateway with Lambda integration
3. **Data Layer**: S3 for storage, DynamoDB for persistence

### Component Details

#### 1. Frontend (React Application)

**Location**: `/frontend`

**Components**:
- `FileUpload.js`: Handles resume file selection with drag-and-drop
- `JobDescriptionInput.js`: Text area for job description input
- `Results.js`: Displays analysis results with visual feedback

**Flow**:
1. User uploads resume → Get presigned S3 URL
2. Upload file directly to S3
3. User enters job description
4. Trigger analysis via API
5. Display results

#### 2. API Gateway

**Endpoints**:
- `POST /upload`: Generate presigned URL for S3 upload
- `POST /analyze`: Trigger full resume analysis
- `GET /results/{analysis_id}`: Retrieve analysis results

**Features**:
- CORS enabled for frontend access
- Request/response validation
- Throttling and rate limiting

#### 3. Lambda Functions

##### Resume Parser Lambda
**Purpose**: Extract structured data from resume

**Input**:
```json
{
  "bucket": "resume-analyzer-bucket",
  "key": "resumes/2024/11/30/resume.pdf"
}
```

**Process**:
1. Download file from S3
2. Extract text (PDF or TXT)
3. Parse using regex patterns:
   - Skills: Match against skill database
   - Education: Degree and institution patterns
   - Experience: Years and job titles
4. Store results in DynamoDB

**Output**:
```json
{
  "analysis_id": "resume_20241130120000",
  "skills": ["python", "aws", "react"],
  "education": ["Bachelor of Computer Science"],
  "experience": {
    "years": 3,
    "positions": ["software engineer"]
  }
}
```

##### Score Calculator Lambda
**Purpose**: Calculate compatibility score

**Input**:
```json
{
  "analysis_id": "resume_20241130120000",
  "job_description": "We are seeking..."
}
```

**Process**:
1. Retrieve parsed resume from DynamoDB
2. Tokenize both resume and job description
3. Calculate TF-IDF vectors
4. Compute cosine similarity
5. Calculate skill match percentage
6. Generate feedback
7. Update DynamoDB with results

**Algorithm**:
```
TF(word) = count(word) / total_words
IDF(word) = log(n_docs / (1 + docs_with_word))
TF-IDF(word) = TF(word) × IDF(word)

cosine_similarity = (vec1 · vec2) / (||vec1|| × ||vec2||)

final_score = (similarity × 0.6 + skill_match × 0.4) × 100
```

**Output**:
```json
{
  "compatibility_score": 75.5,
  "skill_match": 68.2,
  "feedback": {
    "strengths": ["Strong skill set", "3+ years experience"],
    "improvements": ["Add more keywords"],
    "missing_keywords": ["docker", "kubernetes"]
  }
}
```

##### API Handler Lambda
**Purpose**: Orchestrate the analysis workflow

**Functions**:
- Generate presigned URLs for S3 uploads
- Invoke Resume Parser Lambda
- Invoke Score Calculator Lambda
- Handle errors and return responses

#### 4. Data Storage

##### S3 Bucket
**Purpose**: Store uploaded resume files

**Structure**:
```
resume-analyzer-{account-id}-dev/
└── resumes/
    └── 2024/
        └── 11/
            └── 30/
                └── {uuid}_resume.pdf
```

**Features**:
- Lifecycle policy: Delete after 90 days
- Server-side encryption
- CORS configuration for direct uploads
- Private bucket with presigned URLs

##### DynamoDB Table
**Purpose**: Store analysis results

**Schema**:
```
Table: ResumeAnalysisResults-dev
Partition Key: analysis_id (String)

Attributes:
- analysis_id: Unique identifier
- resume_key: S3 object key
- skills: List of skills found
- education: List of education entries
- experience: Object with years and positions
- score: Compatibility score
- feedback: Detailed feedback object
- job_description: Job description (truncated)
- parsed_at: Timestamp
- scored_at: Timestamp
- status: "parsed" | "completed"
```

**Access Pattern**:
- Get by analysis_id (primary lookup)
- No secondary indexes required

### Data Flow

#### Upload Flow
```
1. User selects file in browser
2. Frontend calls POST /upload
3. API Handler generates presigned S3 URL
4. Frontend uploads directly to S3
5. S3 triggers Resume Parser Lambda
6. Parser extracts data → saves to DynamoDB
7. Returns analysis_id to frontend
```

#### Analysis Flow
```
1. User enters job description
2. Frontend calls POST /analyze
3. API Handler invokes Resume Parser (if needed)
4. API Handler invokes Score Calculator
5. Calculator retrieves resume data from DynamoDB
6. Calculator computes scores
7. Calculator updates DynamoDB with results
8. API Handler returns results to frontend
```

#### Results Flow
```
1. Frontend displays results
2. Optional: User can retrieve results later via GET /results/{id}
3. API Handler queries DynamoDB
4. Returns complete analysis data
```

### Security Architecture

#### IAM Roles and Policies

**Lambda Execution Role**:
```yaml
Permissions:
  - S3: GetObject, PutObject
  - DynamoDB: GetItem, PutItem, UpdateItem
  - Lambda: InvokeFunction
  - CloudWatch: PutLogEvents
```

**Least Privilege**: Each Lambda has only necessary permissions

#### Data Security
- S3: Server-side encryption (AES-256)
- DynamoDB: Encryption at rest enabled
- API Gateway: HTTPS only
- Presigned URLs: 1-hour expiration

#### Network Security
- All resources in AWS VPC (optional)
- API Gateway: Regional endpoint
- CORS: Configured for specific origins

### Scalability

#### Auto-Scaling
- **Lambda**: Concurrent executions scale automatically
- **DynamoDB**: On-demand billing scales with traffic
- **S3**: Unlimited storage, auto-scales
- **API Gateway**: Scales automatically

#### Performance Considerations
- Lambda memory: 512 MB (adjustable)
- Lambda timeout: 300 seconds
- Cold start: ~2-3 seconds for first request
- Warm execution: ~100-200ms

#### Cost Optimization
- On-demand DynamoDB (no provisioned capacity)
- Lambda ephemeral storage: Default 512 MB
- S3 lifecycle policies: Delete old files
- CloudWatch log retention: 7 days

### Monitoring and Logging

#### CloudWatch Metrics
- Lambda invocations, duration, errors
- API Gateway requests, latency, 4xx/5xx errors
- DynamoDB read/write capacity
- S3 GET/PUT requests

#### CloudWatch Logs
- Lambda function logs
- API Gateway access logs
- Error traces and stack traces

#### Alerting (Optional)
- SNS topics for errors
- CloudWatch alarms for high error rates
- Email notifications

### Disaster Recovery

#### Backup Strategy
- DynamoDB: Point-in-time recovery enabled
- S3: Versioning disabled (resumes are transient)
- Lambda: Code stored in S3 deployment bucket

#### Recovery Procedures
- Redeploy from CloudFormation template
- Restore DynamoDB from backup
- Re-upload Lambda code from Git repository

### Future Enhancements

1. **Caching Layer**:
   - ElastiCache for frequently accessed results
   - CloudFront CDN for frontend

2. **Advanced Features**:
   - Step Functions for complex workflows
   - SQS for asynchronous processing
   - EventBridge for event-driven architecture

3. **ML Integration**:
   - SageMaker for advanced NLP models
   - Comprehend for entity extraction
   - Textract for better PDF parsing

4. **Multi-Region**:
   - Route 53 for DNS failover
   - S3 cross-region replication
   - DynamoDB global tables

### Technical Decisions

#### Why Serverless?
- Zero server management
- Pay-per-use pricing
- Automatic scaling
- Built-in high availability

#### Why DynamoDB over RDS?
- Faster for single-item lookups
- No connection limits
- Fully managed
- Better for serverless architecture

#### Why Custom TF-IDF vs SageMaker?
- Lower cost for simple use case
- Faster cold starts
- No model training required
- Sufficient accuracy for POC

#### Why React over Streamlit?
- More professional UI
- Better user experience
- Easier to customize
- Industry standard

---

*This architecture is designed for learning purposes and can be extended for production use with additional security, monitoring, and performance optimizations.*
