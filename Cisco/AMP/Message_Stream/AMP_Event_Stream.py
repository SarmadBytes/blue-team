import requests
import time
import amp_api
import json
import sys
import pika
import pysnow
import suds.client
from cryptography.fernet import Fernet
# from tenable.sc import TenableSC


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
username = split_username.split("\n")[1]
# Below will split the object to include the username from the secretitem
split_password = split.split("SecretItem")[6]
# This will remove any blank lines that are stored in the object
password = split_password.split("\n")[1]
# The following will remove any white spaces stored in the string
user = username.split()[2]
# The following will remove any white spaces stored in the string
pass1 = password.split()[2]

# Below will remove the '"' from the object
amp_client_id = user.replace('"', '')
# Below will remove the '"' from the object
amp_api_key = pass1.replace('"', '')

# AMP 3rd Party API Client ID
AMP_CLIENT_ID = amp_client_id

# AMP API Key
AMP_API_KEY = amp_api_key


def verify_auth(session):
    '''Verify which AMP cloud the provided client_id and api_key are valid for.
        Return the Domain and Region Name for the cloud the credentials are valid in.
    '''
    region_domains = {'api.amp.cisco.com': 'North America',
                      'api.apjc.amp.cisco.com': 'Asia',
                      'api.eu.amp.cisco.com': 'Europe'}

    for named_domain in region_domains:
        version_url = 'https://{}/v1/version'.format(named_domain)
        response = session.get(version_url)

        if response.status_code == 200:
            return named_domain, region_domains[named_domain]

    sys.exit('It doesn\'t look like the credentials you provided are valid in any region')


def get_streams(session, domain):
    '''Get existing event streams
    '''
    url = 'https://{}/v1/event_streams'.format(domain)
    response = session.get(url)
    response_json = response.json()
    data = response_json['data']
    return data


def delete_stream(session, domain, stream_id):
    '''Delete an event stream
    '''
    url = 'https://{}/v1/event_streams/{}'.format(domain, stream_id)
    headers = {'accept': 'application/json',
               'content-type': 'application/json',
               'Accept-Encoding': 'gzip, deflate'
               }

    response = session.delete(url, headers=headers)
    return response


def ask_for_stream_id(valid_ids):
    '''Ask the user for a Stream ID
       Keep asking until they enter a valid Stream ID
    '''
    while True:
        reply = str(input('Enter the ID of the stream you would like to delete: ')).strip()
        if reply in valid_ids:
            return reply
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        sys.stdout.write('{} is not a valid stream ID try again.\n'.format(reply))


def main():
    '''The main script logic
    '''

    # Instantiate a session object with authentication
    amp_session = requests.Session()
    amp_session.auth = (AMP_CLIENT_ID, AMP_API_KEY)

    # Check which cloud the credentials are valid in
    domain, region = verify_auth(amp_session)

    # Output which region will be used
    print('Successfully authenticated to: {}\n'.format(region))

    # Query the API for existing Event Streams
    stream_data = get_streams(amp_session, domain)
    streams = {str(stream['id']):stream['name'] for stream in stream_data}

    # Verify that you want to continue
    print('-=== WARNING THIS SCRIPT WILL DELETE THINGS ===-')

    # Exit if there are no existing Event Streams
    if not streams:
        print('There are no streams to delete')
        amp()

    # Print existing Event Streams to the console
    print('{:>3} {:>12}'.format('ID', 'Name'))
    for stream_id, stream_name in streams.items():
        print('{} - {}'.format(stream_id, stream_name))

    # Ask for the Event Stream ID to delete
    to_delete = list(streams.keys())[0]

    # Delete the Event Stream
    delete_response = delete_stream(amp_session, domain, to_delete)

    # Check if errors were returned
    if delete_response.status_code // 100 != 2:
        reason = delete_response.json()['errors'][0]['details'][0]
        sys.exit('\nFailed to create stream: {}'.format(reason))

    print('Request to delete {} sent Successfully'.format(to_delete))
    time.sleep(60)
    amp()


