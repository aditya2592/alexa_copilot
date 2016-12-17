from FlightGear import FlightGear
import time

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

def main():
    fg = FlightGear('192.168.1.4', 5401)

    # Wait five seconds for simulator to settle down
    while 1:
        if fg['/sim/time/elapsed-sec'] > 5:
            break
        time.sleep(1.0)
        print fg['/sim/time/elapsed-sec']


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
