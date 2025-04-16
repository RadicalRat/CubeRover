//#define DEBUGMODE // comment out for getting rid of LED Status lights

#include <RingBuf.h>
#include <elapsedMillis.h>
#include <SerialTransfer.h>
#include <RoboClaw.h>
#include "ControlPacket.h"
#include <Arduino.h>
#include <EEPROM.h>
#include <Adafruit_BNO055.h>
#include <Adafruit_Sensor.h>


// Robot Parameters
float WheelDiam = 15; // diameter of wheels to find cm/s to rpm
float Kp = 11.37910;    // proportional constant for velocity PID
float Ki = 0.345;   // integral constant for velocity PID
float Kd = 0;   // derivative constant for velocity PID
float qpps = 2640; // countable quadrature pulses per second -> found using roboclaw's basicMicro tool
int acceleration = 0;
int deacceleration = 0;

Adafruit_BNO055 IMU = Adafruit_BNO055(55, 0x28);


// Serial Transfer declaration
SerialTransfer rx;


// init roboclaw objects to their serial ports for packet communication
RoboClaw ROBOCLAW_1 = RoboClaw(&Serial1, 10000);
RoboClaw ROBOCLAW_2 = RoboClaw(&Serial2, 10000);


void setup() {
  // Init serial ports for PI / computer communication
  Serial.begin(38400); // set to higher baud rate later if needed
  Serial8.begin(38400);
  rx.begin(Serial);

  // Init serial ports for roboclaws
  ROBOCLAW_1.begin(38400);
  ROBOCLAW_2.begin(38400);
  // turn status LED on
  pinMode(13,OUTPUT);
  #ifdef DEBUGMODE
  pinMode(10,OUTPUT);
  pinMode(9,OUTPUT);
  #endif
  // Init roboclaw PID values
  MemSetup(ROBOCLAW_1, ROBOCLAW_2);
  digitalWrite(13,HIGH);
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
      control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);   // resolves control pointer command
      //digitalWrite(13,HIGH);
    }
  } else {    // if control packet is currently commanding rover:
    if (control->fulfilled(packetBuff)) {   // is the packet done? If yes:
      delete control;   // delete control packet
      control = nullptr;    // set control packet to nullptr
    } else {    // if not done:
      if (rx.available()) {   // check serial buffer:
        packetBuff.push(SerialDecode());    // add serial buffer command to packet buffer
      }
    }
  }
}


//   if (rx.available()) { // TODO -> if packet is "done" -- marked by a flag -> delete and move on. if not, decode 1 packet & add to buffer, send 1 telem packet, check for done, wait some seconds
//     control = SerialDecode();
//     control->resolve(&ROBOCLAW_1, &ROBOCLAW_2);
//     delete control;
//     control = nullptr;
//   }
// }


long int counter = 0;

ControlPacket* SerialDecode () {
  //delay(5000);
  uint16_t recievePOS = 0; // stores position of recieving buffer
  char ID; // stores ID of current packet decoder
  ControlPacket * controlTemp = nullptr; // pointer to decoded packet
  recievePOS = rx.rxObj(ID, recievePOS); // store ID char
  if (ID == 'R') { // Raw control
    controlTemp = new Raw(RetrieveSerial<float>(4,recievePOS)); // creates new packet of type Raw

  } else if (ID == 'V') { // Velocity control
    float * dataPTR = RetrieveSerial<float>(2, recievePOS);
    controlTemp = new VelPID(dataPTR, acceleration, deacceleration); // creates new packet of type Velocity

  } else if (ID == 'D') { // Distance / Position control
    Serial.write("Distance!");
    controlTemp = new PosPID(RetrieveSerial<float>(2,recievePOS), acceleration, deacceleration);

  } else if (ID == 'T') {
    Serial.write("Turning!");
    controlTemp = new AngPID(RetrieveSerial<float>(3,recievePOS), IMU, acceleration, deacceleration);
  }
  
  else if (ID == 'S') { // stops the current rover actions and skips to the next one
    if (control != nullptr) {
      control->stop();
      delete control;
      controlTemp = nullptr;
    }

  } else if (ID == 'E') { // stops the rover and empties the packet buffer -> ideally for emergency / resetting the rover
    if (control != nullptr) {
      control->stop();
      packetBuff.clear();
      delete control;
      controlTemp = nullptr;
    }

  } else if (ID == 'C') { // write to EEPROM memory
    int * dataPTR = RetrieveSerial<int>(2,recievePOS);
    MemWrite(dataPTR[0], dataPTR[1]);

  } else { // Base case
    controlTemp = nullptr;
    
  }
  return controlTemp; // returns pointer to decoded packet

}

// fetch stored configuration parameters and assign to required locations
void MemSetup(RoboClaw & RC1, RoboClaw & RC2) {
  float fsettings[10] = {0}; // stores float settings in an array. [vP,vI,vD,pP,pI,pD,pMI,Deadzone, Acceleration, Deacceleration]
  for (size_t i = 0; i < 9*4; i = i + 4) {
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
  // ROBOCLAW_1.SetM1VelocityPID(0x80, Kp, Ki, Kd, qpps);
  // ROBOCLAW_1.SetM2VelocityPID(0x80, Kp, Ki, Kd, qpps);
  // ROBOCLAW_2.SetM1VelocityPID(0x80, Kp, Ki, Kd, qpps);
  // ROBOCLAW_2.SetM2VelocityPID(0x80, Kp, Ki, Kd, qpps);
  // ROBOCLAW_1.SetM1PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  // ROBOCLAW_1.SetM2PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  // ROBOCLAW_2.SetM1PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  // ROBOCLAW_2.SetM2PositionPID(uint8_t address, float kp, float ki, float kd, uint32_t kiMax, uint32_t deadzone, uint32_t min, uint32_t max);
  acceleration = fsettings[8];    // set acceleration variable
  deacceleration = fsettings[9];    // set deacceleration variable

}

void MemWrite(int adr, int val) {
  EEPROM.update(adr, val);
}


template<class T>
T * RetrieveSerial(size_t len, uint16_t & recievePOS) {
  size_t datasize = len; // sets size of data in the packet
  T * data = new T[datasize]; // creates an empty array of datasize
  for(size_t i = 0; i < datasize; i++) { // takes data from serial port and adds it to the packet
    recievePOS = rx.rxObj(data[i], recievePOS);
    Serial.println(data[i]);
  }
  Serial.write("done!");
  return data;
}


