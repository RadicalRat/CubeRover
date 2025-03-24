
#ifndef CONTROL_PACKET_H
#define CONTROL_PACKET_H

#include <RoboClaw.h>
#include <Adafruit_BNO055.h>
#include <elapsedMillis.h>

elapsedMillis univTimer = 0;


class ControlPacket { // Basic controlpacket parent class
  public:
    ControlPacket() {}; // initializer -> does nothing
    virtual ~ControlPacket(); // destructor -> deletes _dataArr
    virtual void resolve(RoboClaw * RC1, RoboClaw * RC2) = 0; // resolve function -> resolves the packet
    virtual bool fulfilled() = 0;
    virtual void stop() = 0;
  protected:
    void populate(float * data); // populates the _dataArr array
    size_t _dataLength; // holds the length of data
    int * _dataArr; // holds the data to be resolved
    RoboClaw * _RC1;
    RoboClaw * _RC2;
};

// ControlPacket Implementations:
class Raw : public ControlPacket {
  public:
    Raw(float * data); // change to pass size of packet buffer? pass the whole packetbuffer?
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled() final;
    void stop() final;
};

class VelPID : public ControlPacket {
 public:
    VelPID(float * data);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled() final;
    void stop() final;
};

class PosPID : public ControlPacket {
 public:
    PosPID(float * data);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled() final;
    void stop() final;
};

class AngPID : public ControlPacket {
  public:
    AngPID(float * data, Adafruit_BNO055 & IMU);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled() final;
    void stop() final;
  private:
    Adafruit_BNO055 * _IMU = nullptr;
};

// IMPLEMENTATIONS



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementation for parent class ControlPacket
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



ControlPacket::~ControlPacket() {
  delete[] _dataArr;
}

void ControlPacket::populate(float *data) { // deep copys data to _dataArr
  _dataArr = new int[_dataLength];
  for (size_t i = 0; i < _dataLength; i++) {
      _dataArr[i] = data[i];
  }
}



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementations for child class Raw (for raw speed control)
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



Raw::Raw(float * data) { // initializes the raw class
  _dataLength = 4;
  this->populate(data);
}


void Raw::resolve(RoboClaw * RC1, RoboClaw * RC2) { // drives the motors based on the 4 data values initialized
  _RC1 = RC1;
  _RC2 = RC2;
  _RC1->ForwardBackwardM1(0x80, _dataArr[0]); 
  _RC1->ForwardBackwardM2(0x80, _dataArr[1]);
  _RC2->ForwardBackwardM1(0x80, _dataArr[2]);
  _RC2->ForwardBackwardM2(0x80, _dataArr[3]);
  univTimer = 0;    // starts stopping timer
}

bool Raw::fulfilled() {   // checks if packet is complete (based on placeholder 2 second timer)
  if (univTimer >= 2000) {
    _RC1->ForwardBackwardM1(0x80, 64); 
    _RC1->ForwardBackwardM2(0x80, 64);
    _RC2->ForwardBackwardM1(0x80, 64);
    _RC2->ForwardBackwardM2(0x80, 64);
    return true;
  } else {
    return false;
  }
}

void Raw::stop() { // sets the roboclaws to stop before the packet is fulfilled
  _RC1->ForwardBackwardM1(0x80, 64); 
  _RC1->ForwardBackwardM2(0x80, 64);
  _RC2->ForwardBackwardM1(0x80, 64);
  _RC2->ForwardBackwardM2(0x80, 64);
}



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementations for child class VelPID (for velocity speed PID control)
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



VelPID::VelPID(float * data) { // initilizes the Velocity PID speed control packet
  _dataLength = 1;
  this->populate(data);
}

// TODO -> convert to qpps
void VelPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // sets all motors to go at speed denoted by the only number in data
  _RC1 = RC1;
  _RC2 = RC2;
  _RC1->SpeedM1(0x80, _dataArr[0]);
  _RC1->SpeedM2(0x80, _dataArr[0]);
  _RC2->SpeedM1(0x80, _dataArr[0]);
  _RC2->SpeedM2(0x80, _dataArr[0]);
  univTimer = 0;
}

bool VelPID::fulfilled() {    // checks if packet is complete (based on placeholder 2 second timer)
  if (univTimer >= 2000) {
    _RC1->SpeedM1(0x80, 0);
    _RC1->SpeedM2(0x80, 0);
    _RC2->SpeedM1(0x80, 0);
    _RC2->SpeedM2(0x80, 0);
    return true;
  } else {
    return false;
  }
}

void VelPID::stop() { // sets the roboclaws to stop before the packet is fulfilled
  _RC1->SpeedM1(0x80, 0);
  _RC1->SpeedM2(0x80, 0);
  _RC2->SpeedM1(0x80, 0);
  _RC2->SpeedM2(0x80, 0);
}



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementations for child class PosPID (for positional PID control)
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



PosPID::PosPID(float * data) { // initilizes the POSPID Class, for position control
  _dataLength = 2;
  this->populate(data);
}

// TODO -> convert to qpps
void PosPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // tells all motors to go _dataArr[0] distance at _dataArr[1] rpm
  _RC1 = RC1;
  _RC2 = RC2;
  _RC1->SetEncM1(0x80, 0);
  _RC1->SetEncM2(0x80, 0);
  _RC2->SetEncM1(0x80, 0);
  _RC2->SetEncM2(0x80, 0);
  _RC1->SpeedDistanceM1(0x80, _dataArr[0], _dataArr[1]);
  _RC1->SpeedDistanceM2(0x80, _dataArr[0], _dataArr[1]);
  _RC2->SpeedDistanceM1(0x80, _dataArr[0], _dataArr[1]);
  _RC2->SpeedDistanceM2(0x80, _dataArr[0], _dataArr[1]);
}

bool PosPID::fulfilled() {    // checks if packet is complete (based on placeholder 2 second timer)
  int32_t tol = 2;
  int32_t setpoint = _dataArr[0];
  int32_t enc1 = _RC1->ReadEncM1(0x80);
  int32_t enc2 = _RC1->ReadEncM2(0x80);
  int32_t enc3 = _RC2->ReadEncM1(0x80);
  int32_t enc4 = _RC2->ReadEncM2(0x80);
  if ( (abs(enc1 - setpoint) <= tol) || (abs(enc2 - setpoint) <= tol) || (abs(enc3 - setpoint) <= tol) || (abs(enc4 - setpoint) <= tol) ) { // checks if all encoders are within setpoint tolerance
    return true;
  } else {
    return false;
  }
}

void PosPID::stop() { // sets the roboclaws to stop before the packet is fulfilled
  // potentially the wrong method to stop? documentation unclear
  _RC1->SpeedM1(0x80, 0);
  _RC1->SpeedM2(0x80, 0);
  _RC2->SpeedM1(0x80, 0);
  _RC2->SpeedM2(0x80, 0);
}


#endif

