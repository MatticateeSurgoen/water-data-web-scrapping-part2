#!/usr/bin/env	python3

import json			# for parsing json data
import sys	# for arguments
import time
from selenium import webdriver				# import webdriver to communicate with web browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re									# extract data with regular expression selection
from bs4 import BeautifulSoup				# to extract data with help of css selector
import csv									# to write csv file and do operation related to it.
import numpy as np							# to fastup process of array manipulation
import requests

# page hidden inside of site
secrete_page = None

# to search location
location_searcher = None

#TODO:
"""
searching method is very slow so
requirment is to make it fast by using
threads and requests module of python3
rather than selanium

f"https://api.opencagedata.com/geocode/v1/json?q={query_location}&key=03c48dae07364cabb7f121d8c1519492"

where replace query_location with name of city the last one is key
that extracted by analysing code of site.

"""
class getLocationSpeedily:
	def __init__(self):
		latitude = None
		longitude = None

	def parseAddressInMap(self, address):
		ret = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={address}&key=03c48dae07364cabb7f121d8c1519492")
		data = json.loads(ret.text)

		try:
			lat_lng_dict = data["results"][0]["geometry"]

			self.latitude = str(lat_lng_dict["lat"])
			self.longitude = str(lat_lng_dict["lng"])

		# index error is caused when there is
		# json data doesn't able to handle our query
		except IndexError:
			self.latitude = None
			self.longitude = None

	def fetchLatitude(self):
		return self.latitude

	def fetchLongitude(self):
		return self.longitude


"""
class getMeLocation: for searching location
getwebbrowser method:
	will create a chrome browser
	defines a driver for other methods
	to interact with it

setAddress method:
	will the address location of given place by
	using class driver from a website 
	that is been used as back end of 
	to find location from google maps

fetchLatitude method:
	gets latitude of the location by accessing
	document object model of javascript

fetchLongitutde method:
	gets longitude of the location by accessing
	document object model of javascript
"""

class getMeLocation:
	def __init__(self):
		# webbrowser driver
		self.driver = None
		# address of place 
		self.address = None

	def getwebbrowser(self, mode = None):
		options = webdriver.ChromeOptions()
		if mode:
			options.add_argument("--headless")
		self.driver = webdriver.Chrome(options=options)
		self.driver.get("https://www.gps-coordinates.net/")		# from which website we have to scrap data
		self.driver.execute_script("window.scrollBy(0,1700)")

	def setAddress(self, address):
		self.address = address		# set the address from where we have to get latitude and longitude
		self.driver.execute_script(f"document.getElementById('address').value = '{self.address}'")		# set city name 
		self.driver.execute_script("document.getElementsByClassName('btn btn-primary')[0].click()")		# click the Get GPS coordinate button

	def fetchLatitude(self):
		# to return latitude from javascript
		return self.driver.execute_script("return document.getElementById('latitude').value")

	def fetchLongitude(self):
		return self.driver.execute_script("return document.getElementById('longitude').value")

	def close(self):
		# close driver
		self.driver.close()


"""
SecretePage refers to page in side states when 
we click the link it will load other location

show_Contaminants_separately method:
	- clicks the button show contaminants separately
	by using CSS selectors

pages_before_entry method:
	- selects states where to go one by one

sanity_check method:
	- will prevent race condition by check whether
	 page is loaded or not if not try again after
	 some time.

clean_up method:
	- will clean up html and extract table data from it
	to store in output.csv

next_page method:
	will load next page inside secretepage
close method:
	will close the driver 
	and also close the output.csv 
"""


