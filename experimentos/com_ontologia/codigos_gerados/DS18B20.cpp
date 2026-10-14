//Código gerado para: DS18B20


#include <OneWire.h>
#include <DallasTemperature.h>
#include <AUnit.h>

#define DATA_PIN 2

OneWire oneWire(DATA_PIN);
DallasTemperature sensors(&oneWire);

test(DS18B20_Initialization) {
    sensors.begin();
    assertTrue(sensors.getDeviceCount() > 0);
}

test(DS18B20_TemperatureRange) {
    sensors.requestTemperatures();
    float temperature = sensors.getTempCByIndex(0);
    assertTrue(temperature >= -55.0 && temperature <= 125.0);
}

test(DS18B20_ErrorValue) {
    // Simulate disconnection
    float temperature = sensors.getTempCByIndex(0);
    assertEqual(temperature, -127.0);
}

test(DS18B20_StableReading) {
    float previousTemperature = sensors.getTempCByIndex(0);
    delay(5000); // Wait for stable reading duration
    sensors.requestTemperatures();
    float currentTemperature = sensors.getTempCByIndex(0);
    assertNear(currentTemperature, previousTemperature, 0.5);
}

test(DS18B20_ResolutionCheck) {
    sensors.requestTemperatures();
    float temperature = sensors.getTempCByIndex(0);
    assertTrue(fmod(temperature, 0.0625) == 0);
}
