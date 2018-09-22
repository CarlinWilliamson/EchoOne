from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()
driver.get("http://www.echo360.org.au")
#assert "Python" in driver.title
elem = driver.find_element_by_name("email")
elem.clear()
elem.send_keys("carlin.williamson@student.unsw.edu.au")
elem.send_keys(Keys.RETURN)

time.sleep(2.5)

elem = driver.find_element_by_id("userNameInput")
elem.clear()
elem.send_keys("z5122521@ad.unsw.edu.au")
elem = driver.find_element_by_name("Password")
elem.clear()
elem.send_keys("Hackathon2018")
elem.send_keys(Keys.RETURN)

time.sleep(10)

print(driver.page_source)


#assert "No results found." not in driver.page_source
#driver.close()


