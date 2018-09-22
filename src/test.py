from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


#options = webdriver.FirefoxOptions()
#options.add_argument('-headless')

#driver = webdriver.Firefox(firefox_options = options)
driver = webdriver.Firefox()
driver.get("http://www.echo360.org.au")
#assert "Python" in driver.title
elem = driver.find_element_by_name("email")
elem.clear()
elem.send_keys("carlin.williamson@student.unsw.edu.au")
elem.send_keys(Keys.RETURN)

delay = 4
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

delay = 6
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

for match in matches:
	#print ("matchObj.group(0) : " + match.group(0)) #Entire Statement
	#print ("matchObj.group(1) : " + match.group(1)) #id
	print ("matchObj.group(2) : " + match.group(2)) #Course Code


matchDict = {};
for match in matches:
	matchDict[match.group(2)] = match.group(1);

matchid = 0
elm = driver.find_element_by_id(matches[matchid].group(1))
elm.click()

delay = 6
try:
	myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
	print("Page is ready!")
except TimeoutException:
	print("Loading took too much time!")

elms = driver.find_elements_by_class_name("menu-opener")
print(len(elms))
for elm in elms:
	print(elm.get_attribute("aria-controls"))


print("Your Courses:")
counter = 0
for key in matchDict.keys():
	 print(key + ": " + str(counter));
	 counter += 1
inputNum = input("\nSelect a Courses Corrisponding Number:")

elms = driver.find_elements_by_class_name("courseMediaIndicator")
print(len(elms))
elms[0].click()

time.sleep(1)

elm = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/ul/li[2]/a")
elm.click()

time.sleep(1)
#assert "No results found." not in driver.page_source
#driver.close()

#/html/body/div[2]/div[3]/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/ul/li[2]/a
#/html/body/div[2]/div[3]/div/div/div/div[2]/div[2]/div/div/div/div/div/div[2]/ul/li[2]/a
#/html/body/div[2]/div[3]/div/div/div/div[2]/div[3]/div/div/div/div/div/div[2]/ul/li[2]/a

#assert "No results found." not in driver.page_source
#driver.close()

# vim: set softtabstop=8

