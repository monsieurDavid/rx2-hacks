/*
    Realtek RX2 (RX2B) Control via Arduino
 
    Written by David Bernier, Aug. 26, 2013
    https://github.com/monsieurDavid/
    GPL v3 License
    
    This is a hack to send two different pulse trains to a RX2-driven
    RC toy car by an Arduino.
    
    Non-PWM code based upon:
    http://forum.arduino.cc/index.php?topic=171238.msg1274631#msg1274631
    
    Pins:
      Pin 9 or 10 to toy's antenna
      Pin 10 or 9 to LED
      Arduino's GND to toy's GND
      
      Buttons: Pins 3, 4, 5, 6, 7

*/


//Fixed durations as per RX2B datasheet see http://www.datasheetdir.com/RX-2B+download

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
#define ANTENNA     9
#define STATUS_LED 10

//input pins
#define LEFT_BTN  3
#define BWD_BTN   4
#define FWD_BTN   5
#define RIGHT_BTN 6
#define OFF_BTN   7

boolean debug = false; //true;
String debugCache = "";


int mode;
boolean started = false;
boolean trigger_on = false;

//interrupt
unsigned long currentMicros  = 0;

void setup() {

  if (debug) {
    Serial.begin(9600);
  }
  
  pinMode(ANTENNA, OUTPUT);
  pinMode(STATUS_LED, OUTPUT);
    
  pinMode(OFF_BTN, INPUT);
  pinMode(FWD_BTN, INPUT);
  pinMode(LEFT_BTN, INPUT);
  pinMode(RIGHT_BTN, INPUT);
  pinMode(BWD_BTN, INPUT);
}


void loop() {
  //mode = FORWARD;
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
    trigger(ENDCODE);
    trigger_on = false;
  } else if (digitalRead(FWD_BTN) == HIGH) { //FORWARD
    trigger_on = true;
    if (digitalRead(LEFT_BTN) == HIGH && digitalRead(RIGHT_BTN) == LOW) {
      mode = FORWARD_LEFT;      
    } else if (digitalRead(LEFT_BTN) == LOW && digitalRead(RIGHT_BTN) == HIGH) {
      mode = FORWARD_RIGHT;
    } else {
      mode = FORWARD;
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
  
  //start code sequence
  for (int w2 = 0; w2 < 4; w2++) {
    currentMicros = micros();
    while (micros() - currentMicros < 1500) {
      digitalWrite(ANTENNA, HIGH);
      digitalWrite(STATUS_LED, HIGH);
    }
    while (micros() - currentMicros < 2000) {
      digitalWrite(ANTENNA, LOW);
      digitalWrite(STATUS_LED, LOW);
    }
  }
  
  //function code sequence
  for (int w1 = 0; w1 < mode; w1++) {
    currentMicros = micros();
    while (micros() - currentMicros < 500) {
      digitalWrite(ANTENNA, HIGH);
      digitalWrite(STATUS_LED, HIGH);
    }
    while (micros() - currentMicros < 1000) {
      digitalWrite(ANTENNA, LOW);
      digitalWrite(STATUS_LED, LOW);
    }
  }

}
