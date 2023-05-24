from abc import abstractmethod
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
class Extractor():
    @abstractmethod
    def __init__(self,timeout=5,csvOutput=''):
        self.dataFrame = None
        self.csvOutput = csvOutput
        self.timeout = timeout
    
    def getDataFrame(self):
        return self.dataFrame
    
    def driverChrome(self):
        options = Options()
        #options.add_argument("headless")
        options.add_argument("disable-gpu")
        options.add_argument("no-sandbox")       
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(chrome_options=options)
        driver.implicitly_wait(5)
        driver.maximize_window()
        return driver