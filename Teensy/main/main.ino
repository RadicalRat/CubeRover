//#define DEBUGMODE // comment out for getting rid of LED Status lights

#include <RingBuf.h>
#include <elapsedMillis.h>
#include <SerialTransfer.h>
#include <RoboClaw.h>
#include "ControlPacket.h"
#include <Arduino.h>


// Robot Parameters
float WheelDiam = 15; // diameter of wheels to find cm/s to rpm
float Kp = 11.37910;    // proportional constant for velocity PID
float Ki = 0.345;   // integral constant for velocity PID
float Kd = 0;   // derivative constant for velocity PID
float qpps = 2640; // countable quadrature pulses per second -> found using roboclaw's basicMicro tool

// Serial Transfer declaration
SerialTransfer rx;


// init roboclaw objects to their serial ports for packet communication
RoboClaw ROBOCLAW_1 = RoboClaw(&Serial1, 10000);
RoboClaw ROBOCLAW_2 = RoboClaw(&Serial2, 10000);


void setup() {
  // Init serial ports for PI / computer communication
  Serial.begin(38400); // set to higher baud rate later if needed
  Serial8.begin(38400);
  rx.begin(Serial8);

  // Init serial ports for roboclaws
  ROBOCLAW_1.begin(57600);
  ROBOCLAW_2.begin(57600);

  // turn status LED on
  pinMode(13,OUTPUT);
  #ifdef DEBUGMODE
  pinMode(10,OUTPUT);
  pinMode(9,OUTPUT);
  #endif
  // Init roboclaw PID values
  ROBOCLAW_1.SetM1VelocityPID(0x80, Kp, Ki, Kd, qpps);
  ROBOCLAW_1.SetM2VelocityPID(0x80, Kp, Ki, Kd, qpps);
  ROBOCLAW_2.SetM1VelocityPID(0x80, Kp, Ki, Kd, qpps);
  ROBOCLAW_2.SetM2VelocityPID(0x80, Kp, Ki, Kd, qpps);
  // ROBOCLAW_1.SetM1PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  // ROBOCLAW_1.SetM2PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  // ROBOCLAW_2.SetM1PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  // ROBOCLAW_2.SetM2PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
}


ControlPacket * control = nullptr;
RingBuf<ControlPacket*, 20> packetBuff;

void loop() { // Stuff to loop over

  #ifdef DEBUGMODE // debug mode for checking if packetbuffer has anything
  if (!packetBuff.isEmpty()) {
    digitalWrite(10,HIGH);
  } else {
    digitalWrite(10,LOW);
  }
  #endif

  if (control == nullptr) {   // checks if there is currently a control packet commanding the rover, if yes:
    if (!packetBuff.isEmpty()) {    // checks the packet buffer to see if there is a command in queue, if yes:
      packetBuff.pop(control);    // adds queued command to control pointer
      control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);   // resolves control pointer command
    } else if (rx.available()) {    // if no commands in packetBuffer, check serial port, if yes:
      control = SerialDecode();   // adds serial buffer command to control pointer
      control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);   // resolves control pointer command
      Serial.print("Resolved!");
      digitalWrite(13,HIGH);
    }
  } else {    // if control packet is currently commanding rover:
    #ifdef DEBUGMODE
      digitalWrite(9,HIGH);
    #endif
    if (control->fulfilled(packetBuff)) {   // is the packet done? If yes:
      delete control;   // delete control packet
      control = nullptr;    // set control packet to nullptr
      #ifdef DEBUGMODE
      digitalWrite(9,LOW);
      #endif
    } else {    // if not done:
      if (rx.available()) {   // check serial buffer:
        packetBuff.push(SerialDecode());    // add serial buffer command to packet buffer
      }
    }
  }
}

//   size_t datasize = 2;
//   float data[datasize] = {0};
//   for(size_t i = 0; i < datasize; i++) {
//     data[i] = random(1,50);
//   }

// control = new VelPID(data);
// control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);
// delay(1000);

//   if (rx.available()) { // TODO -> if packet is "done" -- marked by a flag -> delete and move on. if not, decode 1 packet & add to buffer, send 1 telem packet, check for done, wait some seconds
//     control = SerialDecode();
//     control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);
//     delete control;
//     control = nullptr;
//   }
// }




ControlPacket* SerialDecode () {
  Serial.write("Decoding...");
  digitalWrite(13,HIGH);
  //delay(5000);
  uint16_t recievePOS = 0; // stores position of recieving buffer
  char ID; // stores ID of current packet decoder
  ControlPacket * controlTemp = nullptr; // pointer to decoded packet

  recievePOS = rx.rxObj(ID, recievePOS); // store ID char
  Serial.write(ID);
  // decode ID char into specific packet
  if (ID == 'R') { // Raw Data
    size_t datasize = 4; // sets size of data in the packet
    float data[datasize] = {0}; // creates an empty array of datasize
    for(size_t i = 0; i < datasize; i++) { // takes data from serial port and adds it to the packet
      recievePOS = rx.rxObj(data[i], recievePOS);
    }
    controlTemp = new Raw(data); // creates new packet of type Raw

  } else if (ID == 'V') { // Velocity Data
    Serial.write("Here!");
    size_t datasize = 2;
    float tempVal = 0;
    float data[datasize] = {0};
    for(size_t i = 0; i < datasize; i++) {
      recievePOS = rx.rxObj(tempVal, recievePOS);
      Serial.println(tempVal);
      data[i] = tempVal;
    }
    controlTemp = new VelPID(data);
    Serial.write("Vel init");
  } else if (ID == 'D') { // Distance / Position Data
    size_t datasize = 2;
    float data[datasize] = {0};
    for(size_t i = 0; i < datasize; i++) {
      recievePOS = rx.rxObj(data[i], recievePOS);
    }
    controlTemp = new PosPID(data);
    
  } else if (ID == 'S') { // stops the current rover actions and skips to the next one
    if (control != nullptr) {
      control->stop();
      delete control;
      control = nullptr;
    }
  } else if (ID == 'E') { // stops the rover and empties the packet buffer -> ideally for emergency / resetting the rover
    if (control != nullptr) {
      control->stop();
      packetBuff.clear();
      delete control;
      control = nullptr;
    }
  } else if (ID == 'P') { // pauses the rover for data[0] ms. stops all movement / actions and waits
    size_t datasize = 1;
    float data[datasize] = {0};
    for(size_t i = 0; i < datasize; i++) {
      recievePOS = rx.rxObj(data[i], recievePOS);
    }
    if (control != nullptr) {
      control->stop();
      delay(data[0]);
      control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);
    }
  }
  else { // Base case -- currently raw data
    float data[4] = {64,64,64,64};
    controlTemp = new Raw(data);
    Serial.write("Base");
  }

  return controlTemp; // returns pointer to decoded packet

}


