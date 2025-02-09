#define FAN_PIN 9

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(FAN_PIN, OUTPUT);
  digitalWrite(FAN_PIN, LOW);  // Start with the fan OFF
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){ //if serial port is available
  
    int mes = Serial.parseInt();
    if(mes == 5){
      digitalWrite(FAN_PIN, HIGH);
    }
    Serial.println(mes);
  }



}
