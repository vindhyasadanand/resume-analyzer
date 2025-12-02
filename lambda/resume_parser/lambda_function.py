"""
Resume Parser Lambda Function
Extracts skills, education, and experience from uploaded resumes
"""
import json
import boto3
import re
import os
from datetime import datetime
import io
from ats_checker import check_ats_compatibility

# Import PDF parsing
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

# No external NLP library needed - using enhanced pattern matching

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'ResumeAnalysisResults'))

# Domain-specific skills database
SKILLS_BY_DOMAIN = {
    'tech': [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
        'php', 'swift', 'kotlin', 'scala', 'perl', 'matlab', 'r programming', 'sql', 'plsql',
        'objective-c', 'dart', 'elixir', 'clojure', 'haskell', 'groovy',
    # Web Technologies
    'html', 'html5', 'css', 'css3', 'sass', 'scss', 'less', 'react', 'reactjs', 'react.js',
    'angular', 'angularjs', 'vue', 'vue.js', 'vuejs', 'svelte', 'nextjs', 'next.js',
    'node.js', 'nodejs', 'express', 'expressjs', 'django', 'flask', 'spring', 'spring boot',
    'asp.net', 'fastapi', 'nestjs', 'laravel', 'ruby on rails', 'redux', 'webpack', 'vite',
    # Mobile Development
    'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova',
    # Cloud & DevOps
    'aws', 'amazon web services', 'azure', 'microsoft azure', 'gcp', 'google cloud',
    'docker', 'kubernetes', 'k8s', 'jenkins', 'terraform', 'ansible', 'puppet', 'chef',
    'ci/cd', 'circleci', 'travis ci', 'git', 'github', 'gitlab', 'bitbucket', 'svn',
    'cloudformation', 'serverless', 'lambda', 'ec2', 's3', 'cloudwatch', 'ecs', 'eks',
    # Databases
    'mysql', 'postgresql', 'mongodb', 'redis', 'dynamodb', 'cassandra', 'elasticsearch',
    'mariadb', 'oracle', 'sql server', 'sqlite', 'neo4j', 'couchdb', 'firestore',
    # Data Science & ML
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
    'pandas', 'numpy', 'scipy', 'spark', 'apache spark', 'hadoop', 'data analysis',
    'nlp', 'natural language processing', 'computer vision', 'opencv', 'data mining',
    'statistical analysis', 'jupyter', 'tableau', 'power bi', 'data visualization',
    # Testing & Quality
    'testing', 'unit testing', 'integration testing', 'junit', 'pytest', 'jest', 'mocha',
    'selenium', 'cypress', 'testng', 'cucumber', 'tdd', 'bdd', 'qa', 'quality assurance',
    # Other
    'agile', 'scrum', 'kanban', 'jira', 'confluence', 'rest api', 'restful', 'graphql',
    'microservices', 'linux', 'unix', 'bash', 'shell scripting', 'api development',
        'oauth', 'jwt', 'websockets', 'grpc', 'rabbitmq', 'kafka', 'nginx', 'apache',
        'mvc', 'mvvm', 'design patterns', 'oop', 'functional programming', 'distributed systems'
    ],
    'medical': [
        'patient care', 'clinical', 'diagnosis', 'treatment', 'healthcare', 'nursing',
        'cpr', 'bls', 'acls', 'pals', 'emr', 'ehr', 'epic', 'cerner', 'meditech',
        'hipaa', 'medical terminology', 'pharmacology', 'anatomy', 'physiology',
        'surgery', 'emergency medicine', 'critical care', 'icu', 'er',
        'radiology', 'cardiology', 'oncology', 'pediatrics', 'obstetrics',
        'medical records', 'icd-10', 'cpt coding', 'medical billing',
        'phlebotomy', 'iv therapy', 'wound care', 'vital signs', 'medications'
    ],
    'business': [
        'sales', 'marketing', 'seo', 'sem', 'ppc', 'google ads', 'facebook ads',
        'content marketing', 'email marketing', 'social media', 'crm', 'salesforce',
        'hubspot', 'market research', 'competitive analysis', 'roi', 'kpi',
        'brand management', 'digital marketing', 'analytics', 'google analytics',
        'campaign management', 'lead generation', 'conversion optimization',
        'b2b', 'b2c', 'ecommerce', 'shopify', 'magento', 'wordpress',
        'copywriting', 'content strategy', 'customer acquisition', 'retention',
        'market segmentation', 'positioning', 'pricing strategy', 'distribution'
    ],
    'finance': [
        'accounting', 'bookkeeping', 'financial analysis', 'budgeting', 'forecasting',
        'quickbooks', 'sage', 'sap', 'oracle financials', 'gaap', 'ifrs',
        'financial reporting', 'audit', 'tax preparation', 'accounts payable',
        'accounts receivable', 'payroll', 'reconciliation', 'general ledger',
        'financial modeling', 'valuation', 'investment analysis', 'portfolio management',
        'risk management', 'derivatives', 'fixed income', 'equity research',
        'excel', 'vba', 'financial statements', 'cash flow analysis', 'variance analysis',
        'cpa', 'cfa', 'cma', 'cia', 'sox compliance', 'internal controls'
    ]
}

