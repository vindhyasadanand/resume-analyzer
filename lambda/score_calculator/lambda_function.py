"""
Score Calculator Lambda Function
Calculates compatibility score between resume and job description
using Enhanced TF-IDF with domain awareness (Lightweight Hybrid approach)
"""
import json
import boto3
import os
from datetime import datetime
import re
from collections import Counter
import math
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'ResumeAnalysisResults'))

def tokenize(text):
    """Tokenize text into words"""
    # Convert to lowercase and split into words
    text = text.lower()
    # Remove special characters and keep only alphanumeric and spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = text.split()
    
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'is', 'are', 'was', 'were', 'been', 'be', 'have', 'has',
        'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
        'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
        'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
        'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
        'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
        'so', 'than', 'too', 'very', 's', 't', 'just', 'don', 'now'
    }
    
    return [word for word in words if word and len(word) > 2 and word not in stop_words]

def compute_tf(tokens):
    """Compute term frequency"""
    tf_dict = {}
    token_count = len(tokens)
    counter = Counter(tokens)
    
    for word, count in counter.items():
        tf_dict[word] = count / token_count
    
    return tf_dict

def compute_idf(documents):
    """Compute inverse document frequency"""
    idf_dict = {}
    n_documents = len(documents)
    
    # Get all unique words
    all_words = set()
    for doc in documents:
        all_words.update(doc)
    
    # Calculate IDF for each word
    for word in all_words:
        doc_count = sum(1 for doc in documents if word in doc)
        idf_dict[word] = math.log(n_documents / (1 + doc_count))
    
    return idf_dict

