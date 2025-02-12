import requests, zipfile, io, tldextract, datetime, os, re, smtplib
import win32com.client as win32
import pandas as pd
from config import (
    UMBRELLA_BASE_URL,
    UMBRELLA_ORG_ID,
	UMBRELLA_TOKEN,
    UMBRELLA_HEADERS,
    NOTIFICATION_EMAIL,
    ALLOWED_DOMAINS
)
	
def automatic():
	#This downloads the csv file from urlhaus, and extracts it as a .txt file.
	hausurl = 'https://urlhaus.abuse.ch/downloads/csv/'
	urlhaus = requests.get(hausurl, stream = True)
	urlzip = zipfile.ZipFile(io.BytesIO(urlhaus.content))
	urlzip.extractall()

	#This is to remove the header prior to it being converted to a csv.
	with open (r'csv.txt', 'r+') as ed:
		lines = ed.readlines()
		ed.seek(0)
		ed.truncate()
		ed.writelines(lines[8:])
	ed.close()

	#Converts the txt to csv and deletes the tct file
	readhaustxt = pd.read_csv(r'csv.txt')
	readhaustxt.to_csv (r'downloadlist.csv', index=None)
	os.remove(r'csv.txt')

	#Stores only the url's as an object and removes any ip address from the column
	haus = pd.read_csv('downloadlist.csv', usecols = ['url'])
	haus = haus[~haus.url.str.findall(r'[0-9]+(?:\.[0-9]+){3}').astype(bool)]
	haus = haus.astype('string')

	#Extracts all the top level domains from the list, and sorts them.
	cleanedhaus = [tldextract.extract(urls, include_psl_private_domains = True) for urls in haus['url']]
	list(dict.fromkeys(cleanedhaus))

	#Here we are making the list of URLs that will be uploaded, it first reads the old url list and stores them in an object. Then compares the txt file previously downloaded, to the old upload list, the allowed list, and a duplicate list. If not found its added to a new txt file
	allowedlist = ["azure.com","1drv.ms","amazon.com","pardot.com","dropbox.com","google.com","amazonaws.com","microsoft.com","sharepoint.com","1drv.com","ac.th","box.com","boxcloud.com","cudasvc.com","dropboxusercontent.com","github.com","githubusercontent.com","go.th","googleapis.com","googleusercontent.com","jquery.com","live.com","naver.com","onedrive.com","orthoclinicaldiagnostics.com","orthoclinicaldx.com","outlook.com","pardot.com","salesforce.com","windows.net","yimg.com"]
	old = open('oldlist.txt','r+')
	oldlist = old.read().split('\n')
	duplist = []
	newold = []
	newurllist = open('uploadlist.txt','w')
	date = datetime.datetime.now()
	today = date.strftime("%x")
	count = 0
	for final in cleanedhaus:
		checklist = allowedlist + oldlist + duplist
		if (final.domain+'.'+final.suffix) not in checklist:
			newurllist.writelines('[{"destination": "%s.%s","comment": "From URLHaus on %s"}]\n'%(final.domain, final.suffix, today))
			newold.append(final.domain+'.'+final.suffix)
			duplist.append(final.domain+'.'+final.suffix)
			count+=1
	newurllist.close()
	oldurls = ['{}\n'.format(x) for x in newold]
	old.writelines(sorted(set((oldurls))))
	old.close()
	print(count)

	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.Subject = 'URLHaus Update'
	mail.To = "(mailbox you want the notification sent to)"
	mail.Body = ("Umbrella auto uploaded %s to the block list." %(newold))
	mail.Send()

def autoupload(name):
	filename = name
	filename = str(filename)
	with open(filename,'r') as newurl:
		umbrellaurl = f"https://management.api.umbrella.com/v1/organizations/{UMBRELLA_ORG_ID}/destinationlists/(destinationlist ID)/destinations"
		while(line := newurl.readline().rstrip()):
			payload = line.strip()
			headers = {
				"Content-Type": "application/json",
				"Accept": "application/json",
				"Authorization": UMBRELLA_TOKEN
			}
			response = requests.request('POST', umbrellaurl, headers = headers, data = payload)
			print(response.text.encode('utf8'))

