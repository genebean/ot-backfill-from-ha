import json
import os
import requests
import time
from requests.auth import HTTPBasicAuth
from datetime import datetime
from datetime import timezone

from dotenv import load_dotenv

load_dotenv()

url = "%s/api/history/period/%s" % (os.getenv("HA_URL"), os.getenv("HA_PERIOD_START"))
params = {
    'filter_entity_id': os.getenv("HA_ENTITIES"),
    'end_time': os.getenv("HA_PERIOD_END")
}
headers = {
    'Authorization': 'Bearer ' + os.getenv("HA_TOKEN"),
    'content-type': 'application/json'
}
response = requests.get(url,headers=headers,params=params)

query_timestamp = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
OT_TOPIC = "owntracks/%s/%s" % (os.getenv("OT_USER"), os.getenv("OT_DEVICE_ID"))
OT_TID = os.getenv("OT_TID")

ot_entries = []

for state in response.json()[0]:
    if state['attributes']['source_type'] == 'gps':
        entry = {}
        entry['topic'] = OT_TOPIC
        entry['bs'] = 0
        entry['tid'] = OT_TID
        entry['created_at'] = query_timestamp
        entry['_type'] = 'location'
        entry['lat'] = state['attributes']['latitude']
        entry['lon'] = state['attributes']['longitude']
        entry['acc'] = int(state['attributes']['gps_accuracy'])
        if 'altitude' in state['attributes']:
            entry['alt'] = int(state['attributes']['altitude'])
        if 'vertical_accuracy' in state['attributes']:
            entry['vac'] = int(state['attributes']['vertical_accuracy'])
        if 'course' in state['attributes']:
            entry['cog'] = int(state['attributes']['course'])
        if 'speed' in state['attributes']:
            entry['vel'] = int(state['attributes']['speed'] * 3.6)
        entry['batt'] = int(state['attributes']['battery_level'])
        entry['tst'] = int(datetime.fromisoformat(state['last_updated']).replace(tzinfo=timezone.utc).timestamp())
        ot_entries.append(entry)



ot_url = os.getenv("OT_URL")
ot_headers = {
    'X-Limit-U': os.getenv("OT_USER"),
    'X-Limit-D': os.getenv("OT_DEVICE_ID")
}
ot_basic = HTTPBasicAuth(os.getenv("OT_AUTH_USER"), os.getenv("OT_AUTH_PASS"))


## This version sends all the updates at once - thus far, this doesn't seem to
## work our right, but I may be doing it wrong.

# ot_response = requests.post(ot_url,headers=ot_headers,auth=ot_basic,json=ot_entries)
# print(json.dumps(ot_response.json(), indent=2))
# print('okay? ' + str(ot_response.ok))
# print('response code: ' + str(ot_response.status_code))

## This version sends each state from Home Assistant individually and sleeps
## for a tenth of a second between POSTs to let things process - I am not
## sure if the sleep is needed as it was added to aide in debugging
for ot_entry in ot_entries:
    ot_response = requests.post(ot_url,headers=ot_headers,auth=ot_basic,json=ot_entry)
    # print(json.dumps(ot_response.json(), indent=2))
    # print('okay? ' + str(ot_response.ok))
    # print('response code: ' + str(ot_response.status_code))
    time.sleep(0.1)
