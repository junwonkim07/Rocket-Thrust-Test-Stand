#include "HX711.h"
// ===== Pin Configuration =====
#define BUTTON_PIN   2
#define BUZZER_PIN   8
#define RELAY_PIN    6        // Relay (igniter) pin
#define HX_DATA_PIN  5        // HX711 DT
#define HX_SCK_PIN   4        // HX711 SCK
HX711 scale;
// State variables
bool systemArmed = false;
unsigned long lastBeepTime = 0;
int countdown = 10;
// ===== SETUP =====
void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(RELAY_PIN, LOW);
  // Initialize HX711
  scale.begin(HX_DATA_PIN, HX_SCK_PIN);
  Serial.println("=== System Ready ===");
}
// ===== Warning Beep =====
void beep(int duration) {
  tone(BUZZER_PIN, 2000);
  delay(duration);
  noTone(BUZZER_PIN);
}
// ===== LOOP =====
void loop() {
  // Continuously output HX711 value to Serial Plotter
  if (scale.is_ready()) {
    long val = scale.read();
    Serial.println(val);   // ← For Serial Plotter
  }
  // Button detection
  if (digitalRead(BUTTON_PIN) == LOW && !systemArmed) {
    systemArmed = true;
    countdown = 10;
    Serial.println("=== Countdown Started ===");
    delay(500); // Debounce delay
  }
  // Countdown logic
  if (systemArmed) {
    unsigned long now = millis();
    if (now - lastBeepTime >= 1000) {
      lastBeepTime = now;
      // Beep
      beep(100);
      // Serial monitor output
      Serial.print("Count: ");
      Serial.println(countdown);
      countdown--;
      // Reached 0 → Activate igniter
      if (countdown < 0) {
        Serial.println("=== IGNITOR ACTIVATED ===");
        // Relay ON
        digitalWrite(RELAY_PIN, HIGH);
        // Long warning tone
        tone(BUZZER_PIN, 4000);
        delay(1000);
        noTone(BUZZER_PIN);
        // Reset
        systemArmed = false;
      }
    }
  }
}