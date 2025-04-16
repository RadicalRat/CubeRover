#include <EEPROM.h>

// velocity PID gains
float pP = 11.37910;
float pI = 0.345;
float pD = 0;

// position PID gains
float vP = 10; 
float vI = 1;
float vD = 3;
float vMI = 0;
float Deadzone = 1; 

// acceleration / deacceleration
float acceleration = 100;
float deacceleration = 100;



void setup() {
  // for (int i = 0; i < EEPROM.length(); i++) {
  //   EEPROM.write(i,0);
  // }
  Serial.begin(38400);

  EEPROM.put(0,pP);
  EEPROM.put(4,pI);
  EEPROM.put(8,pD);
  EEPROM.put(12,vP);
  EEPROM.put(16,vI);
  EEPROM.put(20,vD);
  EEPROM.put(24,vMI);
  EEPROM.put(28,Deadzone);
  EEPROM.put(32,acceleration);
  EEPROM.put(36,deacceleration);

}


int address = 0;
float f = 0;

void loop() {
  EEPROM.get(address, f);
  Serial.write("address: ");
  Serial.print(address);
  Serial.write(" | value: ");
  Serial.print(f);
  Serial.println();
  address = address + 4;

  if (address > 36) {
    address = 0;
  }

  delay(500);
}
