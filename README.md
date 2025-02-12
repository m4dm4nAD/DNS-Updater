# DNS-Updater
For the moment this only works with umbrella. Which is a host based security solution so it only works with TLD's. 
In the config file there is a list of allowed domains, add or remove any that you feel are necessary.
There is no input validation, as Umbrella handles that on its own. I don't have any rate limiting implemented, becasue I didn't think about it when I first started writing this and am not sure where to implement it (nor how).

# Run
The main function is the DNSUploader.py

# Requirements
You will have to know your OrgID, generate a token in both Umbrella and AbuseIP.
No there is no requirements file becasue a)this project started as a small project just for me and a team member so just needed to tell with what to install b)I'll add one formally later.

# Current State of Checker
Ok this was just a thought I had, but realized I have no way to test this so don't know if it will work. But the idea was to check IP's and give the source country, confidence score. If you want to block it, submit it to your own webhook and call it a day. But alas I don't have a webhook to test it on so right now it only checks AbuseIP for location and score. If you want to add the function enjoy.
