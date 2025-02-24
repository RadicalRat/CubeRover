#include <RoboClaw.h>

#ifndef CONTROL_PACKET_H
#define CONTROL_PACKET_H


class ControlPacket {
  public:
    ControlPacket() {};
    virtual ~ControlPacket();
    virtual void resolve(RoboClaw * RC1, RoboClaw * RC2) = 0;
    void populate(int * data);
  protected:
    size_t _dataLength;
    int * _dataArr;
};

class Raw : public ControlPacket {
  public:
    Raw(int * data);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
};

class VelPID : public ControlPacket {
 public:
   VelPID(int * data);
   void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
};

class PosPID : public ControlPacket {
 public:
   PosPID(int * data);
   void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
};

// IMPLEMENTATIONS

// Implementation for parent class ControlPacket

ControlPacket::~ControlPacket() {
  delete[] _dataArr;
}

ControlPacket::populate(int *data) {
  _dataArr = new int[_dataLength];
  for (size_t i = 0; i < _dataLength; i++) {
    _dataArr[i] = data[i];
  }
}

// Implementations for child class Raw (for raw speed control)

Raw::Raw(int * data) {
  _dataLength = 4;
  this->populate(data);
}


void Raw::resolve(RoboClaw * RC1, RoboClaw * RC2) {
  RC1->ForwardBackwardM1(0x80, _dataArr[0]);
  RC1->ForwardBackwardM2(0x80, _dataArr[1]);
  RC2->ForwardBackwardM1(0x80, _dataArr[2]);
  RC2->ForwardBackwardM2(0x80, _dataArr[3]);
}


// Implementations for child class VelPID (for velocity speed PID control)

VelPID::VelPID(int * data) {
  _dataLength = 1;
  this->populate(data);
}

// TODO -> convert to qpps
void VelPID::resolve(RoboClaw * RC1, RoboClaw * RC2) {
  RC1->SpeedM1(0x80, _dataArr[0]);
  RC1->SpeedM2(0x80, _dataArr[0]);
  RC2->SpeedM1(0x80, _dataArr[0]);
  RC2->SpeedM2(0x80, _dataArr[0]);
}


// Implementations for child class VelPID (for velocity speed PID control)

PosPID::PosPID(int * data) {
  _dataLength = 2;
  this->populate(data);
}

// TODO -> convert to qpps
void PosPID::resolve(RoboClaw * RC1, RoboClaw * RC2) {
  RC1->SpeedDistanceM1(0x80, _dataArr[0], _dataArr[1]);
  RC1->SpeedDistanceM2(0x80, _dataArr[0], _dataArr[1]);
  RC2->SpeedDistanceM1(0x80, _dataArr[0], _dataArr[1]);
  RC2->SpeedDistanceM2(0x80, _dataArr[0], _dataArr[1]);
}


#endif

