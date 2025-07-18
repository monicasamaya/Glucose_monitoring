void setup() {
  Serial.begin(9600);        // Start serial communication
  analogReference(DEFAULT);  // Use 5V reference for Arduino UNO; change to INTERNAL for 3.3V boards
}

void loop() {
  int analogValue = analogRead(A0);  // Read from analog pin A0 (0 to 1023)

  // Convert to voltage 
  float voltage = (analogValue / 1023.0) * 3.3;

  Serial.println(voltage, 3);  // Print voltage with 3 decimal places

  delay(100);  // Sample every 100 ms
}
