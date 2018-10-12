from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import getpass
import os.path

def enable_download_in_headless_chrome(driver, download_dir):
    # add missing support for chrome "send_command"  to selenium webdriver
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)


options = Options() 
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

#driver = webdriver.Firefox(firefox_options = options)
#driver = webdriver.Chrome()
driver.get("http://www.echo360.org.au")
#assert "Python" in driver.title


# login to echo360
elem = driver.find_element_by_name("email")
elem.clear()
elem.send_keys("carlin.williamson@student.unsw.edu.au")
elem.send_keys(Keys.RETURN)

time.sleep(2)

# login to microsoft
elem = driver.find_element_by_id("userNameInput")
elem.clear()
elem.send_keys(input("UNSW zID: ") + "@ad.unsw.edu.au")
elem = driver.find_element_by_name("Password")
elem.clear()
elem.send_keys(getpass.getpass())
elem.send_keys(Keys.RETURN)

time.sleep(2)

# choose course
page_source = driver.page_source
page = page_source.split('\n')

matches = []
for line in page:
	matchObj = re.match( r'.*id="(\S*)".*See all classes in (\w*)', line)
	if matchObj:
		matches.append(matchObj)

matchDict = {};
for match in matches:
	matchDict[match.group(2)] = match.group(1);

print("Your Courses:")
counter = 0
keys = list(matchDict.keys());
for key in keys:
	 print(key + ": " + str(counter));
	 counter += 1
courseInput = int(input("\nSelect a Courses Corresponding Number: "))

matchid = courseInput
print(matchDict[keys[courseInput]])
elm = driver.find_element_by_id(matchDict[keys[courseInput]])
elm.click()

time.sleep(2)

# choose lecture video
elms = driver.find_elements_by_class_name("menu-opener")
print("Your Lectures:")
counter = 0
for elm in elms:
	matchObj = re.match( r'.*_(\d{4})-(\d{2})-(\d{2})T.*', elm.get_attribute("aria-controls"))
	print(matchObj.group(3) + "/" + matchObj.group(2) + "/" + matchObj.group(1) + ": " + str(counter))
	counter += 1
lectureInputStart = int(input("\nSelect First Lecture To Download: "))
lectureInputEnd = int(input("\nSelect Last Lecture To Download: "))
for lecture in range(lectureInputStart, lectureInputEnd):
	elms = driver.find_elements_by_class_name("courseMediaIndicator")
	elms[lecture].click()
	time.sleep(0.5)

	# open download page
	elm = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/div[2]/div[" + str(lecture + 1) + "]/div/div/div/div/div/div[2]/ul/li[2]/a")
	elm.click()
	time.sleep(0.5)

	# make the video hd
	#elm = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div/div[1]/div[4]/div[1]/div/div/select/option[2]")
	#elm.click()

	enable_download_in_headless_chrome(driver,"C:\\Users\\marcu\\Downloads")
	#download the video
	elm = driver.find_element_by_class_name("downloadBtn")
	elm.click()

	os.chdir("C:\\Users\\marcu\\Downloads")
	#print("Downloading Lecture " + str(lecture+1))
	while not os.path.exists("sd1.mp4"):
		
		time.sleep(1)
	os.rename("sd1.mp4", keys[courseInput] + "-" + str(lecture + 1) + ".mp4")

	#print("download finished and renamed to " + keys[courseInput] + "-" + str(lecture + 1))

#assert "No results found." not in driver.page_source
#driver.close()

# vim: set softtabstop=8
