from UmbrellaLib import *
import Checker
import UmbrellaLib
import setup
#win32com.client as win32

def main():
    setup.initial_setup()
    print("\t \t \t CLI to upload URL's or IPs to DNS Security tools (Umbrella, Cloudflare, etc.)")
    start = input("What would you like to do? \n(1)Upload to Cisco Umbrella. \n(2)Upload an IP to a private webhook. \n(3)undefined right now")

    if start == '1': 
        umbrella = input("(1) Start the automated URLhaus uploader.\n(2) Choose a custom list to upload. \n(3) Manually add a single URL.\n(4) Delete a specific url (pending)\n")
        if umbrella == '1':
            UmbrellaLib.automatic()
            UmbrellaLib.autoupload('uploadlist.txt')
        elif umbrella == '2':
            filename = input("Please input the file path, to the file you would like to upload.\nIf it's in this folder, just put the file name in.\n")
            comment = input("Enter content date (in YYMMDD format) and source (i.e. 220719 HISAC email)\n")
            UmbrellaLib.fileupload(filename, comment)
            end = input("Press enter to exit.")
        elif umbrella == '3':
            url = input("What is the URL you would like to upload?\n")
            comment = input("Enter comments (Source and date in YYDDMM format)).\n")
            list = input("What is the list ID of the list you would like to upload to?\n If you don't know, type 'lists' to see all available lists.\n")
            if list:
                UmbrellaLib.search_for_lists()
                url = input("What is the URL you would like to upload?\n")
                comment = input("Enter comments (Source and date in YYDDMM format)).\n")
                list = input("What is the list ID of the list you would like to upload to?\n")
                UmbrellaLib.manual(url, comment, list)
            else:
                UmbrellaLib.manual(url, comment, list)
            end = input("Press enter to exit.")
        elif umbrella == '4':
            url = input("What is the URL you would like to search for?\n")
            found_url = UmbrellaLib.search_destinations(url)
            if found_url:
                print(f"URL found in Umbrella: {found_url}")
            else:
                print("URL not found in Umbrella.")
            end = input("Press enter to exit.")
    elif start == '2':
        check = input("What IP would you like to check?")
        Checker.checkip(check)

if __name__ == "__main__":
    main()