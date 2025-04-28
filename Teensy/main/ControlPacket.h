
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
    RoboClaw * _RC1;
    RoboClaw * _RC2;
};

// ControlPacket Implementations:

class VelPID : public ControlPacket {
 public:
    VelPID(float * data, int acceleration, int deacceleration);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) final;
    void stop() final;
  private:
    int _accel;
    int _deaccel;
    int _vL;
    int _vR;
    int _time;
};

class PosPID : public ControlPacket {
 public:
    PosPID(float * data, int acceleration, int deacceleration);
    void resolve(RoboClaw * RC1, RoboClaw * RC2) final;
    bool fulfilled(RingBuf<ControlPacket*, 20>& packetBuff  ) final;
    void stop() final;
  private:
    int _accel;
    int _deaccel;
    int _dist;
    int _vel;
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
    float _wheelBase;
    int _accel;
    int _deaccel;
    float _startVal;
    float _setpoint;
    float _ang;
    float _rad;
    int _vel;
    bool _dir; // T for CW, F for CCW
};

// IMPLEMENTATIONS



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementation for parent class ControlPacket
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



ControlPacket::~ControlPacket() {
  
}


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementations for child class VelPID (for velocity speed PID control)
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



VelPID::VelPID(float * data, int acceleration, int deacceleration) { // initilizes the Velocity PID speed control packet
  _vL = data[0];
  _vR = data[1];
  _time = data[2];
  delete data;
  _accel = acceleration;
  _deaccel = deacceleration;
}

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

  Serial.print(" | VL: ");
  Serial.print(_vL);
  Serial.print(" | VR: ");
  Serial.print(_vR);

  // commanding left roboclaws
  bool speedingUp = (_vL - speed1) * _vL > 0;
  int accelToUse = speedingUp ? _accel : _deaccel;
  _RC1->SpeedAccelM1(0x80, accelToUse, _vL);
  _RC1->SpeedAccelM2(0x80, accelToUse, _vL);
  Serial.print(" | Accel: ");
  Serial.println(accelToUse);

  // commanding right roboclaws
  speedingUp = (_vR - speed1) * _vR > 0;
  accelToUse = speedingUp ? _accel : _deaccel;
  _RC2->SpeedAccelM1(0x80, accelToUse, _vR);
  _RC2->SpeedAccelM2(0x80, accelToUse, _vR);
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

  if (univTimer >= _time) {
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
  _RC1->SpeedAccelM1M2(0x80, _deaccel, 0, 0);
  _RC2->SpeedAccelM1M2(0x80, _deaccel, 0, 0);
}



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementations for child class PosPID (for positional PID control)
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


PosPID::PosPID(float * data, int Acceleration, int Deacceleration) { // initilizes the POSPID Class, for position control
  // _dataLength = 2;
  // this->populate(data);
  _dist = data[0];
  _vel = data[1];
  delete data;
  Serial.write("Distance created");
  _accel = Acceleration;
  _deaccel = Deacceleration;
}

// TODO -> convert to qpps
void PosPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // tells all motors to go _dataArr[0] distance at _dataArr[1] rpm
  _RC1 = RC1;
  _RC2 = RC2;
  _RC1->ResetEncoders(0x80);
  _RC2->ResetEncoders(0x80);
  delay(50);
  _RC1->SpeedAccelDeccelPositionM1(0x80, _accel, _vel, _deaccel, _dist, 1);
  _RC1->SpeedAccelDeccelPositionM2(0x80, _accel, _vel, _deaccel, _dist, 1);
  _RC2->SpeedAccelDeccelPositionM1(0x80, _accel, _vel, _deaccel, _dist, 1);
  _RC2->SpeedAccelDeccelPositionM2(0x80, _accel, _vel, _deaccel, _dist, 1);
}

bool PosPID::fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) {    // checks if packet is complete (based on placeholder 2 second timer)

  _RC1->ReadBuffers(0x80,depth1,depth2);
  _RC2->ReadBuffers(0x80,depth3,depth4);
  delay(20);
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
  _RC1->SpeedAccelM1M2(0x80, _deaccel, 0, 0);
  _RC2->SpeedAccelM1M2(0x80, _deaccel, 0, 0);
}



