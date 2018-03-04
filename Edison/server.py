#!/usr/bin/env python
import socket
import json
import math
import pyupm_i2clcd as lcd
import mraa


def calculateCelcius(tmpVal):
    bVal = 3975

    resistanceVal = (1023-tmpVal) * 10000 / tmpVal

    celciusVal = 1 / (math.log(resistanceVal/10000) / bVal + 1 / 298.15) - 273.15

    return celciusVal

def getSensorData():

    tmp = mraa.Aio(2)
    total = 0.0
    for i in range(0,5):
        total = total + calculateCelcius(float(tmp.read()))

    celciusVal = total / 5
    
    sound = mraa.Aio(0)
    soundVal = int(sound.read())

    light = mraa.Aio(3)
    lightVal = int(light.read())

    dic = {'Temperature': celciusVal, 'Sound': soundVal, 'Light': lightVal}
    return json.dumps(dic)

def changeLedState(status):
    ledPin = mraa.Gpio(4)
    ledPin.dir(mraa.DIR_OUT)
    ledPin.write(status)

def changeLcdText(text):
    lcdDisplay.setCursor(0, 0)
    lcdDisplay.setColor(0, 127 , 127)
    lcdDisplay.write(str(text))

def buzz():
    buz = mraa.Gpio(8)
    buz.dir(mraa.DIR_OUT)
    buz.write(1)

def stopbuzz():
    buz = mraa.Gpio(8)
    buz.dir(mraa.DIR_OUT)
    buz.write(0)

lcdDisplay = lcd.Jhd1313m1(0, 0x3E, 0x62)
address = ('192.168.0.31', 55555)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(1)
server_socket.setblocking(0)
server_socket.settimeout(100000)

print 'starting p on %s port %s' % address

while True:
    try:
        connection, client_address = server_socket.accept()
        print 'connection from', client_address
        if connection:
            connection.settimeout(3)
            while True:
                data = connection.recv(1024)
                args = json.loads(data)
                command = args['command']

                if command == 'SENSORS':
                    print 'sensors'
                    data = getSensorData()
                    connection.send(json.dumps({'size': len(data) }))
                    connection.sendall(data)

                if command == 'LED':
                    print 'led'
                    status = args['status']
                    changeLedState(status)

                if command == 'LCD':
                    print 'lcd'
                    text = args['text']
                    changeLcdText(text)

                if command == 'BUZZER':
                    print 'buzzer'
                    duration = args['duration']
                    buzz()
                    time.sleep(0.2)
                    stopbuzz()

    except Exception as e:
        continue
    finally:
        pass

