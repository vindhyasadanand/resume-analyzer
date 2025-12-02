# IEEE Conference Paper Formatting Guide
## Converting Markdown Report to IEEE Word Document

---

## 📋 **Quick Checklist**

Before you start:
- [ ] Download IEEE template: `conference-template-letter.docx`
- [ ] Have `FINAL_PROJECT_REPORT.md` open
- [ ] Screenshots ready (5 images)
- [ ] Diagrams prepared (optional)
- [ ] Team member names ready
- [ ] Panopto video link ready

---

## 📄 **Step 1: Template Setup**

### **1.1 Open IEEE Template**
1. Open `conference-template-letter.docx` in Microsoft Word
2. Enable "Show/Hide" formatting marks (¶ button) to see structure

### **1.2 Update Header Information**

**Replace placeholder text:**

```
Title: AI-Powered Resume Analyzer with AWS Cloud Infrastructure

Authors:
Keyur Nareshkumar Modi
University of Texas at San Antonio
kmodi@my.utsa.edu

Naveen John
University of Texas at San Antonio
naveen.john@my.utsa.edu

Vindhya Sadanand Hegde  
University of Texas at San Antonio
vindhya.hegde@my.utsa.edu
```

**Format:**
- Title: 24pt, Bold, Centered
- Author names: 12pt, Regular
- Affiliations: 10pt, Italic

---

## 📝 **Step 2: Abstract Section**

### **Copy from FINAL_PROJECT_REPORT.md**

**Abstract (150-250 words):**

```
This paper presents the design and implementation of an AI-powered Resume 
Analyzer system built on AWS cloud infrastructure. The system leverages 
serverless computing, natural language processing, and machine learning 
techniques to provide automated resume analysis, ATS compatibility scoring, 
job matching, and personalized cover letter generation. The application 
demonstrates the practical application of cloud computing principles including 
scalability, cost-efficiency, and high availability. Our solution achieved 
35-75% job matching accuracy with pattern-based NLP for skill extraction and 
implements secure CloudFront CDN distribution for global accessibility.
```

**Keywords (5-7 terms):**
```
Cloud Computing, AWS Lambda, Serverless Architecture, Natural Language 
Processing, Resume Analysis, ATS Scoring
```

**Formatting:**
- Abstract: 10pt, Italic, Justified
- Keywords: 10pt, Bold label "Keywords:", Regular text

---

## 📑 **Step 3: Main Body Sections**

### **Section Formatting Rules:**

1. **Section Headings:** 
   - Font: 12pt, Bold, UPPERCASE
   - Numbering: Roman numerals (I, II, III...)
   - Spacing: 6pt before, 3pt after

2. **Subsection Headings:**
   - Font: 11pt, Bold, Title Case
   - Numbering: Letter format (A, B, C...)
   - Spacing: 3pt before, 2pt after

3. **Body Text:**
   - Font: 10pt, Times New Roman
   - Alignment: Justified (both left and right)
   - Spacing: Single, 0pt before/after
   - First line indent: 0.25 inches

4. **Two-Column Layout:**
   - Columns: 2, equal width
   - Spacing between: 0.25 inches

---

## 🎨 **Step 4: Copy Content Section by Section**

### **Section I: INTRODUCTION**

From FINAL_PROJECT_REPORT.md → copy Introduction section

**Formatting tips:**
- Start with capital letter drop cap (optional)
- Keep paragraphs short (3-5 sentences)
- Use clear topic sentences

**Example structure:**
```
I. INTRODUCTION

In today's competitive job market, candidates struggle to optimize their 
resumes for Applicant Tracking Systems (ATS) and understand how well their 
qualifications match job requirements. This project addresses these challenges 
by creating an automated, cloud-based solution...

A. Background and Motivation
[Content here...]

B. Project Goals
[Content here...]

C. Problem Statement
[Content here...]
```

---

### **Section II: SYSTEM ARCHITECTURE**

**Copy architecture content + INSERT DIAGRAM**

```
II. SYSTEM ARCHITECTURE

The system follows a serverless, event-driven architecture with the following 
components...

[Insert Figure 1 here - System Architecture Diagram]

A. Overall Architecture
The architecture consists of three primary layers...

B. AWS Services Used
1) AWS Lambda (3 Functions): [description]
2) Amazon S3: [description]
...
```

