/*
 Controlling a servo position using a potentiometer (variable resistor)
 by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>

 modified on 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Knob
*/

#include <Servo.h>

Servo myservo;  // create Servo object to control a servo

int potpin = A0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin
int val_180;
int val_1000;
int i;

void setup() {
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the Servo object
}

void loop() {
  /*val = analogRead(potpin);            // reads the value of the potentiometer (value between 0 and 1023)
  val_180 = map(val, 0, 1023, 0, 180);     // scale it for use with the servo (value between 0 and 180)
  val_1000 = map(val, 0, 1023, 1000, 2000);     // scale it for use with the servo (value between 0 and 180)
  //myservo.write(val_180);                  // sets the servo position according to the scaled value
  myservo.writeMicroseconds(val_1000);                  // sets the servo position according to the scaled value
  Serial.println(val_1000);
  delay(15);                           // waits for the servo to get there
*/

  for(i = 0; i <= 400; i++){
    val_180 = map(i, 0, 400, 0, 180);
    val_1000 = map(i, 0, 400, 1000, 2000);
    myservo.writeMicroseconds(val_1000);                  // sets the servo position according to the scaled value
    //myservo.write(val_180);   
    Serial.println(val_1000);
    delay(100);    
  }
  for(i = 400; i >= 0; i--){
    val_180 = map(i, 0, 400, 0, 180);
    val_1000 = map(i, 0, 400, 1000, 2000);
    myservo.writeMicroseconds(val_1000);                  // sets the servo position according to the scaled value
    //myservo.write(val_180);   
    Serial.println(val_1000);
    delay(100);    
  }
}
