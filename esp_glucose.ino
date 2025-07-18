#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <WebSocketsServer.h>

const char* ssid = "sam";       
const char* password = "passtheword";  

AsyncWebServer server(80);
WebSocketsServer webSocket = WebSocketsServer(8765);

String glucoseValue = "Waiting for data...";

// Handle WebSocket messages
void onWebSocketEvent(uint8_t client_num, WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_TEXT) {
    glucoseValue = String((char*)payload);
    Serial.print("Glucose Received: ");
    Serial.println(glucoseValue);
    webSocket.broadcastTXT(glucoseValue);
  }
}

void setup() {
  Serial.begin(115200);

  
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected!");
  Serial.print(" IP Address: ");
  Serial.println(WiFi.localIP());

  // Serve HTML page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", R"rawliteral(
      <!DOCTYPE html>
      <html>
      <head>
        <title>Glucose Monitor</title>
        <style>
          body { font-family: Arial; text-align: center; padding-top: 50px; background: #f3f3f3; }
          h1 { color: #4CAF50; }
          #glucose { font-size: 40px; margin-top: 20px; }
          #warning { font-size: 24px; margin-top: 10px; font-weight: bold; }
        </style>
        <script>
          var ws = new WebSocket("ws://" + window.location.hostname + ":8765");

          ws.onmessage = function(event) {
            var glucose = parseFloat(event.data);
            document.getElementById("glucose").innerHTML = "Glucose Level: " + glucose + " mg/dL";

            var warningDiv = document.getElementById("warning");
            if (glucose > 180) {
              warningDiv.innerHTML = "Glucose rate too high!";
              warningDiv.style.color = "red";
            } else if (glucose >= 40 && glucose <= 60) {
              warningDiv.innerHTML = "Glucose rate too low!";
              warningDiv.style.color = "blue";
            } else {
              warningDiv.innerHTML = "";
            }
          };
        </script>
      </head>
      <body>
        <h1>Real-Time Glucose Monitor</h1>
        <div id="glucose">Waiting for data...</div>
        <div id="warning"></div>
      </body>
      </html>
    )rawliteral");
  });

  // Start WebSocket and HTTP server
  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);
  server.begin();
}

void loop() {
  webSocket.loop();
}
