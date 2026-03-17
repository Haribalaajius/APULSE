#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include "ACS712.h"
#include <Adafruit_MCP3008.h>

// ================= WiFi =================
const char* ssid = "Project";
const char* password = "12345678";

// ================= LCD =================
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ================= Sensors =================
ACS712 ACS(A0, 5.0, 1023, 100);     // ACS712 20A
Adafruit_MCP3008 adc;

// ================= Variables =================
double acVoltage = 0;
double frequency = 0;
int current_mA = 0;

// ================= AC Sampling =================
const int AC_OFFSET = 512;
const int SAMPLE_TIME = 1000;  // 1 second window

// ================= Relay =================
const int relayPin = D4;   // GPIO2 (ACTIVE LOW)

// ================= Web Server =================
ESP8266WebServer server(80);

// =================================================
// STATUS API
void handleStatus() {
  String response = "";
  response += "AC Voltage : " + String(acVoltage, 1) + " V\n";
  response += "Current    : " + String(current_mA) + " mA\n";
  response += "Frequency  : " + String(frequency, 1) + " Hz\n";

  server.send(200, "text/plain", response);
}

// RELAY ON
void handleRelayOn() {
  digitalWrite(relayPin, LOW);   // ON (active LOW)
  server.send(200, "text/plain", "Relay ON");
  Serial.println("Relay ON");
}

// RELAY OFF
void handleRelayOff() {
  digitalWrite(relayPin, HIGH);  // OFF
  server.send(200, "text/plain", "Relay OFF");
  Serial.println("Relay OFF");
}
// =================================================

void setup() {

  Serial.begin(9600);

  // ===== LCD =====
  Wire.begin(D2, D1);
  lcd.begin();
  lcd.backlight();

  // ===== WiFi =====
  WiFi.begin(ssid, password);
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  lcd.clear();
  lcd.print("WiFi Connected");
  delay(1000);

  Serial.println("\nWiFi Connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // ===== MCP3008 SPI =====
  adc.begin();   // default SPI pins

  // ===== ACS Calibration =====
  ACS.autoMidPoint();

  // ===== Relay =====
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);   // Relay OFF initially

  // ===== Server Routes =====
  server.on("/status", handleStatus);
  server.on("/1", handleRelayOn);
  server.on("/2", handleRelayOff);

  server.begin();
  Serial.println("Local Server Started");
}

void loop() {

  long sumSq = 0;
  int zeroCrossCount = 0;
  unsigned long startTime = millis();

  int lastSample = adc.readADC(0);

  while (millis() - startTime < SAMPLE_TIME) {

    int val = adc.readADC(0);

    int deviation = val - AC_OFFSET;
    sumSq += deviation * deviation;

    // Zero crossing detection
    if ((lastSample < AC_OFFSET && val >= AC_OFFSET) ||
        (lastSample > AC_OFFSET && val <= AC_OFFSET)) {
      zeroCrossCount++;
    }

    lastSample = val;
    delayMicroseconds(500);
  }

  // ================= RMS Voltage =================
  double rmsADC = sqrt(sumSq / 1000.0);
  acVoltage = (rmsADC / 512.0) * 230.0;

  if (acVoltage < 2.5)
    acVoltage = 0;
  else
    acVoltage = ((acVoltage - 0.5) * 100) / 8.25;

  acVoltage = acVoltage / 2;

  // ================= Frequency =================
  frequency = zeroCrossCount / 2.0;

  // ================= Current =================
  current_mA = ACS.mA_AC();

  if (current_mA < 200 || (current_mA > 800 && current_mA < 950))
    current_mA = 0;

  // ================= LCD =================
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("V:");
  lcd.print(acVoltage, 1);
  lcd.print(" I:");
  lcd.print(current_mA);

  lcd.setCursor(0, 1);
  lcd.print("F:");
  lcd.print(frequency, 1);
  lcd.print("Hz");

  // ================= Serial Monitor =================
  Serial.print("Voltage: ");
  Serial.print(acVoltage);
  Serial.print(" V  Current: ");
  Serial.print(current_mA);
  Serial.print(" mA  Frequency: ");
  Serial.print(frequency);
  Serial.println(" Hz");

  // ================= Web Server =================
  server.handleClient();
}