# secrete page 
class SecretePage:
	def __init__(self, driver):
		self.driver = driver
		self.file = open("output.csv", 'w', newline='')
		self.csvfile = csv.writer(self.file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		self.wait = WebDriverWait(self.driver, 100)

	# checked contaminants and clicks show
	def show_Contaminants_separately(self):
		self.driver.execute_script("document.getElementById('ContentPlaceHolder_chkAll').checked = true;" +
							"document.getElementById('ContentPlaceHolder_btnGO').click();")
		self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 
					"table.SNewFontReportTable th:nth-of-type(33)")))	
												# wait till 33 table data is loaded

	# pages before entry
	def pages_before_entry(self):
		time.sleep(4)
		length = int(self.driver.execute_script("return document.getElementById('tableReportTable').children[1].childElementCount;"))

		for out in range(length - 1):
			string_data = "ContentPlaceHolder_rpt_lnkSamples_" + str(out)
			self.wait.until(
				 EC.element_to_be_clickable((By.ID, string_data)))
			self.driver.execute_script(f"document.getElementById('{string_data}').click()")
			self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ContentPlaceHolder_chkAll")))
			self.show_Contaminants_separately()
			self.next_page()
 
	# check for clicked element is fully loaded 
	def sanity_check(self, data):
		while (True):
			color = self.driver.execute_script(f"return document.getElementById('ContentPlaceHolder_repIndex_lnkPages_{data}').style.color")
			if color != "red":
				time.sleep(2)
				continue
			break
		
	# cleaning up data for storing in csv format
	def clean_up(self):
		output = ''
		soup = BeautifulSoup(self.driver.page_source, 'html.parser')

		for data in soup.select('table.SNewFontReportTable tr td'):
			output += re.sub(' {2,}', '', BeautifulSoup.get_text(data)) + '|'
									# removes 2 or more space from data
		output = np.array(output[:-1].split('|'))
		output = output.reshape(len(output) // 33, 33)[:, 1:]

		# array to store latitude and longitude of cities
		new_array = []
		for searching_input in output:
			print(searching_input[4])

			# the site is causing error when some particular 
			# location is not found so in order to make
			# chrome browser alive this try and except is there.
			try:
				location_searcher.setAddress(re.sub('\(.*\)', '', searching_input[4]))
				"""
				removes (rv) from column fourth state name
				for example: "Gandhinagar (rv)" it will return "Gandhinagar " only
				"""
				# wait for site to output result
				time.sleep(1)
				new_array.append(np.r_[searching_input, np.array(["{} : {}".format(searching_input[4], location_searcher.fetchLatitude())]) , 
					np.array(["{} : {}".format(searching_input[4], location_searcher.fetchLongitude())])])
			except:
				new_array.append(np.r_[searching_input, np.array(["{} : ".format(searching_input[4])]), 
					np.array(["{}: ".format(searching_input[4])])])

		return new_array




	# writes output into csvfile and traverse through number of page in secretepage
	def next_page(self):
		self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 
								"table.SNewFontReportTable th:nth-of-type(33)"))) # wait until table have 33 th
		length = int(self.driver.execute_script("return document.getElementsByClassName('lnkPages').length"))

		self.csvfile.writerows(self.clean_up())

		for data in range(1, length):
			self.driver.execute_script(f"document.getElementById('ContentPlaceHolder_repIndex_lnkPages_{data}').click()")
			self.sanity_check(data)
			self.csvfile.writerows(self.clean_up())

		self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
							 "table.SNewFontReportTable th:nth-of-type(33)")))				
														# wait till 33 table data is loaded
		self.driver.back()
		self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 
							"table.OuterReportTable")))	# wait till table.OuterReportTable loaded

	# close file before exit
	def close(self):
		self.driver.close()
		self.file.close()



# Get webbrowser with options
def get_webbrowser(mode = None):
	url = "https://ejalshakti.gov.in/IMISReports/Reports/WaterQuality/rpt_WQM_SampleTesting_S.aspx?Rep=0&RP=Y"
	options = webdriver.ChromeOptions()
	options.add_argument('--incognito')
	#options.add_argument('--proxy-server="socks5://127.0.0.1:8080"')		# for proxy options
	if mode:
		options.add_argument('--headless')		# to start in command line interface
	driver = webdriver.Chrome(options=options)
	driver.get(url)
	return driver


# get total number of element with given id
def get_length_from_id(driver, id_d):
	try:
		length = int(driver.execute_script("return document.getElementById('" + id_d + "').length"))
	except:
		driver.back()
		length = int(driver.execute_script("return document.getElementById('" + id_d + "').length"))
	return length

# selects elements by id and click it.
def get_data(id_d, id_num):
	return "document.getElementById('" + id_d  + "').selectedIndex = " + str(id_num) + ';' + "document.getElementById('ContentPlaceHolder_btnGO').click();" 
# clicks tested samples by id
def get_tested_samples_by_id(id_num):
	return f"document.getElementById('ContentPlaceHolder_rpt_lnkSamples_{id_num}').click()"





# parsing state by id
def get_state_district(driver):
	return parser(driver, "ContentPlaceHolder_ddState")

"""
parser:
gets arguments from command line 
and no argument supplied or some
string is supplied then uses default
arguments that is 1, total number
of pages
"""
# parser parses through data 

def parser(driver, id_d):
	global secrete_page
	argv1 = None
	argv2 = None

	length = get_length_from_id(driver, id_d)

	## argument parsing 
	#if len(sys.argv) < 2:

	argv1 = 1
	argv2 = length

	#else:
	#	try:
	#		if len(sys.argv) == 2:
	#			argv1 = int(sys.argv[1])
	#			argv2 = length
	#		elif len(sys.argv) >= 3:
	#			argv1 = int(sys.argv[1])
	#			argv2 = int(sys.argv[2])
	#	except ValueError:
	#		pass

	# loop through states
	for data in range(argv1, argv2):
		driver.execute_script(get_data(id_d, data))
		secrete_page.pages_before_entry()
		time.sleep(4)
	

def main():
	try:
		mode = False
		for i in range(1, len(sys.argv)):
			if sys.argv[i] == "--headless":
				mode = True

		# get webdriver
		driver = get_webbrowser(mode)
		global secrete_page, location_searcher
		secrete_page = SecretePage(driver)

		# create a location_searcher 
		location_searcher = getMeLocation()

		# start web browser for searcher window
		location_searcher.getwebbrowser(mode)

		# traverse through whole options
		get_state_district(driver)

		# close driver and csv file
		location_searcher.close() 
		secrete_page.close()

	# closes opened file
	finally:
		# close everything before closing
		location_searcher.close() 
		secrete_page.file.close()
		

if __name__ == '__main__':
	main()
