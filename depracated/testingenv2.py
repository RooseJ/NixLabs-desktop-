import os
output = os.popen("ping -c 3 google.com").read()


from sys import platform
# print(output)
print (platform)