int ledPin = 13;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') 
    {
      for(int i=0 ; i<5 ; i++ )
      {
        digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
        delay(500);                      // wait for a second
        digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
        delay(500);                      // wait for a second
      }
      Serial.println("LED is ON");
    } 
    
    
    else if (command == '0') {
      digitalWrite(ledPin, LOW); 
      Serial.println("LED is OFF");
    }
  }
}