def amp():
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
    # This will search for the specific secret based on ID
    searchSecret = client.service.GetSecret(token.Token, secretId=8802)
    # The following will split the results from the searchSecret into multiple splices
    split = str(searchSecret)
    # Below will split the object to include the username from the secretitem
    split_username = split.split("SecretItem")[5]
    # This will remove any blank lines that are stored in the object
    username = split_username.split("\n")[1]
    # Below will split the object to include the username from the secretitem
    split_password = split.split("SecretItem")[6]
    # This will remove any blank lines that are stored in the object
    password = split_password.split("\n")[1]
    # The following will remove any white spaces stored in the string
    user = username.split()[2]
    pass1 = password.split()[2]
    # Below will remove the '"' from the object
    SNowuser = user.replace('"', '')
    # Below will remove the '"' from the object
    SNowpass = pass1.replace('"', '')
    # Import variables to get configuration
    log = open("debug.log", "w")
    log.write("**debug - loading in parameters now....\n")
    # Create dictionary of variables
    var = {
        "debug": "true",
        "client_id": AMP_CLIENT_ID,
        "api_key": AMP_API_KEY,
        "endpoint": "api.amp.cisco.com",
        "group_name": "Protect - Global",
        "event_name": "Threat Detected",
        "event_ids": [1107296274, 1107296262, 2164260880, 1091567628,
                      1090519084, 1090519112, 1107296272, 553648166, 1003, 1004, 1005, 553648147, 1107296257, 1107296258,
                      1107296261, 1107296263, 1107296264, 1107296266, 1107296267, 1107296268, 1107296269, 1107296270,
                      1107296271, 1107296273, 1107296275, 1107296276, 1107296277, 1107296278, 1107296280, 1107296281,
                      1107296282, 1107296284, 1107296283, 1090519081, 1090519105, 553648199],
        "event_choice": "id"
    }

    if var["debug"]:
        log.write("**debug - parameters loaded in.... OK!\n")
        log.write("**debug - begin parameter check....\n")
    else:
        log.write("**debug - debug logging is disabled!\n")

    if var["debug"]:
        log.write("**debug - parameter check complete.... OK!\n")

    amp = amp_api.amp(var["endpoint"], var["client_id"], var["api_key"])

    group_data = amp.get("/v1/groups")
    found = False
    for group in group_data["data"]:
        if group["name"] == var["group_name"]:
            group_guid = group["guid"]
            found = True

    if found and var["debug"]:
        log.write("**debug - group found with ID {}.... OK!\n".format(group_guid))
    elif not found:
        print("FAIL - group name doesnt exist: {}".format(var["group_name"]))
        sys.exit()

    if var["event_choice"] == "name":
        found = False
        event_list = amp.get("/v1/event_types")
        for event in event_list["data"]:
            if event["name"] == var["event_name"]:
                event_id = event["id"]
                found = True

        if found and var["debug"]:
            log.write("**debug - event type found with ID {}.... OK!\n".format(event_id))
        elif not found:
            print("FAIL - event type doesnt exist: {}".format(var["event_name"]))
            sys.exit()

        body = {
            "name": "InfoSec_Dev",
            "event_type": ["{}".format(event_id)],
            "group_guid": ["{}".format(group_guid)]
        }
    if var["event_choice"] == "id":
        body = {
            "name": "InfoSec_Dev",
            "event_type": var["event_ids"],
            "group_guid": ["{}".format(group_guid)]
        }
    print(body)
    event_stream = amp.post("/v1/event_streams", body)
    if var["debug"]:
        log.write("**debug - event stream created.... OK!\n")
        log.write("**debug - begining work to start listening for events.... OK!\n")
    print(event_stream)
    print("---------")
    url = "amqps://{}:{}@{}:{}".format(
        event_stream["data"]["amqp_credentials"]["user_name"],
        event_stream["data"]["amqp_credentials"]["password"],
        event_stream["data"]["amqp_credentials"]["host"],
        event_stream["data"]["amqp_credentials"]["port"]
    )
    print(url)

    parameters = pika.URLParameters(url)
    SelectConnection = pika.BlockingConnection(parameters)
    channel = SelectConnection.channel()

    channel.queue_declare(queue=event_stream["data"]["amqp_credentials"]["queue_name"], passive=True)

    c = pysnow.Client(instance='COMPANY', user=SNowuser, password=SNowpass)
    incident = c.resource(api_path='/table/incident')

    def callback(ch, method, properties, body):
        # json_acceptable_string = body.replace("'", "\"")
        d = json.loads(body)
        print(" [x] Received %r" % body)
        event = d["event_type"]
        print(event)
        pc = d["computer"]["hostname"]
        severity = d["severity"]
        log = body.decode('ascii')

        def recursive_items(dictionary):
            for key, value in dictionary.items():
                if type(value) is dict:
                    yield from recursive_items(value)
                else:
                    yield (key, value)

        test = []
        test1 = []
        for key, value in recursive_items(d):
            work_notes = key, "=", value
            test.append(work_notes)

        for tup in test[:-1]:
            a = str('   '.join(map(str, tup)))
            test1.append(a)
        data = "\n".join(test1)
        with open("event.txt", "a") as myfile:
            myfile.write(log)
        new_record = {
                'short_description': 'AMP : ' + severity + ' : Event : ' + event + ' : ' + pc,
                'description': 'As a Cisco AMP security analyst, I need to perform detailed analysis on the following '
                               'event "' + event + '" to determine if any malicious behavior has be identified. All '
                                                   'findings will be documented in this incident.',
                'work_notes': data,
                'contact_type': 'automation',
                'category': 'security',
                'subcategory': 'event',
                'cmdb_ci': 'AMP',
                'assignment_group': 'InfoSec'}
        result = incident.create(payload=new_record)


    # json_acceptable_string = body.replace("'", "\"")

    channel.basic_consume(on_message_callback=callback,
                          queue=event_stream["data"]["amqp_credentials"]["queue_name"])
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
