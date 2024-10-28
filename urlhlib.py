import requests, zipfile, io, tldextract, datetime, os, re, smtplib
import win32com.client as win32
import pandas as pd
	
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
		umbrellaurl = "https://management.api.umbrella.com/v1/organizations/(orgid)/destinationlists/(destinationlist ID)/destinations"
		while(line := newurl.readline().rstrip()):
			payload = line.strip()
			headers = {
				"Content-Type": "application/json",
				"Accept": "application/json",
				"Authorization":"(Token)"
			}
			response = requests.request('POST', umbrellaurl, headers = headers, data = payload)
			print(response.text.encode('utf8'))

def fileupload(name, comment):
	filename = name
	comment = comment
	uploads = []
	with open(filename,'r') as newurl:
		umbrellaurl = "https://management.api.umbrella.com/v1/organizations/(orgid)/destinationlists/(destinationlist ID)/destinations"
		while (line := newurl.readline().rstrip()):
			newline = line.strip()
			newline = re.sub(r"[\[\]]","",newline)
			payload = ('[{"destination": "%s","comment": "From %s"}]\n'%(newline, comment))
			headers = {
				"Content-Type": "application/json",
				"Accept": "application/json",
				"Authorization":"(Token)"
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
			
def manual(name, comment):
	urlname = name
	comment = comment
	umbrellaurl = "https://management.api.umbrella.com/v1/organizations/(orgid)/destinationlists/(destinationlist ID)/destinations"
	payload = ('[{"destination": "%s","comment": "From %s"}]\n'%(urlname, comment))
	headers = {
                "Content-Type": "application/json",
		        "Accept": "application/json",
		        "Authorization":"(Token)"
                }
	response = requests.request('POST', umbrellaurl, headers = headers, data = payload)
	print(response.text.encode('utf8'))
	
def deepwatch_email():
	outlook = win32.Dispatch('outlook.application')
	mapi = outlook.GetNamespace("MAPI")