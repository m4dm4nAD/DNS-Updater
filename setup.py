import os
from pathlib import Path

def initial_setup():
    """Run first-time setup to collect and store API credentials."""
    env_path = Path('.env')
    
    # Check if .env already exists
    if env_path.exists():
        return
    
    print("\n=== First Time Setup ===")
    print("Please enter your API credentials. These will be stored securely in a .env file.\n")
    
    # Collect credentials
    umbrella_org_id = input("Enter your Umbrella Organization ID: ").strip()
    umbrella_token = input("Enter your Umbrella API Token: ").strip()
    abuseipdb_key = input("Enter your AbuseIPDB API Key: ").strip()
    notification_email = input("Enter your notification email (optional): ").strip()
    
    # Create .env file with credentials
    env_content = f"""UMBRELLA_ORG_ID={umbrella_org_id}
UMBRELLA_TOKEN={umbrella_token}
ABUSEIPDB_API_KEY={abuseipdb_key}
NOTIFICATION_EMAIL={notification_email}"""
    
    # Write to .env file
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("\nSetup complete! Credentials have been saved to .env file.") 