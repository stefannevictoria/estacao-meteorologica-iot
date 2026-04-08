void setup() {
  Serial.begin(9600);
}

void loop() {
  // TEMPERATURA (TMP36 - A0)
  int leituraTemp = analogRead(A0);
  float tensao = leituraTemp * (5.0 / 1023.0);
  float temperatura = (tensao - 0.5) * 100;

  // UMIDADE (sensor solo - A1)
  int leituraUmidade = analogRead(A1);
  float umidade = map(leituraUmidade, 0, 1023, 0, 100);

  // POTENCIÔMETRO (A5)
  int leituraPot = analogRead(A5);
  float pressao = map(leituraPot, 0, 1023, 980, 1050); // simula pressão

  // ENVIO JSON
  Serial.print("{");
  Serial.print("\"temperatura\":"); Serial.print(temperatura, 1);
  Serial.print(",\"umidade\":"); Serial.print(umidade, 1);
  Serial.print(",\"pressao\":"); Serial.print(pressao, 1);
  Serial.println("}");

  delay(5000);
}