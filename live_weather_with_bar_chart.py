from get_weather import *
from matplotlib import pyplot as plt

cities = [i for i in input("Enter city names sepearted by spaces: ").split()]
temp = []
for city in cities:
	temp.append(getweather(city))
#weather_mumbai = getweather("Mumbai")
#weather_delhi = getweather("Delhi")
#weather_chennai = getweather("Chennai")

#cities = ["Mumbai", "Delhi", "Chennai"]
#temp = [weather_mumbai, weather_delhi, weather_chennai]
plt.bar(cities, temp, width=0.25, color=['r','g','b'])
plt.show()