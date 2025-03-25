#include <RoboClaw.h>
#include <time.h>



RoboClaw ROBOCLAW_1 = RoboClaw(&Serial1, 10000);


void setup() {
  ROBOCLAW_1.begin(38400);
}

void loop() {
  ROBOCLAW_1.ForwardM1(0x80, 32);
  ROBOCLAW_1.ForwardM2(0x80,32);
  delay(2*1000);
  ROBOCLAW_1.BackwardM1(0x80,32);
  ROBOCLAW_1.BackwardM2(0x80,32);
  delay(2*1000);
}
