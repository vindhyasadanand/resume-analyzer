# 🚀 Deployment & Demo Checklist

## Team 20: Keyur Modi, Naveen John, Vindhya Hegde

---

## 📋 Pre-Deployment Checklist

### Environment Setup
- [ ] AWS Account created and accessible
- [ ] AWS CLI installed (`aws --version`)
- [ ] AWS SAM CLI installed (`sam --version`)
- [ ] Python 3.11+ installed (`python3 --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Git configured properly

### AWS Configuration
- [ ] AWS credentials configured (`aws configure`)
- [ ] Test AWS access (`aws sts get-caller-identity`)
- [ ] Verify region set to `us-east-1` (or your preferred region)
- [ ] Sufficient IAM permissions for deployment

### Local Setup
- [ ] Project cloned/downloaded to local machine
- [ ] Navigate to project directory: `cd /Users/vindhyahegde/Desktop/cloud_proj`
- [ ] All files present (check with `ls -la`)
- [ ] Scripts are executable (`chmod +x infrastructure/deploy.sh scripts/dev.sh`)

---

## 🔧 Backend Deployment Checklist

### Step 1: Prepare Deployment
- [ ] Review `template.yaml` configuration
- [ ] Check Lambda function code is ready
- [ ] Verify requirements.txt files exist in each Lambda folder

### Step 2: Run Deployment Script
```bash
cd /Users/vindhyahegde/Desktop/cloud_proj
./infrastructure/deploy.sh
```

- [ ] Script starts without errors
- [ ] Deployment bucket created
- [ ] Lambda dependencies installed
- [ ] PyMuPDF layer built
- [ ] SAM package successful
- [ ] SAM deploy successful
- [ ] Stack creation complete (wait 5-10 minutes)

### Step 3: Verify Backend Deployment
- [ ] CloudFormation stack status: `CREATE_COMPLETE`
- [ ] Note the API Gateway endpoint URL from output
- [ ] All 3 Lambda functions visible in AWS Console
- [ ] S3 bucket created
- [ ] DynamoDB table created

### Step 4: Test Backend
```bash
# Get the API endpoint
aws cloudformation describe-stacks \
  --stack-name resume-analyzer-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
  --output text

# Test upload endpoint
curl -X POST {YOUR_API_ENDPOINT}/upload \
  -H "Content-Type: application/json" \
  -d '{"filename": "test.pdf"}'
```

- [ ] API endpoint returns valid response
- [ ] Presigned URL generated successfully
- [ ] No CORS errors

---

## 💻 Frontend Setup Checklist

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

- [ ] All npm packages installed successfully
- [ ] No critical vulnerabilities
- [ ] `node_modules` folder created

### Step 2: Configure Environment
```bash
# Create .env file
echo "REACT_APP_API_ENDPOINT=YOUR_API_ENDPOINT_HERE" > .env
```

- [ ] `.env` file created
- [ ] API endpoint URL is correct (from backend deployment)
- [ ] No trailing slash in URL

### Step 3: Test Frontend Locally
```bash
npm start
```

- [ ] Development server starts on port 3000
- [ ] Browser opens automatically
- [ ] No console errors
- [ ] UI loads properly

### Step 4: Verify Frontend Functionality
- [ ] Can see upload area
- [ ] Can see job description textarea
- [ ] All CSS styles loaded
- [ ] Responsive on mobile view

---

## 🧪 End-to-End Testing Checklist

### Test 1: Upload Resume
- [ ] Click or drag-drop a PDF resume
- [ ] File appears in upload component
- [ ] File size shown correctly
- [ ] Can remove and re-upload

### Test 2: Full Analysis Flow
- [ ] Upload a sample resume
- [ ] Click "Upload & Continue"
- [ ] Progress indicator shows step 2
- [ ] Enter or paste job description
- [ ] Job description accepts text input
- [ ] Click "Analyze Resume"
- [ ] Loading indicator appears
- [ ] Results appear within 10 seconds

### Test 3: Results Validation
- [ ] Compatibility score displayed (0-100)
- [ ] Skill match percentage shown
- [ ] Strengths section populated
- [ ] Improvements section populated
- [ ] Missing keywords displayed
- [ ] Color coding correct (green/yellow/red)

### Test 4: Error Handling
- [ ] Test with empty file
- [ ] Test with invalid file type
- [ ] Test with empty job description
- [ ] Error messages displayed correctly
- [ ] Can retry after error

---

## 🔍 AWS Console Verification Checklist

### Lambda Functions
- [ ] Open AWS Console → Lambda
- [ ] See `resume-parser-dev`
- [ ] See `score-calculator-dev`
- [ ] See `api-handler-dev`
- [ ] Click on each, verify code deployed
- [ ] Check environment variables set
- [ ] View recent invocations

### S3 Bucket
- [ ] Open AWS Console → S3
- [ ] See bucket: `resume-analyzer-{account-id}-dev`
- [ ] Check folder structure: `resumes/YYYY/MM/DD/`
- [ ] Verify uploaded resume exists
- [ ] Check bucket properties (encryption, lifecycle)

### DynamoDB
- [ ] Open AWS Console → DynamoDB
- [ ] See table: `ResumeAnalysisResults-dev`
- [ ] Click "Explore table items"
- [ ] See analysis record with your data
- [ ] Verify all fields populated

### CloudWatch Logs
- [ ] Open AWS Console → CloudWatch → Log groups
- [ ] See `/aws/lambda/resume-parser-dev`
- [ ] See `/aws/lambda/score-calculator-dev`
- [ ] See `/aws/lambda/api-handler-dev`
- [ ] Click on recent log stream
- [ ] Verify no ERROR messages

### API Gateway
- [ ] Open AWS Console → API Gateway
- [ ] See `resume-analyzer-api-dev`
- [ ] Check stages (should see "dev")
- [ ] View resources (/upload, /analyze, /results)
- [ ] Check CORS configuration

---

## 📊 Demo Preparation Checklist

### Sample Data
- [ ] Have 2-3 sample resumes ready (PDF format)
- [ ] Prepare sample job descriptions
- [ ] Test each combination beforehand
- [ ] Know expected scores for each

### Demo Script
- [ ] Write step-by-step demo script
- [ ] Practice demo 2-3 times
- [ ] Time the demo (should be 3-5 minutes)
- [ ] Prepare for common questions

### Backup Plan
- [ ] Take screenshots of working demo
- [ ] Record video of successful run
- [ ] Have AWS Console open in background
- [ ] Know how to show logs if needed

### Presentation Materials
- [ ] Review `PRESENTATION_NOTES.md`
- [ ] Prepare architecture diagram slide
- [ ] Create cost breakdown slide
- [ ] Prepare technology stack slide
- [ ] Have code snippets ready to show

---

## 🎯 Presentation Day Checklist

### Before Presentation
- [ ] Good night's sleep
- [ ] Laptop fully charged
- [ ] Backup charger available
- [ ] Internet connection verified
- [ ] AWS Console logged in
- [ ] Frontend running on localhost
- [ ] Sample resume files ready
- [ ] Job description copied to clipboard

### During Demo
- [ ] Explain architecture first
- [ ] Show live application
- [ ] Upload resume and analyze
- [ ] Show results
- [ ] Switch to AWS Console
- [ ] Show Lambda functions
- [ ] Show DynamoDB table
- [ ] Show CloudWatch logs
- [ ] Explain cost and scalability

### If Demo Fails
- [ ] Show screenshots
- [ ] Play recorded video
- [ ] Walk through code
- [ ] Show AWS Console
- [ ] Explain what should happen

---

## 🧹 Post-Demo Cleanup Checklist

### Keep Running (if needed)
- Leave resources running if:
  - [ ] Need to demo again
  - [ ] Want to show others
  - [ ] Testing more features
  - [ ] Working on improvements

### Delete Resources (to save costs)
```bash
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name resume-analyzer-stack

# Wait for deletion
aws cloudformation wait stack-delete-complete --stack-name resume-analyzer-stack

# Delete S3 buckets (if needed)
aws s3 rb s3://resume-analyzer-{account-id}-dev --force
aws s3 rb s3://resume-analyzer-deployment-{account-id} --force
```

- [ ] CloudFormation stack deleted
- [ ] All resources removed
- [ ] S3 buckets deleted (or emptied)
- [ ] No lingering costs
- [ ] Verify in AWS Console

---

## 📝 Documentation Checklist

### Code Documentation
- [ ] All Lambda functions have docstrings
- [ ] Complex algorithms explained
- [ ] Environment variables documented
- [ ] API endpoints documented

### Project Documentation
- [ ] README.md complete
- [ ] QUICKSTART.md tested
- [ ] ARCHITECTURE.md accurate
- [ ] API.md comprehensive
- [ ] PRESENTATION_NOTES.md helpful

### Repository
- [ ] All code committed to Git
- [ ] .gitignore properly configured
- [ ] No sensitive data in repo
- [ ] README renders correctly

---

## 🐛 Troubleshooting Checklist

### Issue: Deployment Fails
- [ ] Check AWS credentials: `aws sts get-caller-identity`
- [ ] Verify SAM version: `sam --version`
- [ ] Check CloudFormation events in AWS Console
- [ ] Look for IAM permission errors
- [ ] Verify S3 bucket names are unique

### Issue: Lambda Timeout
- [ ] Check Lambda logs in CloudWatch
- [ ] Increase timeout in template.yaml
- [ ] Verify Lambda has enough memory
- [ ] Check if file is too large

### Issue: CORS Errors
- [ ] Verify API endpoint in frontend .env
- [ ] Check CORS configuration in template.yaml
- [ ] Clear browser cache
- [ ] Try different browser

### Issue: DynamoDB Errors
- [ ] Verify table name in environment variables
- [ ] Check IAM role permissions
- [ ] Verify table exists in AWS Console
- [ ] Check for throttling errors

### Issue: S3 Upload Fails
- [ ] Verify presigned URL not expired
- [ ] Check file size (max 10MB)
- [ ] Verify bucket name correct
- [ ] Check IAM permissions

---

## ✅ Final Verification Checklist

### Before Declaring "Done"
- [ ] All 3 Lambda functions working
- [ ] Frontend connects to backend
- [ ] Can upload resume successfully
- [ ] Can analyze and get results
- [ ] Results are meaningful
- [ ] No errors in CloudWatch logs
- [ ] AWS Console shows all resources
- [ ] Cost is minimal (under $5/month)
- [ ] Can demo confidently
- [ ] Team understands the code
- [ ] Documentation is complete

### Knowledge Check
Each team member should be able to:
- [ ] Explain the architecture
- [ ] Describe each Lambda function
- [ ] Explain TF-IDF algorithm
- [ ] Show how to deploy
- [ ] Navigate AWS Console
- [ ] Answer basic questions
- [ ] Troubleshoot common issues

---

## 🎉 Success Criteria

✅ **Backend**: All Lambda functions deployed and working  
✅ **Frontend**: React app running and connected to API  
✅ **Integration**: End-to-end flow working  
✅ **Testing**: Tested with multiple resumes  
✅ **Documentation**: Complete and accurate  
✅ **Demo**: Practiced and ready  
✅ **Team**: Everyone understands the project  

---

## 📞 Emergency Contacts

If stuck, refer to:
- AWS Documentation: https://docs.aws.amazon.com
- SAM Documentation: https://docs.aws.amazon.com/serverless-application-model/
- React Documentation: https://react.dev
- Project README: `/README.md`
- Architecture Docs: `/docs/ARCHITECTURE.md`

---

## 🏆 Final Notes

**Remember**:
- This is a learning project - perfection not required
- Document any issues you face
- Be proud of what you built
- Have fun with the demo!

**You've built**:
- A real serverless application
- Integrated 7 AWS services
- Implemented NLP algorithms
- Created a modern web interface
- Learned cloud architecture

**Good luck, Team 20! 🚀**

---

*Last Updated: November 30, 2024*
