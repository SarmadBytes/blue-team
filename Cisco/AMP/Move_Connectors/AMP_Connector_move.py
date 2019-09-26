# 
#
# Author: Trae Horton
#
# Revision: 1.0
# Date: 2019/04/25 $
#
# Description : This script will automatically move PCs in the Audit Policy to the correct policy based off of the
# hostname within AMP
#
#
# The following library is used for HTTP GET, POST, DELETE functions
import requests
# The following library is used for Regular Expressions
import re
# The following library is used to interact with the Thycotic Secret Server SOAP API
import suds.client
# The following library is used to encrypt the password that interacts with the Thycotic API
from cryptography.fernet import Fernet

# This is the key that is used to decrypt the cipher string that contains the username and password
key = b''
# The following pulls the fernet class to tie end with the cipher key
cipher_suite = Fernet(key)
# Below is the cipher text for the password for the SecretServer API
ciphered_text = b''
# We create an object that contains the unencrypted password and store it to a string
unciphered_text = (cipher_suite.decrypt(ciphered_text))
# This will convert the object from byte to string
password = unciphered_text.decode('ascii')
# Below is the cipher text for the username for the SecretServer API
ciphered_text1 = b''
# We create an object that contains the unencrypted password and store it to a string
unciphered_text1 = (cipher_suite.decrypt(ciphered_text1))
# This will convert the object from byte to string
username = unciphered_text1.decode('ascii')

# The following will set the value client to use the SecretServer API
client = suds.client.Client("https://SERVER.secretservercloud.com/webservices/SSWebservice.asmx?wsdl")
# Below will request and store the token based on the SecretServer credentials listed above
token = client.service.Authenticate(username, password, "", "DOMAIN.local")
# This will search for the specific secret based on ID
searchSecret=client.service.GetSecret(token.Token, secretId=8800)
# The following will split the results from the searchSecret into multiple splices
split = str(searchSecret)
# Below will split the object to include the username from the secretitem
split_username = split.split("SecretItem")[5]
# This will remove any blank lines that are stored in the object
username =split_username.split("\n")[1]
# Below will split the object to include the username from the secretitem
split_password = split.split("SecretItem")[6]
# This will remove any blank lines that are stored in the object
password =split_password.split("\n")[1]
# The following will remove any white spaces stored in the string
user = username.split()[2]
# The following will remove any white spaces stored in the string
pass1 = password.split()[2]

# Below will remove the '"' from the object
amp_client_id = user.replace('"', '')
# Below will remove the '"' from the object
amp_api_key = pass1.replace('"', '')

# The following group is the root audit policy within AMP
group_guid = ''
# The following group is the store policy group within AMP
store_guid = ''
# The following group is the Back Office policy group within AMP
ic_guid = ''
# The following group is the DOZ root group within AMP
dev = '1'
# The following group is the BOZ root group within AMP
prod = ''
# The following group is the MOZ root group within AMP
money = ''

# We create a string that contains the path to the AMP REST API
url = 'https://api.amp.cisco.com/v1/computers'
# Below will get the json data from AMP and store it in a dict
request = requests.get(url, auth=(amp_client_id, amp_api_key), data={'group_guid':group_guid})
# The following creates an object and only include the 'data' from the json dict
move = request.json()['data']
# We print the object "move" to list all PCs within the Audit policy
print (move)
# Below will create a for loop to look at each PC within the Audit policy within AMP
for d in move:
    # We set the string 'hostname' from the dict and store it in a string
    hostname = d['hostname']
    # We set the string 'guid' from the dict and store it in a string
    guid = d['connector_guid']
    # we print each hostname and guid within the Audit Policy
    print(d['hostname'], ':', d['connector_guid'])
    # The following will perform a Regular Expression to match/move the computers to the correct policy in AMP
    if re.search(r'^((?!MG)(?!mg)(?!dc1)(?!DC1)(?!NH)(?!nh)(?!..IC)(?!..ic)([A-Za-z]{2}))', hostname):
        url = 'https://api.amp.cisco.com/v1/computers/{}'.format(guid)
        request = requests.patch(url, auth=(amp_client_id, amp_api_key), data={'group_guid': store_guid})
    # The following will perform a Regular Expression to match/move the computers to the correct policy in AMP
    elif re.search(r'^(REG-EX)', hostname):
        url = 'https://api.amp.cisco.com/v1/computers/{}'.format(guid)
        request = requests.patch(url, auth=(amp_client_id, amp_api_key), data={'group_guid': ic_guid})
    # The following will perform a Regular Expression to match/move the computers to the correct policy in AMP
    elif re.search(r'^(REG-EX)',
                   hostname):
        url = 'https://api.amp.cisco.com/v1/computers/{}'.format(guid)
        request = requests.patch(url, auth=(amp_client_id, amp_api_key), data={'group_guid': dev})
    elif re.search(r'^(REG-EX)',
                   hostname):
        url = 'https://api.amp.cisco.com/v1/computers/{}'.format(guid)
        request = requests.patch(url, auth=(amp_client_id, amp_api_key), data={'group_guid': prod})
    elif re.search(r'^(REG-EX)',
                   hostname):
        url = 'https://api.amp.cisco.com/v1/computers/{}'.format(guid)
        request = requests.patch(url, auth=(amp_client_id, amp_api_key), data={'group_guid': money})
