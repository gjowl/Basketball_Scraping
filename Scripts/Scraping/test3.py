#After a couple of tries and a fuck ton of searching, this one works! This took like 10 hours of my life to figure out,
#so if it breaks, come straight back to these two websites for information first. The final one is a troubleshooting
#list that many people on github have used for certain questions and issues.
"""
Information from the following two websites:
    - https://www.selenium.dev/documentation/webdriver/getting_started/first_script/
    - https://github.com/SergeyPirogov/webdriver_manager

Troubleshooting:
    - https://github.com/SeleniumHQ/selenium/issues/6049
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("http://www.google.com")
print(driver.title)

# wait for elements to appear on page (may need longer waits)
driver.implicitly_wait(0.5)

# find the search box and button on google
search_box = driver.find_element(By.NAME, "q")
search_button = driver.find_element(By.NAME, "btnK")

# search for selenium and output the searched term (?)
search_box.send_keys("Selenium")
search_button.click()
print(driver.find_element(By.NAME, "q").get_attribute("value"))

driver.close()