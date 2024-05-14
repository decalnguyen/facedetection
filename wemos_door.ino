Code wemos : 

#include <WiFiClient.h> 

#include <PubSubClient.h> 

#include <ESP8266WiFi.h> 

#include <Servo.h>

  

  

#define WIFI_SSID "your_wifi_ssid" 

#define WIFI_PASSWORD "your_wifi_password" 

  

#define MQTT_SERVER "192.168.120.88" 

#define MQTT_PORT 1883 

#define MQTT_USER "mmtt21-2" 

#define MQTT_PASS "mmtt212ttmm" 

  

#define TOPIC_SUBSCRIBE "door/received" 

#define TOPIC_PUBLISH "door/status" 

#define servo D2 


const char* user = "mmtt21-2"; 

const char* pass = "mmtt212ttmm"; 

const char* ssid = "UiTiOt-E3.1" ; 

const char* password = "UiTiOtAP" ; 

Servo myServo;


WiFiClient espClient; 

PubSubClient client(espClient); 



void setup() { 

  

  Serial.begin(115200); 

  WiFi.begin(ssid, password); 

  

  while (WiFi.status() != WL_CONNECTED) { 

   // reconnect(); 

    delay(500); 

    Serial.println("Not yet connect"); 

  } 

  Serial.println("WiFi connected"); 

  

  client.setServer(MQTT_SERVER, MQTT_PORT); 

  client.setCallback(processMess); 

  

  client.subscribe(TOPIC_SUBSCRIBE); 

  Serial.println("MQTT Success"); 

  myServo.attach(servo);

  
} 

void processMess(char* topic, byte* payload, unsigned int length) { 

  

  Serial.print("Message arrived: "); 

  Serial.println(topic); 

  Serial.println("Message: "); 

  String message; 

  for (int i=0; i<length; i++) { 

    message += char(payload[i]); 

  } 
  Serial.println(message); 
  if (message == "OPEN") { 
    Serial.println("OPEN"); 
    myServo.write(90);
    delay(5000);
    myServo.write(0);
    } 
  

} 

  

void reconnect() { 

  while (!client.connected()) { 

    Serial.println("Connecting "); 

    if (client.connect("WemosD1", user, pass)) { 

      Serial.println("connected"); 

      client.subscribe(TOPIC_SUBSCRIBE); 

    } else { 

      Serial.println("Connect failed. "); 

      Serial.println(client.state()); 

      Serial.println("Again. "); 

      delay(5000); 

    } 

  } 

} 

void loop() { 

  if (client.connected() == false) { 

    reconnect(); 

  } 

// Serial.println("Okay"); 

  client.loop(); 
  if (myServo.read() == 0 ) client.publish(TOPIC_PUBLISH, "CLOSE")
  else
      lient.publish(TOPIC_PUBLISH, "OPEN")

  delay(2000); 

} 