# For backward compatibility
COMMON_SKILLS = SKILLS_BY_DOMAIN['tech']

# Domain detection keywords
DOMAIN_KEYWORDS = {
    'tech': ['software', 'developer', 'engineer', 'programmer', 'coding', 'programming',
             'application', 'system', 'database', 'server', 'api', 'framework', 'library',
             'frontend', 'backend', 'fullstack', 'devops', 'cloud', 'mobile', 'web'],
    'medical': ['patient', 'clinical', 'medical', 'healthcare', 'hospital', 'physician',
                'nurse', 'doctor', 'surgery', 'diagnosis', 'treatment', 'care', 'health',
                'medicine', 'therapeutic', 'clinic', 'emergency', 'pharmacy'],
    'business': ['sales', 'marketing', 'revenue', 'customer', 'client', 'market', 'brand',
                 'campaign', 'strategy', 'business', 'commercial', 'account', 'partner',
                 'vendor', 'proposal', 'negotiation', 'pipeline', 'quota'],
    'finance': ['financial', 'accounting', 'audit', 'tax', 'budget', 'ledger', 'payroll',
                'invoice', 'revenue', 'expense', 'profit', 'loss', 'balance sheet',
                'income statement', 'cash flow', 'investment', 'portfolio', 'asset']
}

def detect_domain(text):
    """Detect the primary domain of a resume/job description"""
    text_lower = text.lower()
    domain_scores = {}
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        domain_scores[domain] = score
    
    # Return domain with highest score, default to 'tech'
    if max(domain_scores.values()) == 0:
        return 'tech'
    return max(domain_scores, key=domain_scores.get)

# Invalid skills to filter out
INVALID_SKILLS = {
    # Single letters/characters
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    # Common words that aren't skills
    'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'the', 'is', 'it',
    'with', 'from', 'by', 'as', 'an', 'be', 'this', 'that', 'have', 'has',
    'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may',
    'might', 'can', 'must', 'shall', 'am', 'are', 'was', 'were', 'been'
}

