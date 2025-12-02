# Team Contributions - AI-Powered Resume Analyzer

## Project Overview
**Team Members:** Keyur Nareshkumar Modi, Naveen John, Vindhya Sadanand Hegde  
**Course:** Cloud Computing - Final Project  
**Institution:** University of Texas at San Antonio  
**Date:** December 2025

---

## Individual Contributions

### Vindhya Sadanand Hegde
**Role:** Backend Architecture & NLP Algorithm Development

**Primary Responsibilities:**
- **Lambda Function Implementation**
  - Designed and implemented Resume Parser Lambda function (350+ lines)
  - Developed Score Calculator Lambda function (817 lines)
  - Built API Handler Lambda function (522 lines) for request orchestration
  
- **NLP Algorithm Development**
  - Implemented pattern-based skill filtering using linguistic patterns
  - Developed TF-IDF similarity calculation for job matching
  - Created technical keyword detection algorithm (CamelCase, hyphenated terms, version numbers)
  - Built soft skill filtering logic (gerunds, abstract nouns, action verbs)
  
- **ATS Scoring System**
  - Designed dynamic scoring algorithm with context-aware penalties
  - Implemented base score calculation with bonus/penalty features
  - Created feedback generation system with actionable recommendations
  
- **AWS Infrastructure Setup**
  - Configured S3 buckets with encryption and presigned URLs
  - Set up DynamoDB tables with proper indexes
  - Implemented IAM roles with least-privilege policies
  
- **Code Contributions:** ~1,700 lines of Python backend code

---

### Naveen John
**Role:** Frontend Development & User Experience

**Primary Responsibilities:**
- **React Application Development**
  - Built main App.js container component with state management
  - Developed FileUpload.js component with drag-and-drop functionality
  - Created Results.js dashboard with multiple sub-components
  - Implemented JobComparison.js for multi-job analysis
  
- **UI/UX Design**
  - Designed responsive layout with mobile support
  - Created custom CSS styling for all components
  - Implemented color-coded ATS score visualization
  - Built intuitive navigation and user flow
  
- **Data Visualization**
  - Integrated Recharts library for skill match graphs
  - Created bar charts for job comparison rankings
  - Implemented interactive charts with tooltips
  
- **Cover Letter Feature**
  - Built CoverLetter.js component with edit/copy/download functionality
  - Implemented html2canvas and jsPDF for PDF generation
  - Created personalized letter display with formatting
  
- **Testing & Bug Fixes**
  - Fixed skills graph showing "1 of 1 (100%)" issue
  - Corrected job comparison displaying wrong skill counts
  - Resolved company name placeholder in cover letters
  - Conducted user acceptance testing with 10+ test cases
  
- **Code Contributions:** ~1,200 lines of JavaScript/React code

---

### Keyur Nareshkumar Modi
**Role:** Infrastructure, Security & Deployment

**Primary Responsibilities:**
- **CloudFront CDN Setup**
  - Configured CloudFront distribution with Origin Access Identity
  - Implemented HTTPS-only access with AWS-managed certificates
  - Set up cache invalidation for instant frontend updates
  - Resolved AWS Block Public Access issue with OAI solution
  
- **Security Configuration**
  - Implemented CORS policies for API Gateway
  - Configured S3 bucket encryption at rest (AES-256)
  - Set up presigned URL expiration (5 minutes)
  - Created IAM policies with least-privilege access
  
- **Deployment Automation**
  - Created AWS SAM template (template.yaml) for Infrastructure as Code
  - Built deployment scripts (deploy-secure.sh) for CloudFront + S3
  - Automated CloudFormation stack deployment
  - Implemented environment management (dev/prod)
  
- **Performance Optimization**
  - Optimized Lambda function memory allocation (512MB/256MB)
  - Configured timeout settings (60s/30s)
  - Implemented CloudWatch logging for debugging
  - Analyzed and reduced API response times to 2-4 seconds
  
- **Monitoring & Logging**
  - Set up CloudWatch metrics for Lambda invocations
  - Configured error tracking and alerting
  - Implemented detailed logging for debugging
  - Created performance dashboards
  
