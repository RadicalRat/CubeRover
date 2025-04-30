#include <RingBuf.h>
#include <elapsedMillis.h>
#include <SerialTransfer.h>
#include <RoboClaw.h>
#include "ControlPacket.h"
#include <Arduino.h>
#include <EEPROM.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>



// Robot Parameters
// float Kp = 11.37910;    // proportional constant for velocity PID
// float Ki = 0.345;   // integral constant for velocity PID
// float Kd = 0;   // derivative constant for velocity PID
float qpps = 3000; // countable quadrature pulses per second -> found using roboclaw's basicMicro tool
float acceleration = 0;
float deacceleration = 0;

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);


// Serial Transfer declaration
SerialTransfer rx;


// init roboclaw objects to their serial ports for packet communication
RoboClaw ROBOCLAW_1 = RoboClaw(&Serial1, 10000);
RoboClaw ROBOCLAW_2 = RoboClaw(&Serial3, 10000);


void setup(void) {
  // Init serial ports for PI / computer communication
  Serial.begin(38400); // Built-in USB port for Teensy
  Serial8.begin(38400); // GPIO pins for Raspberry Pi
  rx.begin(Serial);

  // Init serial ports for roboclaws
  ROBOCLAW_1.begin(38400);
  ROBOCLAW_2.begin(38400);

  // turn status LED on
  pinMode(13,OUTPUT);
  digitalWrite(13,HIGH);
  
  // Init roboclaw values from memory
  MemSetup(ROBOCLAW_1, ROBOCLAW_2);

  delay(100);

  if (!bno.begin())
  {
    for(int i = 0; i < 20; i++) {
      if (!bno.begin()) {
        Serial.print("No BNO055 detected");
        digitalWrite(13,!digitalRead(13));
        delay(500);
      }
    }
  }
  //bno.setExtCrystalUse(true);
  delay(5000);
}


ControlPacket * control = nullptr; // control pointer variable to keep track of what command is being done
RingBuf<ControlPacket*, 20> packetBuff; // packet buffer to keep commands if one is currently being resolved

void loop() { // Stuff to loop over
  if (control == nullptr) {   // checks if there is currently a control packet commanding the rover, if yes:
    if (!packetBuff.isEmpty()) {    // checks the packet buffer to see if there is a command in queue, if yes:
      packetBuff.pop(control);    // adds queued command to control pointer
      control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);   // resolves control pointer command
    } else if (rx.available()) {    // if no commands in packetBuffer, check serial port, if yes:
      control = SerialDecode();   // adds serial buffer command to control pointer
      if (control != nullptr) {
        control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);   // resolves control pointer command
      }
    }
  } 
  if (control != nullptr) { // if control packet is currently commanding rover:
    if (control->fulfilled(packetBuff)) {   // is the packet done? If yes:
      delete control;   // delete control packet
      control = nullptr;    // set control packet to nullptr
    } else {    // if not done:
      if (rx.available()) {   // check serial buffer:
        packetBuff.push(SerialDecode());    // add serial buffer command to packet buffer
      }
    }
  }
  delay(50);

  // int motor1_count = ROBOCLAW_1.ReadEncM1(0x80);
  // Serial.print(motor1_count);
  // delay(500);
  // if (!bno.begin()) {
  //   // Serial.print("IMU Broke");
  //   // delay(1000);
  // }
}


ControlPacket* SerialDecode () {
  //delay(5000);
  uint16_t recievePOS = 0; // stores position of iterator in recieving buffer
  char ID; // stores ID of current packet decoder
  ControlPacket * controlTemp = nullptr; // temp pointer to decoded packet
  recievePOS = rx.rxObj(ID, recievePOS); // store ID char
  Serial.print(ID);
  if (ID == 'V') { // Velocity control
    float * dataPTR = RetrieveSerial<float>(3, recievePOS);
    controlTemp = new VelPID(dataPTR, acceleration, deacceleration); // creates new packet of type Velocity
  } else if (ID == 'P') { // Distance / Position control
    Serial.write("Distance!");
    controlTemp = new PosPID(RetrieveSerial<float>(2,recievePOS), acceleration, deacceleration);
  } else if (ID == 'T') {
    Serial.write("Turning!");
    controlTemp = new AngPID(RetrieveSerial<float>(3,recievePOS), bno, acceleration, deacceleration);
  } else if (ID == 'S') { // stops the current rover actions and skips to the next one
    if (control != nullptr) {
      control->stop();
      delete control;
      controlTemp = nullptr;
    }
  } else if (ID == 'E') { // stops the rover and empties the packet buffer -> ideally for emergency / resetting the rover
    if (control != nullptr) {
      Serial.println("STOP");
      control->stop();
      packetBuff.clear();
      delete control;
      controlTemp = nullptr;
    }
  } else if (ID == 'C') { // write to EEPROM memory
    float * dataPTR = RetrieveSerial<float>(2,recievePOS);
    MemWrite(static_cast<float>(dataPTR[0]), dataPTR[1]);
    MemSetup(ROBOCLAW_1, ROBOCLAW_2);
  } else { // Base case
    controlTemp = nullptr;
  }
  return controlTemp; // returns pointer to decoded packet

}

// fetch stored configuration parameters and assign to required locations
void MemSetup(RoboClaw & RC1, RoboClaw & RC2) {
  float fsettings[10] = {0}; // stores float settings in an array. [vP,vI,vD,pP,pI,pD,pMI,Deadzone, Acceleration, Deacceleration]
  for (size_t i = 0; i < 10*4; i = i + 4) {
    EEPROM.get((i), fsettings[i/4]);
    Serial.println(fsettings[i/4]);
  }
  RC1.SetM1VelocityPID(0x80, fsettings[0], fsettings[1], fsettings[2], qpps); // change the velocity settings
  RC1.SetM2VelocityPID(0x80, fsettings[0], fsettings[1], fsettings[2], qpps);
  RC2.SetM1VelocityPID(0x80, fsettings[0], fsettings[1], fsettings[2], qpps);
  RC2.SetM1VelocityPID(0x80, fsettings[0], fsettings[1], fsettings[2], qpps);
  RC1.SetM1PositionPID(0x80, fsettings[3], fsettings[4], fsettings[5], static_cast<int>(fsettings[6]), fsettings[7], -10000, 10000); // change the position settings
  RC1.SetM2PositionPID(0x80, fsettings[3], fsettings[4], fsettings[5], static_cast<int>(fsettings[6]), fsettings[7], -10000, 10000);
  RC2.SetM1PositionPID(0x80, fsettings[3], fsettings[4], fsettings[5], static_cast<int>(fsettings[6]), fsettings[7], -10000, 10000);
  RC2.SetM2PositionPID(0x80, fsettings[3], fsettings[4], fsettings[5], static_cast<int>(fsettings[6]), fsettings[7], -10000, 10000);
  acceleration = fsettings[8];    // set acceleration variable
  deacceleration = fsettings[9];    // set deacceleration variable
}

void MemWrite(int adr, float val) {
  EEPROM.put(adr, val);
  Serial.println(adr);
  Serial.println(val);
}


template<class T>
T * RetrieveSerial(size_t len, uint16_t & recievePOS) {
  size_t datasize = len; // sets size of data in the packet
  T * data = new T[datasize]; // creates an empty array of datasize
  for(size_t i = 0; i < datasize; i++) { // takes data from serial port and adds it to the packet
    recievePOS = rx.rxObj(data[i], recievePOS);
    Serial.println(data[i]);
  }
  return data;
}


