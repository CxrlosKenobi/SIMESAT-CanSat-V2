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
#import pepitocompa
# CodeExample

'''
GPS Ublox NEO-6M
- Latitud, Longitud, Velocidad, Altitud
'''
#Configurar desde Rasp con alguno de los siguientes:
    #https://github.com/FranzTscharf/Python-NEO-6M-GPS-Raspberry-Pi
    #https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/
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
        gps = "Lat: " + str(lat) + "Long: " + str(long)
        print(gps)


'''
GY-213 HDC1080
- Humedad
- Temperatura
'''

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

'''
Buzzer
    - Emite pitidos.
'''
