import subprocess

# create the empty dictionary
# kc = {'keychains': {'keychain': {'items': {'item': {'name': '', 'class': '', 'version': '', 'attributes': {'attribute': {'id': '', 'type': '', 'value': ''}}}}}}}
kc = {'keychains': {
	'keychain': '', 'items': {
		'item': {
			'version': '', 'class': '', 'attributes': {
				{'attribute': {
					'index': '', 'type': '', 'data': ''
					}
				}
				}				
			}
				
		}
	}
}

# get the raw keychain dump from the security program
# by default this will get all keychains available to the user running the script
step1 = subprocess.check_output(["security", "dump-keychain"])

# create a flag for each keychain item *&^%$
step2 = step1.replace('keychain: ', '*&^%$keychain: ')

# split the string into a list of keychain items using the flag *&^%$
step3 = step2.split('*&^%$')

# remove the first empty item in the list created by the leading flag
del(step3[0])

# strip newline from beginning and end of each item
step4 = [item.strip('\n') for item in step3]

# strip whitespace from beginning and end of each item
step5 = [item.strip(' ') for item in step4]

# split each line into a list item
step6 = [item.split('\n', 3) for item in step5]

# create dictionary keys for each keychain item in the list
step7 = [dict([item.split(':', 1) for item in items]) for items in step6]

# We now have a list of dictionaries. Each keychain item is a dictionary inside a list item
# We still need to split the attributes into dictionary keys and create the final dictionary of keychains
attrdict = {}
for i in range(len(step7)):
	keychain = step7[i]['keychain']
	kversion = step7[i]['version']
	kclass = step7[i]['class']
	attr1 = step7[i]['attributes'].strip('\n')
	attr2 = attr1.split('\n')
	attr3 = [item.strip() for item in attr2]
	iname = i
	for item in attr3:
		keys = ['index', 'type', 'data']
		stepA = item.replace('<', '*&^%$', 1)
		stepB = stepA.replace('>=', '*&^%$', 1)
		stepC = stepB.split('*&^%$')
		newdict = dict(zip(keys, stepC))
		attrdict[i] = (newdict
	
	kc['keychains'][keychain]['items'][i]['version'] = kversion 
	kc['keychains'][keychain]['items'][i]['class'] = kclass
	kc['keychains'][keychain]['items'][i]['attributes'] = attrdict



### print attributes
#print(step7)
#print(step7[0])
#print('**********************')
#print(step8[0]['attributes'])
#print('**********************')
#print(step8[100]['attributes'])
#print('**********************')
#print(step7[100]['keychain'])
#print(step7[100]['class'])
#print(step7[100]['version'])

print(kc)