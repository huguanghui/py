# coding: utf-8
import sys
import os
import requests
import json
import time
import logging

if hasattr(sys, "frozen"):
    os.environ["PATH"] = sys._MEIPASS + ";" + os.environ["PATH"]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def send_get_battery_request():
    url = "http://10.10.10.1/api/msg"
    payload = json.dumps(
        {
            "cmd": "APPS_STATUS",
            "args": "G0C0S0",
            "msg_id": "83151E9F-3947-41A9-76D1-D96AC9147781",
        }
    )
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None


if __name__ == "__main__":
    local_app_data_dir = os.getcwd()
    print("dir:", local_app_data_dir)
    file_handler = logging.FileHandler(os.path.join(local_app_data_dir, "user.log"))
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    while True:
        response = send_get_battery_request()
        if response is not None:
            info_data = json.loads(response)
            electric = info_data["data"]["electricity"]
            logger.info("battery: {0}".format(electric))
        time.sleep(120)
