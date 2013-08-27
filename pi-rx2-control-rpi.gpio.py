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
    
    Requires: RPi.GPIO 5.3a
    
    @todo:
    - Figure out a way to 'hold' the left/right directions after they are set.
    - Reduce timing gap between loops
    
'''

import RPi.GPIO as GPIO
import time


#using GPIO scheme
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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

GPIO.setup(ANTENNA, GPIO.OUT)
GPIO.setup(STATUS_LED, GPIO.OUT) 
GPIO.setup(LEFT_BTN, GPIO.IN) 
GPIO.setup(BWD_BTN, GPIO.IN)  
GPIO.setup(FWD_BTN, GPIO.IN) 
GPIO.setup(RIGHT_BTN, GPIO.IN) 
GPIO.setup(OFF_BTN, GPIO.IN) 

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
            print str(GPIO.input(OFF_BTN)) + " " + str(GPIO.input(FWD_BTN)) + str(GPIO.input(LEFT_BTN)) + str(GPIO.input(RIGHT_BTN)) + str(GPIO.input(BWD_BTN))
        
        if (GPIO.input(OFF_BTN) == GPIO.HIGH):
            trigger(ENDCODE)
            triggerOn = False
        elif (GPIO.input(FWD_BTN) == GPIO.HIGH):
            triggerOn = True
            if (GPIO.input(LEFT_BTN) == GPIO.HIGH and GPIO.input(RIGHT_BTN) == GPIO.LOW):
                mode = FORWARD_LEFT
            elif (GPIO.input(LEFT_BTN) == GPIO.LOW and GPIO.input(RIGHT_BTN) == GPIO.HIGH):
                mode = FORWARD_RIGHT
            else:
                mode = FORWARD
        elif (GPIO.input(BWD_BTN) == GPIO.HIGH):
            triggerOn = True
            if (GPIO.input(LEFT_BTN) == GPIO.HIGH and GPIO.input(RIGHT_BTN) == GPIO.LOW):
                mode = BACKWARD_LEFT
            elif (GPIO.input(LEFT_BTN) == GPIO.LOW and GPIO.input(RIGHT_BTN) == GPIO.HIGH):
                mode = BACKWARD_RIGHT
            else:
                mode = BACKWARD
        elif (GPIO.input(LEFT_BTN) == GPIO.HIGH and GPIO.input(RIGHT_BTN) == GPIO.LOW):
                triggerOn = True
                mode = LEFT
        elif (GPIO.input(LEFT_BTN) == GPIO.LOW and GPIO.input(RIGHT_BTN) == GPIO.HIGH):
                triggerOn = True
                mode = RIGHT
        
        if (debug == True):
            print "trigger: " + str(triggerOn) + "; mode: " + str(mode)  

        if (triggerOn == True):
            trigger(mode)


def trigger(mode):
    w1 = w2 =  0
    while (w2 < 4):
        msec = time.time()
        while (time.time() - msec < 0.001500):
            GPIO.output(ANTENNA, GPIO.HIGH)
            GPIO.output(STATUS_LED, GPIO.HIGH)
        while (time.time() - msec < 0.002000):
            GPIO.output(ANTENNA, GPIO.LOW)
            GPIO.output(STATUS_LED, GPIO.LOW)
        w2 += 1
    while (w1 < mode):
        msec = time.time()
        while (time.time() - msec < 0.000500):
            GPIO.output(ANTENNA, GPIO.HIGH)
            GPIO.output(STATUS_LED, GPIO.HIGH)
        while (time.time() - msec < 0.001000):
            GPIO.output(ANTENNA, GPIO.LOW)
            GPIO.output(STATUS_LED, GPIO.LOW)
        w1 += 1


try:
    run()
except (KeyboardInterrupt, SystemExit):
        trigger(ENDCODE)
        GPIO.output(ANTENNA, GPIO.LOW)
        GPIO.output(STATUS_LED, GPIO.LOW)
        GPIO.cleanup()
        print ""
        print "exit"
 
