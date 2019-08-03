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

def send_qr(camera, scanner, hubManager):
    while True:
        try:
            global SENT_MESSAGES
            
            (width, height, raw_img) = camera.Capture(1)
            (is_qr, text_value) = scanner.ReadQR(width, height, raw_img)

            if(is_qr):            
                #pack and send message
                current_utc_time = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S.%f")[:-2] #remove the last 2 cyphers from ms to obtain 4 cypher ms
                output = {
                    "text_value":text_value,
                    "send_date": current_utc_time,
                }
                outputJson = json.dumps(output)

                message = IoTHubMessage(outputJson)
                map_properties = message.properties()
                map_properties.add("sequenceNumber", str(SENT_MESSAGES))

                hubManager.send_async("output1", message, 0)
                print("-- sent message: {} - {}".format(SENT_MESSAGES, outputJson))
                SENT_MESSAGES += 1
            else:
                print("qr not detected")

        except Exception as e:
            print(e)
            raise
        
        time.sleep(hubManager.MESSAGE_DELAY)

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

        send_qr(camera, scanner, hub_manager)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubModuleClient sample stopped" )

if __name__ == '__main__':
    main(PROTOCOL)