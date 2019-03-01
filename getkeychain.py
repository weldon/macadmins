import subprocess

# get the raw keychain dump from the security program
step1 = subprocess.check_output(["security", "dump-keychain"])

# create a flag for each keychain item *&^%$
step2 = step1.replace('keychain: ', '*&^%$keychain: ')

# split the string into a list of keychain items using the flag *&^%$
step3 = step2.split('*&^%$')

# remove the first empty item in the list created by the leading flag
del(step3[0])

# strip newline from each item
step4 = [item.strip('\n') for item in step3]

# strip whitespace from each item
step5 = [item.strip(' ') for item in step4]

# split each line into a list item
step6 = [item.split('\n', 3) for item in step5]

# create dictionary keys for each keychain item in the list
step7 = [dict([item.split(':', 1) for item in items]) for items in step6]


### print attributes
print(step7[0])
print('**********************')
print(step7[0]['attributes'])
print('**********************')
print(step7[100]['attributes'])
print('**********************')
print(step7[100]['keychain'])