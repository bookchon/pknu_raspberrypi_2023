# LED 깜빡이기
import RPi.GPIO as GPIO
import time

signal_pin = 18

# GPIO.setmode(GPIO.BOARD) # 1 ~ 40 번호를 쓰는 것  
GPIO.setmode(GPIO.BCM) # GPIO 18, GROUND
GPIO.setup(signal_pin, GPIO.OUT) # GPIO18핀에 출력 설정

while (True):
    GPIO.output(signal_pin, True) # GPIO 18핀에 전압 시그널 on
    time.sleep(2)
    GPIO.output(signal_pin, False)
    time.sleep(1) # 1초동안 불 끈 상태로 대기