**How to insert figures:**
1. Click where you want the figure
2. Insert → Pictures → Select image file
3. Resize to fit column width (~3.25 inches)
4. Right-click image → Wrap Text → "Top and Bottom"
5. Below image, insert caption:
   ```
   Insert → Caption → Label: Figure → Position: Below selected item
   Caption: "Fig. 1. High-level system architecture showing request flow from user to AWS services"
   ```

---

### **Section III: METHODOLOGY**

**Copy methodology content, format code snippets**

```
III. METHODOLOGY

A. Resume Parsing Algorithm

1) PDF Text Extraction: Uses PyMuPDF (fitz) library for PDF parsing...

2) Skill Extraction: Pattern-based skill detection...
```

**Code snippets formatting:**
```
Font: Courier New, 9pt
Background: Light gray (RGB: 240, 240, 240)
Border: 1pt solid line
Indentation: 0.1 inch from margins
```

**Example code block:**
```python
def is_valid_skill(skill):
    """Check if extracted skill is valid"""
    if skill.endswith(('ing', 'tion')):
        return False  # Likely soft skill
    if re.match(r'[A-Z][a-z]+[A-Z]', skill):
        return True   # CamelCase = technical
    return True
```

---

### **Section IV: IMPLEMENTATION DETAILS**

**Copy implementation section**

```
IV. IMPLEMENTATION DETAILS

A. Backend Implementation

1) Lambda Function Configuration:
   - Runtime: Python 3.11
   - Memory: 512 MB (Parser), 256 MB (Handler)
   - Timeout: 60 seconds
   ...

B. Frontend Implementation
[Content...]

C. Deployment Process
[Content...]
```

---

### **Section V: KEY FEATURES & INNOVATIONS**

**Highlight unique contributions**

```
V. KEY FEATURES & INNOVATIONS

A. Pattern-Based NLP for Skill Detection

Innovation: Instead of maintaining hardcoded skill lists that become outdated, 
we implemented linguistic pattern recognition...

[Insert Figure 3: NLP Algorithm Flow]
```

---

### **Section VI: TESTING & VALIDATION**

**Copy testing results, format tables**

```
VI. TESTING & VALIDATION

A. Test Cases

Functional Testing:
✓ PDF upload with various file sizes (100KB - 5MB)
✓ Multi-page resume parsing accuracy
...

[Insert Table I: Performance Benchmarks]
```

**Table formatting:**

```
TABLE I
PERFORMANCE BENCHMARKS

Metric              Average    P95     P99
─────────────────────────────────────────
Resume Parsing      1.8s      2.5s    3.2s
Score Calculation   1.2s      1.5s    2.0s
Total Analysis      3.0s      4.0s    5.2s
```

**How to create tables:**
1. Insert → Table → Select rows/columns
2. Format:
   - Header row: Bold, centered
   - Data rows: Regular, centered
   - Borders: All borders, 1pt
   - Caption above: "TABLE I\nPERFORMANCE BENCHMARKS"
   - Font: 9pt

---

### **Section VII: RESULTS & OUTCOMES**

**Copy results with screenshots**

```
VII. RESULTS & OUTCOMES

A. System Performance

Scalability: Serverless architecture supports 1000+ concurrent users...

[Insert Figure 2: Analysis Results Dashboard Screenshot]

B. User Experience

Features Delivered:
✓ PDF resume upload with drag-and-drop
✓ Real-time analysis progress indicators
...

[Insert Figure 4: Generated Cover Letter Screenshot]
```

---

### **Section VIII: PROJECT MANAGEMENT**

**Team contributions**

```
VIII. PROJECT MANAGEMENT

A. Team Contributions

Keyur Nareshkumar Modi:
- Backend architecture design and implementation
- Lambda function development (resume parser, score calculator)
- NLP algorithm development for skill filtering
- AWS infrastructure setup (S3, DynamoDB, API Gateway)

Naveen John:
- Frontend React development and UI/UX design
- Data visualization with Recharts
- Cover letter generation logic
- Testing and bug fixing

Vindhya Sadanand Hegde:
- CloudFront CDN setup with security configuration
- API handler implementation
- Multi-job comparison feature
- Documentation and demo preparation
```

