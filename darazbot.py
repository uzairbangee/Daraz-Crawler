import bs4 as bs
import csv
import urllib.request
import pymysql.cursors
from datetime import datetime


link = 'https://www.daraz.pk/'


header = {'User-Agent': 'Chrome/24.0.1312.27'}

def page_crawler(link):
	while True:
		req = urllib.request.Request(link, headers=header)
		resp = urllib.request.urlopen(req)
		soup = bs.BeautifulSoup(resp, 'lxml')
		for products in soup.find_all('a', class_='link'):
			producturl = products.get('href')
			print(producturl)
			daraz_crawling(producturl)

		for nexter in soup.find_all('link', rel='next'):
			link = nexter.get('href')
			print(link)
		if soup.find('link', rel='next') is None:
			break

def daraz_crawling(link):
	req = urllib.request.Request(link, headers=header)
	resp = urllib.request.urlopen(req)
	soup = bs.BeautifulSoup(resp, 'lxml')
	print(soup.title.string)
	for productname in soup.find_all('h1', class_="title"):
		product = productname.get_text().strip()
		print(product)
	for branding in soup.find_all('div', class_='sub-title'):
		brand = branding.get_text().strip()
		print(brand)
	for price in soup.find_all('span', dir='ltr'):
		productprice = price.get_text().strip()
		print(productprice)

def entering(link):
	req = urllib.request.Request(link, headers=header)
	resp = urllib.request.urlopen(req)
	soup = bs.BeautifulSoup(resp, 'lxml')
	for url in soup.find_all('a', class_='subcategory'):
		urls = url.get('href')
		print (urls)
		page_crawler(urls)

entering(link)

with open('index.csv', 'a') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow([product, brand, price, datetime.now()])
