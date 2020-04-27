### This script will update an existing smart group that has two criteria:
### 	1) application title
###		2) applivation version
### The idea is that this smart group will find computers with a certain (latest?) version -
### of a certain app. When the application version changes, this script can update -
### the version number in the smart group criteria so that the smart group continues to find -
### computers with the latest version of that app.
###
### The script uses the example of updating smart group 11 to look for zoom v4.6.12

### This script will updated an existing smart group by id #


import requests
import getpass

def main():
	
	#### user variables ####
	# enter the name of the smart group to be updated
	sg_name = "Zoom - latest version"
	# enter the id number of the smart group to be updated
	sg_id = "11"
	# enter the search type for the name (eg. "is" or "has")
	name_search_type = "is"
	# enter the application title
	app_title = "zoom.us.app"
	# enter the search type for the version (eg. "is" or "like")
	version_search_type = "like"
	# enter the application version
	app_version = "4.6.12"
	
	#### Jamf Pro Server variables ####
	# site id, leave this set to "-1" and "None" if it doesn't belong in a site
	site_id = "-1"
	site_name = "None"
	# you can optionally hard code the url, username, and password for your Jamf Pro Server
	# if left empty, the script will prompt the user for the values at runtime
	jps_url = ""
	jpsuser = ""
	jpspass = ""
	
	# base URL of JSS
	if jps_url == "":			
		print('Enter your Jamf Pro Server hostname in the form "https://servername.com:8443"')
		jps_url = input('Jamf Pro Server URL: ')
	api_url = jps_url + f'/JSSResource/computergroups/id/{sg_id}'
	
	# JSS API credentials
	if jpsuser == "":
		jpsuser = input('Enter your Jamf Pro username: ')
	if jpspass == "":
		jpspass = getpass.getpass('Enter your Jamf Pro password: ')	
	
	# XML Payload
	payload = f'<?xml version=\"1.0\" encoding=\"UTF-8\"?><computer_group><id>{sg_id}</id><name>{sg_name}</name><is_smart>true</is_smart><site><id>{site_id}</id><name>{site_name}</name></site><criteria><size>2</size><criterion><name>Application Title</name><priority>0</priority><and_or>and</and_or><search_type>{name_search_type}</search_type><value>{app_title}</value><opening_paren>false</opening_paren><closing_paren>false</closing_paren></criterion><criterion><name>Application Version</name><priority>1</priority><and_or>and</and_or><search_type>{version_search_type}</search_type><value>{app_version}</value><opening_paren>false</opening_paren><closing_paren>false</closing_paren></criterion></criteria></computer_group>'
		
	# Request
	try: r  = requests.put(api_url, headers={'Accept': 'application/xml'}, auth=(jpsuser,jpspass), data=payload)
	except:
		print(f"something went wrong with your connection to {jps_url}")
	else:
		print(f"connection to {jps_url} was successful")
	
	# Check if smart group was updated
	if r.status_code == 201:
		print(f"smart group {sg_id} was successfully updated")	
	else:
		print(f"smart group {sg_id} was not updated. Check for errors")
	
if __name__ == '__main__':
	main()