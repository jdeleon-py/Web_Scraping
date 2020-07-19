from bs4 import BeautifulSoup
import requests
import os

if __name__ == '__main__':
	arr = []

	with open('/Users/jamesdeleon/Documents/Programs/HTML_Programs/pokemon_chart.html') as html_file:
		soup = BeautifulSoup(html_file, 'lxml')

	for article in soup.find_all('img'):
		arr.append(article['src'])

	# >>> [http://img4.wikia.nocookie.net/__cb20140328190757/pokemon/images/thumb/2/21/001Bulbasaur.png/200px-001Bulbasaur.png,
	# >>> http://img4.wikia.nocookie.net/__cb20140724195345/pokemon/images/thumb/7/73/004Charmander.png/200px-004Charmander.png,
	# >>> http://img1.wikia.nocookie.net/__cb20140328191525/pokemon/images/thumb/3/39/007Squirtle.png/200px-007Squirtle.png]

	for i in range(3):
		os.system('open ' + arr[i])

	# opens all images on a web browser!

