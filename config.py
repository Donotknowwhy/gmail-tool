"""
Cấu hình cho Gmail Tool
"""
import os

# Gmail API credentials
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# Email filtering settings
DEFAULT_MAX_RESULTS = 100
DEFAULT_QUERY = ''

# Content analysis keywords
COMPLETE_KEYWORDS = ['abc']
ERROR_KEYWORDS = ['xyz']

# Package delivery status keywords based on subject lines
PACKAGE_SUCCESS_KEYWORDS = ['your package has arrived']
PACKAGE_FAILED_KEYWORDS = ['could not be delivered']

# Output settings
OUTPUT_FORMAT = 'table'  # 'table', 'json', 'csv'
