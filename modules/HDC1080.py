from modules import SDL_Pi_HDC1080
import sys
import os

class HDC:
	def __init__(self):
		sys.path.append('./modules/SDL_Pi_HDC1080_Python3')
		self.hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()

	def temp(self, decimal):
		temperature = round(self.hdc1080.readTemperature(), self.decimal)
		return temperature

	def hum(self, decimal):
		humidity = round(self.hdc1080.readHumidity(), self.decimal)
		return humidity
