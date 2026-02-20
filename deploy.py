#!/usr/bin/env python3
import firebase_admin
from firebase_admin import credentials, storage
import os
import glob

# Initialize with service account
cred = credentials.Certificate('/Users/admin/Projects/agentic-labs/firebase-service-account.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'agentic-labs',
    'storageBucket': 'agentic-labs.appspot.com'
})

bucket = storage.bucket()

# Upload all files
files = ['index.html']
for filepath in files:
    full_path = os.path.join('/Users/admin/Projects/ava-force', filepath)
    if os.path.exists(full_path):
        blob = bucket.blob(f'ava-force/{filepath}')
        blob.upload_from_filename(full_path)
        blob.cache_control = 'no-cache'
        blob.patch()
        print(f'✓ Uploaded {filepath}')

print('\n✅ Deployed to: https://agentic-labs.web.app/ava-force/')
