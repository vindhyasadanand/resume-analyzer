import json
import boto3
from lambda_function import extract_resume_text
from score_calculator.lambda_function import calculate_score

dynamodb = boto3.resource('dynamodb')
table_name = 'ResumeAnalysisResults-dev'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    Handle batch comparison of a resume against multiple job descriptions
    """
    try:
        # Parse multipart form data
        body = event.get('body', '')
        if event.get('isBase64Encoded'):
            import base64
            body = base64.b64decode(body)
        
        # Extract resume file and jobs data from the request
        # In a real implementation, you'd parse multipart/form-data
        # For now, we'll assume the jobs are passed as JSON in the event
        
        resume_text = event.get('resume_text', '')
        jobs = json.loads(event.get('jobs', '[]'))
        
        if not resume_text or not jobs:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({'error': 'Resume text and jobs array are required'})
            }
        
        # Compare resume against each job
        results = []
        for job in jobs:
            job_title = job.get('title', 'Untitled Job')
            job_description = job.get('description', '')
            
            if not job_description.strip():
                continue
            
            # Calculate score using existing score calculator
            score_result = calculate_score(resume_text, job_description)
            
            # Extract feedback data
            feedback = score_result.get('feedback', {})
            
            results.append({
                'title': job_title,
                'score': float(score_result['compatibility_score']),
                'skill_match': float(score_result['skill_match']),
                'matched_skills': feedback.get('matched_skills_count', 0),
                'missing_skills': len(feedback.get('missing_keywords', [])),
                'strengths': feedback.get('strengths', 'Excellent skill set alignment'),
                'improvements': feedback.get('improvements', 'Tailor your resume to emphasize skills mentioned in the job description')
            })
        
        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'message': 'Batch comparison completed',
                'results': results
            })
        }
        
    except Exception as e:
        print(f"Error in batch comparison: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }
