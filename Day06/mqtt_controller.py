# MQTT package install - paho-mqtt
# sudo pip install paho-mqtt
# 동시 publish(데이터 전송[출판]) / subscribe(데이터 수신)

from threading import Thread, Timer
import time # time.sleep()
import json
import datetime as dt

import paho.mqtt.client as mqtt
# DHT11 온습도 센서용 library
import Adafruit_DHT as dht
# GPIO
import RPi.GPIO as GPIO

# GPIO, DHT Settings
sensor = dht.DHT11
rcv_pin = 10
green = 22
servo_pin = 18

GPIO.setwarnings(False) # 오류메시지 제거

# green led init(초기화)
GPIO.setmode(GPIO.BCM)
GPIO.setup(green, GPIO.OUT)
GPIO.output(green, GPIO.HIGH) # = True

# servo init(초기화) settings
GPIO.setup(servo_pin, GPIO.OUT) #servo init
pwm = GPIO.PWM(servo_pin, 100) # servo motor 속도
pwm.start(3) # 각도(arcdegree)0 / DutyCycle 3 ~ 20

# Data Push Object
class publisher(Thread):
    def __init__(self):
        Thread.__init__(self) # 스레드 초기화
        self.host = '210.119.12.63'
        self.port = 1883 # 회사에서는 포트를 그대로 쓰지 않음
        self.clientId = 'IOT63'
        self.count = 0
        print('publisher Thread Start')
        self.client = mqtt.Client(client_id = 'IOT63')

    def run(self):
        self.client.connect(self.host, self.port)
        # self.client.username_pw_set() # id/pwd로 로그인 할 때 필요
        self.publish_data_auto()

    def publish_data_auto(self):
        humid, temp = dht.read_retry(sensor, rcv_pin)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 2023-06-14 10:39:24
        origin_data = {'DEV_ID': self.clientId,
                       'CURR_DT': curr,
                       'TYPE': 'TEMPHUMID',
                       'STAT': f'{temp}|{humid}' } # real data
        pub_data =json.dumps(origin_data) # #MQTT로 전송할 json데이터로 변환
        self.client.publish(topic = 'pknu/rpi/control/', payload = pub_data)
        print(f'Data published #{self.count}')
        self.count += 1
        Timer(2.0, self.publish_data_auto).start() # every 2sec publisher

# Data Pull Object
class subscriber(Thread): 
    def __init__(self): # 생성자
        Thread.__init__(self)
        self.host = '210.119.12.63' # Broker IP(Computer IP)
        self.port = 1883
        # self.host = 'https://bookchon.azure.com/iot/service'
        self.clientId = 'IOT63_SUB'
        self.topic = 'pknu/monitor/control/'
        print('subscriber Thread Start')
        self.client = mqtt.Client(client_id = self.clientId)

    def run(self): # Thread.start() 함수를 실행하면 실행되는 함수
        self.client.on_connect = self.onConnect # 접속 성공 신호 처리
        self.client.on_message = self.onMessage # 접속 후 메시지 수신 시 처리
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic = self.topic)
        self.client.loop_forever()

    def onConnect(self, mqttc, obj, flags, rc):
        print(f'subscriber connect rc > {rc}')
    
    def onMessage(self, mqttc, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        # print(f'{msg.topic} / {rcv_msg}')  
        data = json.loads(rcv_msg) # json data로 형변환
        stat = data['STAT']
        print(f'STAT: {stat}')
        if (stat == 'OPEN'):
            GPIO.output(green, GPIO.LOW)
            pwm.ChangeDutyCycle(12) # 90도
        elif (stat == 'CLOSE'):
            GPIO.output(green, GPIO.HIGH)
            pwm.ChangeDutyCycle(3) # 0도

        time.sleep(1.0) 

if __name__ == '__main__':
    thPub = publisher() # publisher object create
    thSub = subscriber() # subscriber object create
    thPub.start()
    thSub.start() # run() 자동실행