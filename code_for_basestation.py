import lora # type: ignore

# LoRa модуль для приема
lora = lora.LoRa(spi_bus=1, freq=868e6, cs=5, reset=4)

# Прием данных
while True:
    packet = lora.receive()
    if packet:
        print("📡 Данные со спутника:", packet.decode())