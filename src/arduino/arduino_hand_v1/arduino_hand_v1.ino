char serialData
int pin=10;

Servo servo1; // Pointing Finger
Servo servo2; // Thumb
Servo servo3; // Index
Servo servo4; // Middle
Servo servo5; // Pinky

void setup() {
  // put your setup code here, to run once:
  servo1.attach(6); // Pointing
  servo2.attach(3); // Thumb
  servo3.attach(9); // Index
  servo4.attach(11); // Middle
  servo5.attach(5); // Pinky
//  pinMode(pin, OUTPUT);
  Serial.begin(9600);
}

void runServos(state) {
  int i;
  int j;
  if (state == "R") {
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
    }} else if (state == "P") {
        for (i=180; i > 0; i--) {
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
    }} else if (state == "S") {
       for (i=180; i < 0; i--){
          servo2.write(i);
          delay(1);
          servo3.write(i);
          delay(1);
          servo5.write(i);
          delay(1);
       }
       for (j=0; j > 180; j++) {
          servo1.write(j);
          delay(1);
          servo4.write(j);
          delay(1);
       }
    }
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    serialData = Serial.read();
    Serial.print(serialData);
    runServos(serialData);
  }
}
