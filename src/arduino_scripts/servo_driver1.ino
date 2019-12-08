#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;


void setup() {
  // put your setup code here, to run once:
  servo1.attach(6);
  servo2.attach(3);
  servo3.attach(9);
  servo4.attach(10);
  
}

void runServo(Servo servo1, Servo servo2, Servo servo3, Servo servo4, Servo servo5) {
  int i = 0;
  for (i=0; i<180; i++) {
    servo1.write(i);
    delay(1);
    servo2.write(i);
    delay(1);
    servo3.write(i);
    delay(1);
    servo4.write(i);
    delay(1);
    servo5.write(i);
    delay(1);
  }

  for (i=180; i > 0; i--) {
    servo1.write(i);
    delay(1);
    servo2.write(i);
    delay(1);
    servo3.write(i);
    delay(1);
    servo4.write(i);
    delay(1);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  runServo(servo1, servo2, servo3, servo4, servo5);
}
