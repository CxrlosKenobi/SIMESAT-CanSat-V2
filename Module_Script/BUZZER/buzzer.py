import RPi.GPIO as GPIO
from time import *

pin = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, 300)

while True:
	GPIO.setwarnings(False)
	GPIO.output(pin, True)
	p.start(0)
	p.ChangeDutyCycle(100)
	p.ChangeFrequency(100)
	sleep(0.5)
	p.stop()

	GPIO.output(pin, False)
	sleep(2)

GPIO.cleanup()