//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Implementation for child class Angle PID for angle control
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


AngPID::AngPID(float * data, Adafruit_BNO055 & BNO, int Acceleration, int Deacceleration) { // initilizes the AngPID Class, for radius turning control
  _ang = data[0];
  _rad = data[1];
  _vel = data[2];
  delete data;
  _IMU = &BNO;
  _accel = Acceleration;
  _deaccel = Deacceleration;
  _wheelBase = 40;
}

// TODO -> convert to qpps
void AngPID::resolve(RoboClaw * RC1, RoboClaw * RC2) { // sets the config settings based on given parameters, 1st is angle, 2nd is radius, 3rd is speed
  _RC1 = RC1;
  _RC2 = RC2;
  sensors_event_t orientationData;
  _IMU->getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);

  if (_rad > 0) {
    _dir = true;
    _wheelBase = _wheelBase;
    _rad = abs(_rad);
    _ang = abs(_ang);
  } else {
    _dir = false;
    _rad = abs(_rad);
    _wheelBase = -_wheelBase;
    _ang = -1 * abs(_ang);
  }
  
  _setpoint = fmod(((orientationData.orientation.x + _ang) + 360.0) , 360.0);
  
  univTimer = 0;
  integralTerm = 0;
  Serial.print(orientationData.orientation.x);
  Serial.println(_setpoint);
}

bool AngPID::fulfilled(RingBuf<ControlPacket*, 20>& packetBuff) {    // checks if packet is complete (based on placeholder 2 second timer)
  // determine if the current orientation is fulfilled
  delay(50);
  sensors_event_t orientationData;
  _IMU->getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  float error;
  if (_dir) {
    error = fmod((_setpoint - orientationData.orientation.x + 360.0), 360.0);
  } else {
    error = fmod((orientationData.orientation.x - _setpoint + 360.0), 360.0);
  }
  // float error = fmod((_setpoint - orientationData.orientation.x), 360.0);
  
  
  Serial.print("Orientation:");
  Serial.print(orientationData.orientation.x);
  Serial.print(" | Setpoint: ");
  Serial.print(_setpoint);
  Serial.print(" | Error: ");
  Serial.print(error);

  if (error > angTol) {
    integralTerm += error * univTimer;

    if (abs(integralTerm * angI) > 500) {
      integralTerm = 500 / angI;
    }

    univTimer = 0;
    double Vel = angP * error + angI * integralTerm;

    if (Vel > _vel) {
      Vel = _vel;
    }

    float vL = Vel * ((_rad + (_wheelBase / 2)) / _rad)  ;
    float vR = Vel * ((_rad - (_wheelBase / 2)) / _rad)  ;
    Serial.print(" | Velocity: ");
    Serial.print(Vel);
    Serial.print(" | VelocityL: ");
    Serial.print(vL);
    Serial.print(" | VelocityR: ");
    Serial.print(vR);
    Serial.print(" | Wheel Base: ");
    Serial.println(_wheelBase);

    // _RC1->SpeedAccelM1M2(0x80, _accel, Vel * ((_dataArr[1] - _wheelBase / 2) / _dataArr[1]), Vel * ((_dataArr[1] - _wheelBase / 2) / _dataArr[1])); // assumes this roboclaw controls left wheels
    // _RC2->SpeedAccelM1M2(0x80, _accel, Vel * ((_dataArr[1] + _wheelBase / 2) / _dataArr[1]), Vel * ((_dataArr[1] + _wheelBase / 2) / _dataArr[1]));
    _RC1->SpeedAccelM1(0x80, _accel, vL);
    _RC1->SpeedAccelM2(0x80, _accel, vL);
    _RC2->SpeedAccelM1(0x80, _accel, vR);
    _RC2->SpeedAccelM2(0x80, _accel, vR);
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

