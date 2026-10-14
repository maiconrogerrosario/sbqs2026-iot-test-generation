//Código gerado para: DS18B20

#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2 // Pino onde o DS18B20 está conectado

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600);
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures(); // Solicita a temperatura
  float temperatureC = sensors.getTempCByIndex(0); // Obtém a temperatura em Celsius

  Serial.print("Temperatura: ");
  Serial.print(temperatureC);
  Serial.println(" °C");

  // Casos de teste
  if (temperatureC < -55 || temperatureC > 125) {
    Serial.println("Erro: Temperatura fora do intervalo esperado.");
  } else {
    Serial.println("Teste de temperatura bem-sucedido.");
  }

  delay(2000); // Aguarda 2 segundos antes da próxima leitura
}
