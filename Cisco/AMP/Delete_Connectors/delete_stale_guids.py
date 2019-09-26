from datetime import datetime
from collections import namedtuple
import configparser
import sys
import requests
# The following library is used to interact with the Thycotic Secret Server SOAP API
import suds.client
# The following library is used to encrypt the password that interacts with the Thycotic API
from cryptography.fernet import Fernet

UTC_NOW = datetime.utcnow()

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

def calculate_time_delta(timestamp):
    '''Calculate how long it has been since the GUID was last seen
    '''
    time_format = '%Y-%m-%dT%H:%M:%SZ'
    datetime_object = datetime.strptime(timestamp, time_format)
    age = (UTC_NOW - datetime_object).days
    return age

def should_delete(age, threshold):
    '''Check if the GUID age is greater than the configured threshold
    '''
    if age > threshold:
        return True
    return False

def process_guid_json(guid_json):
    '''Process the individual GUID entry
    '''
    computer = namedtuple('computer', ['hostname', 'guid', 'age'])
    connector_guid = guid_json.get('connector_guid')
    hostname = guid_json.get('hostname')
    last_seen = guid_json.get('last_seen')
    age = calculate_time_delta(last_seen)
    return computer(hostname, connector_guid, age)

def process_response_json(json, age_threshold):
    '''Process the decoded JSON blob from /computers
    '''
    computers_to_delete = set()
    for entry in json['data']:
        computer = process_guid_json(entry)
        if should_delete(computer.age, age_threshold):
            computers_to_delete.add(computer)
    return computers_to_delete


def delete_guid(session, guid, hostname):
    '''Delete the supplied GUID
    '''
    url = 'https://api.amp.cisco.com/v1/computers/{}'.format(guid)
    response = session.delete(url)
    response_json = response.json()

    if response.status_code == 200 and response_json['data']['deleted']:
        print('Succesfully deleted: {}'.format(hostname))
    else:
        print('Something went wrong deleting: {}'.format(hostname))

def get(session, url):
    '''HTTP GET the URL and return the decoded JSON
    '''
    response = session.get(url)
    response_json = response.json()
    return response_json

def main():
    '''The main logic of the script
    '''

    client_id = amp_client_id
    api_key = amp_api_key
    age_threshold = 30

    # Instantiate requestions session object
    amp_session = requests.session()
    amp_session.auth = (client_id, api_key)

    # Set to store the computer tuples in
    computers_to_delete = set()

    # URL to query AMP
    computers_url = 'https://api.amp.cisco.com/v1/computers'

    # Query the API
    response_json = get(amp_session, computers_url)

    # Print the total number of GUIDs found
    total_guids = response_json['metadata']['results']['total']
    print('GUIDs found in environment: {}'.format(total_guids))

    # Process the returned JSON
    initial_batch = process_response_json(response_json, age_threshold)

    # Store the returned stale GUIDs
    computers_to_delete = computers_to_delete.union(initial_batch)

    # Check if there are more pages and repeat
    while 'next' in response_json['metadata']['links']:
        next_url = response_json['metadata']['links']['next']
        response_json = get(amp_session, next_url)
        index = response_json['metadata']['results']['index']
        print('Processing index: {}'.format(index))
        next_batch = process_response_json(response_json, age_threshold)
        computers_to_delete = computers_to_delete.union(next_batch)

    # Output the number of GUIDs found
    print('Found {} guids that have not been seen for'
          ' at least {} days'.format(len(computers_to_delete), age_threshold))

    if computers_to_delete:
        print('Writing CSV containing stale GUIDs to stale_guids.csv')
        with open('stale_guids.csv', 'w', encoding='utf-8') as file_output:
            file_output.write('Age in days,GUID,Hostname\n')
            for computer in computers_to_delete:
                file_output.write('{},{},{}\n'.format(computer.age,
                                                      computer.guid,
                                                      computer.hostname))
        # Check if the user wants to GUIDs to be deleted

        for computer in computers_to_delete:
            delete_guid(amp_session, computer.guid, computer.hostname)


if __name__ == "__main__":
    main()
