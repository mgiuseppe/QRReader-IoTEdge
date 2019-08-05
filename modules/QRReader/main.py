# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
from datetime import datetime
import sys
import json
# pylint: disable=E0611
from camera import Camera
from scanner import Scanner
from hubmanager import IoTHubMessage, IoTHubTransportProvider, HubManager, IoTHubError

# global counters
SENT_MESSAGES = 0

#MAIN LOOP -------------------------------

def do(camera, scanner, hub_manager):
    while True:
        try:            
            (is_detected, text_value) = detect_code(camera, scanner)        

            if(is_detected):            
                forward_detected_value(text_value, hub_manager)
            else:
                print("qr not detected")

        except Exception as e:
            print(e)
            raise
        
        time.sleep(hub_manager.MESSAGE_DELAY)

def detect_code(camera, scanner):
    (width, height, raw_image) = camera.Capture(1)
    return scanner.ReadQR(width, height, raw_image)

def forward_detected_value(text_value, hub_manager):
    global SENT_MESSAGES

    #pack message
    current_utc_time = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S.%f")[:-2] #remove the last 2 cyphers from ms to obtain 4 cypher ms
    output = {
        "text_value":text_value,
        "send_date": current_utc_time,
    }
    outputJson = json.dumps(output)

    message = IoTHubMessage(outputJson)
    map_properties = message.properties()
    map_properties.add("sequenceNumber", str(SENT_MESSAGES))

    #send message
    hub_manager.send_async("output1", message, 0)
    print("-- sent message: {} - {}".format(SENT_MESSAGES, outputJson))
    SENT_MESSAGES += 1

# MAIN ---------------------------

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT

def main(protocol):
    try:
        print ( "\nPython %s\n" % sys.version )
        print ( "IoT Hub Client for Python" )

        hub_manager = HubManager(protocol)
        camera = Camera()
        scanner = Scanner()

        print ( "Starting the IoT Hub Python QR Scanner using protocol %s..." % hub_manager.client_protocol )
        print ( "The QR Scanner is now ready to transmit messages.  Press Ctrl-C to exit. ")

        do(camera, scanner, hub_manager)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubModuleClient sample stopped" )

if __name__ == '__main__':
    main(PROTOCOL)