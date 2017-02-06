# Watchdog Health Checker

A versatile python app to query a health.txt file on a remote server and perform Slack alerts in the event that the server is malfunctioning.

<center>![Watchdog](images/logo.png)</center>

Installation
------------

### 1. Cloning the repository

Perform a simple "git clone" request from the [URL](https://github.com/bonlineza/watchdog-health-checker.git)
and all the relevant files will be downloaded.

```
$ git clone https://github.com/bonlineza/watchdog-health-checker.git
```

### 2. Installing dependencies

Ensure that Python 3.4+ is installed, along with the following library:

* ```requests```

If ```requests``` is not installed, you can install it through ```pip3```
by opening your terminal and typing

```
$ sudo pip3 install requests
```

If ```pip3``` is not installed, install it by typing
```
$ sudo apt-get install python3-pip
```

### 3. Configuring your JSON file

The provided file ```secrets-sample.json``` illustrates the format required for use with ```watchdog.py```. Duplicate this file and name the
copy ```secrets.json``` (which is the default file that watchdog looks for).

``` json
{
  "webhook": "https://<your Slack webhook>",
  "server": "https://your-domain.com/health.txt",
  "expected": "healthy\n",
  "channel": "alerts",
  "username": "health-alert-bot",
  "text": "Server is down!"
}
```

Usage Instructions
------------
In terminal, navigate to the project directory.
This directory should contain ```watchdog.py```.

To run the script, type:

```
$ python3 watchdog.py
```

The script begins running and gives feedback on its current status.
Press CTRL+C in terminal at any time to stop the script.

For advanced functionality, you can pass parameters into the script
via the command line.

```
$ python3 watchdog.py [-s <secrets-file>] [-n <your-name>] [-p <prepend-message>] [-w <wait-seconds>]
```

This list can be viewed at any time by using either of the help flags:
```
$ python3 watchdog.py -h
$ python3 watchdog.py --help
```

* ```<secrets-file>``` is the JSON file with your configuration details.

* ```<your-name>``` is any string to help identify you on the Slack alerts.

* ```<prepend-message>``` is any string which will come at the start ofthe slack alert.

* ```<wait-seconds>``` is a positive integer that indicates how many seconds the script waits before performing another check.


How does it work?
-----------
```watchdog.py``` utilises the ```requests``` library to assert that the user has internet access.

Thereafter, the script uses ```requests.get(url)``` to retrieve the contents of the [health file](http://hicarbyecar.com/health.txt).

If the request succeeds and the health file contains the expected text, the script begins a ```time.sleep()``` period, after which it iterates again.

If the request fails or the health file contains unexpected text, the ```alert_slack()``` function is called. This uses ```requests.post()``` to send JSON data to the appropriate webhook. Slack then posts the according message to the appropriate group.

Contacts
--------

* Maintained by: [B Online](http://www.bonline.co.za/)
* Original author: [Gianluca Truda](https://github.com/gianlucatruda)
