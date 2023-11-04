import os
import boto3
import json
from botocore.exceptions import ClientError

def handler(event, context):
    s3_client = boto3.client('s3')

    S3_BUCKET = os.getenv('BUCKET_NAME')
    
    # Get the file_name from the path parameter
    file_name = event.get('pathParameters', {}).get('image_name')

    # Make sure a file name is provided
    if not file_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No file name provided'})
        }

    # Make sure a file name is provided
    if not file_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'No file name provided'})
        }

    try:
        presigned_url = s3_client.generate_presigned_url('get_object',
            Params={'Bucket': S3_BUCKET,
                    'Key': file_name},
            ExpiresIn=3600)
    except ClientError as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error generating presigned URL'})
        }

    # Return the presigned URL for the requested file
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Ensure proper CORS settings
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'file_name': file_name, 'presignedUrl': presigned_url})
    }
