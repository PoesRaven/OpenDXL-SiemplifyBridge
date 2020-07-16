# OpenDXL-SiemplifyBridge
Consumers and repeaters for sending DXL messages to the McAfee DXL Integration with Siemplify (https://www.siemplify.co)

Anything connecting to the DXL fabric needs to have gone through the DXL client provisioning process: https://opendxl.github.io/opendxl-client-python/pydoc/basiccliprovisioning.html


## Formatting
When creating a JSON payload needing to be consumed by the DXL subscriber for Siemplify, we expect the following JSON
``` js
{
  "raw_message": {<original message being converted escaped to string>},
  "type": "alert",  // Future proofing. Right now alerts are the only types for creating cases
  "name": "Mimikatz", // Case Name
  "rule_generator": "Matched JTI behavior", // The actual reason the alert/case was created
  "end_time": "2019/12/25 08:00:00 UTC", // Time format is dynamically parsed on the subscriber so no fear
  "priority": "35", // Integer as string 0-100. Defines the Priority value for the Case to be created
  "device_vendor": "McAfee", // String indicating the make of the detecting alarm generator
  "device_product": "Real Protect", // Product triggering the alarm
  "events": [ // Array of events in the following format
    {
      "StartTime": "2019/12/25 08:00:00 UTC", // Time format is dynamically parsed on the subscriber so no fear
      "EndTime": "2019/12/25 08:00:00 UTC", // Time format is dynamically parsed on the subscriber so no fear
      "name": "JTI behavior noticed LSASS activities indicative of Mimikatz", // event name from the originating product
      "SourceHostName": "JohnsComputer",
      "SourceAddress": "12.34.56.78",
      "DestinationHostName": "JanesComputer",
      "DestinationAddress": "12.34.56.87"
    }
    ,...
  ]
}
```
The formatting can be extended but would require updates on the DXL Subscriber integration to ensure it is loaded into the newly created case.

## ESM_alarm.py
This bridge consumes native alarm data from McAfee's ESM alarms which have been published over DXL(This requires ESM 11.3). Then the alarm data is converted into bridge format (see above) and published to the `/mcafee/event/trigger/` topic. Ensure the Siemplify DXL Subscriber is listening to this topic. 

