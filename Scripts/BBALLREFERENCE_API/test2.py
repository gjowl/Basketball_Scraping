from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

#service = Service(executable_path=GeckoDriverManager().install())
#
#driver = webdriver.Chrome(service=service)
options = Options()
myprofile = webdriver.FirefoxProfile()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
#options.add_argument('--devtools.debugger.remote-enabled')
options.binary_location = '/mnt/c/Program Files/Mozilla Firefox/firefox.exe'
driver = webdriver.Firefox(firefox_profile=myprofile, executable_path='/usr/bin/geckodriver', options=options)
driver.get("http://www.google.com")
driver.close()