import requests
import json
from config import ABUSEIPDB_URL, ABUSEIPDB_API_KEY

# Defining the api-endpoint
def checkip(ip):
    querystring = {
        'ipAddress': ip,
        'maxAgeInDays': '90'
    }

    headers = {
        'Accept': 'application/json',
        'Key': ABUSEIPDB_API_KEY
    }

    try:
        response = requests.request(method='GET', url=ABUSEIPDB_URL, headers=headers, params=querystring)
        response.raise_for_status()
        
        data = response.json()
        
        if 'data' in data:
            location_data = data['data']
            print("\nLocation Information:")
            print(f"Country: {location_data.get('countryName', 'Unknown')}")
            print(f"Country Code: {location_data.get('countryCode', 'Unknown')}")
            print(f"City: {location_data.get('city', 'Unknown')}")
            print(f"Region: {location_data.get('region', 'Unknown')}")
            print(f"Latitude: {location_data.get('latitude', 'Unknown')}")
            print(f"Longitude: {location_data.get('longitude', 'Unknown')}")
        else:
            print("No location data found for this IP")
            
    except requests.exceptions.RequestException as e:
        print(f"Error checking IP: {e}")
    except json.JSONDecodeError:
        print("Error parsing API response")

    return data