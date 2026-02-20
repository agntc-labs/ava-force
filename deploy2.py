import firebase_admin
from firebase_admin import credentials
import requests
import json
import os
import base64
import hashlib

# Get access token
from google.auth.transport import requests as google_requests
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/firebase.hosting']
credentials = service_account.Credentials.from_service_account_file(
    '/Users/admin/Projects/agentic-labs/firebase-service-account.json', scopes=SCOPES)
request = google_requests.Request()
credentials.refresh(request)
access_token = credentials.token

project_id = "agentic-labs"
site_id = "ava-force"
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

# Read index.html
with open('index.html', 'rb') as f:
    index_content = f.read()

# Calculate hash
file_hash = hashlib.sha256(index_content).hexdigest()
print(f"File hash: {file_hash}")

# Create a new version
version_url = f"https://firebasehosting.googleapis.com/v1beta1/projects/{project_id}/sites/{site_id}/versions"
version_data = {"config": {"rewrites": [{"glob": "**", "path": "/index.html"}]}}
resp = requests.post(version_url, headers=headers, json=version_data)
print(f"Create version: {resp.status_code}")
version_info = resp.json()
print(f"Version: {version_info}")

if 'name' not in version_info:
    print("Failed to create version")
    exit(1)

version_name = version_info['name']

# Populate files
populate_url = f"https://firebasehosting.googleapis.com/v1beta1/{version_name}:populateFiles"
files_data = {
    "files": {
        "/index.html": base64.b64encode(index_content).decode('utf-8')
    }
}
resp = requests.post(populate_url, headers=headers, json=files_data)
print(f"Populate files: {resp.status_code}")
print(f"Response: {resp.text[:500]}")

# Finalize version
finalize_url = f"https://firebasehosting.googleapis.com/v1beta1/{version_name}:finalize"
resp = requests.patch(finalize_url, headers=headers)
print(f"Finalize: {resp.status_code}")

# Release version
release_url = f"https://firebasehosting.googleapis.com/v1beta1/projects/{project_id}/sites/{site_id}/releases?versionName={version_name}"
resp = requests.post(release_url, headers=headers)
print(f"Release: {resp.status_code}")
print(f"Response: {resp.text}")

print("\n✅ DEPLOYED!")
print(f"🔗 https://ava-force.web.app")
