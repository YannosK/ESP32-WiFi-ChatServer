#include <Arduino.h>
#include <WiFi.h>

void ConnectToWiFi(const char* WIFI_NETWORK, const char* WIFI_PASSWORD);
void ConnectToServer(IPAddress server);
void ClientRead(void);
void ReplyToClient(void);

int status = WL_IDLE_STATUS;

IPAddress server(192, 168, 1, 44);

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
WiFiClient client;

void setup() {
  Serial.begin(115200);

  char WiFi_ssid[32] = "HOME_EXT";
  char WiFi_pswd[32] = "123456789";

  ConnectToWiFi(WiFi_ssid, WiFi_pswd);

  ConnectToServer(server);
}


void loop() {

  while(client.connected()){
    
    while(!client.available())
    {
      ReplyToClient();    
    }
    ClientRead();    
    
  }

  Serial.println();
  Serial.println("disconnecting from server.");
  //client.stop();

  while(true)
  {}
}


void ConnectToWiFi(const char* WIFI_NETWORK, const char* WIFI_PASSWORD) {
  Serial.print("Connecting to WiFi");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_NETWORK, WIFI_PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(500);
  }

  if (WiFi.status() != WL_CONNECTED){
    Serial.println("Connection failed!");
  }
  else{
    Serial.print("\nConected to WiFi network with local IP address:");
    Serial.println(WiFi.localIP()); 
  }
}


void ConnectToServer(IPAddress server)
{
  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  client.connect(server, 80);

  //affirmation that we connected indeed
  if (client.connected()) {
    Serial.println("connected to server");
  }  
}


void ClientRead(void)
{
  // if there are incoming bytes available from the server, read them and print them:
    while(client.available()) {      
      char c = client.read();
      Serial.write(c);
    }
    Serial.println();
}


void ReplyToClient(void)
{
  Serial.print("\nMessage to client: ");
  while(!Serial.available()){
    //delay(1);
    if (client.available()) {break;}
  }
  while(Serial.available())
    {
      String msg_to_client = Serial.readString();
      client.print(msg_to_client);
      Serial.println(msg_to_client);
    }
}