---

### **Section IX: CHALLENGES & LESSONS LEARNED**

```
IX. CHALLENGES & LESSONS LEARNED

A. Technical Challenges

1) PDF Parsing Complexity: Different resume formats (single-column, 
two-column, tables)...
```

---

### **Section X: CONCLUSION**

**Copy conclusion**

```
X. CONCLUSION

This project successfully demonstrates the power of cloud computing for 
building scalable, intelligent applications...

Key Achievements:
✓ Deployed live application with global CDN distribution
✓ Implemented pattern-based NLP for scalable skill detection
...
```

---

### **REFERENCES**

**IEEE Citation Format:**

```
REFERENCES

[1] AWS Lambda Documentation, "Building Lambda functions with Python," 
    Amazon Web Services, 2025. [Online]. Available: 
    https://docs.aws.amazon.com/lambda/

[2] AWS Serverless Application Model (SAM), "Deploying serverless 
    applications," Amazon Web Services, 2025. [Online]. Available: 
    https://aws.amazon.com/serverless/sam/

[3] G. Manning, Natural Language Processing with Python. O'Reilly Media, 
    2023.

[4] PyMuPDF Documentation, "PDF parsing and text extraction," 2025. 
    [Online]. Available: https://pymupdf.readthedocs.io/

[5] React Documentation, "Building user interfaces with React," Meta 
    Platforms, 2025. [Online]. Available: https://react.dev/
```

**Reference formatting:**
- Font: 9pt
- Hanging indent: 0.25 inches
- Numbering: [1], [2], [3]...
- Cite in text: "as described in [1]"

---

### **APPENDIX**

```
APPENDIX A: SYSTEM SCREENSHOTS

[Insert all 5 screenshots with captions]

Screenshot 1: Main Application Interface
Screenshot 2: Analysis Results Dashboard
Screenshot 3: Multi-Job Comparison
Screenshot 4: Generated Cover Letter
Screenshot 5: AWS CloudFormation Stack
```

```
APPENDIX B: SOURCE CODE AVAILABILITY

GitHub Repository: [Insert GitHub URL]

Live Application:
• Frontend: https://dx8h4r4ocvfti.cloudfront.net
• API: https://s0ogqkfqaf.execute-api.us-east-1.amazonaws.com

Project Demo Video:
[Insert Panopto Link Here]

Recording Instructions:
1. Log into UTSA Panopto: https://utsa.hosted.panopto.com
2. Click "Create" → "Record New Session"
3. Enable screen recording + webcam
4. Follow demo script (see DEMO_SCRIPT.md)
5. Upload and share video link
```

---

## 🎨 **Step 5: Final Formatting**

### **5.1 Page Layout**

```
Margins:
- Top: 0.75 inches
- Bottom: 1 inch  
- Left: 0.75 inches
- Right: 0.75 inches

Columns:
- Two columns, equal width
- 0.25 inch spacing between columns

Page size: Letter (8.5" × 11")
```

### **5.2 Typography**

```
Body text: Times New Roman, 10pt
Headings: Times New Roman, Bold
Code: Courier New, 9pt
Captions: Times New Roman, 9pt
```

### **5.3 Spacing**

```
Line spacing: Single (1.0)
Paragraph spacing: 0pt before, 0pt after
Section breaks: 6pt before major sections
```

### **5.4 Page Numbers**

```
Position: Bottom center
Format: Simple page number
Start: Page 1 (after cover page if any)
```

---

## ✅ **Step 6: Pre-Submission Checklist**

### **Content Completeness:**
- [ ] Title and authors correct
- [ ] Abstract (150-250 words)
- [ ] Keywords (5-7 terms)
- [ ] All 10 sections present (I-X)
- [ ] References in IEEE format
- [ ] Appendices with screenshots and links

### **Figures & Tables:**
- [ ] All figures inserted and captioned
- [ ] All tables formatted correctly
- [ ] Figures referenced in text ("Fig. 1", "Fig. 2")
- [ ] Tables referenced in text ("Table I", "Table II")
- [ ] Images are high quality (not blurry)

