import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BUZZER= 18
buzzState = False

GPIO.setup(BUZZER, GPIO.OUT)

tone1 = GPIO.PWM(BUZZER, 100)

tone1.start(50)



star_wars_melody = [
					notes['G4'], notes['G4'], notes['G4'],
					notes['EB4'], 0, notes['BB4'], notes['G4'],
					notes['EB4'], 0, notes['BB4'], notes['G4'], 0,

					notes['D4'], notes['D4'], notes['D4'],
					notes['EB4'], 0, notes['BB3'], notes['FS3'],
					notes['EB3'], 0, notes['BB3'], notes['G3'], 0,

					notes['G4'], 0, notes['G3'], notes['G3'], 0,
					notes['G4'], 0, notes['FS4'], notes['F4'],
					notes['E4'], notes['EB4'], notes['E4'], 0,
					notes['GS3'], notes['CS3'], 0,

					notes['C3'], notes['B3'], notes['BB3'], notes['A3'], notes['BB3'], 0,
					notes['EB3'], notes['FS3'], notes['EB3'], notes['FS3'],
					notes['BB3'], 0, notes['G3'], notes['BB3'], notes['D4'], 0,


					notes['G4'], 0, notes['G3'], notes['G3'], 0,
					notes['G4'], 0, notes['FS4'], notes['F4'],
					notes['E4'], notes['EB4'], notes['E4'], 0,
					notes['GS3'], notes['CS3'], 0,

					notes['C3'], notes['B3'], notes['BB3'], notes['A3'], notes['BB3'], 0,

					notes['EB3'], notes['FS3'], notes['EB3'],
					notes['BB3'], notes['G3'], notes['EB3'], 0, notes['BB3'], notes['G3'],
					]


star_wars_tempo = [
					2, 2, 2,
					4, 8, 6, 2,
					4, 8, 6, 2, 8,

					2, 2, 2,
					4, 8, 6, 2,
					4, 8, 6, 2, 8,

					2, 16, 4, 4, 8,
					2, 8, 4, 6,
					6, 4, 4, 8,
					4, 2, 8,
					4, 4, 6, 4, 2, 8,
					4, 2, 4, 4,
					2, 8, 4, 6, 2, 8,

					2, 16, 4, 4, 8,
					2, 8, 4, 6,
					6, 4, 4, 8,
					4, 2, 8,
					4, 4, 6, 4, 2, 8,
					4, 2, 2,
					4, 2, 4, 8, 4, 2,
					]

