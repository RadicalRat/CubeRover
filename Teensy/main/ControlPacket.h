#ifndef CONTROL_PACKET_H
#define CONTROL_PACKET_H

#include <RoboClaw.h>
#include <elapsedMillis.h>

elapsedMillis univTimer = 0;


class ControlPacket { // Basic controlpacket parent class
  public:
    ControlPacket() {}; // initializer -> does nothing
    virtual ~ControlPacket(); // destructor -> deletes _dataArr
    virtual void resolve(RoboClaw * RC1, RoboClaw * RC2) = 0; // resolve function -> resolves the packet
    virtual bool fulfilled() = 0;
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
    Raw(float * data);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled() final;
};

class VelPID : public ControlPacket {
 public:
   VelPID(float * data);
   void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
   bool fulfilled() final;
};

class PosPID : public ControlPacket {
 public:
   PosPID(float * data);
   void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
   bool fulfilled() final;
};

// IMPLEMENTATIONS

// Implementation for parent class ControlPacket

ControlPacket::~ControlPacket() {
  delete[] _dataArr;
}

void ControlPacket::populate(float *data) { // deep copys data to _dataArr
  _dataArr = new int[_dataLength];
  for (size_t i = 0; i < _dataLength; i++) {
      _dataArr[i] = data[i];
  }
}

// Implementations for child class Raw (for raw speed control)

Raw::Raw(float * data) { // initializes the raw class
  _dataLength = 4;
  this->populate(data);
}


void Raw::resolve(RoboClaw * RC1, RoboClaw * RC2) { // drives the motors based on the 4 data values initialized
  _RC1 = RC1;
  _RC2 = RC2;
  RC1->ForwardBackwardM1(0x80, _dataArr[0]); 
  RC1->ForwardBackwardM2(0x80, _dataArr[1]);
  RC2->ForwardBackwardM1(0x80, _dataArr[2]);
  RC2->ForwardBackwardM2(0x80, _dataArr[3]);
}

bool Raw::fulfilled() {
  return true;
}


// Implementations for child class VelPID (for velocity speed PID control)

VelPID::VelPID(float * data) { // initilizes the Velocity PID speed control packet
  _dataLength = 1;
  this->populate(data);
}

// TODO -> convert to qpps
void VelPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // sets all motors to go at speed denoted by the only number in data
  _RC1 = RC1;
  _RC2 = RC2;
  RC1->SpeedM1(0x80, _dataArr[0]);
  RC1->SpeedM2(0x80, _dataArr[0]);
  RC2->SpeedM1(0x80, _dataArr[0]);
  RC2->SpeedM2(0x80, _dataArr[0]);
  univTimer = 0;
}

bool VelPID::fulfilled() {
  return true;
}


// Implementations for child class VelPID (for velocity speed PID control)

PosPID::PosPID(float * data) { // initilizes the POSPID Class, for position control
  _dataLength = 2;
  this->populate(data);
}

// TODO -> convert to qpps
void PosPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // tells all motors to go _dataArr[0] distance at _dataArr[1] speed
  _RC1 = RC1;
  _RC2 = RC2;
  RC1->SetEncM1(0x80, 0);
  RC1->SetEncM2(0x80, 0);
  RC2->SetEncM1(0x80, 0);
  RC2->SetEncM2(0x80, 0);
  RC1->SpeedDistanceM1(0x80, _dataArr[0], _dataArr[1]);
  RC1->SpeedDistanceM2(0x80, _dataArr[0], _dataArr[1]);
  RC2->SpeedDistanceM1(0x80, _dataArr[0], _dataArr[1]);
  RC2->SpeedDistanceM2(0x80, _dataArr[0], _dataArr[1]);
}

bool PosPID::fulfilled() { // checks to see if all motors have traveled distance
    return true;
}


#endif

