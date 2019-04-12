import json
import requests
import time
import threading
import RPi.GPIO as GPIO

import logging
logging.basicConfig(filename='/opt/divera-pi_alert/pialert.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

# normalize config file dict that returns new dict
def get_conf(config_json):
    conf = {"r_pin" : "" , "api_key" : "", "method" : "", "application" : "", "type" : ""}
    conf["r_pin"] = config_json["hardware"]["reading_pin"]
    conf["api_url"] = config_json["webapi"]["url"]
    conf["api_key"] = config_json["webapi"]["key"]
    conf["req_type"] = config_json["request"]
    logging.debug("configuration:")
    logging.debug(conf)
    return conf


def call_api(conf):
    logging.debug("CALL_Api function started")
    dict_data = conf["req_type"]
    api_uk = conf["api_url"] + conf["api_key"]
    req = requests.get(api_uk)
    logging.debug("Request:")
    logging.debug(req)
    logging.debug("Request-URL:")
    logging.debug(req.url)
    logging.debug("Request-answer:")
    logging.debug(req.content)
    logging.debug("Status_code:")
    logging.debug(req.status_code)
    while req.status_code != 200:
        logging.critical("Request was not successful, Status code:")
        logging.critical(req.status_code)
        logging.critical("Waiting 60 seconds")
        time.sleep(60)
        logging.debug("new try")
        req = requests.get(api_uk)
        logging.critical("Request:")
        logging.critical(req)
        logging.critical("Request-URL:")
        logging.critical(req.url)
        logging.critical("Request-answer:")
        logging.critical(req.content)
        logging.critical("Status_code:")
        logging.critical(req.status_code)


# setup gipo as input and layout
def gpio_in(r_pin):
    # RPi.GPIO Layout verwenden (wie doku)
    logging.debug("Setting GPIO layout as docu")
    GPIO.setmode(GPIO.BCM)
    # Set up the GPIO channels - one input 
    logging.debug("Set up the GPIO channels - one input")
    GPIO.setup(r_pin, GPIO.IN)


def check_state(r_pin):
    if GPIO.input(r_pin) == GPIO.LOW:
        v_pin_state = 0
        time.sleep(0.1)
    elif GPIO.input(r_pin) == GPIO.HIGH:
        v_pin_state = 1
        time.sleep(0.1)
    else:
        return False
    return v_pin_state


def toggle(dict_conf):
    gpio_in(dict_conf['r_pin'])
    first_run = True
    logging.debug("Startet toggle")
    while 1:
        v_state = check_state(dict_conf['r_pin'])

        if first_run:
            logging.debug("first run")
            if v_state == 1:
                log_string = "GPIO" + str(dict_conf['r_pin']) + ": high"
                logging.debug("GPIO-state:")
                logging.debug(log_string)
                # alert
                logging.debug("v_state= 1: Alert: Calling API")
                call_api(dict_conf)
                logging.debug("v_state= 1: Left API CALL, sleeping 120 seconds")
                time.sleep(120)
                logging.debug("End of sleep")
            elif v_state == 0:
                log_string2 = "GPIO" + str(dict_conf['r_pin']) + ": low"
                logging.debug("GPIO-state:")
                logging.debug(log_string2)
        elif v_state != v_state_c:
            logging.debug("not first run")
            if v_state == 1:
                log_string3 = "GPIO" + str(dict_conf['r_pin']) + ": high"
                logging.debug("GPIO-state:")
                logging.debug(log_string3)
                # alert
                logging.debug("v_state!= v_state_c: Alert: Calling API")
                call_api(dict_conf)
                logging.debug("v_state!= v_state_c: Left API CALL, sleeping 120 seconds")
                time.sleep(120)
                logging.debug("End of sleep")
            elif v_state == 0:
                log_string4 = "GPIO" + str(dict_conf['r_pin']) + ": low"
                logging.debug("GPIO-state:")
                logging.debug(log_string4)

        first_run = False
        v_state_c = v_state


def read_json(file):
    with open(file) as json_file:
        config_json = json.load(json_file)
    logging.debug(config_json)
    logging.debug(type(config_json))
    return config_json


def main():
    logging.debug("Pialert started")
    f_conf = read_json("/opt/divera-pi_alert/static/config.json")
    dict_conf = get_conf(f_conf)
    th_gpio = threading.Thread(target=toggle(dict_conf))

main()

