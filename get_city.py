import socket
import requests

def get_city_name():
	try:
		socket.create_connection(("www.google.com",80))
		response = requests.get("https://ipinfo.io")
		data = response.json()
		city = data['city']
		return city
	except OSError:
		return "Check Internet Connection"
		
#if __name__ == "__main__":
#	print(get_city_name())	