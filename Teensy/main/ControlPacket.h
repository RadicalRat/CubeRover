
#ifndef CONTROL_PACKET_H
#define CONTROL_PACKET_H

#include <RoboClaw.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <elapsedMillis.h>

elapsedMillis univTimer = 0;

float angP = 5;
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
    float * _dataArr; // holds the data to be resolved
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
    VelPID(float * data, float Acceleration, float Deacceleration);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) final;
    void stop() final;
  private:
  float _accel;
  float _deaccel;
};

class PosPID : public ControlPacket {
 public:
    PosPID(float * data, float Acceleration, float Deacceleration);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled(RingBuf<ControlPacket*, 20>& packetBuff  ) final;
    void stop() final;
  private:
    float _accel;
    float _deaccel;
    uint8_t depth1,depth2,depth3,depth4; // for holding buffer states
};

class AngPID : public ControlPacket {
  public:
    AngPID(float * data, Adafruit_BNO055 & BNO, int acceleration, int deacceleration);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) final;
    void stop() final;
  private:
    Adafruit_BNO055 * _IMU = nullptr;
    float _wheelBase = 40;
    float _accel;
    float _deaccel;
    float _startVal;
    float _endVal;
};

// IMPLEMENTATIONS



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementation for parent class ControlPacket
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



ControlPacket::~ControlPacket() {
  delete[] _dataArr;
}

void ControlPacket::populate(float * data) { // deep copys data to _dataArr
  _dataArr = new float[_dataLength];
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



VelPID::VelPID(float * data, float acceleration, float deacceleration) { // initilizes the Velocity PID speed control packet
  _dataLength = 3;
  this->populate(data);
  delete data;
  _accel = acceleration;
  _deaccel = deacceleration;
}

// TODO -> convert to qpps
void VelPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // sets all motors to go at speed denoted by the only number in data
  _RC1 = RC1;
  _RC2 = RC2;

  // status conditions to make sure recieved packet is valid
  uint8_t status1,status2;
  bool valid1,valid2;
  int32_t speed1 = _RC1->ReadSpeedM1(0x80, &status1, &valid1);
  int32_t speed2 = _RC2->ReadSpeedM1(0x80, &status2, &valid2);

  while(!valid1 && !valid2) { // if invalid reading, read until valid encoder setpoint
    int32_t speed1 = _RC1->ReadSpeedM1(0x80, &status1, &valid1);
    int32_t speed2 = _RC2->ReadSpeedM1(0x80, &status2, &valid2);
  }

  Serial.print("VL: ");
  Serial.print(speed1);
  Serial.print(" | VR: ");
  Serial.print(speed2);

  if (speed1 >= _dataArr[0]) {
    _RC1->SpeedAccelM1M2(0x80, _deaccel, _dataArr[0], _dataArr[0]);
    Serial.print(" | Accel: ");
    Serial.println(_accel);
  } else {
    _RC1->SpeedAccelM1M2(0x80, _accel, _dataArr[0], _dataArr[0]);
    Serial.print(" | Accel: ");
    Serial.println(_deaccel);
  }
  
  if (speed2 >= _dataArr[1]) {
    _RC2->SpeedAccelM1M2(0x80, _accel, _dataArr[1], _dataArr[1]);
  } else {
    _RC2->SpeedAccelM1M2(0x80, _deaccel, _dataArr[1], _dataArr[1]);
  }
  univTimer = 0;
}

