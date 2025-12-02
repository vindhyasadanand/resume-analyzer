# API Documentation

## Base URL
```
https://{api-id}.execute-api.{region}.amazonaws.com/{stage}
```

Example:
```
https://abc123def.execute-api.us-east-1.amazonaws.com/dev
```

## Authentication
Currently, no authentication is required. For production, consider:
- API Keys
- AWS IAM authorization
- Cognito User Pools

## Endpoints

### 1. Upload Resume

Generate a presigned URL for uploading a resume to S3.

**Endpoint**: `POST /upload`

**Request Body**:
```json
{
  "filename": "john_doe_resume.pdf"
}
```

**Response** (200 OK):
```json
{
  "upload_url": "https://resume-analyzer-bucket.s3.amazonaws.com/resumes/...",
  "key": "resumes/2024/11/30/{uuid}_john_doe_resume.pdf",
  "bucket": "resume-analyzer-123456789012-dev"
}
```

**Usage**:
```javascript
// Step 1: Get presigned URL
const response = await axios.post(`${API_URL}/upload`, {
  filename: file.name
});

// Step 2: Upload file to S3
await axios.put(response.data.upload_url, file, {
  headers: { 'Content-Type': file.type }
});
```

**Errors**:
- `500`: Failed to generate upload URL

---

### 2. Analyze Resume

Trigger the full analysis workflow: parse resume and calculate compatibility score.

**Endpoint**: `POST /analyze`

**Request Body**:
```json
{
  "resume_key": "resumes/2024/11/30/{uuid}_resume.pdf",
  "job_description": "We are seeking a Software Engineer with 3+ years..."
}
```

**Parameters**:
- `resume_key` (string, required): S3 object key from upload response
- `job_description` (string, required): Complete job description text

**Response** (200 OK):
```json
{
  "message": "Analysis completed successfully",
  "analysis_id": "resume.pdf_20241130120000",
  "results": {
    "compatibility_score": 75.5,
    "skill_match": 68.2,
    "feedback": {
      "overall_score": 75.5,
      "skill_match_percentage": 68.2,
      "strengths": [
        "Strong overall match with job requirements",
        "Good skill set alignment",
        "3+ years of experience"
      ],
      "improvements": [
        "Consider tailoring your resume to better match the job description",
        "Add more relevant skills mentioned in the job description"
      ],
      "missing_keywords": [
        "docker",
        "kubernetes",
        "microservices",
        "ci/cd",
        "testing"
      ]
    }
  }
}
```

**Errors**:
- `400`: Missing required fields
- `500`: Resume parsing failed
- `500`: Score calculation failed

---

### 3. Get Analysis Results

Retrieve previously calculated analysis results.

**Endpoint**: `GET /results/{analysis_id}`

**Path Parameters**:
- `analysis_id` (string, required): Unique analysis identifier

**Example Request**:
```
GET /results/resume.pdf_20241130120000
```

**Response** (200 OK):
```json
{
  "analysis": {
    "analysis_id": "resume.pdf_20241130120000",
    "resume_key": "resumes/2024/11/30/{uuid}_resume.pdf",
    "skills": [
      "python",
      "javascript",
      "react",
      "aws",
      "lambda",
      "dynamodb",
      "rest api",
      "git"
    ],
    "education": [
      "Bachelor of Science in Computer Science",
      "University of Technology"
    ],
    "experience": {
      "years": 3,
      "positions": [
        "software engineer",
        "developer"
      ]
    },
    "score": 75.5,
    "feedback": { /* same as analyze response */ },
    "job_description": "We are seeking a Software Engineer...",
    "parsed_at": "2024-11-30T12:00:00.000Z",
    "scored_at": "2024-11-30T12:00:15.000Z",
    "status": "completed"
  }
}
```

**Errors**:
- `404`: Analysis not found

---

### 4. CORS Preflight

Handle OPTIONS requests for CORS.

**Endpoints**: 
- `OPTIONS /upload`
- `OPTIONS /analyze`

**Response** (200 OK):
```
Headers:
  Access-Control-Allow-Origin: *
  Access-Control-Allow-Headers: Content-Type,X-Amz-Date,Authorization,X-Api-Key
  Access-Control-Allow-Methods: GET,POST,OPTIONS
```

---

## Common Response Headers

