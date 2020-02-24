import socket
import requests

def getweather(city):
	try:
		socket.create_connection(("www.google.com", 80))
		api_address = "http://api.openweathermap.org/data/2.5/weather?units=metric" + "&q=" + city + "&appid=f19960f53da88b1ceefc4852de4d1fdf"
		response = requests.get(api_address)
		wdata = requests.get(api_address).json()
		temp = wdata['main']['temp']
		return temp
	except OSError:
		print("Check network")
		return "No Internet"

#if __name__ == '__main__':
#	getweather(input("Enter City:"))