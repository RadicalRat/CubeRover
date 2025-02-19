#include <SerialTransfer.h>
#include <RoboClaw.h>
#include "ControlPacket.h"
#include <Arduino.h>

// Robot Parameters
int QuadCT = 4800;
float WheelDiam = 15;
float Kp = 0;
float Ki = 0;
float Kd = 0;

// Serial Transfer initialization
SerialTransfer rx;



float qpps = 400; // countable quadrature pulses per second

// init roboclaw objects
RoboClaw ROBOCLAW_1 = RoboClaw(&Serial1, 10000);
RoboClaw ROBOCLAW_2 = RoboClaw(&Serial2, 10000);



void setup() {
  // Init serial ports for PI / computer communication
  Serial.begin(38400);
  rx.begin(Serial);
  Serial.print("Serial Init");

  // Init serial ports for roboclaws
  ROBOCLAW_1.begin(38400);
  ROBOCLAW_2.begin(38400);

  // Init roboclaw PID values
  ROBOCLAW_1.SetM1VelocityPID(0x80, Kp, Ki, Kd, qpps);
  ROBOCLAW_1.SetM2VelocityPID(0x80, Kp, Ki, Kd, qpps);
  ROBOCLAW_2.SetM1VelocityPID(0x80, Kp, Ki, Kd, qpps);
  ROBOCLAW_2.SetM2VelocityPID(0x80, Kp, Ki, Kd, qpps);
  Serial.print("Waiting");
  delay(10*1000);
}

void loop() {

  if (rx.available()) {
    Serial.print("Open!");
    ControlPacket * control;
    control = recdecode();
    control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);
    delay(2*1000);
  }


  // int data[4] = {64,64,0,0};
  // ControlPacket * test = new Raw(data);
  // test->resolve(&ROBOCLAW_1, &ROBOCLAW_2);
  // delete test;
  // delay(2*1000);


}

ControlPacket* recdecode () {
  Serial.print("Decoding!");
  size_t recievePOS = 0;
  char ID;
  ControlPacket * control = nullptr;

  recievePOS = rx.rxObj(ID, recievePOS);

  switch (ID) {
    case 'A':
      int * data = new int[4];
      recievePOS = rx.rxObj(data, recievePOS);
      control = new Raw(data);
      break;
  }
  return control;

}