def looks_like_tech_skill(skill):
    """Use linguistic patterns to determine if something is likely a technical skill"""
    skill_lower = skill.lower().strip()
    
    # Pattern 1: Contains numbers (Python3, Angular2, SQL2019)
    if any(c.isdigit() for c in skill_lower):
        return True
    
    # Pattern 2: Contains dots (node.js, .NET, vue.js)
    if '.' in skill_lower and len(skill_lower) <= 15:
        return True
    
    # Pattern 3: Contains hyphens (react-native, test-driven-development)
    if '-' in skill_lower and len(skill_lower) >= 5:
        return True
    
    # Pattern 4: Contains + or # (C++, C#, .NET)
    if any(c in skill_lower for c in ['+', '#']):
        return True
    
    # Pattern 5: All caps 2-5 letters (AWS, SQL, API, REST, CI/CD)
    if skill.isupper() and 2 <= len(skill) <= 5 and skill.isalpha():
        return True
    
    # Pattern 6: Tech-specific word parts
    tech_parts = ['script', 'base', 'flow', 'ware', 'sys', 'sql', 'data',
                  'web', 'net', 'cloud', 'micro', 'api', 'dev', 'ops', 'bot',
                  'app', 'mobile', 'server', 'client', 'proto', 'graph']
    if any(part in skill_lower for part in tech_parts):
        return True
    
    # Pattern 7: Common programming language patterns
    lang_patterns = ['python', 'java', 'ruby', 'rust', 'swift', 'kotlin',
                    'scala', 'perl', 'php', 'bash', 'shell', 'react', 'angular',
                    'vue', 'node', 'django', 'flask', 'spring', 'docker', 'kubernetes']
    if any(lang in skill_lower for lang in lang_patterns):
        return True
    
    return False

def is_valid_skill(skill):
    """Check if extracted skill is valid using pattern recognition"""
    skill_lower = skill.lower().strip()
    
    # Basic validation
    if skill_lower in INVALID_SKILLS or len(skill_lower) < 2:
        return False
    
    if not re.search(r'[a-zA-Z]', skill) or skill.isdigit():
        return False
    
    # Pattern-based soft skill detection (reject these)
    soft_skill_patterns = [
        # Ends in -ing (but not tech terms)
        lambda s: s.endswith('ing') and not any(t in s for t in ['testing', 'programming', 'debugging', 'logging', 'caching', 'parsing', 'rendering', 'scaling', 'monitoring', 'computing', 'processing', 'engineering', 'modeling', 'training']),
        # Ends in abstract noun suffixes
        lambda s: s.endswith(('ness', 'ship', 'hood', 'dom')) and not any(t in s for t in ['relationship']),
        # Ends in -tion/-sion (but not tech terms)
        lambda s: s.endswith(('tion', 'sion')) and not any(t in s for t in ['authentication', 'authorization', 'implementation', 'configuration', 'automation', 'virtualization', 'integration', 'migration']),
        # Ends in -ment (but not tech terms)
        lambda s: s.endswith('ment') and not any(t in s for t in ['development', 'deployment', 'environment', 'management']),
        # Ends in -ance/-ence
        lambda s: s.endswith(('ance', 'ence')) and not any(t in s for t in ['performance', 'intelligence', 'compliance']),
        # Ends in -ful/-ive/-able/-ible (adjectives)
        lambda s: s.endswith(('ful', 'ive', 'able', 'ible', 'ous', 'ent', 'ant')),
        # Common soft skill words
        lambda s: s in {'clinical', 'others', 'matters', 'details', 'various', 'multiple',
                       'several', 'strong', 'excellent', 'great', 'issues', 'needs',
                       'results', 'benefits', 'values', 'people', 'teams', 'ways'}
    ]
    
    # If it matches soft skill patterns, check if it has tech characteristics
    if any(pattern(skill_lower) for pattern in soft_skill_patterns):
        # Only accept if it clearly looks like a tech skill
        if not looks_like_tech_skill(skill):
            return False
    
    return True

def extract_text_from_pdf(file_content):
    """Extract text from PDF file"""
    if fitz is None:
        return None
    
    try:
        pdf_document = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        pdf_document.close()
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {str(e)}")
        return None

