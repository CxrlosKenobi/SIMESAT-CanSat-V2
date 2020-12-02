import os
#Creando el requirements.txt
dir = os.system('pwd')
os.system(f'pipreqs {dir} --force')
os.system('clear')

'''
Módulo GY-91
- Acelerómetro
- Giroscopio
- Magnetómetro
- Presión
- Temperatura
'''


'''
GPS Ublox NEO-6M
- Latitud, Longitud, Velocidad, Altitud
'''
#Configurar desde Rasp con alguno de los siguientes:
    #https://github.com/FranzTscharf/Python-NEO-6M-GPS-Raspberry-Pi
    #https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/
#Chequear en internet para printear también la Velocidad y la Altitud.
import serial
import time
import string
import pynmea2

while True:
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata = ser.readline()

    if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        long = newmsg.longitude
        gps = "Lat: " + str(lat) + " Long: " + str(long)
        print(gps)
#Output:
#Lat: XX.XXXXXXX  Long: XX.XXXXXXX
#Lat: XX.XXXXXXX  Long: XX.XXXXXXX


'''
GY-213 HDC1080
- Humedad
- Temperatura
'''
#Configurar desde Rasp | Posibles enlaces con info:
    #https://github.com/switchdoclabs/SDL_Pi_HDC1000


'''
Placa STM32F103C8T
    - Temporizador.
    - Reloj integrado.
    - Conversor de senñal analógica a digial(viceversa)
'''


'''
Módulo LoRa RFM95W para 915MHz | Marca: HopeRF
    - Receptor y emisor de paquetes.
    -
'''
#https://pypi.org/project/raspi-lora/
#https://pypi.org/project/pyLoraRFM9x/


'''
Buzzer
    - Emite pitidos.
'''
