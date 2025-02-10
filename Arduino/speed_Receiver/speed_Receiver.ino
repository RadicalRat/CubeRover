#include <Wire.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Select two motors (M1 and M2)
Adafruit_DCMotor *motor1 = AFMS.getMotor(1);
Adafruit_DCMotor *motor2 = AFMS.getMotor(2);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  AFMS.begin();
  setMotorSpeed(motor1, 0);
  setMotorSpeed(motor2, 0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){ //if serial port is available
  
    String mes = Serial.readStringUntil('\n');
    mes.trim();

    if(mes.length() > 1) { //separating data if its a valid input
      int pwm = mes.substring(0, mes.length()-1).toInt();
      char dir = mes.charAt(mes.length()-1);

      if(dir == 'F'){
        setMotorSpeed(motor1, pwm);
        setMotorSpeed(motor2, pwm);

      }

      else if (dir == 'B'){
        setMotorSpeed(motor1, -pwm);
        setMotorSpeed(motor2, -pwm);
      }

      else if (dir == 'R'){
        setMotorSpeed(motor1, pwm);
        setMotorSpeed(motor2, -pwm);
      }
      
      else if (dir == 'L'){
        setMotorSpeed(motor1, -pwm);
        setMotorSpeed(motor2, pwm);
      }
    }

  }



}



void setMotorSpeed(Adafruit_DCMotor *motor, int speed) {
    if (speed > 0) {
        motor->setSpeed(speed);  // Set PWM speed
        motor->run(FORWARD);  // Move forward
    } 
    else if (speed < 0) {
        motor->setSpeed(abs(speed));  // Set PWM speed
        motor->run(BACKWARD);  // Move backward
    } 
    else {
        motor->setSpeed(0);
        motor->run(RELEASE);  // Stop motor
    }
}