def extract_skills(text):
    """Extract skills from resume text using domain-aware pattern matching"""
    found_skills = []
    text_lower = text.lower()
    
    # Detect domain first
    domain = detect_domain(text)
    domain_skills = SKILLS_BY_DOMAIN.get(domain, SKILLS_BY_DOMAIN['tech'])
    
    # Method 1: Match against domain-specific skills list
    for skill in domain_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    
    # Method 2: Extract from Skills section with enhanced parsing
    skills_section_patterns = [
        # "Skills:" or "Technical Skills:" section
        r'(?:technical\s+)?skills?\s*:?\s*\n((?:[^\n]+\n?)+?)(?:\n\n|(?=[A-Z][a-z]+\s*:)|\Z)',
        # "Key Skills" or "Core Competencies"
        r'(?:key|core)\s+(?:technical\s+)?(?:skills|competencies|technologies)\s*:?\s*\n((?:[^\n]+\n?)+?)(?:\n\n|(?=[A-Z][a-z]+\s*:)|\Z)',
        # "Technologies Used"
        r'technologies?\s+(?:used|known|familiar)\s*:?\s*\n?((?:[^\n]+\n?)+?)(?:\n\n|(?=[A-Z][a-z]+\s*:)|\Z)',
        # "Programming Languages"
        r'programming\s+languages?\s*:?\s*\n?((?:[^\n]+\n?)+?)(?:\n\n|(?=[A-Z][a-z]+\s*:)|\Z)'
    ]
    
    for pattern in skills_section_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            skills_text = match.group(1)
            # Split by various separators
            potential_skills = re.split(r'[,;•●○▪▫|・\n\t&]', skills_text)
            
            for skill in potential_skills:
                skill = skill.strip()
                # Remove leading bullets/dashes/numbers/parentheses
                skill = re.sub(r'^[-–—\s*\d.()[\]]+', '', skill)
                # Remove trailing parentheses content (e.g., "Python (Expert)")
                skill = re.sub(r'\s*\([^)]*\)\s*$', '', skill)
                skill = skill.strip()
                
                if 2 <= len(skill) <= 35 and is_valid_skill(skill):
                    found_skills.append(skill)
    
    # Method 3: ONLY extract well-known CamelCase tech terms (strict whitelist)
    camel_case_tech = {
        'JavaScript', 'TypeScript', 'DevOps', 'GraphQL', 'MongoDB', 'PostgreSQL',
        'MySQL', 'DynamoDB', 'CloudFormation', 'CloudFront', 'GitHub', 'GitLab',
        'BitBucket', 'TensorFlow', 'PyTorch', 'PowerShell', 'AutoCAD'
    }
    for tech in camel_case_tech:
        if tech in text:
            found_skills.append(tech)
    
    # Method 4: ONLY extract known tech acronyms (strict whitelist)
    tech_acronyms = {
        'AWS', 'GCP', 'SQL', 'API', 'REST', 'HTTP', 'HTTPS', 'JSON', 'XML', 
        'HTML', 'CSS', 'iOS', 'SDK', 'IDE', 'CLI', 'ORM', 'JWT',
        'CI/CD', 'ML', 'AI', 'NLP', 'UI', 'UX', 'DOM', 'SPA',
        'MVC', 'MVVM', 'TDD', 'BDD', 'OOP', 'ETL', 'CRUD', 'AJAX'
    }
    acronym_pattern = r'\b([A-Z]{2,6}(?:/[A-Z]{2,6})?)\b'
    matches = re.findall(acronym_pattern, text)
    for match in matches:
        if match in tech_acronyms:
            found_skills.append(match)
    
    # Method 5: Extract .js, .py framework names (node.js, vue.js, etc.)
    dotjs_pattern = r'\b([a-z]+\.js)\b'
    matches = re.findall(dotjs_pattern, text_lower)
    for match in matches:
        if len(match) <= 12:  # Reasonable length
            found_skills.append(match)
    
    # Filter and validate all extracted skills
    valid_skills = []
    for skill in found_skills:
        skill_clean = skill.strip()
        if is_valid_skill(skill_clean) and len(skill_clean) >= 2:
            valid_skills.append(skill_clean)
    
    # Remove duplicates (case-insensitive) while preserving original casing
    seen = set()
    unique_skills = []
    for skill in valid_skills:
        skill_lower = skill.lower().strip()
        if skill_lower not in seen:
            seen.add(skill_lower)
            unique_skills.append(skill)
    
    # Sort by length (prefer full names over abbreviations) and limit
    unique_skills.sort(key=lambda x: (-len(x), x.lower()))
    return unique_skills[:50]  # Return top 50 skills