def fileupload(name, comment):
	filename = name
	comment = comment
	uploads = []
	with open(filename,'r') as newurl:
		umbrellaurl = f"https://management.api.umbrella.com/v1/organizations/{UMBRELLA_ORG_ID}/destinationlists/(destinationlist ID)/destinations"
		while (line := newurl.readline().rstrip()):
			newline = line.strip()
			newline = re.sub(r"[\[\]]","",newline)
			payload = ('[{"destination": "%s","comment": "From %s"}]\n'%(newline, comment))
			headers = {
				"Content-Type": "application/json",
				"Accept": "application/json",
				"Authorization": UMBRELLA_TOKEN
			}
			response = requests.request('POST', umbrellaurl, headers = headers, data = payload)
			print(response.text.encode('utf8'))
			uploads.append(newline)
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.Subject = 'URLHaus Update'
	mail.To = "(mailbox you want notification sent to)"
	mail.Body = ("Umbrella auto uploaded %s to the block list." %(uploads))
	mail.Send()
			
def manual(name, comment, list_id):
	urlname = name
	comment = comment
	umbrellaurl = f"{UMBRELLA_BASE_URL}/{UMBRELLA_ORG_ID}/destinationlists/{list_id}/destinations"
	payload = f'[{{"destination": "{urlname}","comment": "From {comment}"}}]\n'
	
	response = requests.request('POST', umbrellaurl, headers=UMBRELLA_HEADERS, data=payload)
	print(response.text.encode('utf8'))


def search_for_lists():
    """
    Search all destination lists in Umbrella and print the results
    """
    umbrellaurl = f"https://management.api.umbrella.com/v1/organizations/{UMBRELLA_ORG_ID}/destinationlists"
    
    headers = {
        "Accept": "application/json",
        "Authorization": UMBRELLA_TOKEN
    }
    
    try:
        response = requests.get(umbrellaurl, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        destination_lists = response.json()
        
        if not destination_lists:
            print("No destination lists found")
            return
            
        for dest_list in destination_lists:
            print(f"\nList Name: {dest_list.get('name')}")
            print(f"List ID: {dest_list.get('id')}")
            print(f"Is Enabled: {dest_list.get('isEnabled')}")
            print(f"Total Entries: {dest_list.get('totalEntries')}")
            print("-" * 50)
            
    except requests.exceptions.RequestException as e:
        print(f"Error accessing Umbrella API: {e}")

def search_destinations(url):
    # First get all destination lists
    umbrellaurl = f"https://management.api.umbrella.com/v1/organizations/{UMBRELLA_ORG_ID}/destinationlists"
    headers = {
        "Accept": "application/json",
        "Authorization": UMBRELLA_TOKEN
    }
    try:
        # Get all destination lists
        response = requests.get(umbrellaurl, headers=headers)
        response.raise_for_status()
        destination_lists = response.json()    
        found = False
        # Search through each destination list
        for dest_list in destination_lists:
            list_id = dest_list.get('id')
            list_name = dest_list.get('name')            
            # Get destinations for this specific list
            destinations_url = f"{umbrellaurl}/{list_id}/destinations"
            dest_response = requests.get(destinations_url, headers=headers)
            dest_response.raise_for_status()
            destinations = dest_response.json()
            # Search for the URL in this list
            for destination in destinations:
                if url.lower() in destination.get('destination', '').lower():
                    found = True
                    print(f"\nFound in list: {list_name}")
                    print(f"List ID: {list_id}")
                    print(f"Exact match: {destination.get('destination')}")
                    print(f"Comment: {destination.get('comment')}")
                    print("-" * 50)  
        if not found:
            print(f"URL '{url}' not found in any destination lists")         
    except requests.exceptions.RequestException as e:
        print(f"Error accessing Umbrella API: {e}")

# def deepwatch_email():
# 	outlook = win32.Dispatch('outlook.application')
# 	mapi = outlook.GetNamespace("MAPI")