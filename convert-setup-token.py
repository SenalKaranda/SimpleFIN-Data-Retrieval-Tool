import os
import requests
import base64
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the SIMPLEFIN_SETUP_TOKEN from the environment
SIMPLEFIN_API_KEY = os.getenv("SIMPLEFIN_SETUP_TOKEN")

# Check if the API key exists
if not SIMPLEFIN_API_KEY:
    raise ValueError("SIMPLEFIN_SETUP_TOKEN is not set in the .env file or environment.")

# Decode the Base64-encoded token
claim_url = base64.b64decode(SIMPLEFIN_API_KEY).decode('utf-8')

# 2. Claim an Access URL
response = requests.post(claim_url)
if response.status_code != 200:
    raise Exception(f"Failed to claim URL: {response.status_code}, {response.text}")

access_url = response.text

# 3. Get some data
scheme, rest = access_url.split('//', 1)
auth, rest = rest.split('@', 1)
url = scheme + '//' + rest + '/accounts'
username, password = auth.split(':', 1)

print(f"Access URL: {url}")
print(f"Username: {username}")
print(f"Password: {password}")
