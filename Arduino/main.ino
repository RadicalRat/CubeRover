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

float qpps = 2640; // countable quadrature pulses per second -> found using roboclaw's basicMicro tool

// init roboclaw objects to their serial ports for packet communication
RoboClaw ROBOCLAW_1 = RoboClaw(&Serial1, 10000);
RoboClaw ROBOCLAW_2 = RoboClaw(&Serial2, 10000);


void setup() {
  // Init serial ports for PI / computer communication
  Serial.begin(38400); // set to higher baud rate later if needed
  rx.begin(Serial);
  Serial.print("Serial Init");

  // Init serial ports for roboclaws
  ROBOCLAW_1.begin(38400);
  ROBOCLAW_2.begin(38400);

  // turn status LED on
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

  if (rx.available()) { // TODO -> if packet is "done" -- marked by a flag -> delete and move on. if not, decode 1 packet & add to buffer, send 1 telem packet, check for done, wait some seconds
    ControlPacket * control = SerialDecode();
    control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);
    delete control;
    Serial.println("Completed");
  }
}

ControlPacket* SerialDecode () {
  delay(2*1000); // timing delay for my sake
  Serial.println("Decoding!");

  size_t recievePOS = 0; // stores position of recieving buffer
  char ID; // stores ID of current packet decoder
  ControlPacket * control = nullptr; // pointer to decoded packet

  recievePOS = rx.rxObj(ID, recievePOS); // store ID char
  

  // decode ID char into specific packet

  if (ID == 'R') { // Raw Data
    Serial.println("R");
    size_t datasize = 4; // sets size of data in the packet
    float data[datasize] = {0}; // creates an empty array of datasize
    for(size_t i = 0; i < datasize; i++) { // takes data from serial port and adds it to the packet
      recievePOS = rx.rxObj(data[i], recievePOS);
      Serial.println(data[i]);
    }
    Serial.println("Error");
    control = new Raw(data); // creates new packet of type Raw
  } else if (ID == 'V') { // Velocity Data
    Serial.println("Vel PID");
    size_t datasize = 1;
    float data[datasize] = {0};
    for(size_t i = 0; i < datasize; i++) {
      recievePOS = rx.rxObj(data[i], recievePOS);
      Serial.println(data[i]);
    }
    Serial.println("Error");
    control = new VelPID(data);
  } else if (ID == 'D') { // Distance / Position Data
    Serial.println("D");
    size_t datasize = 2;
    float data[datasize] = {0};
    for(size_t i = 0; i < datasize; i++) {
      recievePOS = rx.rxObj(data[i], recievePOS);
      Serial.println(data[i]);
    }
    Serial.println("Error");
    control = new PosPID(data);
  } else { // Base case -- currently raw data
    float data[4] = {32,32,0,0};
    control = new Raw(data);
  }

  return control; // returns pointer to decoded packet

}


