# pylint: disable=E0611
import RPi.GPIO as GPIO
import random
import time
import sys
import iothub_client
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider, DeviceMethodReturnValue
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError

# blink_callback is invoked when an incoming message arrives on the specified input queue (in the case of this sample, "input1").
def blink_callback(message, hubManager):
    print("Message received")
    try:
        blink_led()
    except Exception as e:
        print(e)
    return IoTHubMessageDispositionResult.ACCEPTED

def blink_led():
    global LED_GPIO
    if GPIO.input(LED_GPIO) == 0:
        print ("LED on")
        GPIO.output(LED_GPIO,GPIO.HIGH)
        time.sleep(.5) #500ms
        print(GPIO.input(LED_GPIO))
        GPIO.output(LED_GPIO,GPIO.LOW)
        print ("LED off")

def module_method_callback(method_name, payload, user_context):
    print ( "\nMethod callback called with:\nmethodName = {}\npayload = {}".format(method_name, payload) )
    if(method_name == "switch_led_on"): #Attention: if you change the method name you've to change it also in the alexa function
        blink_led()
    retval = DeviceMethodReturnValue()
    retval.status = 200
    retval.response = "{\"key\":\"value\"}"
    return retval

class HubManager(object):

    def __init__(
            self,
            protocol=IoTHubTransportProvider.MQTT):
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)
        
        # sets the callback when a message arrives on "input1" queue. Messages sent to other inputs or to the default will be silently discarded.
        self.client.set_message_callback("input1", blink_callback, self)
        self.client.set_module_method_callback(module_method_callback, None)

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT
LED_GPIO = 18

def main(protocol):
    try:
        print ( "\nPython %s\n" % sys.version )
        print ( "IoT Hub Client for Python" )

        #init GPIO
        print ( "init LED GPIO {}".format(LED_GPIO) )
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(LED_GPIO,GPIO.OUT)
        GPIO.output(LED_GPIO,GPIO.LOW)
        
        print ( "Starting the IoT Hub Python sample using protocol %s..." % protocol )
        hub_manager = HubManager(protocol)

        print ( "The sample is now waiting for messages and will indefinitely.  Press Ctrl-C to exit. ")

        while True:
            time.sleep(10)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubModuleClient sample stopped" )

if __name__ == '__main__':
    main(PROTOCOL)