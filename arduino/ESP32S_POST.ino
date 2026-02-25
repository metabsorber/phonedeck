//https://arduino.esp8266.com/stable/package_esp8266com_index.json
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#define station_id "0001"
#define WIFI_SSID "RT-WiFi-EB4F"
#define WIFI_PASSWORD "2803003762"
//String serverName = "http://jsonplaceholder.typicode.com/posts";
String serverName = "http://89.110.121.226:5000/save";
WiFiClient client;
HTTPClient http;
int httpCode = 0;
String payload = "";
String Data_Send = "";
JsonDocument doc;
void setup(){
  Serial.begin(115200);   
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while((WiFi.status() != WL_CONNECTED))
    delay(100);
  
  delay(1000);
  doc["name"] = "Силяков";
  doc["model"] = "TCL";
  doc["charge"] = "87";
  doc["connection_time"] = "15:16";
  doc["disconnection_time"] = "15:21";
  serializeJson(doc, Data_Send);
  Serial.println(serverName);
  serializeJson(doc, Serial);
  Serial.println();
  delay(1000);
  http.begin(client, serverName);
  http.addHeader("Content-Type", "application/json; charset=UTF-8");
  httpCode = http.POST(Data_Send);
  payload = http.getString();
  http.end();
  Serial.println(payload);
  Serial.println(httpCode);
  payload = "";
  httpCode = 0;
}
void loop(){     

}