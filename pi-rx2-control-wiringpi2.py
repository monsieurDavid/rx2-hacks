#!/usr/bin/python

'''
    Realtek RX2 (RX2B) Control via Raspberry Pi
 
    Written by David Bernier, Aug. 26, 2013
    https://github.com/monsieurDavid/
    GPL v3 License
    
    This is a hack to send two different pulse trains to a RX2-driven
    RC toy car by a Raspberry Pi.
    
    Non-PWM code based upon:
    http://forum.arduino.cc/index.php?topic=171238.msg1274631#msg1274631
    
    Fixed durations as per RX2B datasheet see http://www.datasheetdir.com/RX-2B+download
    
    Requires: wiringpi2 (https://github.com/Gadgetoid/WiringPi2-Python)
    
    @todo:
    - Figure out a way to 'hold' the left/right directions after they are set.
    - Reduce timing gap between loops
    
'''

import wiringpi2


#using GPIO scheme
wiringpi2.wiringPiSetupGpio()

#pins assignment
    #output
ANTENNA     =  7 # wiringpi  7 "CE1"
STATUS_LED  =  8 #          10 "CE0" 

    #input
LEFT_BTN    = 11 #          14 "SCLK"
BWD_BTN     =  9 #          13 "MISO"
FWD_BTN     = 10 #          12 "MOSI"
RIGHT_BTN   = 22 #           3
OFF_BTN     = 17 #           0

wiringpi2.pinMode(ANTENNA, wiringpi2.GPIO.OUTPUT) 
wiringpi2.pinMode(STATUS_LED, wiringpi2.GPIO.OUTPUT) 
wiringpi2.pinMode(LEFT_BTN, wiringpi2.GPIO.INPUT) 
wiringpi2.pinMode(BWD_BTN, wiringpi2.GPIO.INPUT) 
wiringpi2.pinMode(FWD_BTN, wiringpi2.GPIO.INPUT) 
wiringpi2.pinMode(RIGHT_BTN, wiringpi2.GPIO.INPUT) 
wiringpi2.pinMode(OFF_BTN, wiringpi2.GPIO.INPUT) 

ENDCODE        =  4
FORWARD        = 10
FORWARD_TURBO  = 16
TURBO          = 22
FORWARD_LEFT   = 28
FORWARD_RIGHT  = 34
BACKWARD       = 40
BACKWARD_RIGHT = 46
BACKWARD_LEFT  = 52
LEFT           = 58
RIGHT          = 64

debug = False # Warning: printing on the screen slows things down too much for the  pulse train to work correctly

def run():
    mode = ENDCODE
    triggerOn = False
    
    while (True):
        if (debug == True):
            print str(wiringpi2.digitalRead(OFF_BTN)) + " " + str(wiringpi2.digitalRead(FWD_BTN)) + str(wiringpi2.digitalRead(LEFT_BTN)) + str(wiringpi2.digitalRead(RIGHT_BTN)) + str(wiringpi2.digitalRead(BWD_BTN))
        
        if (wiringpi2.digitalRead(OFF_BTN) == wiringpi2.GPIO.HIGH):
            trigger(ENDCODE)
            triggerOn = False
        elif (wiringpi2.digitalRead(FWD_BTN) == wiringpi2.GPIO.HIGH):
            triggerOn = True
            if (wiringpi2.digitalRead(LEFT_BTN) == wiringpi2.GPIO.HIGH and wiringpi2.digitalRead(RIGHT_BTN) == wiringpi2.GPIO.LOW):
                mode = FORWARD_LEFT
            elif (wiringpi2.digitalRead(LEFT_BTN) == wiringpi2.GPIO.LOW and wiringpi2.digitalRead(RIGHT_BTN) == wiringpi2.GPIO.HIGH):
                mode = FORWARD_RIGHT
            else:
                mode = FORWARD
        elif (wiringpi2.digitalRead(BWD_BTN) == wiringpi2.GPIO.HIGH):
            triggerOn = True
            if (wiringpi2.digitalRead(LEFT_BTN) == wiringpi2.GPIO.HIGH and wiringpi2.digitalRead(RIGHT_BTN) == wiringpi2.GPIO.LOW):
                mode = BACKWARD_LEFT
            elif (wiringpi2.digitalRead(LEFT_BTN) == wiringpi2.GPIO.LOW and wiringpi2.digitalRead(RIGHT_BTN) == wiringpi2.GPIO.HIGH):
                mode = BACKWARD_RIGHT
            else:
                mode = BACKWARD
        elif (wiringpi2.digitalRead(LEFT_BTN) == wiringpi2.GPIO.HIGH and wiringpi2.digitalRead(RIGHT_BTN) == wiringpi2.GPIO.LOW):
                triggerOn = True
                mode = LEFT
        elif (wiringpi2.digitalRead(LEFT_BTN) == wiringpi2.GPIO.LOW and wiringpi2.digitalRead(RIGHT_BTN) == wiringpi2.GPIO.HIGH):
                triggerOn = True
                mode = RIGHT
        
        if (debug == True):
            print "trigger: " + str(triggerOn) + "; mode: " + str(mode)  

        if (triggerOn == True):
            trigger(mode)


def trigger(mode):
    w1 = w2 =  0
    while (w2 < 4):
        msec = wiringpi2.micros()
        while (wiringpi2.micros() - msec < 1500):
            wiringpi2.digitalWrite(ANTENNA, wiringpi2.GPIO.HIGH)
            wiringpi2.digitalWrite(STATUS_LED, wiringpi2.GPIO.HIGH)
        while (wiringpi2.micros() - msec < 2000):
            wiringpi2.digitalWrite(ANTENNA, wiringpi2.GPIO.LOW)
            wiringpi2.digitalWrite(STATUS_LED, wiringpi2.GPIO.LOW)
        w2 += 1
    while (w1 < mode):
        msec = wiringpi2.micros()
        while (wiringpi2.micros() - msec < 500):
            wiringpi2.digitalWrite(ANTENNA, wiringpi2.GPIO.HIGH)
            wiringpi2.digitalWrite(STATUS_LED, wiringpi2.GPIO.HIGH)
        while (wiringpi2.micros() - msec < 1000):
            wiringpi2.digitalWrite(ANTENNA, wiringpi2.GPIO.LOW)
            wiringpi2.digitalWrite(STATUS_LED, wiringpi2.GPIO.LOW)
        w1 += 1


try:
    run()
except (KeyboardInterrupt, SystemExit):
        trigger(ENDCODE)
        wiringpi2.digitalWrite(ANTENNA, wiringpi2.GPIO.LOW)
        wiringpi2.digitalWrite(STATUS_LED, wiringpi2.GPIO.LOW)
        print ""
        print "exit"
