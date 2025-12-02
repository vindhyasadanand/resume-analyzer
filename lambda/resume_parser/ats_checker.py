"""
ATS (Applicant Tracking System) Checker
Analyzes resume for ATS compatibility
"""
import re

def check_ats_compatibility(text, resume_data):
    """
    Enhanced ATS compatibility checker
    Returns detailed ATS score and recommendations
    """
    score = 100
    issues = []
    recommendations = []
    text_lower = text.lower()
    
    # Check 1: Resume length (optimal 400-3000 chars)
    text_length = len(text)
    if text_length < 400:
        score -= 25
        issues.append("Resume is too brief - needs more detail")
        recommendations.append("Expand your resume with detailed descriptions of your experience and achievements")
    elif text_length > 5000:
        score -= 10
        issues.append("Resume is too lengthy")
        recommendations.append("Condense to 1-2 pages focusing on most relevant experience")
    
    # Check 2: Skills section (critical for ATS)
    skills_count = len(resume_data.get('skills', []))
    
    # Check if there's a skills section even if we didn't detect many
    has_skills_section = bool(re.search(r'(?:technical\s+)?skills?\s*:', text_lower, re.IGNORECASE))
    
    if skills_count == 0 and not has_skills_section:
        score -= 25
        issues.append("No technical skills section detected")
        recommendations.append("Add a dedicated Skills section with specific technologies and tools")
    elif skills_count == 0 and has_skills_section:
        score -= 10
        issues.append("Skills section found but couldn't parse specific technologies")
        recommendations.append("Use standard technology names (e.g., Python, JavaScript, AWS)")
    elif skills_count < 3:
        score -= 15
        issues.append(f"Limited technical skills detected - add more relevant technologies")
        recommendations.append("List 8-12 technical skills including languages, frameworks, and tools")
    elif skills_count < 6:
        score -= 5
        issues.append("Good start on skills, but could list more")
        recommendations.append("Expand skills section with additional relevant technologies")
    elif skills_count >= 8:
        score += 5  # Bonus for good skills coverage
    
    # Check 3: Education section
    education = resume_data.get('education', [])
    if not education:
        score -= 15
        issues.append("No education section found")
        recommendations.append("Include degree, major, university, and graduation year")
    else:
        # Check for degree keywords
        education_text = ' '.join(education).lower()
        if any(deg in education_text for deg in ['bachelor', 'master', 'phd', 'degree', 'university']):
            score += 5  # Bonus for clear education info
    
    # Check 4: Experience section with quantifiable details
    experience = resume_data.get('experience', {})
    positions = experience.get('positions', [])
    years = experience.get('years', 0)
    
    if not positions:
        score -= 20
        issues.append("No work experience details detected")
        recommendations.append("Add work history with company names, roles, dates, and responsibilities")
    else:
        # Check for date patterns (year formats)
        date_patterns = r'\b(19|20)\d{2}\b|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'
        dates_found = len(re.findall(date_patterns, text))
        if dates_found < 2:
            score -= 10
            issues.append("Missing dates in experience section")
            recommendations.append("Include start and end dates for each position (MM/YYYY format)")
    
    # Check 5: Action verbs and impact statements
    strong_verbs = [
        'achieved', 'improved', 'developed', 'implemented', 'designed', 'managed',
        'led', 'created', 'built', 'increased', 'reduced', 'optimized',
        'established', 'launched', 'delivered', 'architected', 'engineered'
    ]
    verb_count = sum(1 for verb in strong_verbs if verb in text_lower)
    
    if verb_count < 3:
        score -= 15
        issues.append("Limited use of strong action verbs")
        recommendations.append("Start bullet points with action verbs like 'developed', 'led', 'improved'")
    elif verb_count >= 8:
        score += 5  # Bonus for good verb usage
    
    # Check 6: Quantifiable achievements (numbers)
    numbers = re.findall(r'\d+[%+]|\$\d+|\d+x', text)
    if len(numbers) < 2:
        score -= 10
        issues.append("Few quantifiable achievements")
        recommendations.append("Add metrics and numbers to demonstrate impact (e.g., 'improved performance by 40%')")
    
    # Check 7: Contact information completeness
    has_email = '@' in text and '.' in text
    has_phone = bool(re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text))
    
    if not has_email:
        score -= 15
        issues.append("No email address found")
        recommendations.append("Add professional email address at the top of resume")
    
    if not has_phone:
        score -= 5
        issues.append("No phone number detected")
        recommendations.append("Include phone number in contact section")
    
    # Check 8: Professional summary/objective
    has_summary = any(word in text_lower for word in ['summary', 'objective', 'profile', 'about'])
    if not has_summary and text_length > 500:
        score -= 5
        issues.append("No professional summary section")
        recommendations.append("Consider adding a brief professional summary at the top")
    
    # Check 9: Keywords density (not too sparse, not keyword stuffing)
    words = text_lower.split()
    unique_words = set(words)
    if len(words) > 100:  # Only check if substantial text
        keyword_density = len(unique_words) / len(words)
        if keyword_density < 0.3:  # Too repetitive
            score -= 10
            issues.append("Content appears repetitive")
            recommendations.append("Diversify vocabulary and avoid excessive repetition")
    
    # Check 10: Section headers (good for ATS parsing)
    section_headers = ['experience', 'education', 'skills', 'projects', 'certifications']
    headers_found = sum(1 for header in section_headers if header in text_lower)
    if headers_found < 3:
        score -= 10
        issues.append("Missing standard section headers")
        recommendations.append("Use clear section headers: Experience, Education, Skills, etc.")
    
    # Ensure score is within bounds
    score = max(0, min(100, score))
    
    # Determine overall ATS compatibility
    if score >= 85:
        ats_rating = "Excellent"
    elif score >= 70:
        ats_rating = "Good"
    elif score >= 50:
        ats_rating = "Fair"
    else:
        ats_rating = "Needs Improvement"
    
    return {
        'score': score,
        'rating': ats_rating,
        'issues': issues[:8],  # Limit to top 8 issues
        'recommendations': recommendations[:8]
    }
