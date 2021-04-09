
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define DHTPIN 2  // пин данных датчика DHT11

OneWire oneWire(15); // вход датчиков 18B20, аналоговый А1, он же 15 цифровой
DallasTemperature ds(&oneWire);  //объект датчика Dallas 18B20
DHT dht(DHTPIN, DHT11);  // объект датчика DHT11
int analogPin = 0;
int val = 0;
char command;

void setup() {
  // все необходимые инициализации
  Serial.begin(9600);
  ds.begin();
  dht.begin();
}

void loop() {
  if (Serial.available() > 0) { // если есть данные в порту

    command = Serial.read();

    delay(100); // без задержки pycharm  не успевает среагировать

    if (command == 'r') {  // проверяем команду на чтение
    
      ds.requestTemperatures(); //Измеряем температуру
      Serial.print("Dallas-DS18B20(t°C): ");
      Serial.println(ds.getTempCByIndex(0));

      float h = dht.readHumidity(); //Измеряем влажность
      float t = dht.readTemperature(); //Измеряем температуру
      Serial.print("DHT11(h%): ");
      Serial.println(h);
      Serial.print("DHT11(t°C): ");
      Serial.println(t);

      val = analogRead(analogPin); // измеряем освещенность
      Serial.print("illumination: ");
      Serial.println(val);

      //Serial.println("END"); // конец передачи
    }
  }
}
