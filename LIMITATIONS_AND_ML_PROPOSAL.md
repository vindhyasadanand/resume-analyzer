# SYSTEM LIMITATIONS AND FUTURE IMPROVEMENTS

## Current Limitations

### 1. Domain-Specific Bias
**Issue:** The system is heavily optimized for software engineering and IT roles
- Pattern matching favors tech terms (script, base, flow, ware, sys, api, dev, ops)
- COMMON_SKILLS list contains primarily programming languages and frameworks
- Skill extraction looks for technical acronyms (AWS, SQL, API, etc.)

**Impact:**
- ❌ **Medical/Healthcare resumes:** Won't recognize clinical skills, medical procedures, certifications (ACLS, BLS, CPR)
- ❌ **Business/Marketing roles:** Misses SEO, PPC, market analysis, brand strategy
- ❌ **Legal professions:** Doesn't detect litigation, contract law, legal research
- ❌ **Creative fields:** Won't identify Adobe Creative Suite, UX design, video editing
- ❌ **Finance/Accounting:** Misses QuickBooks, financial modeling, audit experience
- ❌ **Education:** Doesn't recognize curriculum development, classroom management
- ❌ **Construction/Engineering:** Won't detect AutoCAD, structural analysis, project management

**Example Failures:**
```
Resume: "Certified Public Accountant with QuickBooks expertise"
Job: "Accountant needed - CPA required, QuickBooks experience"
Result: 0% match (both "CPA" and "QuickBooks" filtered as non-tech)
```

### 2. Pattern-Based Limitations
**Issue:** Relies on hardcoded patterns instead of semantic understanding

**Problems:**
- Can't understand context (e.g., "Java" the language vs "Java" the island)
- Misses synonyms and variations (e.g., "JS" vs "JavaScript" sometimes)
- Doesn't understand skill relationships (knowing React implies knowing JavaScript)
- Can't detect emerging technologies not in the pattern list

### 3. Skills Extraction Issues
**Issue:** Over-aggressive filtering removes valid skills

