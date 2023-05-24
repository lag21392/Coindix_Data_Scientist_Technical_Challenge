from Extractor import Extractor

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import pandas as pd
class ExtractorCoindixStablecoins(Extractor):
    def __init__(self,timeout=5,csvOutput='data_Coindix_StableCoins.csv'):
        Extractor.__init__(self,timeout=timeout,csvOutput=csvOutput)
    def extract(self):
        def extractTableTRs(driver,timeout):
            time.sleep(3)
            #search table
            xpathSelector="//tbody[@id='xdefivaults']/tr"
            try:
                WebDriverWait(driver,timeout).until(EC.presence_of_element_located((By.XPATH,xpathSelector)))
                trs=driver.find_elements(By.XPATH,xpathSelector)
                return trs
            except TimeoutException:
                print("Timed out waiting for page to load")
                return None
        driver = self.driverChrome()        
        # Acceder a la aplicación web
        url='https://nanoly.com/kind:stable-sort:apy:desc'#'https://coindix.com/'
        driver.get(url)

        #click in stablecoins
        '''xpathSelector="//div[@class='clearfix']/div[@class='fleft filterbtn'][4]"
        try:
            WebDriverWait(driver,self.timeout).until(EC.element_to_be_clickable((By.XPATH,xpathSelector))).click()
        except TimeoutException:
            print("Timed out waiting for page to load")'''

        finishExtract=False
        trs=extractTableTRs(driver,self.timeout)
        rows=[]
        while not finishExtract:
            #iterator rows  
            for tr in trs:
                row = [td.text for td in tr.find_elements_by_tag_name('td')]
                row=row[1:10]
                row = [col.replace('$','').replace(',','').replace('%','').replace('-','0').replace('\nSIGN UP','').replace('\n','-') for col in row]
                row.pop(5)
                rows.append(row)
                

            #search next table
            xpathSelector="//div[@id='pagination']/a[@class='arrow-right']"
            try:
                driver.execute_script("window.scrollBy(0, 10000);")
                WebDriverWait(driver,self.timeout).until(EC.element_to_be_clickable((By.XPATH,xpathSelector))).click()   
                trs=extractTableTRs(driver,self.timeout)
                if trs == None:
                    finishExtract=True
                    driver.quit()
            except TimeoutException:
                finishExtract=True
                driver.quit()
                print("Timed out waiting for page to load Finish Extract")
            
            #load DataFrame
        #print(rows)
        #pd.options.display.max_columns=20
        columnas=['Name','Protocol - Chain','Base_APY_$','Reward_APY_%','Rewards','APY_%','7d_ago_%','TVL_$']
        df = pd.DataFrame(rows, columns=columnas)
        df = df.astype({'Name': 'object','Protocol - Chain': 'object', 'Base_APY_$': 'float64', 'Reward_APY_%': 'float64', 'Rewards': 'object','APY_%': 'float64', '7d_ago_%': 'float64','TVL_$': 'int32'})
        df['Rewards']=df['Rewards'].replace('0','')
        df = df.set_index(['Name','Protocol - Chain'])
        if self.csvOutput!='':
            df.to_csv(self.csvOutput)  
        self.dataFrame = df