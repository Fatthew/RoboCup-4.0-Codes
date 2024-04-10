#include <WiFi.h>
#include <WiFiClient.h>
#include <ESPAsyncWebServer.h>

//const char* ssid = "BELL603";
//const char* password = "AD744EAC157D";

const char* ssid = "Matts Phone";
const char* password = "MattsHotspot";

const int uartTxPin = 4; // TX pin on ESP32

AsyncWebServer server(80);

bool isSignalOn = true; // Variable to track the signal state




void serr() {
  Serial2.print("n/serr");
  Serial.println("Moving Servo Right!");
}


void serm() {
  Serial2.print("n/serm");
  Serial.println("Moving Servo Middle!");
}


void serl() {
  Serial2.print("n/serl");
  Serial.println("Moving Servo Left!");
}



void rigt() {
  Serial2.print("n/rigt");
  Serial.println("Spinning Right!");
}

void left() {
  Serial2.print("n/left");
  Serial.println("Spinning Left!");
}


void bkwd() {
  Serial2.print("n/bkwd");
  Serial.println("Going Backward!");
}



void frwd() {
  Serial2.print("n/frwd");
  Serial.println("Going Forward!");
}



void kick() {
  Serial2.print("n/kick");
  Serial.println("Kicked!");
}




void setup() {
  Serial.begin(9600);
  Serial2.begin(9600, SERIAL_8N1, 2, uartTxPin);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
    
  }
  Serial.print("Connected to WiFi - IP: ");
  Serial.println(WiFi.localIP());

  // HTTP server routes
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/html", "<html><body>"
      "<button onclick=\"sendData('n/frwd')\">Forward</button>"
      "<button onclick=\"sendData('n/bkwd')\">Backwards</button>"
      "<button onclick=\"sendData('n/left')\">Left</button>"
      "<button onclick=\"sendData('n/rigt')\">Right</button>"
      "<button onclick=\"sendData('n/stop')\">Stop</button>"
      "<button onclick=\"sendData('n/kick')\">Kick</button>"
      "<button onclick=\"sendData('n/circ')\">Circle</button>"
      "<button onclick=\"sendData('n/drbl')\">Dribble</button>"
      "<button onclick=\"sendData('n/serv')\">Servo</button>"
      "<button onclick=\"sendData('n/mlft')\">MoveLeft</button>"
      "<button onclick=\"sendData('n/mrgt')\">MoveRight</button>"
      "<button onclick=\"sendData('n/full')\">Full</button>"
      "<script>"
      "function sendData(value) {"
      "  fetch('/serial?data=' + value);"
      "}"
      "</script></body></html>");
  });

  // Add a new endpoint for sending data directly to Serial2
  server.on("/serial", HTTP_GET, [](AsyncWebServerRequest *request){
    if (request->hasParam("data")) {
      String data = request->getParam("data")->value();
      Serial2.print(data); // Send data directly to Serial2
    }
    request->send(200, "text/plain", "OK");
  });

  // Define HTTP endpoint for receiving kicks
  server.on("/kick", HTTP_GET, [](AsyncWebServerRequest *request) {
    // Handle the kick request here
    kick();
    request->send(200, "text/plain", "Kicked!");
  });

  server.begin();



  // Define HTTP endpoint for receiving kicks
  server.on("/frwd", HTTP_GET, [](AsyncWebServerRequest *request) {
    // Handle the kick request here
    frwd();
    request->send(200, "text/plain", "Going Forward!");
  });

  server.begin();


  // Define HTTP endpoint for receiving kicks
  server.on("/bkwd", HTTP_GET, [](AsyncWebServerRequest *request) {
    // Handle the kick request here
    bkwd();
    request->send(200, "text/plain", "Going Backward!");
  });

  server.begin();



  // Define HTTP endpoint for receiving kicks
  server.on("/left", HTTP_GET, [](AsyncWebServerRequest *request) {
    // Handle the kick request here
    left();
    request->send(200, "text/plain", "Spinning Left!");
  });

  server.begin();



  // Define HTTP endpoint for receiving kicks
  server.on("/rigt", HTTP_GET, [](AsyncWebServerRequest *request) {
    // Handle the kick request here
    rigt();
    request->send(200, "text/plain", "Spinning Right!");
  });

  server.begin();



  // Define HTTP endpoint for receiving kicks
  server.on("/serl", HTTP_GET, [](AsyncWebServerRequest *request) {
    // Handle the kick request here
    serl();
    request->send(200, "text/plain", "Moving Servo Left!");
  });

  server.begin();



  // Define HTTP endpoint for receiving kicks
  server.on("/serm", HTTP_GET, [](AsyncWebServerRequest *request) {
    // Handle the kick request here
    serm();
    request->send(200, "text/plain", "Moving Servo Middle!");
  });

  server.begin();



  // Define HTTP endpoint for receiving kicks
  server.on("/serr", HTTP_GET, [](AsyncWebServerRequest *request) {
    // Handle the kick request here
    serr();
    request->send(200, "text/plain", "Moving Servo Right!");
  });

  server.begin();
}


void loop() {
  // Handle other tasks in the loop
}