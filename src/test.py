from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


options = webdriver.FirefoxOptions()
options.add_argument('-headless')

driver = webdriver.Firefox(firefox_options = options)
driver.get("http://www.echo360.org.au")
#assert "Python" in driver.title
elem = driver.find_element_by_name("email")
elem.clear()
elem.send_keys("carlin.williamson@student.unsw.edu.au")
elem.send_keys(Keys.RETURN)

delay = 5
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

elem = driver.find_element_by_id("userNameInput")
elem.clear()
elem.send_keys("z5122521@ad.unsw.edu.au")
elem = driver.find_element_by_name("Password")
elem.clear()
elem.send_keys("Hackathon2018")
elem.send_keys(Keys.RETURN)

delay = 10
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

page_source = driver.page_source
page = page_source.split('\n')

matches = []
for line in page:
	matchObj = re.match( r'.*id="(\S*)".*See all classes in (\w*)', line)
	if matchObj:
		matches.append(matchObj)

print("Your Courses:")
counter = 0
for match in matches:
	 print(match.group(2) + ": " counter);
	 counter += 1
inputNum = input("\nSelect a Courses Corrisponding Number:")

#assert "No results found." not in driver.page_source
#driver.close()


