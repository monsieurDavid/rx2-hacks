/*
    RX2B PWM Control via via Arduino
 
    Written by David Bernier
    https://github.com/monsieurDavid/
    GPL v3 License
     
    PWM variable frequency code from:
    http://www.oxgadgets.com/2011/04/creating-variable-frequency-pwm-output.html

    What follows is a hack to send two different pulse trains to a RX2B-driven
    RC toy car. 
    
    This has been tested an Arduino UNO r3
    Demo: 
 
    Firmware variables:
      OCR1A: PWM Pin 9
      OCR1B: PWM Pin 10
      IRC1: the frequency handling register for Timer1

    Pins:
      Pin 9 or 10 to toy's antenna
      Pin 10 or 9 to LED
      Arduino's GND to toy's GND
      
      Buttons: Pins 3, 4, 5, 6, 7

*/

//values for ICR1
#define W1_FREQ 1000
#define W2_FREQ 2000

//duties
#define W1_DUTY 50
#define W2_DUTY 75

//Fixed durations as per RX2B datasheet see http://www.datasheetdir.com/RX-2B+download
//W2
#define START_CODE      8

//W1
#define ENDCODE         4
#define FORWARD        10
#define FORWARD_TURBO  16
#define TURBO          22
#define FORWARD_LEFT   28
#define FORWARD_RIGHT  34
#define BACKWARD       40
#define BACKWARD_RIGHT 46
#define BACKWARD_LEFT  52
#define LEFT           58
#define RIGHT          64

//output pins
#define ANTENNA     9  //to car antenna a.k.a. OCR1A
#define STATUS_LED 10  //LED, a.k.a. OCR1B

//input pins
#define LEFT_BTN  3
#define BWD_BTN   4
#define FWD_BTN   5
#define RIGHT_BTN 6
#define OFF_BTN   7

boolean debug = true;
String debugCache = "";


int mode;
boolean started = false;
boolean trigger_on = false;

//interrupt
unsigned long currentMillis  = 0;
unsigned long previousMillis = 0;



void setup() {

  if (debug) {
    Serial.begin(9600);
  }
  
  pinMode(ANTENNA, OUTPUT);
  pinMode(STATUS_LED, OUTPUT);
  
  //some deep value coding as per Arduino Cookbook
  TCCR1A = _BV(COM1A1) | _BV(COM1B1);
  TCCR1B = _BV(WGM13) | _BV(CS11);
  
  pinMode(OFF_BTN, INPUT);
  pinMode(FWD_BTN, INPUT);
  pinMode(LEFT_BTN, INPUT);
  pinMode(RIGHT_BTN, INPUT);
  pinMode(BWD_BTN, INPUT);
}


void loop() {
  //mode = TURBO;
  //trigger(mode);

  if (debug) {
    debugCache = (String) digitalRead(OFF_BTN)
                  + " "
                  + digitalRead(FWD_BTN) 
                  + digitalRead(LEFT_BTN) 
                  + digitalRead(RIGHT_BTN) 
                  + digitalRead(BWD_BTN);
  }

  if (digitalRead(OFF_BTN) == HIGH) { //TURN OFF
    trigger_on = false;    
  } else if (digitalRead(FWD_BTN) == HIGH) { //FORWARD
    trigger_on = true;
    if (digitalRead(LEFT_BTN) == HIGH && digitalRead(RIGHT_BTN) == LOW) {
      mode = FORWARD_LEFT;      
    } else if (digitalRead(LEFT_BTN) == LOW && digitalRead(RIGHT_BTN) == HIGH) {
      mode = FORWARD_RIGHT;
    } else {
      mode = TURBO;
    }
  } else if (digitalRead(BWD_BTN) == HIGH) { //BACKWARD
    trigger_on = true;
    if (digitalRead(LEFT_BTN) == HIGH && digitalRead(RIGHT_BTN) == LOW) {
      mode = BACKWARD_LEFT;
    } else if (digitalRead(LEFT_BTN) == LOW && digitalRead(RIGHT_BTN) == HIGH) {
      mode = BACKWARD_RIGHT;
    } else {
      mode = BACKWARD;
    }
  //DIRECTION ONLY -- no throttle
  } else if (digitalRead(LEFT_BTN) == HIGH && digitalRead(RIGHT_BTN) == LOW) {
      trigger_on = true;
      mode = LEFT;
  } else if (digitalRead(LEFT_BTN) == LOW && digitalRead(RIGHT_BTN) == HIGH) {
      trigger_on = true;
      mode = RIGHT;
  } 
  
  if (debug){
    debugCache = (String) trigger_on + " " + debugCache + " " + mode;
    Serial.println(debugCache);
  }
   
  //Send the command, if any, to the toy
  if (trigger_on == true) {
    trigger(mode);
  } 

}


void trigger(int mode) {

  currentMillis = millis();
  
  if (!started) {
    started = !started; //toggle
    
    //start sequence
    ICR1 = W2_FREQ;
    OCR1B = OCR1A = W2_DUTY * ICR1 / 100;
        while (millis() - currentMillis < START_CODE) {  
      ; //empty statement
    }
  } else {
    started = !started; //toggle again
    
    //function word sequence
    ICR1 = W1_FREQ;
    OCR1B = OCR1A = W1_DUTY * ICR1 / 100;
        while (millis() - currentMillis < mode) {
      ; //empty statement
    }
  }
}