**Examples:**
- "Communication" → Filtered out (but it's a valid soft skill)
- "Leadership" → Filtered out (important for management roles)
- "Scalability" → Filtered out (but it's a real system design skill)

### 4. No Semantic Understanding
**Issue:** System doesn't understand meaning, only matches keywords

**Limitations:**
- Can't detect related skills (knowing Python + pandas ≈ data analysis)
- Doesn't understand skill levels (beginner vs expert)
- Can't infer skills from job titles (e.g., "Senior ML Engineer" → knows ML)
- Doesn't recognize certifications properly

### 5. Job Description Parsing
**Issue:** Assumes job descriptions are well-formatted with clear skill lists

**Problems:**
- Fails on poorly written job descriptions
- Misses skills mentioned in paragraphs vs bullet points
- Can't extract requirements vs nice-to-haves
- Doesn't understand "X years of experience in Y"

---

## Proposed Solution: Machine Learning Model

### Why ML Would Help

1. **Domain Agnostic**
   - Train on diverse job categories (tech, healthcare, business, creative, etc.)
   - Learn what constitutes a "skill" across different fields
   - Adapt to new domains without code changes

2. **Semantic Understanding**
   - Understand skill relationships (React → JavaScript, Python + pandas → Data Science)
   - Detect synonyms (JS = JavaScript, AWS = Amazon Web Services)
   - Context-aware extraction (Java programming vs Java coffee)

3. **Better Accuracy**
   - Named Entity Recognition (NER) for skill extraction
   - BERT/Transformer models for semantic similarity
   - Confidence scores for matches

### Recommended ML Approach

#### Option 1: Fine-tuned BERT Model (Best Quality)
**Architecture:**
```
Resume Text → BERT Encoder → Skill NER → Extracted Skills
Job Description → BERT Encoder → Required Skills
Both → Similarity Model → Match Score
```

**Advantages:**
- ✅ State-of-the-art accuracy
- ✅ Understands context and semantics
- ✅ Works across all domains
- ✅ Can be fine-tuned on job posting datasets

**Challenges:**
- ⚠️ Model size (400MB+ for BERT-base)
- ⚠️ Lambda 250MB deployment limit (need SageMaker or EFS)
- ⚠️ Slower inference (500ms-2s vs 100ms current)
- ⚠️ Higher cost ($0.20 per 1M chars vs $0.002 current)

**Implementation:**
```python
# Use Hugging Face Transformers
from transformers import pipeline

# Skill extraction
ner = pipeline("ner", model="jjzha/jobbert_skill_extraction")
skills = ner(resume_text)

# Similarity matching
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
similarity = model.similarity(resume_embedding, job_embedding)
```

#### Option 2: Lightweight spaCy NER (Balanced)
**Architecture:**
```
Resume → spaCy NER → Skills
Job Description → spaCy NER → Requirements
Skills ∩ Requirements → Match Score
```

**Advantages:**
- ✅ Lighter (40MB model)
- ✅ Fits in Lambda with custom layer
- ✅ Fast inference (100-300ms)
- ✅ Good accuracy for common cases

**Challenges:**
- ⚠️ Needs custom training for multi-domain skills
- ⚠️ Less accurate than BERT for semantic matching

**Implementation:**
```python
import spacy
nlp = spacy.load("en_core_web_sm")

# Custom NER training for skills
from spacy.training import Example
examples = [
    ("Python developer with 5 years experience", {"entities": [(0, 6, "SKILL")]})
]
nlp.update(examples)
```

#### Option 3: Hybrid Approach (Recommended)
**Combine pattern matching + lightweight ML**

```
1. Pattern matching (current) → Fast, high-precision for known tech skills
2. spaCy NER → Extract domain-specific skills
3. Sentence embeddings → Semantic similarity for final scoring
```

**Advantages:**
- ✅ Fast (200-400ms total)
- ✅ Works for tech + non-tech domains
- ✅ Fits in Lambda budget
- ✅ Incremental improvement (not a complete rewrite)

---

## Implementation Plan (3 Days)

### Day 1: Data Preparation & Model Selection
- [ ] Collect labeled dataset (job postings + resumes across domains)
- [ ] Choose model: spaCy custom NER + sentence-transformers
- [ ] Set up training pipeline
- [ ] Test locally

### Day 2: Integration
- [ ] Create Lambda layer with spaCy + model
- [ ] Update resume_parser to use NER
- [ ] Update score_calculator to use semantic similarity
- [ ] Test with diverse resumes (tech, medical, business)

### Day 3: Deployment & Validation
- [ ] Deploy to AWS Lambda
- [ ] Performance testing (latency, accuracy)
- [ ] A/B test against current system
- [ ] Documentation

---

## Quick Fix (Without ML) - 2 Hours

If you want to improve NOW without ML:

### 1. Add Domain Detection
```python
def detect_domain(text):
    domains = {
        'tech': ['python', 'java', 'aws', 'api', 'database'],
        'medical': ['patient', 'clinical', 'diagnosis', 'treatment'],
        'business': ['sales', 'marketing', 'roi', 'revenue'],
        'finance': ['accounting', 'audit', 'financial', 'ledger']
    }
    # Count matches per domain
    scores = {domain: sum(1 for kw in keywords if kw in text.lower()) 
              for domain, keywords in domains.items()}
    return max(scores, key=scores.get)
```

### 2. Domain-Specific Skill Lists
```python
SKILLS_BY_DOMAIN = {
    'tech': CURRENT_TECH_SKILLS,
    'medical': ['CPR', 'ACLS', 'BLS', 'EMR', 'HIPAA', 'patient care'],
    'business': ['SEO', 'PPC', 'CRM', 'Salesforce', 'market research'],
    'finance': ['QuickBooks', 'SAP', 'GAAP', 'financial modeling']
}
```

### 3. Use Universal Patterns
Instead of tech-specific patterns, use universal skill indicators:
- Certifications: "Certified X", "X Certification"
- Software: Proper nouns + "software", "tool", "platform"
- Proficiency statements: "proficient in X", "experienced with X"

---

## Recommendation

**For Dec 4 deadline:** Use current system + document limitations
**Post-deadline:** Implement Hybrid ML approach (Option 3) over winter break

Current system works **well for tech roles** (your target use case). Document limitations clearly in your report's "Future Work" section. This shows you understand the system's scope and have a roadmap for improvement.

**Want me to help implement the quick fix (2 hours) or prepare you for the ML approach?**
