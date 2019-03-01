#!/usr/local/bin/python3
# This script requires the python3 version of requests

import requests
import base64
import json
import getpass

def main():

	# base URL of JSS
	print('Enter your Jamf Pro Server URL in the form "https://servername.com:8443"')
	base_url = input('Jamf Pro Server URL: ')
	jss_url = base_url + '/JSSResource'
	users_url = jss_url + '/users'
	classes_url = jss_url + '/classes'
	
	# JSS API credentials
	UsernameVar = input('Enter your Jamf Pro username: ')
	PasswordVar = getpass.getpass('Enter your Jamf Pro password: ')

	print ('Fetching class list from JSS...')
	print ('')

	# requests method
	response  = requests.get(classes_url, headers={'Accept': 'application/json'}, auth=(UsernameVar,PasswordVar))
	response_json = json.loads(response.text)
	# end of requests method

	# get list of classes with ID
	jss_class_list = response_json['classes']

	# print list of classes for user
	for x in jss_class_list:
		jss_class_id = x['id']
		jss_class_name = x['name']
		print ('ID: %s' % jss_class_id + ' (' + jss_class_name + ')' )

	# ask the user to enter the ID of a class
	jss_class_id = input('Enter the Class ID number: ')

	# get class name for selected id
	class_url = classes_url + '/id/' + jss_class_id

	# request selected class details
	response  = requests.get(class_url, headers={'Accept': 'application/json'}, auth=(UsernameVar,PasswordVar))
	response_json = json.loads(response.text)
	jss_class_name = response_json['class']['name']

	# Get api endpoint for selected class
	class_url = jss_url + '/classes/id/%s' % jss_class_id

	# request class details from api
	response  = requests.get(class_url, headers={'Accept': 'application/json'}, auth=(UsernameVar,PasswordVar))
	response_json = json.loads(response.text)
	# end of requests method

	# build list of mobile devices in class
	jss_class_device_list = response_json['class']['mobile_devices']

	# create empty array to hold list of device udids
	udid_list = []

	for x in jss_class_device_list:
		jss_device_udid = x['udid']
		udid_list.append(jss_device_udid)

	# create empty array to hold list of device ids
	device_list = []

	# udid url
	udid_base_url = jss_url + '/mobiledevices/udid/'

	print ('Fetching device ids from JSS...')

	# get list of jss ids for devices in udid_list array
	for x in udid_list:
		udid_url = udid_base_url + x

		# request device id from udid
		response  = requests.get(udid_url, headers={'Accept': 'application/json'}, auth=(UsernameVar,PasswordVar))
		response_json = json.loads(response.text)

		# get device details
		jss_device_id = response_json['mobile_device']['general']['id']

		#append to list of devices by id
		device_list.append(jss_device_id)
		#end of for loop
		
	# print list of devices in the class
	print('Devices in ' + jss_class_name)
	print(device_list)

	print('Creating the mobile device group…')
	# create xml for static group for selected class and add all device ids found
	group_xml = '<mobile_device_group><name>' + jss_class_name + ' Class group</name><is_smart>false</is_smart><mobile_devices>'
	for x in device_list:
		group_xml = group_xml + '<mobile_device><id>' + str(x) + '</id></mobile_device>'
	group_xml = group_xml + '</mobile_devices></mobile_device_group>'

#	# post static group xml to API endpoint
	group_url = jss_url + '/mobiledevicegroups/id/0'

	# requests block
	response  = requests.post(group_url, data=group_xml, headers={'Content-Type': 'text/xml'}, auth=(UsernameVar,PasswordVar))
	print(response.status_code, response.reason)
	if response.status_code == 409:
		print('The selected class already has a mobile device group with the same name')
		update = input('Enter "y" to update, or "n" to quit: ')
		if update == 'y':
			group_url = jss_url + '/mobiledevicegroups/name/' + requests.utils.requote_uri(jss_class_name) + requests.utils.requote_uri(' Class group')
			print(group_url)
			response  = requests.put(group_url, data=group_xml, headers={'Content-Type': 'text/xml'}, auth=(UsernameVar,PasswordVar))
			print(response.status_code, response.reason)


if __name__ == '__main__':
	main()
