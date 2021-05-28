import sys
import SDL_Pi_HDC1080
import os

class HDC:
	def __init__(self):
		sys.path.append('./SDL_Pi_HDC1080_Python3')
		self.hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

	def temp(self, decimal):
		temperature = round(hdc1080.readTemperature(), self.decimal)
		return temperature

	def hum(self, decimal):
		humidity = round(hdc1080.readHumidity(), self.decimal)
		return humidity
