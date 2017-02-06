"""
Python 3.4 (may work on 2.7+ but not supported).
Checks if server returns expected health check.
Alerts a selected Slack channel if server down.
Version 1.1
06-02-2017

Dependencies:
- requests
"""

# Importing required libraries and dependencies.
import json
import requests
import time
import sys
import getopt

# Defining some default parameters for use in the standard case.
secrets_file_name = 'secrets.json'
prepend = 'ALERT'
my_name = 'DEFAULT'
wait_time = '60'


def online():
    """
    Checks if the user is currently connected to the internet.
    :return: boolean
    """
    try:
        response = requests.get('https://www.google.co.za')
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException as e:
        return False


def alert_slack(data, message='0'):
    """
    Alerts the pre-selected Slack channel about server being down.
    :param data: The json data from the config file.
    :param message: An optional message to display instead of the one in the config file.
    :return: boolean
    """
    if message == '0':
        message = data['text']
    slack_data = {"channel": data['channel'], "username": data['username'],
                  "text": prepend+' || '+ message + '\nsent from ' + my_name}
    slack_payload = json.dumps(slack_data)
    response = requests.post(slack_url, data=slack_payload)
    if response.status_code != 200:
        print('ERROR: Alert could not be sent to Slack!')
        return False
    else:
        print('Alert sent to Slack.')
        return True

if __name__ == '__main__':

    # Code to manage and respond to user command line parameters.
    argv = sys.argv[1:]
    usage_text = "[-s <secrets-file>] [-n <your-name>] [-p <prepend-message>] [-w <wait-seconds>] [-h Help]"
    try:
        opts, args = getopt.getopt(argv, 's:n:p:w:h', ["secrets=", "name=", "prepend=", "wait=", "help"])
    except getopt.GetoptError:
        print('ERROR in commandline parameters.\n'+usage_text)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--secrets"):
            secrets_file_name = arg
        elif opt in ("-n", "--name"):
            my_name = arg
        elif opt in ("-p", "--prepend"):
            prepend = arg
        elif opt in ("-w", "--wait"):
            wait_time = arg
            if float(wait_time) < 5.0:
                wait_time = '5'
        elif opt in ("-h", "--help"):
            print(usage_text)
            sys.exit(2)

    try:    # This try-except is to catch keyboard interrupt (ctrl+c).
        try:    # The script attempts to retrieve configuration from the json file.
            with open(secrets_file_name) as data_file:
                try:
                    secrets = json.load(data_file)
                except:
                    print("Error: Your .json file couldn't be found or is incorrectly formatted.")
                    sys.exit(2)
                server_url = secrets['server']
                slack_url = secrets['webhook']
        except:
            print("Error: Your .json file couldn't be found or is incorrectly formatted.")
            sys.exit(2)
        print("Press ctrl+c to exit.")

        # The script infinitely loops and checks the status of the server at regular intervals.
        while True:
            if online():    # the script only attempts a request if the machine is online.
                try:
                    check = requests.get(server_url)
                    if check.text != secrets['expected']:
                        print('Server', secrets['server'], 'is down!.')
                        alert_slack(secrets)
                    else:
                        print('Server', secrets['server'], 'is healthy.')
                except requests.RequestException as e:
                    alert_slack(secrets, message="Something is wrong with watchdog.py | The server may have a problem!")
                    print('ERROR: Cannot retrieve health data!')
            else:
                print('ERROR: Your internet connection is offline.')

            # The script waits for the user-determined duration (seconds) and then re-tries.
            time.sleep(float(wait_time))

    except KeyboardInterrupt:
        sys.exit(3)