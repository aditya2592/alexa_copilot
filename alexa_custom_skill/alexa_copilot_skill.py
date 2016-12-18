import logging
import json
import paho.mqtt.client as paho
import sys
import os, sys, inspect
sys.path.append( os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/../modules/" )
from Payload import Payload

from flask import Flask
from flask_ask import Ask, request, session, question, statement

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def on_publish(client, userdata, mid):
    print("published : "+str(mid) + " " + str(userdata))
 
def cleanAndExit():
    print "Cleaning..."
    client.disconnect()
    print "Bye!"
    sys.exit()

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_message(client, userdata, msg):
    jsonMsg = json.loads(str(msg.payload))
  

deviceID = "DEVICE_1"
appID = "APP_1"      
client = paho.Client(client_id=appID)
client.on_publish = on_publish
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

broker_local = "192.168.1.11"
broker_net = "broker.mqttdashboard.com"

client.connect(broker_local, 1883)
client.subscribe("acop/status", qos=0)
packet = Payload(deviceID,appID)


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Hi, I am your Copilot. You can talk to me through Alexa'
    return question(speech_text).reprompt(speech_text).simple_card('CopilotResponse', speech_text)


@ask.intent('EngineIntent',
    mapping={'throttle': 'THROTTLE', 'mixture': 'MIXTURE', 'prime' : 'PRIME'})
def change_engine_params(throttle, mixture, prime):
	if throttle is not None:
		packet.setType("throttle", throttle)
		speech_text = 'setting throttle to %s percent' % throttle
	elif mixture is not None:
		packet.setType("mixture", mixture)
		speech_text = 'setting mixture level to %s percent' % mixture
	elif prime is not None:
		packet.setType("prime", prime)
		speech_text = 'priming engine %s times' % prime
	else :
		speech_text = "sorry I dont understand this instruction"

	client.publish("acop/engine", json.dumps(packet.__dict__), qos=0)
	client.loop()
	return statement(speech_text).simple_card('CopilotResponse', speech_text)

@ask.intent('AutoStartIntent')
def autostart():
	packet.setType("autostart", "true")
	speech_text = 'starting engines captain'
	client.publish("acop/engine", json.dumps(packet.__dict__), qos=0)
	return statement(speech_text).simple_card('CopilotResponse', speech_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'trust me captain, we will not crash'
    return question(speech_text).reprompt(speech_text).simple_card('CopilotResponse', speech_text)


@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)