- **Documentation & Demo**
  - Wrote comprehensive project documentation
  - Created IEEE conference paper (5,800 words, 26KB)
  - Developed demo script for 12-15 minute presentation
  - Prepared architecture diagrams and screenshots guide
  - Built HTML demo presentation with 20 slides
  
- **Code Contributions:** ~400 lines of YAML/Bash scripts + extensive documentation

---

## Collaborative Work

### Joint Responsibilities (All Team Members):
- **Requirements Gathering & Architecture Design** (Weeks 1-2)
  - Brainstormed features and user requirements
  - Designed serverless architecture diagram
  - Decided on AWS services and technology stack
  
- **Integration Testing** (Week 7)
  - End-to-end testing of frontend → API → Lambda → Storage flow
  - Cross-browser compatibility testing
  - Performance testing with various resume formats
  
- **Code Reviews & Quality Assurance**
  - Peer reviews of all major code changes
  - Collaborative debugging sessions
  - Ensuring code quality and best practices
  
- **Final Report & Presentation** (Week 10)
  - Compiled technical documentation
  - Created presentation materials
  - Recorded project demo video
  - Prepared submission package

---

## Technology Expertise by Team Member

| Technology/Service | Vindhya Hegde | Naveen John | Keyur Modi |
|-------------------|-----------|------------|---------------|
| **AWS Lambda** | ✓✓✓ Primary | ✓ Integration | ✓✓ Configuration |
| **Python Backend** | ✓✓✓ Primary | - | ✓ Scripts |
| **React Frontend** | - | ✓✓✓ Primary | ✓ Testing |
| **AWS S3** | ✓✓ Implementation | ✓ Integration | ✓✓✓ Configuration |
| **DynamoDB** | ✓✓✓ Primary | ✓ Integration | ✓ Monitoring |
| **API Gateway** | ✓✓ Setup | ✓✓ Integration | ✓✓ CORS Config |
| **CloudFront** | - | - | ✓✓✓ Primary |
| **AWS SAM/IaC** | ✓ Development | - | ✓✓✓ Primary |
| **NLP Algorithms** | ✓✓✓ Primary | - | ✓ Testing |
| **UI/UX Design** | - | ✓✓✓ Primary | ✓ Review |
| **Security/IAM** | ✓✓ Implementation | ✓ Frontend | ✓✓✓ Infrastructure |

**Legend:** ✓✓✓ Primary responsibility | ✓✓ Major contribution | ✓ Supporting work

---

## Code Statistics

### Backend (Python)
- **lambda/resume_parser/lambda_function.py:** 350+ lines (Vindhya)
- **lambda/resume_parser/ats_checker.py:** 150+ lines (Vindhya)
- **lambda/score_calculator/lambda_function.py:** 817 lines (Vindhya)
- **lambda/api_handler/lambda_function.py:** 522 lines (Vindhya)
- **Total Backend:** ~1,839 lines

### Frontend (JavaScript/React)
- **frontend/src/App.js:** 200+ lines (Naveen)
- **frontend/src/components/Results.js:** 250+ lines (Naveen)
- **frontend/src/components/FileUpload.js:** 150+ lines (Naveen)
- **frontend/src/components/JobComparison.js:** 200+ lines (Naveen)
- **frontend/src/components/CoverLetter.js:** 180+ lines (Naveen)
- **frontend/src/components/ATSScore.js:** 120+ lines (Naveen)
- **frontend/src/components/LearningPath.js:** 100+ lines (Naveen)
- **Total Frontend:** ~1,200 lines

### Infrastructure (YAML/Bash)
- **template.yaml:** 250+ lines (Keyur)
- **scripts/deploy-secure.sh:** 150+ lines (Keyur)
- **Other deployment scripts:** 100+ lines (Keyur)
- **Total Infrastructure:** ~500 lines

### Documentation
- **FINAL_PROJECT_REPORT.md:** 5,800 words, 26KB (Keyur - lead, All - contributions)
- **DEMO_SCRIPT.md:** 14KB (Keyur)
- **Architecture diagrams:** 30KB (Keyur)
- **Screenshot guides:** 9.2KB (Keyur)
- **Other documentation:** 50KB+ (All team members)

---

## Project Milestones & Ownership

