### This script will updated an existing smart group by id # to update the criteria
### The intent of the script is to allow you to update the version number in a smart group
### to identify computers with the latest available version


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
	# you can optionally hard code the url, username, and password for your Jamf Pro Server
	# if left empty, the script will prompt the user for the values at runtime
	base_url = ""
	jssuser = ""
	jsspass = ""
	
	# base URL of JSS
	if base_url == "":			
		print('Enter your Jamf Pro Server hostname in the form "https://servername.com:8443"')
		base_url = input('Jamf Pro Server URL: ')
	api_url = base_url + '/JSSResource/computergroups/id/{id}'.format(id = sg_id)

		
	# JSS API credentials
	if jssuser == "":
		jssuser = input('Enter your Jamf Pro username: ')
	if jsspass == "":
		jsspass = getpass.getpass('Enter your Jamf Pro password: ')	
	
	# XML Payload
	payload = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><computer_group><id>{id}</id><name>{name}</name><is_smart>true</is_smart><site><id>-1</id><name>None</name></site><criteria><size>2</size><criterion><name>Application Title</name><priority>0</priority><and_or>and</and_or><search_type>{name_type}</search_type><value>{app}</value><opening_paren>false</opening_paren><closing_paren>false</closing_paren></criterion><criterion><name>Application Version</name><priority>1</priority><and_or>and</and_or><search_type>{version_type}</search_type><value>{version}</value><opening_paren>false</opening_paren><closing_paren>false</closing_paren></criterion></criteria></computer_group>'.format(id=sg_id, name=sg_name, name_type=name_search_type, app=app_title, version_type=version_search_type, version=app_version)
		
	# Request
	try: r  = requests.put(api_url, headers={'Accept': 'application/xml'}, auth=(jssuser,jsspass), data=payload)
	except:
		print("something went wrong with your connection to the JPS")
	else:
		print("connection to JPS was successful")
	
	# Check if smart group was updated
	if r.status_code == 201:
		print("smart group {id} was successfully updated".format(id=sg_id))	
	else:
		print("smart group {id} was not updated. Check for errors".format(id=sg_id))
	
if __name__ == '__main__':
	main()