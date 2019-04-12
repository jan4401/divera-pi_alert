# FF Raspberry PI to Divera Project
This project has the following functionalities:
1) Read GPIO to check for alert on DME station
2) Request Divera24/7 WebAPI 


## GPIO Functionality
Reads GPIO that is specified in config file as input.
If GPIO changes from low to high, an alert will be triggered at DIVERA24/7.

## DIVERA24/7 API
A HTTPS GET request is sent to the DIVERA24/7 Web API to trigger an alert.
I used the python3 requests bib (installation: pip3 install requests).
 

## Config file
The config file is located in the static directory

* hardware: Reading GPIO Port
* webapi: DIVERA24/7 API Key
* request: JSON POST Request

## Hardware Specification
This project is using a Raspberry PI3 that is connected with an Oelmann LX4 home station.
One GPIO has to be in reading mode and is connected to the relay output of the LX4 home station.
If the relay is closed by an alert, the GPIO state changes from LOW to high and a request to DIVERA24/7 Web API is triggered.
The reading/input GPIO must be connected to a pull down resistor (e.g. 100kOhm) that connects the GPIO to the Raspberry PI Ground.



## External Information/Documentation
* RPi
 ** GPIO: https://de.pinout.xyz/
* DIVERA24/7
  ** API: https://www.divera247.com/downloads/divera247_webschnittstelle_zur_alarmierung.pdf
* Python
  ** Requests: http://www.pythonforbeginners.com/requests/using-requests-in-python
  ** GPIO: http://raspberrypiguide.de/howtos/raspberry-pi-gpio-how-to/
