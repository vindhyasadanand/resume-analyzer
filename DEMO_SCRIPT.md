# Project Demo Script (10+ Minutes)
## AI-Powered Resume Analyzer - Cloud Computing Final Project

**Total Duration:** 12-15 minutes  
**Recording Tool:** UTSA Panopto (https://odl.utsa.edu/digital-tools/content-creation/panopto/)

---

## SETUP BEFORE RECORDING

1. **Prepare Materials:**
   - ✅ 2-3 sample PDF resumes ready to upload
   - ✅ 2-3 sample job descriptions copied to clipboard/notepad
   - ✅ Browser tabs open:
     - Frontend: https://dx8h4r4ocvfti.cloudfront.net
     - AWS Console: CloudFormation, Lambda, S3, DynamoDB
   - ✅ Architecture diagram visible (can use VISUAL_ARCHITECTURE.txt)

2. **Technical Setup:**
   - ✅ Close unnecessary applications
   - ✅ Clear browser cache/cookies for clean demo
   - ✅ Enable "Do Not Disturb" to avoid notifications
   - ✅ Test microphone and screen recording
   - ✅ Have a glass of water nearby

3. **Panopto Setup:**
   - Log in to UTSA Panopto
   - Click "Create" → "Record New Session"
   - Enable: Primary Screen + Webcam (optional)
   - Test audio levels
   - Click "Record" when ready

---

## DEMO SCRIPT

### PART 1: Introduction & Overview (2 minutes)

**[Show yourself on camera or start with title slide]**

"Hello, my name is [Your Name], and today I'll be demonstrating our Cloud Computing final project: an AI-Powered Resume Analyzer built on AWS infrastructure.

**[Switch to architecture diagram or draw on whiteboard]**

This application helps job seekers optimize their resumes by:
1. Parsing PDF resumes and extracting skills and experience
2. Calculating ATS (Applicant Tracking System) compatibility scores
3. Matching resumes against job descriptions with percentage scores
4. Generating personalized cover letters
5. Comparing multiple job opportunities side-by-side

**[Show architecture diagram]**

The system uses a serverless architecture with these AWS components:
- **Frontend:** React application hosted on S3 with CloudFront CDN for global distribution
- **API Layer:** API Gateway routing requests to Lambda functions
- **Compute:** Three Lambda functions - Resume Parser, Score Calculator, and API Handler
- **Storage:** S3 for resume files, DynamoDB for analysis results
- **Security:** CloudFront Origin Access Identity for secure S3 access, presigned URLs for uploads

The entire infrastructure is deployed using AWS SAM (Serverless Application Model) for Infrastructure as Code.

Now let me show you the live application."

---

### PART 2: Application Demo - Basic Analysis (3 minutes)

**[Navigate to: https://dx8h4r4ocvfti.cloudfront.net]**

"Here's our live application running on CloudFront. You can access it from anywhere in the world over HTTPS.

**[Show the main interface]**

The interface is clean and intuitive. Let me walk you through a typical user workflow:

**Step 1: Upload Resume**

[Click on file upload area or drag-and-drop a sample PDF]

'I'm uploading a sample software engineer resume. Notice the file is validated - we only accept PDF files up to 5MB.'

[Wait for upload confirmation - should be instant]

'The resume is securely uploaded to our S3 bucket using presigned URLs, which means the file goes directly from the browser to S3 without touching our Lambda functions.'

**Step 2: Enter Job Description**

[Paste a software engineer job description into the text area]

'Now I'm entering a job description for a Senior Software Engineer position. This is from a real job posting requiring skills like Python, AWS, React, and Docker.'

[Click 'Analyze Resume']

'When I click Analyze, here's what happens behind the scenes:
1. API Gateway receives the request
2. The Resume Parser Lambda extracts text from the PDF using PyMuPDF
3. It identifies skills, education, and experience using regex patterns and NLP
4. The Score Calculator Lambda computes TF-IDF similarity between resume and job description
5. It calculates ATS compatibility score with specific feedback
6. Results are stored in DynamoDB and returned to the frontend

This typically takes 2-4 seconds...'

**[Wait for results to load]**

'And here are our results!'

---

### PART 3: Results Explanation (3 minutes)

**[Show the Results Dashboard]**

**ATS Score Section:**

'First, we see the ATS Compatibility Score - this one is 78 out of 100, which is in the GOOD range. 

[Point to the score visualization]

The score is color-coded:
- Green (80-100): Excellent
- Yellow (60-79): Good  
- Orange (40-59): Fair
- Red (below 40): Poor

Below the score, we provide specific feedback on what affects the ATS score. For example, this resume scores well because it:
- Has a dedicated Skills section
- Includes relevant keywords
- Has good formatting

If the score were lower, we'd see actionable suggestions like "Add a Skills section" or "Include more technical keywords".'

**Skills Match Section:**

[Scroll to Skills Coverage graph]

'Next, we have the Skills Coverage visualization. This bar chart shows:
- Matched skills: Technical skills from the resume that appear in the job description
- Unmatched skills: Skills in the resume not relevant to this specific job

This helps candidates understand which of their skills align with the job requirements.

The percentage here - 65% - means 65% of this candidate's skills match what the job requires.'

**Missing Keywords Section:**

[Show the missing keywords list]

'This section is particularly valuable. It lists technical keywords and skills from the job description that are NOT found in the resume.

Notice these are all technical terms - Python, Docker, Kubernetes, CI/CD. Our algorithm uses pattern-based NLP to filter out soft skills and business jargon, focusing only on concrete technical skills.

This is powered by linguistic pattern recognition that identifies:
- CamelCase terms (e.g., JavaScript)
- Hyphenated tech terms (e.g., CI/CD)
- Version numbers (e.g., Python3)
- And filters out gerunds, abstract nouns, and action verbs

This approach scales automatically - no need to maintain hardcoded lists of technologies.'

**Cover Letter Section:**

[Scroll to cover letter]

'Finally, we automatically generate a personalized cover letter. 

[Show the letter content]

Notice how it:
- Mentions specific matched skills (Python, AWS, React)
- Acknowledges growth areas (Docker, Kubernetes)
- Uses a professional tone
- Is completely editable

Users can edit it directly in the interface, copy to clipboard, or download as a PDF using the buttons below.'

---

### PART 4: Multi-Job Comparison (2 minutes)

**[Navigate to Job Comparison tab/section]**

'One of our most powerful features is the ability to compare multiple job opportunities side-by-side.

[Show the Job Comparison interface]

Let me add three different job descriptions:

[Paste Job 1: Senior Software Engineer]
[Paste Job 2: DevOps Engineer]  
[Paste Job 3: Full Stack Developer]

[Click "Compare All Jobs"]

'The system now analyzes the same resume against all three jobs simultaneously...'

[Wait for results - should be 5-8 seconds for 3 jobs]

'Here are the results!

[Show the bar chart]

The visual comparison makes it immediately clear which opportunities are the best fit:
- Job 1 (Senior Software Engineer): 75% match - Excellent fit
- Job 3 (Full Stack Developer): 68% match - Good fit
- Job 2 (DevOps Engineer): 45% match - Fair match, needs skill development

[Show the ranking table]

The table provides more detail:
- **Match Score:** Overall compatibility percentage
- **Skills Match:** Ratio of resume skills that match each job (e.g., 6/8 means 6 out of 8 resume skills match)
- **Recommendation:** Color-coded advice on whether to apply

[Show the "Best Match" card below]

For the top-ranked job, we provide:
- **Strengths:** What makes this a good match
- **Improvement Tips:** How to strengthen the application

This feature helps candidates make data-driven decisions about where to focus their job search efforts.'

---

### PART 5: AWS Infrastructure Tour (2 minutes)

**[Switch to AWS Console]**

'Now let me show you the cloud infrastructure powering this application.

**CloudFormation Stack:**

[Navigate to CloudFormation → resume-analyzer-stack]

'Everything is deployed using Infrastructure as Code with AWS SAM. Here's our CloudFormation stack with all resources:

[Show the Resources tab]

- 3 Lambda functions (ResumeParser, ScoreCalculator, ApiHandler)
- S3 bucket for resume storage
- DynamoDB table for analysis results
- API Gateway REST API
- IAM roles with least-privilege policies
- Lambda layer for PyMuPDF library (77MB)

**Lambda Functions:**

[Click on one Lambda function, e.g., ResumeParserFunction]

'Here's the Resume Parser Lambda function:
- Runtime: Python 3.11
- Memory: 512 MB
- Timeout: 60 seconds
- Recent invocations: [show metrics if available]

[Show the Monitoring tab]

CloudWatch automatically tracks:
- Invocation count
- Duration (average 1-2 seconds)
- Error rate (should be near 0%)
- Throttles

**S3 Bucket:**

[Navigate to S3 → resume-analyzer-ACCOUNT_ID-dev]

'Here's our S3 bucket containing uploaded resumes. Notice:
- Encryption at rest is enabled (AES-256)
- Bucket is private (Block Public Access enabled)
- Files are organized by analysis ID

[Show one sample resume file]

Access is controlled via presigned URLs that expire after 5 minutes.'

**DynamoDB Table:**

[Navigate to DynamoDB → ResumeAnalysisResults-dev]

'Analysis results are stored in DynamoDB for quick retrieval:
- On-demand billing (pay per request)
- Auto-scaling as demand grows
- Millisecond query latency

[Show Items tab with sample items if available]

Each item contains:
- Analysis ID (partition key)
- Parsed resume data (skills, education, experience)
- Compatibility scores
- Generated feedback
- Timestamp

**CloudFront Distribution:**

[Navigate to CloudFront → dx8h4r4ocvfti.cloudfront.net]

'Our frontend is distributed globally via CloudFront CDN:
- HTTPS enabled with AWS-managed certificates
- Origin Access Identity secures S3 access (no public bucket needed)
- Edge locations worldwide for low latency
- Cache invalidation for instant updates

[Show the Origins tab]

Origin: resume-analyzer-frontend-ACCOUNT_ID.s3.amazonaws.com
Origin Access Identity: resume-analyzer-oai

This architecture respects AWS security best practices while providing fast, global access.'

---

### PART 6: Code Highlights (1 minute)

**[Switch to VS Code or show code snippets]**

'Let me quickly highlight some key implementation details:

**Pattern-Based Skill Detection:**

[Show or describe the is_likely_soft_skill_or_business_term function]

'Instead of hardcoded lists, we use linguistic patterns:
- Words ending in -ing, -tion, -ment are likely soft skills
- CamelCase words are likely technical (e.g., JavaScript)
- This scales automatically to new technologies'

**TF-IDF Similarity:**

[Show or describe the cosine_similarity function]

'We use Term Frequency-Inverse Document Frequency to calculate semantic similarity between resume and job description, not just keyword counting. This captures meaning, not just exact matches.'

**Dynamic ATS Scoring:**

[Show or describe the ATS checker logic]

'ATS scores are context-aware:
- Checks for Skills section existence
- Applies penalties based on skill count
- Provides specific, actionable feedback
- Scores vary by resume (not uniform)'

---

### PART 7: Conclusion & Lessons Learned (1 minute)

**[Return to yourself on camera or summary slide]**

'To summarize, we've built a production-ready, cloud-native application that:

**Technical Achievements:**
- ✅ Deployed on AWS with 99.9% uptime SLA
- ✅ Serverless architecture that scales automatically
- ✅ Sub-4-second response times for analysis
- ✅ Global CDN distribution with HTTPS
- ✅ Infrastructure as Code for reproducible deployments

**Key Learnings:**
1. **Serverless is powerful** - No server management, automatic scaling, pay-per-use
2. **Security first** - CloudFront OAI, presigned URLs, least-privilege IAM
3. **Pattern-based NLP scales better** than hardcoded lists
4. **Infrastructure as Code** makes deployment repeatable and version-controlled

**Future Improvements:**
- Machine Learning for improved skill extraction
- User authentication with AWS Cognito
- LinkedIn profile integration
- Interview question generation

**Impact:**
This tool democratizes access to resume optimization services, helping job seekers compete more effectively in today's market.

Thank you for watching this demonstration. The live application is available at https://dx8h4r4ocvfti.cloudfront.net, and all source code is available in our GitHub repository.

[End recording]

---

## POST-RECORDING CHECKLIST

1. ✅ Review the video for audio/visual quality
2. ✅ Trim any dead air at beginning/end
3. ✅ Add captions in Panopto (optional but recommended)
4. ✅ Set video privacy to "Unlisted" or "Public"
5. ✅ Copy the Panopto share link
6. ✅ Paste the link into Section X.B of the final report
7. ✅ Test the link in an incognito window to ensure access
8. ✅ Submit the report with working video link

---

## TROUBLESHOOTING TIPS

**If the application is slow:**
- Mention: "Lambda cold starts can add 2-3 seconds on first request"
- Solution: Keep talking while it loads, explain what's happening

**If there's an error:**
- Stay calm, say: "Let me show you our error handling"
- Open browser console to show error message
- Explain: "This is logged to CloudWatch for debugging"

**If you forget something:**
- Pause, say: "Let me also show you..."
- Panopto allows editing, so you can splice in additional footage

**If time is running short:**
- Skip the code highlights section
- Focus on the live demo and AWS infrastructure

**If time is running long:**
- Shorten the AWS Console tour
- Combine sections 2 and 3 (basic analysis + results)

---

**Recording Tips:**
- Speak clearly and at a moderate pace
- Pause briefly between sections for editing
- Use phrases like "as you can see here" when pointing to screen elements
- Show enthusiasm - you built something cool!
- Smile when on camera (if using webcam)

**Good luck with your demo!** 🚀