All responses include:
```
Content-Type: application/json
Access-Control-Allow-Origin: *
```

## Error Response Format

All errors follow this format:
```json
{
  "error": "Error message",
  "details": "Detailed error information (optional)"
}
```

## Rate Limiting

Default AWS API Gateway limits:
- 10,000 requests per second
- 5,000 concurrent requests

Can be adjusted in API Gateway settings.

## Examples

### Complete Workflow Example (JavaScript)

```javascript
import axios from 'axios';

const API_URL = 'https://your-api-id.execute-api.us-east-1.amazonaws.com/dev';

async function analyzeResume(resumeFile, jobDescription) {
  try {
    // Step 1: Get upload URL
    const uploadResponse = await axios.post(`${API_URL}/upload`, {
      filename: resumeFile.name
    });
    
    const { upload_url, key } = uploadResponse.data;
    
    // Step 2: Upload resume to S3
    await axios.put(upload_url, resumeFile, {
      headers: {
        'Content-Type': resumeFile.type
      }
    });
    
    // Step 3: Analyze resume
    const analyzeResponse = await axios.post(`${API_URL}/analyze`, {
      resume_key: key,
      job_description: jobDescription
    });
    
    // Step 4: Get results
    const { results, analysis_id } = analyzeResponse.data;
    
    console.log('Analysis ID:', analysis_id);
    console.log('Compatibility Score:', results.compatibility_score);
    console.log('Feedback:', results.feedback);
    
    return results;
    
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    throw error;
  }
}

// Usage
const file = document.getElementById('file-input').files[0];
const jobDesc = document.getElementById('job-description').value;

analyzeResume(file, jobDesc)
  .then(results => {
    // Display results
  })
  .catch(error => {
    // Handle error
  });
```

### Python Example

```python
import requests
import json

API_URL = 'https://your-api-id.execute-api.us-east-1.amazonaws.com/dev'

def analyze_resume(resume_path, job_description):
    # Step 1: Get upload URL
    upload_response = requests.post(
        f'{API_URL}/upload',
        json={'filename': 'resume.pdf'}
    )
    upload_data = upload_response.json()
    
    # Step 2: Upload file
    with open(resume_path, 'rb') as f:
        requests.put(
            upload_data['upload_url'],
            data=f,
            headers={'Content-Type': 'application/pdf'}
        )
    
    # Step 3: Analyze
    analyze_response = requests.post(
        f'{API_URL}/analyze',
        json={
            'resume_key': upload_data['key'],
            'job_description': job_description
        }
    )
    
    results = analyze_response.json()
    return results

# Usage
results = analyze_resume(
    'path/to/resume.pdf',
    'Job description text...'
)

print(f"Score: {results['results']['compatibility_score']}")
```

### cURL Examples

```bash
# 1. Get upload URL
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/upload \
  -H "Content-Type: application/json" \
  -d '{"filename": "resume.pdf"}'

# 2. Upload file (use URL from step 1)
curl -X PUT "PRESIGNED_URL_HERE" \
  --upload-file resume.pdf \
  -H "Content-Type: application/pdf"

# 3. Analyze resume
curl -X POST https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_key": "resumes/2024/11/30/uuid_resume.pdf",
    "job_description": "We are seeking..."
  }'

# 4. Get results
curl -X GET https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/results/resume.pdf_20241130120000
```

## Testing

### Test with Sample Data

```bash
# Create test job description file
cat > job_description.txt << EOF
We are seeking a Software Engineer with 3+ years of experience in Python, 
AWS, React, and modern web development. Must have strong problem-solving 
skills and experience with cloud services, databases, and API development. 
Bachelor's degree in Computer Science or related field required.
EOF

# Test analyze endpoint
curl -X POST $API_URL/analyze \
  -H "Content-Type: application/json" \
  -d @- << EOF
{
  "resume_key": "resumes/test/sample_resume.pdf",
  "job_description": "$(cat job_description.txt)"
}
EOF
```

## Monitoring

Monitor API usage through AWS CloudWatch:

```bash
# Get API metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiName,Value=resume-analyzer-api-dev \
  --start-time 2024-11-30T00:00:00Z \
  --end-time 2024-11-30T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

---

## Support

For issues or questions, contact:
- Keyur Modi
- Naveen John
- Vindhya Hegde
