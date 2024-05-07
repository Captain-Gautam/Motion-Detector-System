const int buttonPin1 = 2;
const int buttonPin2 = 3;
const int buttonPin3 = 4;
const int buttonPin4 = 5;
const int buttonPin5 = 6;
const int buttonPin6 = 7;
const int buttonPin7 = 8;
const int ledPin = 13;  // LED pin for button feedback

const int PIN_TO_SENSOR = 9;  // Sensor pin
const int LED = 10;           // Additional LED pin
const int LED1 = 12;          // Additional LED1 pin
int pinStateCurrent = LOW;    // Current sensor state
int pinStatePrevious = LOW;   // Previous sensor state

int buttonState1 = 0;
int buttonState2 = 0;
int buttonState3 = 0;
int buttonState4 = 0;
int buttonState5 = 0;
int buttonState6 = 0;
int buttonState7 = 0;

unsigned long motionSensorTriggeredMillis = 0; // Timestamp when motion sensor was last triggered
const long motionSensorDelay = 60000; // Delay before motion sensor can trigger again
bool motionSensorCooldown = false; // Indicates if we're in the cooldown period

void setup() {
  Serial.begin(9600);
  
  pinMode(ledPin, OUTPUT);
  
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
  pinMode(buttonPin4, INPUT);
  pinMode(buttonPin5, INPUT);
  pinMode(buttonPin6, INPUT);
  pinMode(buttonPin7, INPUT);
  
  pinMode(LED, OUTPUT);
  pinMode(LED1, OUTPUT);
  pinMode(PIN_TO_SENSOR, INPUT);
}

void loop() {
  unsigned long currentMillis = millis();
  
  // Check button states
  readAndActOnButton(buttonPin1, '1');
  readAndActOnButton(buttonPin2, '2');
  readAndActOnButton(buttonPin3, '3');
  readAndActOnButton(buttonPin4, '4');
  readAndActOnButton(buttonPin5, '5');
  readAndActOnButton(buttonPin6, '6');
  readAndActOnButton(buttonPin7, '7');

  // Non-blocking motion sensor check, with cooldown
  if (!motionSensorCooldown) {
    // Check sensor state changes without interrupting the loop
    pinStatePrevious = pinStateCurrent;
    pinStateCurrent = digitalRead(PIN_TO_SENSOR);

    if (pinStatePrevious == LOW && pinStateCurrent == HIGH) {
      // Motion detected
      Serial.write('9');
      flashLEDs(); // Function to flash LEDs
      motionSensorTriggeredMillis = currentMillis;
      motionSensorCooldown = true;
    }
  } else if (currentMillis - motionSensorTriggeredMillis >= motionSensorDelay) {
    // Cooldown period has passed
    motionSensorCooldown = false;
  }

  // Continue with other loop code...
}

void flashLEDs() {
  // Function to flash LEDs without using delay()
  for (int i = 0; i <= 17; i++) {
    digitalWrite(LED, HIGH);
    digitalWrite(LED1, HIGH);
    delay(150);
    digitalWrite(LED, LOW);
    digitalWrite(LED1, LOW);
    delay(150);
  }
}

void readAndActOnButton(int buttonPin, char signal) {
  if (digitalRead(buttonPin) == HIGH) {
    digitalWrite(ledPin, HIGH);
    Serial.write(signal); // Send button ID
    delay(100);
    digitalWrite(ledPin, LOW);
    delay(100);
  }
}
