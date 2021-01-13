import RPi.GPIO as GPIO
from time import *

pin = 16

GPIO.setmode(GPIO.BOARD)
<<<<<<< HEAD
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, 300)
#GPIO.setwarings(False)

while True:
	GPIO.output(pin, True)
	p.start(100)
=======
GPIO.setup(13, GPIO.OUT)

p = GPIO.PWM(13, 300)

while True:
	GPIO.output(13, True)
	p.start(0)
>>>>>>> 9736f085fddd37672d90009b1caa9922289c5418
	p.ChangeDutyCycle(100)
	p.ChangeFrequency(100)
	sleep(0.5)
	p.stop()

<<<<<<< HEAD
	GPIO.output(pin, False)
=======
	GPIO.output(13, False)
>>>>>>> 9736f085fddd37672d90009b1caa9922289c5418
	sleep(2)

GPIO.cleanup()
