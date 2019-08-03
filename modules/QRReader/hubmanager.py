import json
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError

CONFIRMATION_RECEIVED = 0
# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubModuleClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

#HubManager - wraps IoTHubModuleClient
class HubManager(object):

    def __init__(
            self,
            protocol=IoTHubTransportProvider.MQTT):
        # init Instance Attributes
        self.MESSAGE_DELAY = 0

        # init IoTHubModuleClient
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)

        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)
        self.client.set_module_twin_callback(module_twin_callback, self)

    # send a message to the next stage in the process.
    def send_async(self, outputQueueName, event, send_context):
        self.client.send_event_async(
            outputQueueName, event, send_confirmation_callback, send_context)

    #update modules twin reported properties
    def send_reported_state(self, reported_state, size, user_context):
        self.client.send_reported_state(
            reported_state, size,
            send_reported_state_callback, user_context)

# Callback received when the message that we're sending is processed.
def send_confirmation_callback(message, result, user_context):
    global CONFIRMATION_RECEIVED
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    CONFIRMATION_RECEIVED += 1
    print ( "    Total calls confirmed: %d" % CONFIRMATION_RECEIVED )

# invoked when the module twin's desired properties are updated.
def module_twin_callback(update_state, payload, user_context):
    print ( "\nTwin callback called with:\nupdateStatus = {}\npayload = {}\ncontext = {}".format(update_state, payload, user_context) )
    data = json.loads(payload)
    
    #For the first call (updateStatus = COMPLETE)
    if "desired" in data and "SendDelay" in data["desired"]:
        user_context.MESSAGE_DELAY = data["desired"]["SendDelay"]
    #For subsequent calls (updateStatus = PARTIAL)
    if "SendDelay" in data:
        user_context.MESSAGE_DELAY = data["SendDelay"]
    
    reported_state = "{{ \"SendDelay\":{} }}".format(user_context.MESSAGE_DELAY)
    user_context.send_reported_state(reported_state, len(reported_state), user_context)
    print("Reported: {}".format(reported_state))

# invoked when the module twin's reported properties are processed.
def send_reported_state_callback(status_code, user_context):
    print ( "Confirmation for reported state received with:\nstatus_code = [%d]\ncontext = %s" % (status_code, user_context) )