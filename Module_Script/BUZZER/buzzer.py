import RPi.GPIO as GPIO
from time import *

<<<<<<< HEAD
pin = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
=======
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
>>>>>>> fbbdebdbe6046001078a5d4fd3c2100fb6b9dd08

p = GPIO.PWM(pin, 300)

while True:
	GPIO.output(pin, True)
	p.start(0)
>>>>>>> 9736f085fddd37672d90009b1caa9922289c5418
	p.ChangeDutyCycle(100)
	p.ChangeFrequency(100)
	sleep(0.5)
	p.stop()

<<<<<<< HEAD
	GPIO.output(pin, False)
=======
<<<<<<< HEAD
	GPIO.output(pin, False)
=======
	GPIO.output(13, False)
>>>>>>> 9736f085fddd37672d90009b1caa9922289c5418
>>>>>>> fbbdebdbe6046001078a5d4fd3c2100fb6b9dd08
	sleep(2)

GPIO.cleanup()
