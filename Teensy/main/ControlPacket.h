
#ifndef CONTROL_PACKET_H
#define CONTROL_PACKET_H

#include <RoboClaw.h>
#include <Adafruit_BNO055.h>
#include <elapsedMillis.h>

elapsedMillis univTimer = 0;

float angP = 11;
float angI = 0.3;
float integralTerm;
float angTol = 3;

class ControlPacket { // Basic controlpacket parent class
  public:
    ControlPacket() {}; // initializer -> does nothing
    virtual ~ControlPacket(); // destructor -> deletes _dataArr
    virtual void resolve(RoboClaw * RC1, RoboClaw * RC2) = 0; // resolve function -> resolves the packet
    virtual bool fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) = 0;
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
    bool fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) final;
    void stop() final;
};

class VelPID : public ControlPacket {
 public:
    VelPID(float * data, int Acceleration, int Deacceleration);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) final;
    void stop() final;
  private:
  int _accel;
  int _deaccel;
};

class PosPID : public ControlPacket {
 public:
    PosPID(float * data, int Acceleration, int Deacceleration);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled(RingBuf<ControlPacket*, 20>& packetBuff  ) final;
    void stop() final;
  private:
    int _accel;
    int _deaccel;
};

class AngPID : public ControlPacket {
  public:
    AngPID(float * data, Adafruit_BNO055 & IMU, int acceleration, int deacceleration);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) final;
    void stop() final;
  private:
    Adafruit_BNO055 * _IMU = nullptr;
    float _wheelBase = 40;
    int _accel;
    int _deaccel;
};

// IMPLEMENTATIONS



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementation for parent class ControlPacket
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



ControlPacket::~ControlPacket() {
  delete[] _dataArr;
}

void ControlPacket::populate(float * data) { // deep copys data to _dataArr
  _dataArr = new int[_dataLength];
  for (size_t i = 0; i < _dataLength; i++) {
    _dataArr[i] = data[i];
  }
}



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementations for child class Raw (for raw speed control)
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



