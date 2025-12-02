"""
API Handler Lambda Function
Provides REST API endpoints for the resume analyzer
"""
import json
import boto3
import os
import uuid
from datetime import datetime
from decimal import Decimal

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'ResumeAnalysisResults'))
lambda_client = boto3.client('lambda')

BUCKET_NAME = os.environ.get('S3_BUCKET', 'resume-analyzer-uploads')
PARSER_FUNCTION = os.environ.get('PARSER_FUNCTION', 'resume-parser')
SCORER_FUNCTION = os.environ.get('SCORER_FUNCTION', 'score-calculator')

def convert_decimals(obj):
    """Convert Decimal objects to float for JSON serialization"""
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

def generate_presigned_url(bucket, key, content_type='application/octet-stream', expiration=3600):
    """Generate a presigned URL for S3 upload"""
    try:
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket,
                'Key': key,
                'ContentType': content_type
            },
            ExpiresIn=expiration
        )
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {str(e)}")
        return None

def lambda_handler(event, context):
    """
    Main API Gateway handler
    Routes: 
    - POST /upload - Get presigned URL for resume upload
    - POST /analyze - Trigger full analysis (parse + score)
    - GET /results/{analysis_id} - Get analysis results
    """
    try:
        print(f"Full event: {json.dumps(event)}")
        
        # Handle both HTTP API (v2) and REST API (v1) format
        # HTTP API v2 format
        http_method = event.get('requestContext', {}).get('http', {}).get('method', '')
        path = event.get('requestContext', {}).get('http', {}).get('path', '')
        
        # Fallback to REST API v1 format
        if not http_method:
            http_method = event.get('httpMethod', '')
        if not path:
            path = event.get('path', '')
        
        # Also check rawPath
        raw_path = event.get('rawPath', '')
        if raw_path and not path:
            path = raw_path
        
        print(f"Method: {http_method}, Path: {path}")
        
        # Use rawPath if available (HTTP API v2)
        if raw_path:
            path = raw_path
        
        # CORS preflight
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key',
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
                },
                'body': ''
            }
        
        # POST /upload - Generate presigned URL
        if http_method == 'POST' and '/upload' in path:
            body = json.loads(event.get('body', '{}'))
            filename = body.get('filename', f'resume_{uuid.uuid4()}.pdf')
            file_type = body.get('fileType', 'application/pdf')
            
            # Generate unique key
            key = f"resumes/{datetime.now().strftime('%Y/%m/%d')}/{uuid.uuid4()}_{filename}"
            
            presigned_url = generate_presigned_url(BUCKET_NAME, key, file_type)
            
            if presigned_url:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'upload_url': presigned_url,
                        'key': key,
                        'bucket': BUCKET_NAME
                    })
                }
            else:
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Failed to generate upload URL'})
                }
        
        # POST /analyze - Run full analysis
        elif http_method == 'POST' and '/analyze' in path:
            body = json.loads(event.get('body', '{}'))
            resume_key = body.get('resume_key')
            job_description = body.get('job_description')
            
            if not resume_key or not job_description:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Missing required fields: resume_key and job_description'
                    })
                }
            
            # Step 1: Invoke parser Lambda
            parser_payload = {
                'body': json.dumps({
                    'bucket': BUCKET_NAME,
                    'key': resume_key
                })
            }
            
            parser_response = lambda_client.invoke(
                FunctionName=PARSER_FUNCTION,
                InvocationType='RequestResponse',
                Payload=json.dumps(parser_payload)
            )
            
            parser_result = json.loads(parser_response['Payload'].read())
            parser_body = json.loads(parser_result.get('body', '{}'))
            
            if parser_result.get('statusCode') != 200:
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Resume parsing failed',
                        'details': parser_body
                    })
                }
            
            analysis_id = parser_body.get('analysis_id')
            
            # Step 2: Invoke scorer Lambda
            scorer_payload = {
                'body': json.dumps({
                    'analysis_id': analysis_id,
                    'job_description': job_description
                })
            }
            
            scorer_response = lambda_client.invoke(
                FunctionName=SCORER_FUNCTION,
                InvocationType='RequestResponse',
                Payload=json.dumps(scorer_payload)
            )
            
            scorer_result = json.loads(scorer_response['Payload'].read())
            scorer_body = json.loads(scorer_result.get('body', '{}'))
            
            if scorer_result.get('statusCode') != 200:
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Score calculation failed',
                        'details': scorer_body
                    })
                }
            
            # Get ATS score from DynamoDB
            try:
                db_response = table.get_item(Key={'analysis_id': analysis_id})
                ats_score = db_response.get('Item', {}).get('ats_score', None)
            except Exception as e:
                print(f"Error fetching ATS score: {str(e)}")
                ats_score = None
            
            # Convert Decimals to floats for JSON serialization
            results_data = convert_decimals(scorer_body.get('results'))
            ats_score = convert_decimals(ats_score)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Analysis completed successfully',
                    'analysis_id': analysis_id,
                    'results': results_data,
                    'ats_score': ats_score
                })
            }
        
        # GET /results/{analysis_id}
        elif http_method == 'GET' and '/results/' in path:
            analysis_id = path.split('/results/')[-1]
            
            response = table.get_item(Key={'analysis_id': analysis_id})
            
            if 'Item' not in response:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Analysis not found'})
                }
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'analysis': response['Item']
                })
            }
        
        # POST /batch-compare - Compare resume against multiple jobs
        elif http_method == 'POST' and '/batch-compare' in path:
            body = json.loads(event.get('body', '{}'))
            resume_key = body.get('resume_key')
            jobs = body.get('jobs', [])
            
            if not resume_key or not jobs or len(jobs) < 2:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Missing required fields: resume_key and at least 2 jobs'
                    })
                }
            
            # Step 1: Parse resume once
            parser_payload = {
                'body': json.dumps({
                    'bucket': BUCKET_NAME,
                    'key': resume_key
                })
            }
            
            parser_response = lambda_client.invoke(
                FunctionName=PARSER_FUNCTION,
                InvocationType='RequestResponse',
                Payload=json.dumps(parser_payload)
            )
            
            parser_result = json.loads(parser_response['Payload'].read())
            parser_body = json.loads(parser_result.get('body', '{}'))
            
            if parser_result.get('statusCode') != 200:
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Resume parsing failed',
                        'details': parser_body
                    })
                }
            
            analysis_id = parser_body.get('analysis_id')
            
            # Step 2: Score against each job
            results = []
            for job in jobs:
                job_title = job.get('title', 'Untitled Job')
                job_description = job.get('description', '')
                
                if not job_description.strip():
                    continue
                
                scorer_payload = {
                    'body': json.dumps({
                        'analysis_id': analysis_id,
                        'job_description': job_description
                    })
                }
                
                scorer_response = lambda_client.invoke(
                    FunctionName=SCORER_FUNCTION,
                    InvocationType='RequestResponse',
                    Payload=json.dumps(scorer_payload)
                )
                
                scorer_result = json.loads(scorer_response['Payload'].read())
                scorer_body = json.loads(scorer_result.get('body', '{}'))
                
                if scorer_result.get('statusCode') == 200:
                    score_data = scorer_body.get('results', {})
                    feedback = score_data.get('feedback', {})
                    
                    results.append({
                        'title': job_title,
                        'score': float(score_data.get('compatibility_score', 0)),
                        'skill_match': float(score_data.get('skill_match', 0)),
                        'matched_skills': feedback.get('matched_skills_count', 0),
                        'missing_skills': len(feedback.get('missing_keywords', [])),
                        'strengths': feedback.get('strengths', 'Good alignment with job requirements'),
                        'improvements': feedback.get('improvements', 'Consider highlighting more relevant experience')
                    })
            
            # Sort by score descending
            results.sort(key=lambda x: x['score'], reverse=True)
            
            # Convert Decimals to floats for JSON serialization
            results = convert_decimals(results)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Batch comparison completed',
                    'results': results
                })
            }
        
        # POST /generate-cover-letter - Generate personalized cover letter
        elif http_method == 'POST' and '/generate-cover-letter' in path:
            body = json.loads(event.get('body', '{}'))
            resume_key = body.get('resume_key')
            job_description = body.get('job_description')
            
            if not resume_key or not job_description:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Missing required fields: resume_key and job_description'
                    })
                }
            
            # Step 1: Parse resume to get structured data
            parser_payload = {
                'body': json.dumps({
                    'bucket': BUCKET_NAME,
                    'key': resume_key
                })
            }
            
            parser_response = lambda_client.invoke(
                FunctionName=PARSER_FUNCTION,
                InvocationType='RequestResponse',
                Payload=json.dumps(parser_payload)
            )
            
            parser_result = json.loads(parser_response['Payload'].read())
            parser_body = json.loads(parser_result.get('body', '{}'))
            
            if parser_result.get('statusCode') != 200:
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Resume parsing failed',
                        'details': parser_body
                    })
                }
            
            analysis_id = parser_body.get('analysis_id')
            
            # Step 2: Get resume data from DynamoDB
            try:
                db_response = table.get_item(Key={'analysis_id': analysis_id})
                if 'Item' not in db_response:
                    return {
                        'statusCode': 404,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({'error': 'Resume data not found'})
                    }
                
                resume_data = db_response['Item']
                
                # Step 3: Generate cover letter using scorer function
                # We'll invoke the scorer with a special flag
                cover_letter_payload = {
                    'action': 'generate_cover_letter',
                    'resume_data': convert_decimals(resume_data),
                    'job_description': job_description
                }
                
                scorer_response = lambda_client.invoke(
                    FunctionName=SCORER_FUNCTION,
                    InvocationType='RequestResponse',
                    Payload=json.dumps(cover_letter_payload)
                )
                
                scorer_result = json.loads(scorer_response['Payload'].read())
                print(f"Scorer response: {scorer_result}")
                
                # Check if it's already parsed JSON
                if isinstance(scorer_result, dict) and 'statusCode' in scorer_result:
                    if scorer_result['statusCode'] != 200:
                        error_body = json.loads(scorer_result.get('body', '{}')) if isinstance(scorer_result.get('body'), str) else scorer_result.get('body', {})
                        return {
                            'statusCode': 500,
                            'headers': {
                                'Content-Type': 'application/json',
                                'Access-Control-Allow-Origin': '*'
                            },
                            'body': json.dumps({
                                'error': 'Cover letter generation failed',
                                'details': error_body
                            })
                        }
                    scorer_body = json.loads(scorer_result['body']) if isinstance(scorer_result['body'], str) else scorer_result['body']
                else:
                    scorer_body = scorer_result
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'message': 'Cover letter generated successfully',
                        'cover_letter': scorer_body.get('cover_letter', {}),
                        'analysis_id': analysis_id
                    })
                }
                
            except Exception as e:
                print(f"Error generating cover letter: {str(e)}")
                import traceback
                traceback.print_exc()
                return {
                    'statusCode': 500,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Failed to generate cover letter',
                        'details': str(e)
                    })
                }
        
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Endpoint not found'})
            }
        
    except Exception as e:
        print(f"API Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            })
        }
