import requests
import json

# Defining the api-endpoint
url = 'https://api.abuseipdb.com/api/v2/check'

querystring = {
    'ipAddress': '118.25.6.39',
    'maxAgeInDays': '90'
}

headers = {
    'Accept': 'application/json',
    'Key': 'YOUR_OWN_API_KEY'
}

response = requests.request(method='GET', url=url, headers=headers, params=querystring)

# Formatted output
decodedResponse = json.loads(response.text)
print (json.dumps(decodedResponse, sort_keys=True, indent=4))