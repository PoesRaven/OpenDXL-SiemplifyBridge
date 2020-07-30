# OpenDXL-SiemplifyBridge
Consumers and repeaters for sending DXL messages to the McAfee DXL Integration with Siemplify (https://www.siemplify.co)

Anything connecting to the DXL fabric needs to have gone through the DXL client provisioning process: https://opendxl.github.io/opendxl-client-python/pydoc/basiccliprovisioning.html


## Formatting
When creating a JSON payload needing to be consumed by the DXL subscriber for Siemplify, we expect the following JSON
``` js
{
  "raw_message": {<original message being converted escaped to string>}, // <REQUIRED>
  "type": "alert",  // <REQUIRED> Future proofing. Right now alerts are the only types for creating cases
  "name": "Mimikatz", // <REQUIRED> Case Name
  "rule_generator": "Matched JTI behavior", // <REQUIRED> The actual reason the alert/case was created
  "end_time": "2019/12/25 08:00:00 UTC", // <REQUIRED> Time format is dynamically parsed on the subscriber so no fear
  "priority": "35", // <REQUIRED> Integer as string 0-100. Defines the Priority value for the Case to be created
  "device_vendor": "McAfee", // <REQUIRED> String indicating the make of the detecting alarm generator
  "device_product": "Real Protect", // <REQUIRED> Product triggering the alarm
  "events": [ // [OPTIONAL] Array of events in the following format
    {
      "StartTime": "2019/12/25 08:00:00 UTC", // [OPTIONAL] Time format is dynamically parsed on the subscriber so no fear
      "EndTime": "2019/12/25 08:00:00 UTC", // [OPTIONAL] Time format is dynamically parsed on the subscriber so no fear
      "name": "JTI behavior noticed LSASS activities indicative of Mimikatz", // <REQUIRED> event name from the originating product
      "SourceHostName": "JohnsComputer", // [OPTIONAL]
      "SourceAddress": "12.34.56.78", // [OPTIONAL]
      "DestinationHostName": "JanesComputer", // [OPTIONAL]
      "DestinationAddress": "12.34.56.87", // [OPTIONAL]
      "ManagerTime": "2019/12/25 08:00:00 UTC", // [OPTIONAL] Time format is dynamically parsed on the subscriber so no fear
      "device_product": "Real Protect", // [OPTIONAL] Product triggering the event (Could be different from the correlated alarm)
      "application_protocol": "https", // [OPTIONAL] Protocol of detected event
      "category_outcome": "Remediated", // [OPTIONAL]
      "destination_port": "443", // [OPTIONAL]
      "destination_username": "jdoe", // [OPTIONAL]
      "device_address": "12.34.56.78", // [OPTIONAL]
      "device_event_class_id": "fdsHotBeefDead", // [OPTIONAL]
      "device_host_name": "JohnsComputer", // [OPTIONAL]
      "device_product": "ENS", // [OPTIONAL]
      "usb": "Kingston-UEFI123", // [OPTIONAL]
      "device_vendor": "McAfee", // [OPTIONAL]
      "event_id": "123-321asdf-3434", // [OPTIONAL]
      "message": "Hot dog, we found it!", // [OPTIONAL]
      "source_user_name": "janeDoe", // [OPTIONAL]
      "severity": "High", // [OPTIONAL]
      "source_type": "IoT", // [OPTIONAL]
      "threat_signature": "RealProtect Cloud Detection", // [OPTIONAL]
      "credit_card": "Visa", // [OPTIONAL]
      "destination_mac_address": "DEADBEEF-DEADBEEF-DEADBEEF-DEADBEEF", // [OPTIONAL]
      "deployment": "global", // [OPTIONAL]
      "generic_entity": "HotDog", // [OPTIONAL]
      "email_subject": "You may want to read this...", // [OPTIONAL]
      "file_hash": "abc123bc85be543456fedacbae6594", // [OPTIONAL]
      "file_name": "HotDog.exe", // [OPTIONAL]
      "source_type": "email", // [OPTIONAL]
      "threat_campaign": "Operation Iron Ore", // [OPTIONAL]
      "destination_url": "https://example.com/ironore/hotdogs_are_yummy", // [OPTIONAL]
      "destination_process_name": "lsass.exe", // [OPTIONAL]
      "source_process_name": "rundll32.exe", // [OPTIONAL]
      "threat_actor": "APT29", // [OPTIONAL]
      "cve": "CVE-2020943", // [OPTIONAL]
      "phone_number": "423-555-1234", // [OPTIONAL]
      "source_mac_address": "BEEFDEAD-BEEFDEAD-BEEFDEAD-BEEFDEAD", // [OPTIONAL]
      "destination_dns_domain": "example.com", // [OPTIONAL]
      "destination_nt_domain": "EXAMPLE, // [OPTIONAL]
      "source_dns_domain": "hotdogs.net", // [OPTIONAL]
      "source_nt_domain": "HOTDOGS" // [OPTIONAL]
    }
    ,...
  ]
}
```
The formatting can be extended but would require updates on the DXL Subscriber integration to ensure it is loaded into the newly created case.

## ESM_alarm.py
This bridge consumes native alarm data from McAfee's ESM alarms which have been published over DXL(This requires ESM 11.3). Then the alarm data is converted into bridge format (see above) and published to the `/mcafee/event/trigger/` topic. Ensure the Siemplify DXL Subscriber is listening to this topic. 

