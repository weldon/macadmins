# macadmin

## jss-creategroupfromclass

This python script will walk you through selecting a class imported from Apple School Manager and then it will create a static mobile device group with the devices that are on the roster for that class.

## getkeychain

This python script is a work in progress
The goal is to take the keychain dump and put it into a nice python dictionary so you can easily find items. One of the use cases is to find keychain items related to AD passwords (Exchange, Outlook account password, fileshare passwords, etc.) so you can then remove those after a password update in Nomad or through some other method to preven the account being locked from services sending the old password automatically.

## check_profile_payload.py

This python script will use the Jamf Pro API to check each configuration profile for the presence of a test string in the payload of the profile. This is useful if you want to find all the profiles that have a particular kind of payload, like all profiles with wi-fi defined, or all profiles with a VPN config. The output of the script is the URL to view the profile in your web browser (using the Jamf Pro Server web interface). If a particular profile is NOT a match, then there is an entry that says so.