import time
from selenium import webdriver
import re
import requests


my_ig = 'acuteanalytica'
my_ig_full_name = "Acute Analytica"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-data-dir=C:\\Users\\charles.fawole\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
chrome_options.add_argument("--window-size=1920,1080")


driver = webdriver.Chrome(options=chrome_options)  # Optional argument, if not specified will search path.
#driver.get('http://www.google.com/')


driver.get('https://marketplace.akc.org/breeder/mickey-kern-43400/poodle/234178')

page_source = (driver.page_source)

f = open('test_akc3.txt','w')
f.write("hello")
f.close()