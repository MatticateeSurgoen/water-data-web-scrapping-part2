#!/usr/bin/env	python3
from selenium import webdriver
import re
from bs4 import BeautifulSoup
import csv

# checked contaminants and clicks show
def show_Contaminants_separately(driver):
	driver.execute_script("document.getElementById('ContentPlaceHolder_chkAll').checked = true;" +
							"document.getElementById('ContentPlaceHolder_btnGO').click();")


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


def get_tested_samples_by_id(id_d):
	return f"document.getElementById('ContentPlaceHolder_rpt_lnkSamples_{id_d}').click()"

# cleaning up data for storing in csv format
def clean_up(driver):
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	soup
