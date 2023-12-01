# coding: utf-8
import requests
import json

url = "http://192.168.3.234/api/msg"

payload = json.dumps({
  "cmd": "APPS_SYS_INFO",
  "args": "G0C0S0",
  "msg_id": "83151E9F-3947-41A9-76D1-D96AC9147781"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
