from urlhlib import *
import Checker
import urlhlib
#win32com.client as win32

print ("\t \t \t CLI to upload URL's or IPs to DNS Security tools (Umbrella, Cloudflare, etc.)")
start = input ("What would you like to do? \n(1)Upload to Cisco Umbrella. \n(2)Upload an IP to a private webhook. \n(3)undefined right now")

if start == '1': 
    umbrella = input("(1) Start the automated URLhaus uploader.\n(2) Choose a custom list to upload. \n(3) Manually add a single URL.\n(4) Delete a specific url (pending)\n")
    if umbrella == '1':
            urlhlib.automatic()
            urlhlib.autoupload('uploadlist.txt')

    elif umbrella == '2':
        filename = input("Please input the file path, to the file you would like to upload.\nIf it's in this folder, just put the file name in.\n")
        comment =  input("Enter content date (in YYMMDD format) and source (i.e. 220719 HISAC email)\n")
        urlhlib.fileupload(filename, comment)
        end = input("Press enter to exit.")

    elif umbrella == '3':
        url = input("What is the URL you would like to upload?\n")
        comment = input("Enter comments (Source and date in YYDDMM format)).\n")
        urlhlib.manual(url, comment)
        end = input("Press enter to exit.")
    elif umbrella =='4':
        print("Not functional yet./n Goodbye.")
elif start == '2':
     check = input ("What IP would you like to check?")
     Checker.checkip(check)