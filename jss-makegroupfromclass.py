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
	print(classes_url)
	
	# JSS API credentials
	UsernameVar = input('Enter your Jamf Pro username: ')
	PasswordVar = getpass.getpass('Enter your Jamf Pro password: ')

	print ('Fetching class list from JSS...')
	print ('')

	# requests method
	response  = requests.get(classes_url, headers={'Accept': 'application/json'}, auth=(UsernameVar,PasswordVar))
	print('Status code from request: %s' % response.status_code)
	response_json = json.loads(response.text)
	# end of requests method

	# print list of classes with ID
	jss_class_list = response_json['classes']

	for x in jss_class_list:
		jss_class_id = x['id']
		jss_class_name = x['name']
		print ('Class: %s' % jss_class_id + ' ' + jss_class_name )

	jss_class_id = input('Enter the class ID: ')

	# get class name for selected id
	class_url = classes_url + '/id/' + jss_class_id

	# requests method
	response  = requests.get(class_url, headers={'Accept': 'application/json'}, auth=(UsernameVar,PasswordVar))
	print('Status code from request: %s' % response.status_code)
	response_json = json.loads(response.text)
	jss_class_name = response_json['class']['name']

	# Get list of students in selected class
	class_url = jss_url + '/classes/id/%s' % jss_class_id
	print(class_url)

	# requests method
	response  = requests.get(class_url, headers={'Accept': 'application/json'}, auth=(UsernameVar,PasswordVar))
	print('Status code from request: %s' % response.status_code)
	response_json = json.loads(response.text)
	# end of requests method

	# get list of mobile devices in class
	jss_class_device_list = response_json['class']['mobile_devices']

	# create empty array to hold list of devices
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

		# requests block
		response  = requests.get(udid_url, headers={'Accept': 'application/json'}, auth=(UsernameVar,PasswordVar))
		response_json = json.loads(response.text)

		# get device object
		jss_device_id = response_json['mobile_device']['general']['id']

		#append to array
		device_list.append(jss_device_id)
		#end of for loop
	print('Devices in ' + jss_class_name)
	print(device_list)

	# create xml for static group for selected class and add all device ids found
	group_xml = '<mobile_device_group><name>' + jss_class_name + ' Class group</name><is_smart>false</is_smart><mobile_devices>'
	for x in device_list:
		group_xml = group_xml + '<mobile_device><id>' + str(x) + '</id></mobile_device>'
	group_xml = group_xml + '</mobile_devices></mobile_device_group>'
	print(group_xml)

#	# post static group xml to API endpoint
	group_url = jss_url + '/mobiledevicegroups/id/0'
	print(group_url)
	# requests block
	response  = requests.post(group_url, data=group_xml, headers={'Content-Type': 'text/xml'}, auth=(UsernameVar,PasswordVar))
	print(response.status_code, response.reason)


if __name__ == '__main__':
	main()