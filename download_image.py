import bs4
import requests
import datetime
def a_image_download():
	response = requests.get("https://www.brainyquote.com/quote_of_the_day.html")


	soup = bs4.BeautifulSoup(response.text, 'lxml')

	quote = soup.find('img',{"class":"p-qotd"})

	image_url = "https://www.brainyquote.com/"+ quote['data-img-url']


	response_of_image = requests.get(image_url)

	image_name = "quote_of_day "+ str(datetime.datetime.now().date()) +".jpg" 

	with open(image_name,'wb') as f:
		f.write(response_of_image.content)
