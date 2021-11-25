#!/usr/bin/env	python3
from selenium import webdriver
# import webdriver to communicate with web browser

class getMeLocation:
	def __init__(self):
		# webbrowser driver
		self.driver = None
		# address of place 
		self.address = None

	def getwebbrowser(self):
		options = webdriver.ChromeOptions()
		options.add_argument("--headless")
		self.driver = webdriver.Chrome(options=options)
		self.driver.get("https://www.gps-coordinates.net/")		# from which website we have to scrap data
		self.driver.execute_script("window.scrollBy(0,1700)")

	def setAddress(self, address):
		self.address = address		# set the address from where we have to get latitude and longitude
		self.driver.execute_script(f"document.getElementById('address').value = '{self.address}'")		# set city name 
		self.driver.execute_script("document.getElementsByClassName('btn btn-primary')[0].click()")		# click the Get GPS coordinate button

	def fetchLatitude(self):
		return self.driver.execute_script("return document.getElementById('latitude').value")		# to return latitude from javascript

	def fetchLongitude(self):
		return self.driver.execute_script("return document.getElementById('longitude').value")		# to return longitude from javascript


	def close(self):
		# close driver
		self.driver.close()
