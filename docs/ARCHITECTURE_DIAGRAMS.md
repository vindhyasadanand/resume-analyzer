# Architecture Diagrams for IEEE Report
## AI-Powered Resume Analyzer

---

## DIAGRAM 1: High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         END USERS                                    │
│                   (Web Browsers Worldwide)                           │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 │ HTTPS (TLS 1.2+)
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AMAZON CLOUDFRONT                               │
│                   (Global CDN - Edge Locations)                      │
│                                                                      │
│  ┌────────────────────────────────────────────────────────┐        │
│  │         Origin Access Identity (OAI)                   │        │
│  │  • Secure S3 access without public bucket              │        │
│  │  • HTTPS-only delivery                                 │        │
│  │  • Cache control headers                               │        │
│  └────────────────────────────────────────────────────────┘        │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │      AMAZON S3         │
                    │  (Frontend Assets)     │
                    │                        │
                    │  • index.html          │
                    │  • static/js/*.js      │
                    │  • static/css/*.css    │
                    │  • Encrypted at rest   │
                    └────────────────────────┘

                                 │ API Requests
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AMAZON API GATEWAY                                │
│                      (REST API v2)                                   │
│                                                                      │
│  Endpoints:                                                          │
│  • POST   /upload          → Generate presigned S3 URL              │
│  • POST   /analyze         → Full resume analysis                   │
│  • POST   /batch-compare   → Multi-job comparison                   │
│  • GET    /results/{id}    → Retrieve stored results                │
│  • OPTIONS /*              → CORS preflight                          │
│                                                                      │
│  Security: API Keys, Throttling, Request Validation                 │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 │ Lambda Invocation
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AWS LAMBDA FUNCTIONS                            │
│                      (Python 3.11 Runtime)                           │
│                                                                      │
│  ┌──────────────────────┐  ┌──────────────────────┐                │
│  │   API Handler        │  │   Resume Parser      │                │
│  │   (Orchestrator)     │  │   (PDF Processing)   │                │
│  │                      │  │                      │                │
│  │  • Request routing   │  │  • PyMuPDF library   │                │
│  │  • Auth & validation │  │  • Text extraction   │                │
│  │  • Error handling    │  │  • Skill detection   │                │
│  │  • Response format   │  │  • ATS scoring       │                │
│  │                      │  │                      │                │
│  │  Memory: 256 MB      │  │  Memory: 512 MB      │                │
│  │  Timeout: 30s        │  │  Timeout: 60s        │                │
│  └──────────────────────┘  └──────────────────────┘                │
│                                                                      │
│  ┌──────────────────────────────────────────┐                       │
│  │        Score Calculator                  │                       │
│  │     (NLP & Matching Engine)              │                       │
│  │                                           │                       │
│  │  • TF-IDF computation                    │                       │
│  │  • Cosine similarity                     │                       │
│  │  • Pattern-based skill filtering         │                       │
│  │  • Cover letter generation               │                       │
│  │  • Feedback synthesis                    │                       │
│  │                                           │                       │
│  │  Memory: 512 MB                          │                       │
│  │  Timeout: 60s                            │                       │
│  └──────────────────────────────────────────┘                       │
└────────┬──────────────────────────┬──────────────────────────────────┘
         │                          │
         │                          │
         ▼                          ▼
┌────────────────────┐      ┌─────────────────────────┐
│   AMAZON S3        │      │   AMAZON DYNAMODB       │
│  (Resume Storage)  │      │  (Analysis Results)     │
│                    │      │                         │
│  • Encrypted       │      │  • analysis_id (PK)     │
│  • Versioning      │      │  • timestamp            │
│  • Lifecycle rules │      │  • ats_score            │
│  • Presigned URLs  │      │  • compatibility_score  │
│    (5 min expiry)  │      │  • parsed_data          │
│                    │      │  • feedback             │
│                    │      │  • On-demand billing    │
└────────────────────┘      └─────────────────────────┘

         │                          │
         └──────────────┬───────────┘
                        │
                        ▼
              ┌─────────────────────┐
              │  AMAZON CLOUDWATCH  │
              │   (Monitoring)      │
              │                     │
              │  • Lambda metrics   │
              │  • API Gateway logs │
              │  • Error tracking   │
              │  • Alarms           │
              └─────────────────────┘
```

**Figure 1: Complete system architecture showing request flow from user to AWS services**

---

## DIAGRAM 2: Lambda Function Flow

```
                    ┌─────────────────────┐
                    │   API Gateway       │
                    │   Request Received  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   API Handler       │
                    │   Lambda Function   │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
    /upload Route        /analyze Route      /batch-compare
          │                    │                    │
          │                    │                    │
          ▼                    ▼                    ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Generate         │  │ Invoke:          │  │ Invoke Multiple: │
│ Presigned S3 URL │  │ 1. Resume Parser │  │ 1. Resume Parser │
│                  │  │ 2. Score Calc    │  │ 2. Score Calc    │
│ Return:          │  │                  │  │    (N times)     │
│ • upload_url     │  │ Return:          │  │                  │
│ • s3_key         │  │ • ATS score      │  │ Return:          │
└──────────────────┘  │ • Match %        │  │ • Sorted results │
                      │ • Feedback       │  │ • Comparisons    │
                      │ • Cover letter   │  └──────────────────┘
                      └──────────────────┘
```

**Figure 2: Lambda function invocation flow and data processing pipeline**

---

## DIAGRAM 3: NLP Algorithm Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    RESUME TEXT INPUT                         │
│           "Experienced Python developer with AWS..."         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │   Tokenization   │
                  │  • Lowercase     │
                  │  • Remove punct. │
                  │  • Split words   │
                  └─────────┬────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Stop Word       │
                  │  Removal         │
                  │  (the, is, at)   │
                  └─────────┬────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
   ┌─────────────┐   ┌─────────────┐  ┌──────────────┐
   │ Skill       │   │ TF (Term    │  │ Pattern-Based│
   │ Extraction  │   │ Frequency)  │  │ Filtering    │
   │             │   │             │  │              │
   │ • Regex     │   │ word_count  │  │ • Detect -ing│
   │ • Keywords  │   │ ──────────  │  │ • Detect -tion│
   │ • Section   │   │ total_words │  │ • CamelCase  │
   │   parsing   │   │             │  │ • Tech terms │
   └──────┬──────┘   └──────┬──────┘  └──────┬───────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  IDF Computation │
                  │  (Inverse Doc    │
                  │   Frequency)     │
                  │                  │
                  │  log(N / df)     │
                  └─────────┬────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  TF-IDF Vector   │
                  │  Construction    │
                  │                  │
                  │  TF × IDF        │
                  └─────────┬────────┘
                            │
                            ▼
          ┌─────────────────────────────────┐
          │    Cosine Similarity            │
          │                                 │
          │         dot(A, B)               │
          │  cos(θ) = ──────────            │
          │         ||A|| × ||B||           │
          │                                 │
          │  Output: 0.0 - 1.0              │
          │  Convert to percentage: 0-100%  │
          └────────────────┬────────────────┘
                           │
                           ▼
          ┌─────────────────────────────────┐
          │    COMPATIBILITY SCORE           │
          │         75.3%                    │
          └──────────────────────────────────┘
```

**Figure 3: Natural Language Processing pipeline for resume analysis**

---

## DIAGRAM 4: ATS Scoring Algorithm

```
                    ┌─────────────────────┐
                    │  Parsed Resume Data │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Base Score: 70    │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   ┌─────────────┐      ┌─────────────┐     ┌─────────────┐
   │ Skills      │      │ Keywords    │     │ Structure   │
   │ Analysis    │      │ Density     │     │ Check       │
   └──────┬──────┘      └──────┬──────┘     └──────┬──────┘
          │                    │                    │
          ▼                    ▼                    ▼
   Has "Skills:"        High Keyword           Professional
   section?             Coverage?               Format?
          │                    │                    │
    ┌─────┴─────┐         ┌────┴────┐         ┌────┴────┐
    │           │         │         │         │         │
    Yes         No        Yes       No        Yes       No
    │           │         │         │         │         │
    +10         -25       +5        -5        +5        -10
    │           │         │         │         │         │
    └───────────┴─────────┴─────────┴─────────┴─────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Skill Count Check  │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
      0 skills            1-2 skills           8+ skills
        -25                  -15                  +5
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Final ATS Score    │
                    │                     │
                    │  Range: 0-100       │
                    │                     │
                    │  < 40: Poor         │
                    │  40-59: Fair        │
                    │  60-79: Good        │
                    │  80-100: Excellent  │
                    └─────────────────────┘
```

**Figure 4: Dynamic ATS scoring algorithm with context-aware penalties**

---

## DIAGRAM 5: Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              DEVELOPER WORKSTATION                           │
│                                                              │
│  ┌────────────────────────────────────────────┐            │
│  │  AWS SAM CLI                               │            │
│  │  • sam build                               │            │
│  │  • sam package                             │            │
│  │  • sam deploy                              │            │
│  └──────────────────┬─────────────────────────┘            │
└────────────────────┬┼────────────────────────────────────────┘
                     ││
                     │└────────────────┐
                     │                 │
                     ▼                 ▼
        ┌────────────────────┐  ┌────────────────────┐
        │  S3 DEPLOYMENT     │  │  CLOUDFORMATION    │
        │  BUCKET            │  │  SERVICE           │
        │                    │  │                    │
        │  • Lambda packages │  │  • Stack create    │
        │  • Template YAML   │  │  • Resource deploy │
        │  • Artifacts       │  │  • Rollback        │
        └────────────────────┘  └─────────┬──────────┘
                                          │
              ┌───────────────────────────┼───────────────────────────┐
              │                           │                           │
              ▼                           ▼                           ▼
   ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
   │  Lambda Function │      │  API Gateway     │      │  S3 Bucket       │
   │  Deployed        │      │  Endpoints       │      │  Created         │
   │                  │      │  Created         │      │                  │
   │  • Code updated  │      │  • Routes mapped │      │  • Policies set  │
   │  • Env vars set  │      │  • CORS enabled  │      │  • Encryption on │
   │  • Layers added  │      │  • Throttling    │      │                  │
   └──────────────────┘      └──────────────────┘      └──────────────────┘
              │                           │                           │
              └───────────────────────────┼───────────────────────────┘
                                          │
                                          ▼
                              ┌──────────────────────┐
                              │  CloudWatch Logs     │
                              │  Monitoring Enabled  │
                              └──────────────────────┘

                                          │
                                          ▼
                              ┌──────────────────────┐
                              │  PRODUCTION READY    │
                              │  ✓ Stack Complete    │
                              └──────────────────────┘
```

**Figure 5: Infrastructure deployment flow using AWS SAM and CloudFormation**

---

## DIAGRAM 6: Data Flow - Resume Analysis

```
┌──────────┐
│  USER    │
└────┬─────┘
     │ 1. Upload resume.pdf
     ▼
┌─────────────────┐
│  React Frontend │
└────┬────────────┘
     │ 2. POST /upload
     ▼
┌─────────────────┐
│  API Gateway    │
└────┬────────────┘
     │ 3. Invoke API Handler
     ▼
┌──────────────────────┐
│  Lambda: API Handler │
└────┬─────────────────┘
     │ 4. Generate presigned URL
     ▼
┌─────────────┐
│  S3 Bucket  │◄───── 5. Direct upload from browser
└─────────────┘
     │
     │ 6. POST /analyze {resume_key, job_description}
     ▼
┌──────────────────────┐
│  Lambda: API Handler │
└────┬─────────────────┘
     │ 7. Invoke Resume Parser
     ▼
┌──────────────────────┐
│ Lambda: Resume Parser│
│  • Download from S3  │
│  • Extract text      │
│  • Parse skills      │
│  • ATS scoring       │
└────┬─────────────────┘
     │ 8. Return parsed_data
     ▼
┌──────────────────────┐
│  Lambda: API Handler │
│  • Store in DynamoDB │
└────┬─────────────────┘
     │ 9. Invoke Score Calculator
     ▼
┌───────────────────────┐
│Lambda: Score Calc     │
│  • TF-IDF similarity  │
│  • Skill matching     │
│  • Cover letter gen   │
│  • Feedback creation  │
└────┬──────────────────┘
     │ 10. Return results
     ▼
┌──────────────────────┐
│  Lambda: API Handler │
│  • Update DynamoDB   │
│  • Format response   │
└────┬─────────────────┘
     │ 11. Return to API Gateway
     ▼
┌─────────────────┐
│  API Gateway    │
└────┬────────────┘
     │ 12. JSON Response
     ▼
┌─────────────────┐
│  React Frontend │
│  • Display score│
│  • Show charts  │
│  • Render letter│
└────┬────────────┘
     │ 13. Results displayed
     ▼
┌──────────┐
│  USER    │
└──────────┘
```

**Figure 6: Complete data flow for resume analysis from upload to results**

---

## DIAGRAM 7: Cost Optimization Strategy

```
                    ┌─────────────────────┐
                    │   Cost Optimization │
                    │   Strategies        │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   ┌─────────────┐      ┌─────────────┐     ┌─────────────┐
   │ Lambda      │      │ Storage     │     │ Data        │
   │ Optimization│      │ Efficiency  │     │ Transfer    │
   └──────┬──────┘      └──────┬──────┘     └──────┬──────┘
          │                    │                    │
          ▼                    ▼                    ▼
   • Memory sizing      • S3 Lifecycle      • CloudFront CDN
   • Execution time     • DynamoDB          • Edge caching
   • Provisioned        • On-demand         • Compression
     concurrency        • TTL cleanup       • Regional data
   • Code optimization  • Intelligent       • API caching
   • Layer reuse          tiering           
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Monthly Cost       │
                    │  1000 users:        │
                    │  $13-30 (vs $200+   │
                    │  traditional server)│
                    └─────────────────────┘
```

**Figure 7: Cost optimization techniques for serverless architecture**

---

## How to Use These Diagrams in IEEE Report

### In Microsoft Word (IEEE Template):

1. **Copy ASCII diagrams** into a monospace font text box:
   ```
   Insert → Text Box → Draw Text Box
   Paste diagram
   Font: Courier New, 8pt
   ```

2. **Or create visual diagrams** using:
   - Microsoft Visio
   - draw.io (free, online)
   - Lucidchart
   - PowerPoint SmartArt

3. **Insert as figures:**
   ```
   Insert → Pictures → [Select diagram image]
   Right-click → Insert Caption
   Format: "Figure X: [Description]"
   ```

4. **Reference in text:**
   ```
   "The system architecture (Figure 1) demonstrates..."
   "As shown in Figure 3, the NLP pipeline..."
   ```

---

## Recommended Placement in Report

| Diagram | Section | Page |
|---------|---------|------|
| Figure 1: System Architecture | II. System Architecture (A) | 2 |
| Figure 2: Lambda Flow | II. System Architecture (B) | 3 |
| Figure 3: NLP Algorithm | III. Methodology (B) | 4 |
| Figure 4: ATS Scoring | III. Methodology (B) | 4 |
| Figure 5: Deployment | IV. Implementation (C) | 5 |
| Figure 6: Data Flow | III. Methodology (A) | 3 |
| Figure 7: Cost Optimization | VII. Results (A) | 6 |

---

These diagrams provide complete visual documentation of your system!