def compute_tfidf(tf, idf):
    """Compute TF-IDF"""
    tfidf = {}
    for word, tf_value in tf.items():
        tfidf[word] = tf_value * idf.get(word, 0)
    return tfidf

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two TF-IDF vectors"""
    # Get all unique words
    all_words = set(vec1.keys()) | set(vec2.keys())
    
    # Calculate dot product
    dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in all_words)
    
    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    magnitude2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def calculate_enhanced_similarity(text1, text2):
    """
    Calculate enhanced TF-IDF similarity with domain-aware boosting.
    Lightweight hybrid approach without external ML libraries.
    """
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    
    # Standard TF-IDF calculation
    tf1 = compute_tf(tokens1)
    tf2 = compute_tf(tokens2)
    idf = compute_idf([tokens1, tokens2])
    tfidf1 = {word: tf1[word] * idf[word] for word in tf1}
    tfidf2 = {word: tf2[word] * idf[word] for word in tf2}
    
    base_similarity = cosine_similarity(tfidf1, tfidf2)
    
    # Boost similarity if there are exact technical keyword matches
    tech_boost = 0
    tokens1_set = set(tokens1)
    tokens2_set = set(tokens2)
    
    # Find technical terms that appear in both
    common_tech_terms = []
    for token in tokens1_set.intersection(tokens2_set):
        if is_technical_keyword(token):
            common_tech_terms.append(token)
    
    # Apply boost based on number of shared technical terms
    if len(common_tech_terms) > 0:
        # Each shared technical term adds a small boost (max 15% total)
        tech_boost = min(0.15, len(common_tech_terms) * 0.02)
    
    # Return boosted similarity (capped at 1.0)
    return min(1.0, base_similarity + tech_boost)

def is_technical_keyword(word, context_words=None):
    """
    Use NLP-based scoring to determine if a word is a technical keyword.
    Uses pattern recognition and semantic analysis instead of hardcoded lists.
    """
    word_lower = word.lower()
    
    # First, check against known technical domains (core technical terms only)
    tech_domains = {
        'languages': ['python', 'java', 'javascript', 'typescript', 'kotlin', 'swift', 'ruby', 
                      'php', 'golang', 'rust', 'scala', 'cpp', 'csharp', 'perl', 'dart', 'sql'],
        'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 
                       'fastapi', 'nextjs', 'gatsby', 'svelte', 'rails', 'laravel', 'dotnet', 'redux'],
        'cloud': ['aws', 'azure', 'gcp', 'ec2', 's3', 'lambda', 'dynamodb', 'cloudformation',
                  'terraform', 'ansible', 'puppet', 'chef', 'kubernetes', 'docker', 'k8s'],
        'databases': ['mongodb', 'postgresql', 'mysql', 'redis', 'cassandra', 'elasticsearch', 
                      'neo4j', 'oracle', 'sqlite', 'dynamodb', 'firebase', 'mariadb'],
        'tools': ['git', 'jenkins', 'gitlab', 'github', 'circleci', 'jira', 'gradle', 'maven', 
                  'npm', 'yarn', 'webpack', 'vite', 'babel'],
        'ml_ai': ['tensorflow', 'pytorch', 'keras', 'pandas', 'numpy', 'spark', 'scikit',
                  'hadoop', 'airflow', 'mlflow', 'sagemaker', 'opencv'],
        'testing': ['junit', 'pytest', 'jest', 'mocha', 'selenium', 'cypress', 'testng'],
        'protocols': ['graphql', 'grpc', 'websocket', 'mqtt', 'amqp', 'kafka', 'rabbitmq'],
    }
    
    # Check if word is in any technical domain
    for domain, keywords in tech_domains.items():
        if word_lower in keywords:
            return True
        # Check if word contains a technical term (e.g., "react-native" contains "react")
        if any(tech in word_lower for tech in keywords if len(tech) > 3):
            return True
    
    # Pattern-based detection for technical terms
    tech_patterns = [
        lambda w: w.endswith(('js', 'py', 'rb', 'go', 'rs')) and len(w) <= 10,  # Language extensions
        lambda w: w.endswith(('.js', '.py', '.java', '.cpp', '.rb')),  # File extensions
        lambda w: w.endswith(('sql', 'db', 'ql')) and len(w) > 2,  # Database/Query languages
        lambda w: any(x in w for x in ['sdk', 'ide', 'cli', 'orm', 'jwt', 'oauth', 'saml', 'xml', 'json', 'yaml']) and len(w) <= 15,  # Tech acronyms
    ]
    
    if any(pattern(word_lower) for pattern in tech_patterns):
        return True
    
    # Technical acronyms (2-4 uppercase letters)
    if len(word) <= 4 and word.isupper() and len(word) >= 2 and word.isalpha():
        return True
    
    # Semantic pattern recognition: technical words have specific characteristics
    # 1. Contains version numbers or dots (e.g., "node.js", "c++", "python3")
    if any(char in word_lower for char in ['.', '+']) and len(word_lower) <= 12:
        return True
    
    # 2. CamelCase or PascalCase (common in tech: "TypeScript", "JavaScript", "DevOps")
    if word[0].isupper() and any(c.isupper() for c in word[1:]) and len(word) > 3:
        return True
    
    # 3. Hyphenated technical compounds (e.g., "react-native", "end-to-end")
    if '-' in word_lower and len(word_lower) > 5:
        parts = word_lower.split('-')
        # At least one part should be a known technical term
        if any(part in tech_term for domain in tech_domains.values() for tech_term in domain for part in parts):
            return True
    
    # 4. Contains numbers (version indicators: python3, angular2, etc.)
    if any(c.isdigit() for c in word) and len(word) <= 15:
        # But not just numbers, must have letters too
        if any(c.isalpha() for c in word):
            return True
    
    # If none of the patterns match, it's likely not a technical keyword
    return False

def extract_keywords(text, top_n=20):
    """Extract top technical keywords from text using ML-inspired approach"""
    tokens = tokenize(text)
    
    # Get context words for better classification
    context_words = set(text.lower().split())
    
    # Core stop words - supplemented by pattern-based detection
    generic_words = {
        # Common verbs (will catch -ing forms with pattern detection)
        'experience', 'work', 'build', 'create', 'develop', 'implement', 'maintain',
        'design', 'write', 'test', 'deploy', 'drive', 'manage', 'lead', 'help',
        
        # Position-related terms
        'senior', 'junior', 'lead', 'principal', 'staff', 'associate', 'intern',
        'manager', 'director', 'engineer', 'engineers', 'developer', 'developers',
        'architect', 'consultant', 'team', 'teams', 'member', 'members',
        
        # Generic tech context words
        'product', 'products', 'project', 'projects', 'platform', 'platforms',
        'system', 'systems', 'service', 'services', 'application', 'applications',
        'solution', 'solutions', 'feature', 'features', 'component', 'components',
        'code', 'software', 'hardware', 'tool', 'tools', 'environment',
        
        # Time & quantities
        'years', 'year', 'months', 'month', 'day', 'days', 'experience',
        'millions', 'thousands', 'scale', 'least', 'active',
        
        # Role descriptors
        'requirements', 'responsibilities', 'duties', 'tasks', 'qualifications',
        'skills', 'skill', 'ability', 'knowledge', 'expertise', 'proficiency',
        
        # Common tech-adjacent words that aren't skills
        'production', 'field', 'based', 'related', 'using', 'native',
        'computer', 'machines', 'user', 'users', 'client', 'clients',
        'customer', 'customers', 'people', 'person', 'business', 'company'
    }
    
    # Use ML-inspired scoring: combine frequency + technical classification
    technical_tokens = []
    for token in tokens:
        # Skip generic words and very short words
        if token in generic_words or len(token) < 3:
            continue
        # Only include if it's classified as technical
        if is_technical_keyword(token, context_words):
            technical_tokens.append(token)
    
    # Score tokens by frequency (TF-IDF intuition)
    counter = Counter(technical_tokens)
    
    # Return top N most frequent technical keywords
    return [word for word, _ in counter.most_common(top_n)]

def is_likely_soft_skill_or_business_term(word):
    """
    Use linguistic patterns to detect soft skills and business terms.
    This is more scalable than maintaining a hardcoded list.
    """
    word_lower = word.lower().strip()
    
    # Pattern 1: Gerunds (ending in -ing) are often soft skills or actions
    if word_lower.endswith('ing') and len(word_lower) > 5:
        # Exceptions: some -ing words are technical (e.g., "testing", "profiling")
        tech_ing_words = {'testing', 'profiling', 'debugging', 'logging', 'caching', 
                          'hashing', 'parsing', 'rendering', 'scaling', 'monitoring'}
        if word_lower not in tech_ing_words:
            return True
    
    # Pattern 2: Abstract nouns ending in -tion, -ment, -ness, -ship, -ity
    if word_lower.endswith(('tion', 'sion', 'ment', 'ness', 'ship', 'ity', 'ance', 'ence')):
        return True
    
    # Pattern 3: Plural generic terms (teams, peers, partners, people, users)
    if word_lower.endswith('s') and len(word_lower) > 3:
        singular = word_lower[:-1]
        generic_plurals = ['team', 'peer', 'partner', 'people', 'person', 'member', 
                          'client', 'customer', 'user', 'engineer', 'developer', 'blocker', 'answer']
        if singular in generic_plurals or word_lower in [p + 's' for p in generic_plurals]:
            return True
    
    # Pattern 4: Adjectives ending in -ful, -ive, -able, -ible (meaningful, effective, scalable)
    if word_lower.endswith(('ful', 'ive', 'able', 'ible', 'ous', 'ent', 'ant')):
        return True
    
    # Pattern 5: Common action verbs (identify, escalate, coordinate, etc.)
    action_verbs = {'identify', 'escalate', 'coordinate', 'facilitate', 'enable', 'drive',
                    'ensure', 'provide', 'support', 'assist', 'help', 'deliver', 'achieve',
                    'establish', 'maintain', 'develop', 'create', 'build', 'implement',
                    'execute', 'perform', 'conduct', 'manage', 'oversee', 'direct'}
    if word_lower in action_verbs:
        return True
    
    # Pattern 6: Common soft skill roots
    soft_skill_roots = ['trust', 'leader', 'manage', 'collaborat', 'communi', 'organiz',
                       'motiv', 'passion', 'creativ', 'innov', 'strate', 'vision', 'escalat',
                       'integrit', 'hones', 'ethic', 'transparen', 'accountab', 'depend',
                       'cooperat', 'interpers', 'empath', 'adapt', 'resilien', 'patien', 'diligen']
    if any(root in word_lower for root in soft_skill_roots):
        return True
    
    # Pattern 7: Exact soft skill words (catch common ones directly)
    exact_soft_skills = {'trust', 'integrity', 'honesty', 'ethics', 'transparency',
                        'accountability', 'teamwork', 'leadership', 'empathy', 'patience',
                        'adaptability', 'flexibility', 'resilience', 'diligence'}
    if word_lower in exact_soft_skills:
        return True
    
    return False

def is_valid_skill(skill):
    """Check if extracted skill is valid and likely technical"""
    if not skill:
        return False
    
    skill_lower = skill.lower().strip()
    
    # Must be at least 2 characters
    if len(skill_lower) < 2:
        return False
    
    # Must contain at least one letter
    if not re.search(r'[a-zA-Z]', skill):
        return False
    
    # Single letters are not skills
    if len(skill_lower) == 1:
        return False
    
    # Check if it's a soft skill or business term
    if is_likely_soft_skill_or_business_term(skill):
        return False
    
    return True

def calculate_skill_match(resume_skills, job_description):
    """Calculate percentage of required skills matched with better accuracy"""
    # Filter out invalid skills
    resume_skills = [skill for skill in resume_skills if is_valid_skill(skill)]
    
    if not resume_skills:
        return 0.0, 0, 0
    
    job_text_lower = job_description.lower()
    job_tokens = set(tokenize(job_description))
    
    # Define skill synonyms for better matching
    skill_synonyms = {
        'python': ['python', 'py', 'python3'],
        'javascript': ['javascript', 'js', 'nodejs', 'node.js', 'node'],
        'java': ['java', 'jvm'],
        'react': ['react', 'reactjs', 'react.js'],
        'angular': ['angular', 'angularjs'],
        'vue': ['vue', 'vuejs', 'vue.js'],
        'docker': ['docker', 'containerization', 'containers'],
        'kubernetes': ['kubernetes', 'k8s'],
        'aws': ['aws', 'amazon web services', 'ec2', 's3', 'lambda'],
        'azure': ['azure', 'microsoft azure'],
        'gcp': ['gcp', 'google cloud', 'google cloud platform'],
        'sql': ['sql', 'mysql', 'postgresql', 'postgres', 'database'],
        'nosql': ['nosql', 'mongodb', 'cassandra', 'dynamodb'],
        'api': ['api', 'rest', 'restful', 'graphql'],
        'ci/cd': ['ci/cd', 'cicd', 'jenkins', 'github actions', 'gitlab'],
        'machine learning': ['machine learning', 'ml', 'ai', 'artificial intelligence'],
        'android': ['android', 'android sdk'],
        'ios': ['ios', 'swift', 'objective-c'],
        'kotlin': ['kotlin', 'kt']
    }
    
    matched_skills = []
    resume_skill_set = [skill.lower().strip() for skill in resume_skills if skill]
    
    for resume_skill in resume_skill_set:
        # Direct substring match in job description
        if resume_skill in job_text_lower:
            matched_skills.append(resume_skill)
            continue
        
        # Check with synonyms
        matched = False
        for canonical, variants in skill_synonyms.items():
            if resume_skill in variants:
                # Check if any variant is in job description
                if any(variant in job_text_lower for variant in variants):
                    matched_skills.append(resume_skill)
                    matched = True
                    break
        
        if matched:
            continue
        
        # Token-based matching for multi-word skills
        resume_skill_tokens = set(resume_skill.split())
        if resume_skill_tokens.issubset(job_tokens):
            matched_skills.append(resume_skill)
            continue
        
        # Partial match (at least 70% of skill tokens in job)
        if len(resume_skill_tokens) > 1:
            overlap = resume_skill_tokens.intersection(job_tokens)
            if len(overlap) / len(resume_skill_tokens) >= 0.7:
                matched_skills.append(resume_skill)
    
    if not resume_skill_set:
        return 0.0, 0, 0
    
    # Return: (percentage, matched_count, total_resume_skills)
    return (len(matched_skills) / len(resume_skill_set)) * 100, len(matched_skills), len(resume_skill_set)

def generate_feedback(score, skill_match, resume_data, job_keywords, job_description="", matched_count=0, total_resume_skills=0):
    """Generate detailed feedback with ML-inspired keyword filtering"""
    feedback = {
        'overall_score': round(score, 2),
        'skill_match_percentage': round(skill_match, 2),
        'matched_skills_count': matched_count,
        'total_resume_skills': total_resume_skills,
        'strengths': [],
        'improvements': [],
        'missing_keywords': [],
        'matched_skills': [],
        'resume_skills': resume_data.get('skills', [])
    }
    
    # Enhanced filtering for missing keywords
    non_skill_words = {
        'distributed', 'drive', 'end', 'engineer', 'features', 'platforms',
        'impactful', 'systems', 'services', 'tools', 'solutions', 'processes',
        'environment', 'infrastructure', 'architecture', 'implementation',
        'development', 'application', 'system', 'service', 'tool', 'solution',
        'process', 'feature', 'platform', 'component', 'module', 'library',
        'package', 'framework', 'project', 'product', 'user', 'users',
        'client', 'server', 'backend', 'frontend', 'fullstack', 'senior',
        'junior', 'lead', 'principal', 'staff', 'associate', 'intern',
        'mission', 'critical', 'scalable', 'reliable', 'efficient', 'optimize',
        'improve', 'enhance', 'develop', 'create', 'build', 'implement',
        'deploy', 'maintain', 'support', 'deliver', 'collaborate', 'work',
        'responsible', 'ownership', 'initiative', 'proactive', 'detail',
        'android', 'restful', 'apis', 'interest', 'learning', 'curiosity',
        'passion', 'motivated', 'team', 'communication', 'skills', 'ability',
        'years', 'knowledge', 'understanding', 'problem', 'solving', 'based',
        'machines', 'interested', 'excited', 'enthusiastic', 'eager', 'dedicated',
        'focused', 'oriented', 'minded', 'driven', 'proficiency', 'expertise',
        'professional', 'quality', 'best', 'practices', 'standards', 'requirements',
        'responsibilities', 'duties', 'tasks', 'activities', 'operations',
        # Additional soft skills and buzzwords
        'scalability', 'flexibility', 'reliability', 'availability', 'maintainability',
        'productivity', 'efficiency', 'performance', 'optimization', 'integration',
        'collaboration', 'innovation', 'creativity', 'leadership', 'management',
        'strategy', 'planning', 'execution', 'delivery', 'success', 'growth',
        'impact', 'value', 'excellence', 'commitment', 'dedication', 'passion',
        'experience', 'background', 'knowledge', 'expertise', 'proficiency',
        'capability', 'competency', 'skill', 'qualification', 'requirement',
        'strong', 'excellent', 'good', 'great', 'high', 'advanced', 'expert',
        # Soft skill words that should NEVER appear as technical skills
        'trust', 'trustworthy', 'integrity', 'honest', 'honesty', 'ethics', 'ethical',
        'transparency', 'accountable', 'accountability', 'dependable', 'reliable',
        'collaborative', 'cooperative', 'teamwork', 'interpersonal', 'empathy',
        'adaptable', 'flexible', 'resilient', 'patient', 'persistent', 'diligent'
    }
    
    # Find matched skills
    all_resume_skills = resume_data.get('skills', [])
    # Filter out invalid skills
    valid_resume_skills = [skill for skill in all_resume_skills if is_valid_skill(skill)]
    resume_skills_lower = {skill.lower(): skill for skill in valid_resume_skills}
    job_keywords_lower = set(kw.lower() for kw in job_keywords[:20])
    
    for skill_lower, skill_original in resume_skills_lower.items():
        if skill_lower in job_keywords_lower or any(skill_lower in kw or kw in skill_lower for kw in job_keywords_lower):
            feedback['matched_skills'].append(skill_original)
    
    # Strengths with more specific criteria
    if score >= 75:
        feedback['strengths'].append('Excellent match - Strong alignment with job requirements')
    elif score >= 60:
        feedback['strengths'].append('Good match with job requirements')
    
    if skill_match >= 70:
        feedback['strengths'].append('Excellent skill set alignment')
    elif skill_match >= 50:
        feedback['strengths'].append('Good technical skills coverage')
    
    if len(feedback['matched_skills']) > 8:
        feedback['strengths'].append(f'{len(feedback["matched_skills"])} highly relevant skills identified')
    elif len(feedback['matched_skills']) > 4:
        feedback['strengths'].append(f'{len(feedback["matched_skills"])} relevant skills matched')
    
    years_exp = resume_data.get('experience', {}).get('years', 0)
    if years_exp >= 5:
        feedback['strengths'].append(f'Strong experience background ({years_exp}+ years)')
    elif years_exp >= 2:
        feedback['strengths'].append(f'Good experience level ({years_exp}+ years)')
    
    # Improvements with actionable suggestions
    if score < 60:
        feedback['improvements'].append('Tailor your resume to emphasize skills mentioned in the job description')
    if skill_match < 50:
        feedback['improvements'].append('Add or highlight more technical skills from the job requirements')
    if len(feedback['matched_skills']) < 5:
        feedback['improvements'].append('Showcase more skills that directly align with the position')
    if years_exp < 2:
        feedback['improvements'].append('Highlight relevant projects and internships to demonstrate experience')
    if not resume_data.get('education'):
        feedback['improvements'].append('Include your educational background and relevant coursework')
    
    # SIMPLIFIED APPROACH: Extract technical keywords directly from job description
    # Only show keywords that appear explicitly in the job text
    job_lower = job_description.lower()
    
    # Define a comprehensive whitelist of technical terms
    tech_whitelist = {
        # Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
        'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'c', 'objective-c',
        # Frameworks
        'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'nextjs',
        'node.js', 'nodejs', 'node', 'fastapi', 'laravel', 'rails', '.net', 'asp.net',
        # Cloud/DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'k8s', 'terraform', 'ansible',
        'jenkins', 'gitlab', 'github', 'circleci', 'cloudformation', 'lambda', 'ec2', 's3',
        # Databases
        'sql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'dynamodb', 'cassandra',
        'elasticsearch', 'oracle', 'sqlite', 'mariadb',
        # ML/Data
        'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy', 'spark', 'hadoop',
        'scikit-learn', 'scikit', 'machine learning', 'ml', 'deep learning', 'ai',
        # Testing
        'junit', 'pytest', 'jest', 'mocha', 'selenium', 'cypress', 'testng',
        # Other
        'graphql', 'rest', 'restful', 'api', 'microservices', 'git', 'linux', 'unix', 'bash'
    }
    
    # Find technical terms mentioned in job description but missing from resume
    missing_technical = []
    for tech in tech_whitelist:
        # Check if technical term is in job description
        if tech in job_lower:
            # Check if it's NOT in resume skills (case-insensitive)
            if tech not in {s.lower() for s in resume_data.get('skills', [])}:
                missing_technical.append(tech)
    
    # Limit to 8 most important ones (prioritize by length - longer = more specific)
    missing_technical.sort(key=len, reverse=True)
    feedback['missing_keywords'] = missing_technical[:8]
    feedback['matched_skills'] = feedback['matched_skills'][:15]
    
    return feedback

def generate_cover_letter(resume_data, job_description):
    """Generate a personalized cover letter based on resume and job description"""
    
    # Extract key information
    skills = resume_data.get('skills', [])
    education = resume_data.get('education', [])
    experience_data = resume_data.get('experience', {})
    years_exp = experience_data.get('years', 0)
    positions = experience_data.get('positions', [])
    
    # Analyze job description for key requirements
    job_tokens = tokenize(job_description)
    job_keywords = extract_keywords(job_description, top_n=10)
    
    # Find matching skills
    matched_skills = []
    job_text_lower = job_description.lower()
    for skill in skills[:15]:
        if skill.lower() in job_text_lower:
            matched_skills.append(skill)
    
    # Select top 5 most relevant skills
    top_skills = matched_skills[:5] if len(matched_skills) >= 5 else skills[:5]
    
    # Identify key technical areas mentioned in job
    tech_areas = {
        'backend': ['backend', 'server', 'api', 'database', 'sql', 'python', 'java', 'node'],
        'frontend': ['frontend', 'react', 'angular', 'vue', 'javascript', 'ui', 'ux'],
        'cloud': ['aws', 'azure', 'gcp', 'cloud', 'serverless', 'lambda', 'docker', 'kubernetes'],
        'mobile': ['android', 'ios', 'mobile', 'swift', 'kotlin', 'react native'],
        'data': ['data', 'analytics', 'machine learning', 'ml', 'ai', 'tensorflow', 'spark'],
        'devops': ['devops', 'ci/cd', 'jenkins', 'gitlab', 'terraform', 'ansible']
    }
    
    relevant_areas = []
    for area, keywords in tech_areas.items():
        if any(kw in job_text_lower for kw in keywords):
            relevant_areas.append(area)
    
    # Build cover letter sections
    
    # Opening paragraph
    opening = "I am writing to express my strong interest in this position. "
    if years_exp >= 3:
        opening += f"With over {years_exp} years of professional experience in software development, "
    elif years_exp >= 1:
        opening += f"With {years_exp}+ years of hands-on experience in software engineering, "
    else:
        opening += "As a passionate software developer with a strong technical foundation, "
    
    opening += "I am excited about the opportunity to contribute to your team and help drive innovative solutions."
    
    # Skills paragraph
    skills_para = "My technical expertise aligns well with your requirements. "
    if top_skills:
        skills_list = ', '.join(top_skills[:3])
        if len(top_skills) > 3:
            skills_list += f", and {top_skills[3]}"
        skills_para += f"I have strong proficiency in {skills_list}, "
        
        if relevant_areas:
            area_desc = {
                'backend': 'building robust server-side applications',
                'frontend': 'creating engaging user interfaces',
                'cloud': 'designing scalable cloud architectures',
                'mobile': 'developing mobile applications',
                'data': 'implementing data-driven solutions',
                'devops': 'automating deployment pipelines'
            }
            capabilities = [area_desc[area] for area in relevant_areas[:2]]
            skills_para += f"which I have successfully applied in {' and '.join(capabilities)}."
        else:
            skills_para += "which I have successfully applied in various challenging projects."
    else:
        skills_para += "I have developed a comprehensive skill set that directly addresses your technical needs."
    
    # Experience paragraph
    exp_para = ""
    if years_exp >= 2:
        exp_para = "Throughout my professional journey, I have consistently delivered high-quality solutions and collaborated effectively with cross-functional teams. "
        if positions:
            exp_para += f"My experience includes working on {', '.join(positions[:2]) if len(positions) >= 2 else positions[0]}, "
        exp_para += "where I focused on writing clean, maintainable code and following best practices. "
        
        # Highlight achievements based on job keywords
        if any(kw in job_text_lower for kw in ['scale', 'scalable', 'performance', 'optimize']):
            exp_para += "I have a proven track record of optimizing application performance and building scalable systems. "
        if any(kw in job_text_lower for kw in ['agile', 'scrum', 'team', 'collaboration']):
            exp_para += "I thrive in agile environments and excel at collaborating with diverse teams to achieve project goals."
    elif years_exp >= 1:
        exp_para = "In my professional experience, I have gained hands-on expertise in software development and contributed to meaningful projects. "
        exp_para += "I am eager to bring my technical skills and enthusiasm to your team while continuing to grow as a developer."
    else:
        exp_para = "Through academic projects and practical applications, I have developed strong problem-solving abilities and a solid understanding of software development principles. "
        exp_para += "I am eager to apply my knowledge and contribute to real-world challenges at your organization."
    
    # Education paragraph (if relevant)
    edu_para = ""
    if education:
        edu_text = ' '.join(education).lower()
        if any(deg in edu_text for deg in ['bachelor', 'master', 'phd', 'degree']):
            edu_para = "My educational background in "
            if any(field in edu_text for field in ['computer science', 'software', 'engineering', 'cs']):
                edu_para += "Computer Science and Software Engineering "
            else:
                edu_para += "technology "
            edu_para += "has provided me with a strong theoretical foundation, which I complement with practical, hands-on experience. "
    
    # Closing paragraph
    closing = "I am excited about the prospect of joining your team and contributing to your innovative projects. "
    closing += "I am confident that my technical skills, problem-solving abilities, and passion for creating quality software "
    closing += "make me a strong fit for this role. I would welcome the opportunity to discuss how I can contribute to your team's success."
    
    # Assemble full letter
    cover_letter = {
        'opening': opening,
        'skills': skills_para,
        'experience': exp_para,
        'education': edu_para,
        'closing': closing,
        'full_text': f"{opening}\n\n{skills_para}\n\n{exp_para}\n\n{edu_para}\n\n{closing}".replace('\n\n\n', '\n\n').strip()
    }
    
    return cover_letter

def lambda_handler(event, context):
    """
    Lambda handler for score calculation
    Expects analysis_id and job_description in the request
    """
    try:
        print(f"Received event: {json.dumps(event)}")
        
        # Check if this is a cover letter generation request
        if isinstance(event, dict) and event.get('action') == 'generate_cover_letter':
            resume_data = event.get('resume_data')
            job_description = event.get('job_description')
            
            if not resume_data or not job_description:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': 'Missing resume_data or job_description'
                    })
                }
            
            cover_letter = generate_cover_letter(resume_data, job_description)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Cover letter generated successfully',
                    'cover_letter': cover_letter
                })
            }
        
        # Parse request body for normal scoring
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        analysis_id = body.get('analysis_id')
        job_description = body.get('job_description')
        
        if not analysis_id or not job_description:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Missing required fields: analysis_id and job_description'
                })
            }
        
        # Retrieve resume data from DynamoDB
        response = table.get_item(Key={'analysis_id': analysis_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Resume analysis not found'
                })
            }
        
        resume_data = response['Item']
        
        # Prepare texts for comparison
        resume_text = ' '.join([
            ' '.join(resume_data.get('skills', [])),
            ' '.join(resume_data.get('education', [])),
            ' '.join(resume_data.get('experience', {}).get('positions', []))
        ])
        
        # Calculate enhanced TF-IDF similarity with domain-aware boosting
        # Lightweight hybrid approach - no external ML libraries needed
        # Returns 0-1, we'll convert to percentage in final_score calculation
        similarity_score = calculate_enhanced_similarity(resume_text, job_description)
        
        # Calculate skill match percentage
        skill_match, matched_count, total_resume_skills = calculate_skill_match(resume_data.get('skills', []), job_description)
        
        # Enhanced weighted scoring with multiple factors
        # Weights: TF-IDF similarity (40%), Skill match (35%), Experience relevance (15%), Education (10%)
        
        # Check experience relevance
        experience_score = 0
        if resume_data.get('experience', {}).get('years', 0) > 0:
            years = resume_data['experience']['years']
            if 'years' in job_description.lower() or 'experience' in job_description.lower():
                # Extract required years from job description
                import re
                year_matches = re.findall(r'(\d+)\+?\s*year', job_description.lower())
                if year_matches:
                    required_years = max([int(y) for y in year_matches])
                    experience_score = min(100, (years / required_years) * 100) if required_years > 0 else 50
                else:
                    experience_score = min(100, years * 20)  # 5 years = 100%
            else:
                experience_score = min(100, years * 20)
        
        # Check education relevance
        education_score = 0
        if resume_data.get('education'):
            education_text = ' '.join(resume_data['education']).lower()
            job_lower = job_description.lower()
            
            # Check for degree match
            if any(deg in education_text for deg in ['phd', 'doctorate']):
                education_score = 100
            elif any(deg in education_text for deg in ['master', 'msc', 'ms', 'mba']):
                education_score = 85
            elif any(deg in education_text for deg in ['bachelor', 'bsc', 'bs', 'be', 'btech']):
                education_score = 70
            
            # Boost if relevant field
            relevant_fields = ['computer science', 'software', 'engineering', 'information technology', 'cs']
            if any(field in education_text for field in relevant_fields):
                education_score = min(100, education_score + 15)
        
        # Calculate weighted final score (all components are 0-100 scale)
        # similarity_score is 0-1, multiply by 100 to get percentage
        # Then apply weights: 40% similarity, 35% skills, 15% experience, 10% education
        final_score = (
            (similarity_score * 100) * 0.40 +
            skill_match * 0.35 +
            experience_score * 0.15 +
            education_score * 0.10
        )
        
        # Ensure score is capped at 100
        final_score = min(100, max(0, final_score))
        
        # Extract job keywords
        job_keywords = extract_keywords(job_description)
        
        # Generate feedback
        feedback = generate_feedback(final_score, skill_match, resume_data, job_keywords, job_description, matched_count, total_resume_skills)
        
        # Convert float values to Decimal for DynamoDB
        def convert_floats(obj):
            if isinstance(obj, float):
                return Decimal(str(obj))
            elif isinstance(obj, dict):
                return {k: convert_floats(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_floats(item) for item in obj]
            return obj
        
        feedback_decimal = convert_floats(feedback)
        
        # Update DynamoDB with results
        table.update_item(
            Key={'analysis_id': analysis_id},
            UpdateExpression='SET #score = :score, #feedback = :feedback, #job_desc = :job_desc, #scored_at = :scored_at, #status = :status',
            ExpressionAttributeNames={
                '#score': 'score',
                '#feedback': 'feedback',
                '#job_desc': 'job_description',
                '#scored_at': 'scored_at',
                '#status': 'status'
            },
            ExpressionAttributeValues={
                ':score': feedback_decimal['overall_score'],
                ':feedback': feedback_decimal,
                ':job_desc': job_description[:500],  # Store first 500 chars
                ':scored_at': datetime.now().isoformat(),
                ':status': 'completed'
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Score calculated successfully',
                'analysis_id': analysis_id,
                'results': {
                    'compatibility_score': feedback['overall_score'],
                    'skill_match': feedback['skill_match_percentage'],
                    'feedback': feedback
                }
            })
        }
        
    except Exception as e:
        print(f"Error calculating score: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Failed to calculate score',
                'details': str(e)
            })
        }
