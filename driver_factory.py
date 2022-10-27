from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class FirefoxDriver():
    def __new__(self, timeout):
        options = FirefoxOptions()
        #options.headless = True
        driver = webdriver.Firefox(service=FirefoxService(
            GeckoDriverManager().install()), options=options)
        driver.implicitly_wait(timeout)
        return driver

