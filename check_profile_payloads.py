import requests
import json
import getpass

# string to look for in profile payload
# example: '<key>PayloadType</key><string>com.apple.vpn.managed</string>' to find profiles with a VPN payload
payload_test = '<key>PayloadType</key><string>com.apple.vpn.managed</string>'

def main():

	# base URL of JSS
	print('Enter your Jamf Pro Server hostname in the form "https://servername.com:8443"')
	base_url = input('Jamf Pro Server URL: ')
	api_url = base_url + '/JSSResource/mobiledeviceconfigurationprofiles'
	
	# JSS API credentials
	jssuser = input('Enter your Jamf Pro username: ')
	jsspass = getpass.getpass('Enter your Jamf Pro password: ')	

	# requests method
	r  = requests.get(api_url, headers={'Accept': 'application/json'}, auth=(jssuser,jsspass))
#	print (r)
#	print (r.headers)
#	print (r.text)
	r_json = json.loads(r.text)
	# end of requests method
	
	# grab the list of profiles from the json
	profile_list = r_json['configuration_profiles']
#	print (profile_list)
#	print (profile_list[0])
	# create an empty array to hold the matching profiles
	profiles_match = []
	
	# test each profile in profile_list
	# this generates a new http request to get the details of each profile
	for x in profile_list:
		# get the id number of the profile
		profile_id = x['id']
		# build the url for the api endpoint to get the profile details, including payload
		test_url = api_url + '/id/{}/subset/general'.format(profile_id)
		# perform the http api request
		r  = requests.get(test_url, headers={'Accept': 'application/json'}, auth=(jssuser,jsspass))
		# grab the json from the response
		r_json = json.loads(r.text)
		# grab the payload details from the response
		r_payload = r_json['configuration_profile']['general']['payloads']
		# test to see if the string appears in the payload
		if payload_test in r_payload:
			# build the url to the profile so that the admin can copy to edit the profile
			profile_url = base_url + '/iOSConfigurationProfiles.html?id={}'.format(profile_id)
			profiles_match.append(profile_url)
		else:
			# create an entry in the list for non-matching profiles just for completeness
			# but without the URL so the admin will know that profile doesn't need editing
			profiles_match.append('test string not found in profile {}'.format(profile_id))
	
#	print(profiles_match)

	for x in profiles_match:
		# print the list of matches
		print(x)
	
if __name__ == '__main__':
	main()