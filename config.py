import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API URLs
URLHAUS_URL = 'https://urlhaus.abuse.ch/downloads/csv/'
UMBRELLA_BASE_URL = 'https://management.api.umbrella.com/v1/organizations'
ABUSEIPDB_URL = 'https://api.abuseipdb.com/api/v2/check'

# Organization settings
UMBRELLA_ORG_ID = os.getenv('UMBRELLA_ORG_ID')
UMBRELLA_TOKEN = os.getenv('UMBRELLA_TOKEN')
ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY')

# Email settings
NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL')

# Allowed domains list
ALLOWED_DOMAINS = [
    "azure.com",
    "1drv.ms",
    "amazon.com",
    "pardot.com",
    "dropbox.com",
    "google.com",
    "amazonaws.com",
    "microsoft.com",
    "sharepoint.com",
    # ... rest of the domains
]

# API Headers
UMBRELLA_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": UMBRELLA_TOKEN
}

# File paths
UPLOAD_LIST_PATH = 'uploadlist.txt'
OLD_LIST_PATH = 'oldlist.txt'
DOWNLOAD_LIST_PATH = 'downloadlist.csv' 