#!/usr/bin/env	python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup
import csv
import numpy as np


class SecretePage:
	def __init__(self, driver):
		self.driver = driver

	# checked contaminants and clicks show
	def show_Contaminants_separately(self):
		self.driver.execute_script("document.getElementById('ContentPlaceHolder_chkAll').checked = true;" +
							"document.getElementById('ContentPlaceHolder_btnGO').click();")
	def pages(self):
		length = int(self.driver.execute_script("return document.getElementById('tableReportTable').children[1].childElementCount;"))
		# self.driver.execute_script(get_length_from_id())

		for out in range(length - 1):
			try:
				element = WebDriverWait(self.driver, 2).until(
					 EC.element_to_be_clickable((By.ID, f"ContentPlaceHolder_rpt_lnkSamples_{out}")))
			except:
				continue
 
		
	# cleaning up data for storing in csv format
	def clean_up(self):
		output = ''
		soup = BeautifulSoup(self.driver.page_source, 'html.parser')
		for data in soup.select('table.SNewFontReportTable tr td'):
			output += re.sub(' {2,}', '', BeautifulSoup.get_text(data)) + '|'
		output = np.array(output[:-1].split('|'))
		return output.reshape(len(output) // 33, 33)[:, 1:]

	def next_page(self):
		length = int(self.driver.execute_script("return document.getElementsByClassName('lnkPages').length"))
		for data in range(length):
			self.driver.execute_script(f"document.getElementById('ContentPlaceHolder_repIndex_lnkPages_{data}').click()")
			yield self.clean_up()
			time.sleep(4)

	
	def close(self):
		self.driver.back()


# Get webbrowser with options
def get_webbrowser():
	url = "https://ejalshakti.gov.in/IMISReports/Reports/WaterQuality/rpt_WQM_SampleTesting_S.aspx?Rep=0&RP=Y"
	options = webdriver.ChromeOptions()
	options.add_argument('--incognito')
	#options.add_argument('--headless')		# to start in command line interface
	driver = webdriver.Chrome(options=options)
	driver.get(url)
	return driver


def get_length_from_id(driver, id_d):
	length = int(driver.execute_script("return document.getElementById('" + id_d + "').length"))
	return length

def get_data(id_d, id_num):
	return "document.getElementById('" + id_d + "').selectedIndex = " + str(id_num) + ';' + "document.getElementById('ContentPlaceHolder_btnGO').click();"


def get_tested_samples_by_id(id_num):
	return f"document.getElementById('ContentPlaceHolder_rpt_lnkSamples_{id_num}').click()"


# parsing villages by id
def get_village(driver):
	return parser(driver, "ContentPlaceHolder_ddVillage")

# parsing panchayat by id
def get_panchayat_village(driver):
	return parser(driver, "ContentPlaceHolder_ddPanchayat")

# parsing blocks by id
def get_block_panchayat(driver):
	return parser(driver, "ContentPlaceHolder_ddBlock")

def get_district_block(driver):
	return parser(driver, "ContentPlaceHolder_dddistrict")

# parsing state by id
def get_state_district(driver):
	return parser(driver, "ContentPlaceHolder_ddState")


# parser parses through data 
def parser(driver, id_d):
	length = get_length_from_id(driver, id_d)
	secrete_page = SecretePage(driver)

	for data in range(1, length):
		driver.execute_script(get_data(id_d, data))
		time.sleep(4)
		yield 
	
def main():
	# get webdriver
	driver = get_webbrowser()
	
	for state in get_state_district(driver):
		for district in get_district_block(driver):
			for block in get_block_panchayat(driver):
				for panchayat in get_panchayat_village(driver):
					for village in get_village(driver):
						pass
	

if __name__ == '__main__':
	main()
