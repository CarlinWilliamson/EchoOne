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
import glob


def enable_download_in_headless_chrome(driver, download_dir):
	# add missing support for chrome "send_command"  to selenium webdriver
	driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

	params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
	command_result = driver.execute("send_command", params)

options = Options() 
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
#driver = webdriver.Firefox(firefox_options = options)
driver.get("http://www.echo360.org.au")

# login to echo360
elem = driver.find_element_by_name("email")
elem.clear()

# It doesn't matter whos email it is
# Might fail if carlin williamson graduates
elem.send_keys("carlin.williamson@unsw.edu.au")
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
elms = driver.find_elements_by_tag_name("a")
elms = list(filter(lambda x:x.get_attribute("aria-label"), elms))
elms = list(filter(lambda x:len(x.get_attribute("aria-label")) > 10, elms))
print("\nYour Courses:")
print("    Course   Term LectureStream")
for i, elm in enumerate(elms):
	text = elm.get_attribute("aria-label")
	if (text is None or len(text) < 10):
		continue
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
print("\nYour Lectures:")
counter = 0
for elm in elms:
	matchObj = re.match( r'.*_(\d{4})-(\d{2})-(\d{2})T.*', elm.get_attribute("aria-controls"))
	if matchObj:
		date = matchObj.group(3) + "/" + matchObj.group(2) + "/" + matchObj.group(1)
		print("{:2d}: {}".format(counter, date))
		counter += 1

lectureInputStart = int(input("\nSelect First Lecture To Download: "))
lectureInputEnd = int(input("\nSelect Last Lecture To Download: "))

downloadHD = input("\nDownload High Definition video? (y/n): ")
downloadFolder = courseName

# make sure the folder exists
if not os.path.exists(downloadFolder):
	os.mkdir(downloadFolder)
os.chdir(downloadFolder)

# make sure there are no .crdownload files in the folder
# these are created when chrome is closed ungracefully
# the script relies on the crdownload file disappearing to tell
# when the download is finished
if len(glob.glob("*.crdownload")) != 0:
	input("\n{} contains .crdownload files. "
		  "delete these files then press enter".format(courseName))

enable_download_in_headless_chrome(driver, os.getcwd())

for lecture in range(lectureInputStart, lectureInputEnd + 1):
	# open lecture popup menu
	elms = driver.find_elements_by_class_name("courseMediaIndicator")
	elms[lecture].click()
	time.sleep(0.5)

	# open download modal
	# The next line can fail if the lecture video isn't avaliable yet
	# i.e. the lecture is either recording or hasn't been uploaded yet
	elm = driver.find_element_by_partial_link_text("Download original")
	elm.click()
	time.sleep(1)

	# make the video hd
	if (downloadHD == "y"):
		elm = driver.find_elements_by_tag_name("option")[1]
		elm.click()
		time.sleep(0.5)

	# get their download link and swap out the name for ours
	elm = driver.find_element_by_class_name("downloadBtn")
	filename = "{}_{:02d}.mp4".format(courseName, lecture)
	url = elm.get_attribute("href")
	# replacing after the last '='
	url = "=".join(url.split("=")[:-1]) + "=" + filename
	driver.get(url) # download the video

	# exit the modal
	elm = driver.find_element_by_class_name("left")
	elm = elm.find_element_by_tag_name("a")
	elm.click()
	time.sleep(0.5)

	# wait for the crdownload file to disappear
	while len(glob.glob("*.crdownload")) != 0:
		time.sleep(0.5)

	print("Finished Downloading %s" % filename)

driver.close()

# vim: set softtabstop=8
