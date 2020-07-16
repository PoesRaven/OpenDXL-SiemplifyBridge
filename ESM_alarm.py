from __future__ import absolute_import
from __future__ import print_function
import logging
import os
import sys
import time
import json
from threading import Condition

from dxlclient.callbacks import EventCallback
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event

from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# The topic to listen on
EVENT_TOPIC = "/mcafee/event/esm/alarm"
SIEMPLIFY_EVENT_TOPIC = "/mcafee/event/trigger"


# Condition/lock used to protect changes to counter
event_count_condition = Condition()

# The events received (use an array so we can modify in callback)
event_count = [0]

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

# Create the client
with DxlClient(config) as client:

    # Connect to the fabric
    client.connect()

    #
    # Register callback and subscribe
    #

    # Create and add event listener
    class MyEventCallback(EventCallback):
        def on_event(self, event):
            with event_count_condition:
                # Print the payload for the received event
                print("Received event {}: {}".format(event_count[0], event.payload.decode()))

                # Import the JSON for manipulation
                event_payload_in = json.loads(event.payload.decode())

                # Since we are listening on the SIEM topic, we know the exsting SIEM format. 
                # Buld an out payload standardized for SIEMplify
                event_payload_out = {}
                event_payload_out['raw_message'] = event.payload.decode()
                event_payload_out['type'] = "alert"
                event_payload_out['name'] = event_payload_in['AlarmName']
                event_payload_out['rule_generator'] = event_payload_in['Summary']
                event_payload_out['end_time'] = event_payload_in['TriggerDate']
                event_payload_out['priority'] = event_payload_in['Severity']
                event_payload_out['device_vendor'] = "McAfee"
                event_payload_out['device_product'] = "ESM"
                event_payload_out['events'] = []

                # Cycle through each of the events for SIEM Alarm and append them to the Siemplify payload
                for event in event_payload_in['Events']:
                    if len(event) > 0:
                        print(event)
                        event_out = {}
                        event_out['StartTime'] = event['LastTime']
                        event_out['EndTime'] = event['LastTime']
                        event_out['name'] = event['Message']
                        event_out['SourceHostName'] = "N/A"
                        event_out['DestinationHostName'] = "N/A"
                        event_out['SourceAddress'] = event['SourceIP']
                        event_out['DestinationAddress'] = event['DestinationIP']
    
                        event_payload_out['events'].append(event_out)



                # Create the event
                siemplify_event = Event(SIEMPLIFY_EVENT_TOPIC)
                # Set the payload
                siemplify_event.payload = json.dumps(event_payload_out, indent=2).encode()
                # Send the event
                client.send_event(siemplify_event)


                logger.info(event_payload_out)
                logfile = open('log.txt', "w")
                logfile.write(json.dumps(event_payload_out))
                logfile.close()


                # Increment the count
                event_count[0] += 1
                # Notify that the count was increment
                event_count_condition.notify_all()

    # Register the callback with the client
    client.add_event_callback(EVENT_TOPIC, MyEventCallback())



    print("Waiting for events to be received...")
    with event_count_condition:
        while True:
            event_count_condition.wait()

