#include "DHT.h"

#define DHTPIN  2
#define DHTTYPE DHT11   

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  Serial.println("{\"status\":\"iniciado\"}");
}

void loop() {
  // Aguarda leitura estabilizar
  delay(5000);

  float temp = dht.readTemperature();   // Celsius
  float umid = dht.readHumidity();

  // Verifica se a leitura é válida
  if (isnan(temp) || isnan(umid)) {
    Serial.println("{\"erro\":\"falha na leitura do sensor\"}");
    return;
  }

  // Envia JSON compacto (uma linha por leitura)
  Serial.print("{");
  Serial.print("\"temperatura\":"); Serial.print(temp, 1);
  Serial.print(",\"umidade\":");    Serial.print(umid, 1);
  Serial.print(",\"localizacao\":\"Lab\"");
  Serial.println("}");
}
