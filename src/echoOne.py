from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import getpass
import os.path
import time
import re


def enable_download_in_headless_chrome(driver, download_dir):
    # add missing support for chrome "send_command"  to selenium webdriver
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)

start = time.time()

options = Options() 
options.add_argument("--headless")


driver = webdriver.Chrome(options=options)
#driver = webdriver.Firefox(firefox_options = options)

driver.get("https://ssologin.unsw.edu.au/cas/login?service=https://moodle.telt.unsw.edu.au/login/index.php?authCAS=CAS")

elem = driver.find_element_by_name("username")
elem.clear()
elem.send_keys(input("UNSW zID: "))
elem = driver.find_element_by_name("password")
elem.clear()
elem.send_keys(getpass.getpass())
elem.send_keys(Keys.RETURN)

# look for a link with a year in it (pretty much any will do...)
elm = None
year = 2019
while not elm:
	try:
		elm = driver.find_element_by_partial_link_text(str(year))
	except:
		pass

	year = year + 1

elm.click()


elm = driver.find_element_by_partial_link_text("record")
elm.click()

time.sleep(2)
driver.get("https://echo360.org.au/home")
time.sleep(1)


# We should be at the echo360
elms = driver.find_elements_by_class_name("hlBdZn")

print("Your Courses:")
print("    Course   Term LectureStream")
for i, elm in enumerate(elms):
	text = elm.get_attribute("aria-label")
	courseName = text.split(" - ")[1].split("/")[0]
	reg = re.match(r'\d{2}(\d{2})TP(\d)', text.split(" - ")[2])
	term = "{}T{}".format(reg.group(1), reg.group(2))
	reg = re.match(r'.*(\d)', text.split(" - ")[2])
	stream = reg.group(1)
	#print(text)
	print("{:2d}: {} {} {}".format(i, courseName, term, stream))

courseInput = int(input("\nSelect a Courses Corresponding Number: "))

elm = elms[courseInput]
courseName = elm.get_attribute("aria-label").split(" - ")[1].split("/")[0]
elm.click()

time.sleep(2)

# choose lecture video
elms = driver.find_elements_by_class_name("menu-opener")
print("Your Lectures:")
counter = 0
for elm in elms:
	matchObj = re.match( r'.*_(\d{4})-(\d{2})-(\d{2})T.*', elm.get_attribute("aria-controls"))
	if (matchObj):
		print(matchObj.group(3) + "/" + matchObj.group(2) + "/" + matchObj.group(1) + ": " + str(counter))
		counter += 1

lectureInputStart = int(input("\nSelect First Lecture To Download: "))
lectureInputEnd = int(input("\nSelect Last Lecture To Download: "))

downloadHD = input("\nDownload High Definition video? (y/n): ")
downloadFolder = courseName

if not os.path.exists(downloadFolder):
    os.mkdir(downloadFolder)
os.chdir(downloadFolder)

downloadName = "sd1.mp4"
if (downloadHD == "y"):
	downloadName = "hd1.mp4"

for lecture in range(lectureInputStart, lectureInputEnd + 1):
	elms = driver.find_elements_by_class_name("courseMediaIndicator")
	elms[lecture].click()
	time.sleep(0.5)

	# open download page
	# The next line can fail if the lecture video isn't avaliable yet
	# i.e. the lecture is either recording or hasn't been uploaded yet
	elm = driver.find_element_by_partial_link_text("Download original")
	elm.click()
	time.sleep(1)

	# make the video hd
	if (downloadHD == "y"):
		time.sleep(0.75)
		elms = driver.find_elements_by_tag_name("option")
		elms[1].click()
		time.sleep(0.75)

	#download the video
	enable_download_in_headless_chrome(driver, downloadFolder)
	elm = driver.find_element_by_class_name("downloadBtn")
	elm.click()

	#print("Downloading Lecture " + str(lecture+1))
	while not os.path.exists(downloadName):
		time.sleep(1)
	os.rename(downloadName, "{}_{:02d}.mp4".format(courseName, lecture))

	print("Download finished and renamed to {}_{:02d}.mp4".format(courseName, lecture))

#assert "No results found." not in driver.page_source
driver.close()

# vim: set softtabstop=8
