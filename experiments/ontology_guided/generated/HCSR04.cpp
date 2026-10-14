//Código gerado para: HCSR04

#include <NewPing.h>

#define TRIGGER_PIN  12  // Pino de Trigger do HCSR04
#define ECHO_PIN     11  // Pino de Echo do HCSR04
#define MAX_DISTANCE 200 // Distância máxima em cm

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
  Serial.begin(9600);
}

void loop() {
  delay(100); // Aguarda 100ms entre leituras
  unsigned int uS = sonar.ping(); // Envia o pulso e recebe o tempo de retorno
  float distance = uS / US_ROUNDTRIP_CM; // Converte o tempo em distância

  Serial.print("Distância: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Casos de teste
  if (distance < 10) {
    Serial.println("Teste: Objeto muito próximo.");
  } else if (distance >= 10 && distance < 50) {
    Serial.println("Teste: Objeto a uma distância média.");
  } else if (distance >= 50 && distance <= 200) {
    Serial.println("Teste: Objeto a uma distância longa.");
  } else {
    Serial.println("Teste: Fora do alcance.");
  }
}

  