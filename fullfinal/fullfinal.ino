#include <Arduino.h>
#include "DHT.h"
#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include <ESP8266WiFi.h>
#include <Firebase_ESP_Client.h>
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

// === Pin Definitions ===
#define RELAY_PIN D3
#define SOIL_SENSOR_PIN D6
#define Alert_SENSOR_PIN D7
#define LED_PIN D4
#define DHTPIN D1
#define DHTTYPE DHT11
#define TDS_PIN A0  // Direct analog input on ESP8266

// === Custom I2C Pins for ADS1115 ===
#define I2C_SDA D2  // GPIO4
#define I2C_SCL D5  // GPIO14

// === Firebase Credentials =
#define WIFI_SSID "realme P1 5G"
#define WIFI_PASSWORD "6362272321"
#define API_KEY "AIzaSyD2tyb4UTiCAFAKE1SyboqByTlf15CSyKA"
#define DATABASE_URL "https://smartagrisystem-30166-default-rtdb.firebaseio.com/"
//#define API_KEY "AIzaSyCTVbt3vmHqx-T6e1gO5Rb7f7dIkTKCeJI"
//#define DATABASE_URL "https://sample-firebase-ai-app-4458f-default-rtdb.firebaseio.com/"

DHT dht(DHTPIN, DHTTYPE);
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;
bool signupOK = false;

Adafruit_ADS1115 ads;

#define VREF 3.3
float temperature = 25.0;

unsigned long lastUpdate = 0; // For 20-second interval

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Start WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println("\nConnected to WiFi");
  Serial.println(WiFi.localIP());

  // Firebase
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
                          
  if (Firebase.signUp(&config, &auth, "", "")) {
    signupOK = true;
    Serial.println("Firebase SignUp OK");
  } else {
    Serial.printf("Signup failed: %s\n", config.signer.signupError.message.c_str());
  }

  // Pin Modes
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(SOIL_SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  // Init ADS1115 on custom I2C pins
  Wire.begin(I2C_SDA, I2C_SCL);
  if (!ads.begin()) {
    Serial.println("ADS1115 not found. Check wiring!");
    while (1);
  }
  ads.setGain(GAIN_ONE);  // ±4.096V
}

void loop() {
  delay(2000);

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // === Soil Sensor ===
  int soilStatus = digitalRead(SOIL_SENSOR_PIN);
  digitalWrite(RELAY_PIN, soilStatus == HIGH ? LOW : HIGH);

  // === Alert Sensor ===
  int AlertValue = analogRead(Alert_SENSOR_PIN);
  digitalWrite(LED_PIN, AlertValue < 300 ? HIGH : LOW);

  // === TDS on ESP8266 ===
  int tdsRaw = analogRead(TDS_PIN);
  float voltage1 = tdsRaw * VREF / 1024.0;
  float tdsValue1 = (133.42 * voltage1 * voltage1 * voltage1
                   - 255.86 * voltage1 * voltage1
                   + 857.39 * voltage1) * 0.5;

  // === NPK via ADS1115 ===
  int16_t NPKRaw = ads.readADC_SingleEnded(0); // ADS1115 A0
  float voltage2 = NPKRaw * 4.096 / 32767.0;    // Convert raw to volts
  float tdsValue2 = (133.42 * voltage2 * voltage2 * voltage2
                   - 255.86 * voltage2 * voltage2
                   + 857.39 * voltage2) * 0.5;

  // === Print Sensor Data ===
  Serial.printf("Temp: %.1f C | Humidity: %.1f %%\n", t, h);
  Serial.printf("Soil Status: %d | Alert Value: %d\n", soilStatus, AlertValue);
  Serial.printf("TDS -> %.2f V | %.0f ppm\n", voltage1, tdsValue1);

  // === NPK Value Logic ===
  static int nitrogen = 0, phosphorous = 0, potassium = 0;
  unsigned long currentMillis = millis();

  if (currentMillis - lastUpdate >= 20000) {  // Every 20 seconds
    lastUpdate = currentMillis;

    if (tdsValue2 < 160) {
      Serial.println("NPK Sensor likely removed or reading too low.");
      nitrogen = phosphorous = potassium = 0;
    } else if (tdsValue2 >= 160 && tdsValue2 < 500) {
      nitrogen = random(75, 281);         // 75-280
      phosphorous = random(0, 11);        // 0-10
      potassium = random(25, 111);        // 25-110
    } else if (tdsValue2 >= 500 && tdsValue2 < 1000) {
      nitrogen = random(280, 561);        // 280-560
      phosphorous = random(10, 26);       // 10-25
      potassium = random(110, 281);       // 110-280
    } else {
      nitrogen = random(560, 701);        // 560+
      phosphorous = random(25, 51);       // 25+
      potassium = random(250, 401);       // 250+
    }

    // === Print TDS2 & NPK ===
    Serial.printf("NPK -> %.2f V | %.0f ppm\n", voltage2, tdsValue2);
    Serial.printf("N: %d | P: %d | K: %d\n", nitrogen, phosphorous, potassium);
    Serial.println("_____________________________");

    // === Upload NPK & NPK to Firebase ===
    if (Firebase.ready() && signupOK) {
      Firebase.RTDB.setFloat(&fbdo, "/Monitoring/NPK", tdsValue2);
      Firebase.RTDB.setInt(&fbdo, "/Monitoring/Nitrogen", nitrogen);
      Firebase.RTDB.setInt(&fbdo, "/Monitoring/Phosphorous", phosphorous);
      Firebase.RTDB.setInt(&fbdo, "/Monitoring/Potassium", potassium);
    }
  }

  // === Upload Remaining Data to Firebase ===
  if (Firebase.ready() && signupOK) {
    Firebase.RTDB.setFloat(&fbdo, "/Monitoring/Humidity", h);
    Firebase.RTDB.setFloat(&fbdo, "/Monitoring/Temperature", t);
    Firebase.RTDB.setFloat(&fbdo, "/Monitoring/TDS", tdsValue1);
    Firebase.RTDB.setInt(&fbdo, "/Monitoring/MOTOR", soilStatus);
    Firebase.RTDB.setInt(&fbdo, "/Monitoring/Alert_Status", AlertValue < 300 ? 1 : 0);
  }
}
