#include "Arduino_LED_Matrix.h"

ArduinoLEDMatrix matrix;
String Inputs;

void setup() {
  Serial.begin(115200);
  matrix.begin();
  matrix.loadFrame(LEDMATRIX_UNO);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) { //If Serial port is open (not being used to write by python script)
    Inputs = Serial.readStringUntil('\n'); // sets the input variable to last written serial string until newline delim
    if (Inputs == "Happy") {
        matrix.loadFrame(LEDMATRIX_EMOJI_HAPPY);
        Serial.write("Passed");
    } else if (Inputs == "Sad") {
        matrix.loadFrame(LEDMATRIX_EMOJI_SAD);
        Serial.write("Passed");
    } else if (Inputs == "Heart") {
        matrix.loadFrame(LEDMATRIX_HEART_BIG);
        Serial.write("Passed");
    } else {
        matrix.loadFrame(LEDMATRIX_RESISTOR);
        Serial.write("Invalid");
    }
  }
}
