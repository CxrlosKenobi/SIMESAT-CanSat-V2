import RPi.GPIO as GPIO
from time import *

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)

p = GPIO.PWM(13, 300)

while True:
	GPIO.output(13, True)
	p.start(0)
	p.ChangeDutyCycle(100)
	p.ChangeFrequency(400)
	sleep(0.5)
	p.stop()

	GPIO.output(13, False)
	sleep(2)

GPIO.cleanup()
