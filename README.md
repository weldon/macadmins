# macadmin

jss-creategroupfromclass

This python script will walk you through selecting a class imported from Apple School Manager and then it will create a static mobile device group with the devices that are on the roster for that class.

getkeychain

This python script is a work in progress
The goal is to take the keychain dump and put it into a nice python dictionary so you can easily find items. One of the use cases is to find keychain items related to AD passwords (Exchange, Outlook account password, fileshare passwords, etc.) so you can then remove those after a password update in Nomad or through some other method to preven the account being locked from services sending the old password automatically.
