#include <SerialTransfer.h>
#include <RoboClaw.h>
#include "ControlPacket.h"
#include <Arduino.h>

// Robot Parameters
float WheelDiam = 15;
float Kp = 15;
float Ki = 0.675;
float Kd = 0;

// Serial Transfer initialization
SerialTransfer rx;

float qpps = 2640; // countable quadrature pulses per second

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

  pinMode(13,OUTPUT);

  // Init roboclaw PID values
  ROBOCLAW_1.SetM1VelocityPID(0x80, Kp, Ki, Kd, qpps);
  ROBOCLAW_1.SetM2VelocityPID(0x80, Kp, Ki, Kd, qpps);
  ROBOCLAW_2.SetM1VelocityPID(0x80, Kp, Ki, Kd, qpps);
  ROBOCLAW_2.SetM2VelocityPID(0x80, Kp, Ki, Kd, qpps);
  // ROBOCLAW_1.SetM1PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  // ROBOCLAW_1.SetM2PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  // ROBOCLAW_2.SetM1PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  // ROBOCLAW_2.SetM2PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  Serial.print("Waiting");
  digitalWrite(13,HIGH);
}


void loop() {

  if (rx.available()) { // if packet is "done" -- marked by a flag -> delete and move on. if not, decode 1 packet & add to buffer, send 1 telem packet, check for done, wait some seconds
    ControlPacket * control = SerialDecode();
    control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);
    delete control;
    Serial.println("Completed");
  }

  // sets random speeds for motor
  // int data[4] = {64,64,0,0};
  // ControlPacket * test = new Raw(data);
  // test->resolve(&ROBOCLAW_1, &ROBOCLAW_2);
  // delete test;
  // delay(2*1000);


}

ControlPacket* SerialDecode () {
  Serial.println("Decoding!");

  size_t recievePOS = 0; // stores position of recieving buffer
  char ID; // stores ID of current packet decoder
  ControlPacket * control = nullptr; // pointer to decoded packet
  // delay(5*1000);

  recievePOS = rx.rxObj(ID, recievePOS); // store ID char
  
  Serial.println(char(ID));

  // decode ID char into specific packet
  if (ID == 'A') { // Raw Data
    size_t datasize = 4;
    int data[datasize] = {0};
    for(size_t i = 0; i < datasize; i++) {
      recievePOS = rx.rxObj(data[i], recievePOS);
    }
    control = new Raw(data);
  } else if (ID == 'V') {
    Serial.println("Vel PID");
    size_t datasize = 1;
    int data[datasize] = {0};
    for(size_t i = 0; i < datasize; i++) {
      recievePOS = rx.rxObj(data[i], recievePOS);
    }
    control = new VelPID(data);
  } else if (ID == 'D') {
    size_t datasize = 2;
    int data[datasize] = {0};
    for(size_t i = 0; i < datasize; i++) {
      recievePOS = rx.rxObj(data[i], recievePOS);
    }
    control = new PosPID(data);
  } else { // Base case -- currently raw data
    int data[4] = {32,32,0,0};
    control = new Raw(data);
  }

  return control; // returns pointer to decoded packet

}


