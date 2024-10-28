from urlhlib import *
import urlhlib
#win32com.client as win32

print ("\t \t \t CLI to upload URL's to Umbrella")

start = input("(1) Start the automated URLhaus uploader.\n(2) Choose a custom list to upload. \n(3) Manually add a single URL.\n(4) Delete a specific url (pending)\n")

if start == '1':
    urlhlib.automatic()
    urlhlib.autoupload('uploadlist.txt')

elif start == '2':
    filename = input("Please input the file path, to the file you would like to upload.\nIf it's in this folder, just put the file name in.\n")
    comment =  input("Enter content date (in YYMMDD format) and source (i.e. 220719 HISAC email)\n")
    urlhlib.fileupload(filename, comment)
    end = input("Press enter to exit.")

elif start == '3':
    url = input("What is the URL you would like to upload?\n")
    comment = input("Enter comments (Source and date in YYDDMM format)).\n")
    urlhlib.manual(url, comment)
    end = input("Press enter to exit.")
elif start =='4':
    print("Not functional yet./n Goodbye.")