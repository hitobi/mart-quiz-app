from microbit import *

while True:
    temperature = temperature()
    uart.write(str(temperature) + "\n")
    sleep(1000)  # 1초마다 데이터 전송