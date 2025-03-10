from machine import Pin, I2C, ADC # type: ignore
import time
import lora  # type: ignore # Библиотека для LoRa
import bme680  # type: ignore # Датчик атмосферы
import dht  # type: ignore # Температура и влажность
import gps  # type: ignore # GPS модуль CAM-M8
import camera  # type: ignore # Камера IMX477

# Инициализация датчиков
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
bme = bme680.BME680(i2c=i2c)
dht22 = dht.DHT22(Pin(14))
gps_module = gps.GPS(Pin(17, Pin.IN), baudrate=9600)

# LoRa модуль
lora = lora.LoRa(spi_bus=1, freq=868e6, cs=Pin(5), reset=Pin(4))

# Функция сбора данных
def collect_data():
    # Датчики температуры, влажности, давления
    dht22.measure()
    temperature = dht22.temperature()
    humidity = dht22.humidity()
    pressure = bme.pressure
    co2 = bme.gas

    # Данные GPS
    latitude, longitude, altitude = gps_module.get_location()

    # Фото с камеры
    img = camera.capture()

    # Формирование пакета данных
    data = {
        "temp": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "co2": co2,
        "lat": latitude,
        "lon": longitude,
        "alt": altitude
    }

    return data, img

# Цикл работы спутника
while True:
    data, img = collect_data()
    print("📡 Отправка данных:", data)
    
    # Отправка по LoRa
    lora.send(str(data).encode())

    # Сохранение фото (передача по LoRa возможна только сжатого фото)
    with open("image.jpg", "wb") as f:
        f.write(img)

    time.sleep(60)  # Отправляем данные раз в минуту