# LED RGB 깜빡이기
import RPi.GPIO as GPIO
import time

red = 17
green = 27
blue = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.output(red, True)
GPIO.output(green, True)
GPIO.output(blue, True) # 초기화

try:
    while True:
        GPIO.output(red, False) # RED 켜짐
        GPIO.output(green, True)
        GPIO.output(blue, True)
        time.sleep(1)
        GPIO.output(red, True)
        GPIO.output(green, False) # GREEN 켜짐
        GPIO.output(blue, True)
        time.sleep(1)
        GPIO.output(red, True)
        GPIO.output(green, True)
        GPIO.output(blue, False) # BLUE 켜짐
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()