bool VelPID::fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) {    // checks if packet is complete (based on placeholder 2 second timer)
  uint8_t status1,status2;
  bool valid1,valid2;
  int32_t speed1 = _RC1->ReadSpeedM1(0x80, &status1, &valid1);
  int32_t speed2 = _RC2->ReadSpeedM1(0x80, &status2, &valid2);
  Serial.print("VL: ");
  Serial.print(speed1);
  Serial.print(" | VR: ");
  Serial.println(speed2);

  if (univTimer >= _dataArr[2]) {
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



PosPID::PosPID(float * data, float Acceleration, float Deacceleration) { // initilizes the POSPID Class, for position control
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
  delay(50);
  Serial.write("Distance Resolved");
  Serial.println(_dataArr[0]);
  Serial.println(_dataArr[1]);
  _RC1->ResetEncoders(0x80);
  _RC2->ResetEncoders(0x80);
  _RC1->SpeedAccelDistanceM1(0x80, _accel, static_cast<uint32_t>(_dataArr[1]), static_cast<uint32_t>(_dataArr[0]), 1);
  _RC1->SpeedAccelDistanceM2(0x80, _accel, _dataArr[1], _dataArr[0], 1);
  _RC2->SpeedAccelDistanceM1(0x80, _accel, _dataArr[1], _dataArr[0], 1);
  _RC2->SpeedAccelDistanceM2(0x80, _accel, _dataArr[1], _dataArr[0], 1);
}

bool PosPID::fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) {    // checks if packet is complete (based on placeholder 2 second timer)
  

  // status conditions to make sure recieved packet is valid
  delay(50);
  // uint8_t status1,status2,status3,status4;
  // bool valid1,valid2,valid3,valid4;
  // int32_t enc1= _RC1->ReadEncM1(0x80, &status1, &valid1);
  // int32_t enc2= _RC1->ReadEncM2(0x80, &status2, &valid2);
  // int32_t enc3= _RC2->ReadEncM1(0x80, &status3, &valid3);
  // int32_t enc4= _RC2->ReadEncM2(0x80, &status4, &valid4);
  // Serial.print(_dataArr[0]); Serial.print(" | ");
  // Serial.print(enc1); Serial.print(" | ");
  // Serial.print(enc2); Serial.print(" | ");
  // Serial.print(enc3); Serial.print(" | ");
  // Serial.print(enc4); Serial.println(" | ");

  // int32_t error1 = abs(setpoint - enc1);
  // int32_t error2 = abs(setpoint - enc2);
  // int32_t error3 = abs(setpoint - enc3);
  // int32_t error4 = abs(setpoint - enc4);

  _RC1->ReadBuffers(0x80,depth1,depth2);
  _RC2->ReadBuffers(0x80,depth3,depth4);

  Serial.print(depth1); Serial.print(" | ");
  Serial.print(depth2); Serial.print(" | ");
  Serial.print(depth3); Serial.print(" | ");
  Serial.print(depth4); Serial.println(" | ");


  if (depth1==0x80 && depth2==0x80 && depth3==0x80 && depth4==0x80) { // if all 4 roboclaw buffers state POS is reached
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


AngPID::AngPID(float * data, Adafruit_BNO055 & BNO, int Acceleration, int Deacceleration) { // initilizes the AngPID Class, for radius turning control
  _dataLength = 3;
  this->populate(data);
  delete data;
  Serial.write("Ang created");
  _IMU = &BNO;
  _accel = Acceleration;
  _deaccel = Deacceleration;
}

// TODO -> convert to qpps
void AngPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // sets the config settings based on given parameters, 1st is angle, 2nd is radius, 3rd is speed
  _RC1 = RC1;
  _RC2 = RC2;
  sensors_event_t orientationData;
  _IMU->getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  if (_dataArr[1] < 0) {
    _wheelBase = _wheelBase * -1;
    _endVal = orientationData.orientation.x - _dataArr[0];
  } else {
    _endVal = orientationData.orientation.x + _dataArr[0];
  }

  if (_endVal > 360) {
    _endVal += -360;
  } else if (_endVal < 0) {
    _endVal += 360;
  }
  univTimer = 0;
  integralTerm = 0;
  Serial.print(orientationData.orientation.x);
  Serial.println(_endVal);
}

bool AngPID::fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) {    // checks if packet is complete (based on placeholder 2 second timer)
  // determine if the current orientation is fulfilled
  delay(100);
  sensors_event_t orientationData;
  _IMU->getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  float error = _endVal - orientationData.orientation.x;
  Serial.print("Orientation:");
  Serial.print(orientationData.orientation.x);
  Serial.print(" | Error: ");
  Serial.print(error);
  if (abs(error) > angTol) {
    integralTerm += abs(error) * univTimer;

    if (abs(integralTerm * angI) > 500) {
      integralTerm = 500 / angI;
    }

    univTimer = 0;
    double Vel = angP * error + angI * integralTerm;

    if (Vel > _dataArr[2]) {
      Vel = _dataArr[2];
    }
    Serial.print(" | Velocity: ");
    Serial.print(Vel);
    Serial.print(" | VelocityL: ");
    Serial.print(Vel * ((_dataArr[1] - _wheelBase / 2) / _dataArr[1]));
    Serial.print(" | VelocityR: ");
    Serial.println(Vel * ((_dataArr[1] + _wheelBase / 2) / _dataArr[1]));
    _RC1->SpeedAccelM1M2(0x80, _accel, Vel * ((_dataArr[1] - _wheelBase / 2) / _dataArr[1]), Vel * ((_dataArr[1] - _wheelBase / 2) / _dataArr[1])); // assumes this roboclaw controls left wheels
    _RC2->SpeedAccelM1M2(0x80, _accel, Vel * ((_dataArr[1] + _wheelBase / 2) / _dataArr[1]), Vel * ((_dataArr[1] + _wheelBase / 2) / _dataArr[1]));
    return false;
  }
  else {
    _RC1->SpeedM1(0x80, 0);
    _RC1->SpeedM2(0x80, 0);
    _RC2->SpeedM1(0x80, 0);
    _RC2->SpeedM2(0x80, 0);
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