def extract_education(text):
    """Extract education information"""
    education = []
    
    # Degree patterns
    degree_patterns = [
        r'(bachelor|b\.?s\.?|b\.?a\.?|master|m\.?s\.?|m\.?a\.?|phd|ph\.?d\.?|doctorate)\s+(of|in)?\s+([a-zA-Z\s]+)',
        r'(undergraduate|graduate)\s+degree\s+in\s+([a-zA-Z\s]+)'
    ]
    
    for pattern in degree_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            education.append(match.group(0).strip())
    
    # Universities
    university_pattern = r'(university|college|institute)\s+of\s+([a-zA-Z\s]+)|([a-zA-Z\s]+)\s+(university|college|institute)'
    matches = re.finditer(university_pattern, text, re.IGNORECASE)
    for match in matches:
        education.append(match.group(0).strip())
    
    return list(set(education))[:5]  # Limit to 5 entries

def extract_experience(text):
    """Extract years of experience and job titles"""
    experience = {
        'years': 0,
        'positions': []
    }
    
    # Extract years of experience
    year_patterns = [
        r'(\d+)\+?\s*years?\s*(of)?\s*experience',
        r'experience\s*[:\-]?\s*(\d+)\+?\s*years?'
    ]
    
    for pattern in year_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            years = int(match.group(1))
            if years > experience['years']:
                experience['years'] = years
    
    # Extract job titles (common patterns)
    job_titles = [
        'software engineer', 'developer', 'data scientist', 'analyst', 'manager',
        'architect', 'consultant', 'designer', 'administrator', 'specialist',
        'lead', 'senior', 'junior', 'intern', 'director', 'coordinator'
    ]
    
    for title in job_titles:
        pattern = r'\b' + re.escape(title) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            experience['positions'].append(title)
    
    experience['positions'] = list(set(experience['positions']))[:10]
    
    return experience

def lambda_handler(event, context):
    """
    Lambda handler for resume parsing
    Triggered by S3 upload event or API Gateway request
    """
    try:
        print(f"Received event: {json.dumps(event)}")
        
        # Handle S3 trigger
        if 'Records' in event and event['Records'][0].get('eventSource') == 'aws:s3':
            bucket = event['Records'][0]['s3']['bucket']['name']
            key = event['Records'][0]['s3']['object']['key']
        # Handle API Gateway request
        elif 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
            bucket = body.get('bucket')
            key = body.get('key')
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid event format'})
            }
        
        # Download file from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read()
        
        # Extract text based on file type
        if key.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_content)
            if text is None:
                text = file_content.decode('utf-8', errors='ignore')
        else:
            text = file_content.decode('utf-8', errors='ignore')
        
        # Parse resume
        skills = extract_skills(text)
        education = extract_education(text)
        experience = extract_experience(text)
        
        # Check ATS compatibility
        ats_data = check_ats_compatibility(text, {
            'skills': skills,
            'education': education,
            'experience': experience
        })
        
        # Prepare result
        analysis_id = f"{key.split('/')[-1]}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        result = {
            'analysis_id': analysis_id,
            'resume_key': key,
            'skills': skills,
            'education': education,
            'experience': experience,
            'ats_score': ats_data,
            'raw_text_length': len(text),
            'parsed_at': datetime.now().isoformat(),
            'status': 'parsed'
        }
        
        # Store in DynamoDB
        table.put_item(Item=result)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Resume parsed successfully',
                'analysis_id': analysis_id,
                'data': result
            })
        }
        
    except Exception as e:
        print(f"Error processing resume: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Failed to parse resume',
                'details': str(e)
            })
        }
