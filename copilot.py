from FlightGear import FlightGear, EngineAction
import time
import json
import paho.mqtt.client as paho
from Payload import Payload


# Engine Startup State
# magnetos =      '3'     (int)
# throttle =      '0.2'   (double)
# mixture =       '1'     (double)
# condition =     '1'     (double)
# propeller-pitch =       '1'     (double)
# faults/
# primer =        '0'     (double)
# primer-lever =  'false' (bool)
# use-primer =    'false' (bool)
# fuel-pump =     'false' (bool)
# fire-switch =   'false' (bool)
# fire-bottle-discharge = 'false' (bool)
# cutoff =        'true'  (bool)
# feed_tank =     '-1'    (int)
# WEP =   'false' (bool)
# cowl-flaps-norm =       '0'     (double)
# propeller-feather =     'false' (bool)
# ignition =      '0'     (int)
# augmentation =  'false' (bool)
# reverser =      'false' (bool)
# water-injection =       'false' (bool)

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def on_publish(client, userdata, mid):
    print("published : "+str(mid) + " " + userdata)
 
def cleanAndExit():
    print "Cleaning..."
    fg.quit()
    client.disconnect()
    print "Bye!"
    sys.exit()

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_message(client, userdata, msg):
    jsonMsg = json.loads(str(msg.payload))
    #print(str(jsonMsg['deviceID']))
    print("Test")
    print("Message Received this Device " + str(msg.payload))
    if msg.topic == "acop/engine" :
        if(jsonMsg['deviceID']==deviceID):
            print("Message Received this Device " + jsonMsg['ctype'] + " " + jsonMsg['cvalue'])
            fg.set_engine_action(jsonMsg['ctype'], jsonMsg['cvalue'])
            fg.engine.execute_action()

deviceID = "DEVICE_1"
appID = "APP_1"
        
client = paho.Client(client_id=deviceID)
client.on_publish = on_publish
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

broker_local = "192.168.1.11"
fg_sim_ip = "127.0.0.1"
broker_net = "broker.mqttdashboard.com"

client.connect(broker_local, 1883)
client.subscribe("acop/engine", qos=0)
packet = Payload(deviceID,appID)
client.loop_start()

fg = FlightGear(fg_sim_ip, 5401)

def main():

    print "Running"
    # Wait five seconds for simulator to settle down
    while 1:
        if fg['/sim/time/elapsed-sec'] > 5:
            break
        time.sleep(1.0)
        print fg['/sim/time/elapsed-sec']

    test_run = 0
    if test_run == 0:
        print "Running"
        while True:
            running = True;
            time.sleep(1)
    else:
        # parking brake on
        fg['/controls/parking-brake'] = 1

        heading = fg['/orientation/heading-deg']

        # Switch to external view for for 'walk around'.
        #fg.view_next()

        #fg['/sim/current-view/goal-heading-offset-deg'] = 180.0
        #fg.wait_for_prop_eq('/sim/current-view/heading-offset-deg', 180.0)

        #fg['/sim/current-view/goal-heading-offset-deg'] = 90.0
        #fg.wait_for_prop_eq('/sim/current-view/heading-offset-deg', 90.0)

        #fg['/sim/current-view/goal-heading-offset-deg'] = 0.0
        #fg.wait_for_prop_eq('/sim/current-view/heading-offset-deg', 0.0)

        #time.sleep(2.0)

        # Switch back to cockpit view
        #fg.view_prev()

        time.sleep(2.0)

        fg['/controls/flaps'] = 0.34
        # Flaps to take off position.34

        #fg.set_bool('/controls/electric/battery-switch', 1)
        #fg.set_bool('/engines/active-engine/auto-start', 1)
        fg['/controls/engines/current-engine/throttle'] = 0
        fg['/controls/engines/current-engine/mixture'] = 0

        fg.set_bool('/controls/switches/starter', 1)
        time.sleep(1.0)

        prime = 1

        if prime == 1:
            fg.set_bool('/controls/engines/engine/use-primer', 0)
            fg['/controls/engines/engine/primer'] = 0
            for engine in range(0, 1) :
                for num in range(0, 5) :    
                    engine_path = '/controls/engines/engine[%d]/primer-lever' % engine
                    fg.set_bool(engine_path,1)
                    fg.set_bool(engine_path,0)

        time.sleep(1.0)

        fg['/controls/engines/current-engine/mixture'] = 1
        fg['/controls/engines/current-engine/throttle'] = 0.2
        #fg.set_bool('/controls/engines/current-engine/starter', 1)
        fg['/controls/switches/magnetos'] = 3
        fg.set_bool('/controls/electric/external-power', 1)
    #fg.set_bool('/controls/switches/starter', 1)

    #fg.quit()
if __name__ == '__main__':
    main()
