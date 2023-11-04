import base64

def handler(event, context):
    # Get request and request headers
    request = event['Records'][0]['cf']['request']
    headers = request.get('headers', {})

    # Configure authentication
    auth_user = 'user'
    auth_pass = 'pass'

    # Construct the Basic Auth string
    auth_string = 'Basic ' + base64.b64encode(f'{auth_user}:{auth_pass}'.encode()).decode()

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