Raw::Raw(float * data) { // initializes the raw class -> TODO: Add reference to packet buffer? Want to fulfill if another packet is available and time duration is done
  _dataLength = 4;
  this->populate(data);
  delete data;
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

bool Raw::fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) {   // checks if packet is complete (based on placeholder 2 second timer)
  if (univTimer >= 1000) {
    _RC1->ForwardBackwardM1(0x80, 64); 
    _RC1->ForwardBackwardM2(0x80, 64);
    _RC2->ForwardBackwardM1(0x80, 64);
    _RC2->ForwardBackwardM2(0x80, 64);
    return true;
  } else if (packetBuff.size() >= 1) {
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



VelPID::VelPID(float * data, int acceleration, int deacceleration) { // initilizes the Velocity PID speed control packet
  _dataLength = 2;
  Serial.println(data[0]);
  this->populate(data);
  delete data;
  _accel = acceleration;
  _deaccel = deacceleration;
}

// TODO -> convert to qpps
void VelPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // sets all motors to go at speed denoted by the only number in data
  _RC1 = RC1;
  _RC2 = RC2;
  int speedM1 = _RC1->ReadSpeedM1(0x80);
  if (speedM1 >= _dataArr[0]) {
    _RC1->SpeedAccelM1M2(0x80, _accel, _dataArr[0], _dataArr[0]);
  } else {
    _RC1->SpeedAccelM1M2(0x80, _deaccel, _dataArr[0], _dataArr[0]);
  }
  int speedM3 = _RC2->ReadSpeedM1(0x80);
  if (speedM3 >- _dataArr[1]) {
    _RC2->SpeedAccelM1M2(0x80, _accel, _dataArr[1], _dataArr[1]);
  } else {
    _RC2->SpeedAccelM1M2(0x80, _deaccel, _dataArr[1], _dataArr[1]);
  }
  univTimer = 0;
}

bool VelPID::fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) {    // checks if packet is complete (based on placeholder 2 second timer)
  if (univTimer >= 500) {
    _RC1->SpeedAccelM1M2(0x80, _deaccel, 0, 0);
    _RC2->SpeedAccelM1M2(0x80, _deaccel, 0, 0);
    return true;
  } else if ( packetBuff.size() >= 1 ) {
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



PosPID::PosPID(float * data, int Acceleration, int Deacceleration) { // initilizes the POSPID Class, for position control
  _dataLength = 2;
  this->populate(data);
  delete data;
  Serial.write("Distance created");
  _accel = Acceleration;
  _deaccel = Deacceleration;
}

// TODO -> convert to qpps
void PosPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // tells all motors to go _dataArr[0] distance at _dataArr[1] rpm
  _RC1 = RC1;
  _RC2 = RC2;
  Serial.write("Distance Resolved");
  _RC1->SetEncM1(0x80, 0);
  _RC1->SetEncM2(0x80, 0);
  _RC2->SetEncM1(0x80, 0);
  _RC2->SetEncM2(0x80, 0);
  _RC1->SpeedAccelDistanceM1M2(0x80, _accel, _dataArr[1], _dataArr[0], _dataArr[1], _dataArr[0]);
  _RC2->SpeedAccelDistanceM1M2(0x80, _accel, _dataArr[1], _dataArr[0], _dataArr[1], _dataArr[0]);
}

bool PosPID::fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) {    // checks if packet is complete (based on placeholder 2 second timer)
  int32_t tol = 1;
  int32_t setpoint = _dataArr[0];
  int32_t enc1 = _RC1->ReadEncM1(0x80);
  int32_t enc2 = _RC1->ReadEncM2(0x80);
  int32_t enc3 = _RC2->ReadEncM1(0x80);
  int32_t enc4 = _RC2->ReadEncM2(0x80);
  Serial.println(setpoint - enc1);
  delay(500);
  if ( (abs(enc1 - setpoint) <= tol) && (abs(enc2 - setpoint) <= tol) && (abs(enc3 - setpoint) <= tol) && (abs(enc4 - setpoint) <= tol) ) { // checks if all encoders are within setpoint tolerance
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



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementation for child class Angle PID for angle control
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


AngPID::AngPID(float * data, Adafruit_BNO055 & IMU, int Acceleration, int Deacceleration) { // initilizes the POSPID Class, for position control
  _dataLength = 3;
  this->populate(data);
  delete data;
  Serial.write("Ang created");
  _IMU = &IMU;
  _accel = Acceleration;
  _deaccel = Deacceleration;
}

// TODO -> convert to qpps
void AngPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // tells all motors to go _dataArr[0] distance at _dataArr[1] rpm
  _RC1 = RC1;
  _RC2 = RC2;
  if (_dataArr[1] < 0) {
    _wheelBase = _wheelBase * -1;
  }
  univTimer = 0;
  integralTerm = 0;
}

bool AngPID::fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) {    // checks if packet is complete (based on placeholder 2 second timer)
  // determine if the current orientation is fulfilled
  sensors_event_t orientationData;
  _IMU->getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  float error = _dataArr[0] - orientationData.orientation.x;
  if (abs(error) > angTol) {
    integralTerm += error * univTimer;
    univTimer = 0;
    double Vel = angP * error + angI * integralTerm;
    if (Vel > _dataArr[2]) {
      Vel = _dataArr[2];
    }
    _RC1->SpeedAccelM1M2(0x80, _accel, Vel * ((_dataArr[1] - _wheelBase / 2) / _dataArr[1]), Vel * ((_dataArr[1] - _wheelBase / 2) / _dataArr[1])); // assumes this roboclaw controls left wheels
    _RC2->SpeedAccelM1M2(0x80, _accel, Vel * ((_dataArr[1] - _wheelBase / 2) / _dataArr[1]), Vel * ((_dataArr[1] - _wheelBase / 2) / _dataArr[1]));
    return false;
  }
  else {
    return true;
  }
}

void AngPID::stop() { // sets the roboclaws to stop before the packet is fulfilled
  // potentially the wrong method to stop? documentation unclear
  _RC1->SpeedM1(0x80, 0);
  _RC1->SpeedM2(0x80, 0);
  _RC2->SpeedM1(0x80, 0);
  _RC2->SpeedM2(0x80, 0);
}


#endif

