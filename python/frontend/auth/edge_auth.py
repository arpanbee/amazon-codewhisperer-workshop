import base64
import boto3

def handler(event, context):
    # Get request and request headers
    request = event['Records'][0]['cf']['request']
    headers = request.get('headers', {})

    # Configure authentication
    user_secret_arn = "arn:aws:secretsmanager:us-east-1:629080472841:secret:UserSecret"
    pass_secret_arn = "arn:aws:secretsmanager:us-east-1:629080472841:secret:PassSecret"

    client = boto3.client('secretsmanager')

    user_value_response = client.get_secret_value(
        SecretId=user_secret_arn
    )

    pass_value_response = client.get_secret_value(
        SecretId=pass_secret_arn
    )
    
    AUTH_USER = user_value_response['SecretString']
    AUTH_PASS = pass_value_response['SecretString']
    

    # Construct the Basic Auth string
    auth_string = 'Basic ' + base64.b64encode(f'{AUTH_USER}:{AUTH_PASS}'.encode()).decode()

    # Require Basic authentication
    expected_auth = headers.get('authorization', [{}])[0].get('value', '')
    if not expected_auth or expected_auth != auth_string:
        body = 'Unauthorized'
        response = {
            'status': '401',
            'statusDescription': 'Unauthorized',
            'body': body,
            'headers': {
                'www-authenticate': [{'key': 'WWW-Authenticate', 'value': 'Basic'}]
            },
        }
        return response

    # Continue request processing if authentication passed
    return request