### **Formatting:**
- [ ] Two-column layout (except abstract)
- [ ] IEEE template style applied
- [ ] Consistent fonts throughout
- [ ] Page numbers present
- [ ] 5-6 pages total length

### **Technical Accuracy:**
- [ ] No Lorem Ipsum placeholder text
- [ ] All code snippets formatted
- [ ] URLs are clickable
- [ ] Panopto video link works
- [ ] Team contributions accurate

### **Grammar & Style:**
- [ ] Spell-checked (F7 in Word)
- [ ] Grammar-checked
- [ ] Consistent terminology
- [ ] Professional tone
- [ ] No first-person ("I", "we" is okay for team)

---

## 🔧 **Common Issues & Fixes**

### **Issue 1: Images Breaking Columns**
**Fix:** 
```
Right-click image → Wrap Text → "Tight"
Resize image to fit column width (3.2 inches max)
```

### **Issue 2: Code Overflowing Margins**
**Fix:**
```
Select code block
Format → Paragraph → Indentation: 0.1" from left/right
Font size: Reduce to 8pt if needed
Use line breaks for long lines
```

### **Issue 3: Two-Column Layout Breaking**
**Fix:**
```
Layout → Columns → Two
Layout → Breaks → Column break (to force new column)
```

### **Issue 4: References Not Auto-Numbering**
**Fix:**
```
Home → Numbering → Define New Number Format
Format: [1], [2], [3]...
Alignment: Left
```

### **Issue 5: Page Count Too Long**
**Fix:**
```
Reduce margins slightly (0.75" → 0.6")
Decrease figure sizes
Condense verbose paragraphs
Move some content to Appendix
```

---

## 💾 **Step 7: Save & Export**

### **7.1 Save Multiple Versions**

```
Final_Project_Report_v1.docx (working copy)
Final_Project_Report_v2.docx (after first review)
Final_Project_Report_FINAL.docx (submission version)
```

### **7.2 Export as PDF** (optional backup)

```
File → Save As → PDF
Settings:
- Standard (publishing online)
- Document structure tags for accessibility
- Optimize for: Standard
```

### **7.3 Backup**

```
Save to:
- Local folder
- Cloud storage (Google Drive, OneDrive)
- Email to yourself
```

---

## 📤 **Step 8: Submit**

### **Submission Package:**

1. ✅ `Final_Project_Report_[YourNames].docx` (5-6 pages, IEEE format)
2. ✅ `Resume_Analyzer_SourceCode.zip` (source code archive)
3. ✅ Panopto video link (included in report Appendix B)

### **Final Check:**

```
- [ ] Open document in Word (not preview)
- [ ] Verify all images load
- [ ] Click all links to test
- [ ] Review page count (5-6 pages)
- [ ] Check file size (<10MB)
- [ ] Submit before deadline!
```

---

## 🎓 **IEEE Formatting Examples**

### **Example: Citing a Figure**

**In text:**
```
"The system architecture (Fig. 1) demonstrates a serverless approach..."
```

**Caption:**
```
Fig. 1. High-level system architecture showing request flow from user to AWS services.
```

### **Example: Citing a Table**

**In text:**
```
"Performance benchmarks are shown in Table I."
```

**Caption:**
```
TABLE I
PERFORMANCE BENCHMARKS
```

### **Example: Citing a Reference**

**In text:**
```
"Serverless computing offers cost advantages [1, 2]."
"As described in [3], NLP techniques can..."
```

**In References:**
```
[1] A. Author, "Title of Paper," Conference Name, pp. 1-5, 2025.
```

---

## 📊 **IEEE Template Quick Reference**

| Element | Font | Size | Style |
|---------|------|------|-------|
| Title | Times | 24pt | Bold |
| Authors | Times | 12pt | Regular |
| Section Heading | Times | 12pt | Bold, CAPS |
| Subsection | Times | 11pt | Bold |
| Body Text | Times | 10pt | Regular |
| Captions | Times | 9pt | Regular |
| Code | Courier | 9pt | Regular |
| References | Times | 9pt | Regular |

---

**You're ready to create your IEEE report!** 📄✨

Follow these steps carefully, and you'll have a professional conference paper ready for submission.
