#include "ESP8266WiFi.h"

const char *ssid = "SSID";
const char *password = "PASSWORD";

int led_current_status = 0;

WiFiServer wifiServer(80);

void setup()
{

  Serial.begin(115200);

  delay(1000);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting..");
  }

  Serial.print("Connected to WiFi. IP:");
  Serial.println(WiFi.localIP());

  wifiServer.begin();
}

void loop()
{

  WiFiClient client = wifiServer.available();

  if (client)
  {

    while (client.connected())
    {

      while (client.available() > 0)
      {

        String line = client.readStringUntil('|');
        delay(10);

        if (line == "LED")
        {
          if (led_current_status == 0)
          { //0 means high and 1 means LOW
            digitalWrite(LED_BUILTIN, LOW);
            led_current_status = 1;
          }
          else if (led_current_status == 1)
          {
            digitalWrite(LED_BUILTIN, HIGH);
            led_current_status = 0;
          }
        }

        if (line.startsWith("CREATE-BLOCK "))
        {
          Serial.println("Creating block!");
          client.write(line.c_str());
        }

        Serial.println(line);
        line = "";
      }

      delay(10);
    }

    client.stop();
    Serial.println("Client disconnected");
  }
}