| Week | Milestone | Primary Owner | Contributors |
|------|-----------|---------------|--------------||
| 1-2 | Architecture Design | All | All |
| 3 | Lambda Functions Setup | Vindhya | Keyur |
| 4 | NLP Algorithm Implementation | Vindhya | - |
| 5 | Frontend Components | Naveen | - |
| 6 | UI/UX Polish & Charts | Naveen | - |
| 7 | Integration Testing | All | All |
| 8 | AWS Deployment | Keyur | Vindhya, Naveen |
| 9 | CloudFront CDN | Keyur | - |
| 9 | Performance Optimization | Keyur | Vindhya |
| 10 | Bug Fixes & Testing | All | All |
| 10 | Documentation & Demo | Keyur | All |

---

## Problem-Solving Contributions

### Major Bugs Fixed:

1. **Company name placeholder issue** (Week 9)
   - **Identified by:** Naveen (during frontend testing)
   - **Fixed by:** Vindhya (removed unused parameter)
   - **Verified by:** All team members

2. **Skills graph showing "1 of 1"** (Week 9)
   - **Identified by:** Vindhya (backend data analysis)
   - **Fixed by:** Naveen (conditional rendering in Results.js)
   - **Verified by:** Keyur

3. **Random non-technical keywords** (Week 8)
   - **Identified by:** Keyur (during testing)
   - **Fixed by:** Vindhya (pattern-based NLP filtering)
   - **Verified by:** All team members

4. **Identical ATS scores** (Week 9)
   - **Identified by:** Naveen (user testing)
   - **Fixed by:** Vindhya (dynamic scoring with penalties)
   - **Verified by:** All team members

5. **AWS Block Public Access issue** (Week 8)
   - **Identified by:** Keyur (deployment failure)
   - **Fixed by:** Keyur (CloudFront OAI solution)
   - **Verified by:** All team members

6. **Job comparison contradictory metrics** (Week 10)
   - **Identified by:** User feedback (shown to Keyur)
   - **Fixed by:** Vindhya (corrected skills count calculation)
   - **Verified by:** Naveen, Keyur

---

## Communication & Collaboration

### Team Meetings:
- **Weekly sync:** Every Monday 6:00 PM (10 weeks)
- **Code review sessions:** Wednesdays as needed
- **Integration sprints:** Week 7, Week 10

### Tools Used:
- **GitHub:** Version control and code collaboration
- **Slack/Discord:** Daily communication
- **Zoom:** Virtual meetings and pair programming
- **AWS Console:** Shared access for testing
- **VS Code Live Share:** Collaborative debugging

---

## Individual Strengths Applied

### Vindhya Sadanand Hegde:
- **Strength:** Backend development, algorithms, data processing
- **Applied:** Built entire Python backend with sophisticated NLP algorithms
- **Innovation:** Pattern-based skill detection that scales automatically

### Naveen John:
- **Strength:** Frontend development, UI/UX design, user experience
- **Applied:** Created intuitive, responsive React application
- **Innovation:** Interactive visualizations for job comparison

### Keyur Nareshkumar Modi:
- **Strength:** DevOps, cloud infrastructure, security, documentation
- **Applied:** Production-ready AWS deployment with professional documentation
- **Innovation:** Secure CloudFront distribution bypassing S3 public access

---

## Acknowledgments

Each team member brought unique expertise that was essential to the project's success:

- **Vindhya** made the system intelligent with advanced NLP algorithms
- **Naveen** made the system usable with beautiful UI/UX design
- **Keyur** made the system production-ready with robust infrastructure

The project would not have been possible without the collaborative effort and complementary skills of all three team members.

---

## Final Metrics

- **Total Project Duration:** 10 weeks
- **Total Lines of Code:** 3,500+
- **Total Documentation:** 130KB+ (markdown/text)
- **Team Meetings:** 15+
- **GitHub Commits:** 100+
- **AWS Resources Deployed:** 15+
- **Features Delivered:** 8 major features
- **Bugs Fixed:** 6 major issues

**Project Status:** ✅ Successfully deployed to production  
**Live URL:** https://dx8h4r4ocvfti.cloudfront.net

---

**Last Updated:** December 1, 2025
