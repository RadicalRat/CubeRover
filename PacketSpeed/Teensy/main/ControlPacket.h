#include <RoboClaw.h>

#ifndef CONTROL_PACKET_H
#define CONTROL_PACKET_H





class ControlPacket {
  public:
    ControlPacket() {};
    virtual ~ControlPacket();
    virtual void resolve(RoboClaw * RC1, RoboClaw * RC2) = 0;
  protected:
    int _dataLength;
    int * _dataArr;
};

class Raw : public ControlPacket {
  public:
    Raw(int * data);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
};

//class VelPID : public ControlPacket {
//  public:
//    VelPID(int * data, RoboClaw * RC1, RoboClaw * RC2);
//    void resolve(const float * PID, float speed) final;
//}
//
//class PosPID : public ControlPacket {
//  public:
//    PosPId(int * data, RoboClaw * RC1, RoboClaw * RC2);
//    void resolve(const float * PID, float dist) final;
//}

// IMPLEMENTATIONS

// Implementation for parent class ControlPacket

ControlPacket::~ControlPacket() {
  delete[] _dataArr;
}

// Implementations for child class Raw (for raw speed control)

Raw::Raw(int * data) {
  size_t _dataLength = 4;
  _dataArr = new int[_dataLength];
  for (size_t i = 0; i < _dataLength; i++) {
    _dataArr[i] = data[i];
  }
}


void Raw::resolve(RoboClaw * RC1, RoboClaw * RC2) {
  RC1->ForwardM1(0x80, _dataArr[0]);
  RC1->ForwardM2(0x80, _dataArr[1]);
  RC2->ForwardM1(0x80, _dataArr[2]);
  RC2->ForwardM2(0x80, _dataArr[3]);
}


//// Implementations for child class VelPID (for velocity speed PID control)
//
//VelPID:VelPID(int * data, RoboClaw * RC1, RoboClaw * RC2) {
//  _RC1 = RC1;
//  _RC2 = RC2;
//  _dataLength = 4;
//  _dataArr = new int[_dataLength];
//  for (size_t i = 0; i < _dataLength; i++) {
//    _dataArr[i] = data[i];
//  }
//}
//
//// TODO -> convert to qpps
//void VelPID::resolve(const float * PID, float speed) {
//  // _RC1->SetM1VelocityPID(0x80, float Kp, float Ki, float Kd, int qpps);
//  // _RC1->SetM2VelocityPID(0x80, float Kp, float Ki, float Kd, int qpps);
//  // _RC1->SetM1VelocityPID(0x80, float Kp, float Ki, float Kd, int qpps);
//  // _RC1->SetM2VelocityPID(0x80, float Kp, float Ki, float Kd, int qpps);
//}
//
//
//// Implementations for child class VelPID (for velocity speed PID control)
//
//PosPID:PosPID(int * data, RoboClaw * RC1, RoboClaw * RC2) {
//  _RC1 = RC1;
//  _RC2 = RC2;
//  _dataLength = 4;
//  _dataArr = new int[_dataLength];
//  for (size_t i = 0; i < _dataLength; i++) {
//    _dataArr[i] = data[i];
//  }
//}
//
//// TODO -> convert to qpps
//void PosPID::resolve(const float * PID, float speed) {
//  _RC1->SetM1PositionPID()
//  _RC1
//}


#endif

