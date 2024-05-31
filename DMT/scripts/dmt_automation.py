from logging import exception
from time import sleep
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import numpy as np



def DMTautomation(text_Numberplate):
    results = []
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"

    options = webdriver.ChromeOptions()
    #options.headless = True
    #options.add_argument("headless")
    options.add_argument("--headless=new")
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')


    #PATH = "C:\Program Files (x86)\chromedriver.exe"
    #PATH = ".\DriveFiles\chromedriver"

    #web = webdriver.Chrome(executable_path="./DriveFiles/chromedriver.exe", options=options)
    #web = webdriver.Chrome(executable_path=r"D:\zkewed\product\chrome\chromedriver-win64\chromedriver.exe", options=options)


    web = webdriver.Chrome(executable_path=r"C:\Users\PC\Documents\Zkewed\Product\DMT\DriveFiles\chromedriver.exe", options=options)
    #web.get('http://selenium.dev/')
    print('get webdriver')

    web.get('http://eservices.motortraffic.gov.lk/VehicleInfo/logoutOauth.action')
    print(web.title)
    sleep(3)
    
    ProceedBtn = web.find_element_by_xpath('//*[@id="es-content"]/div[5]/div[6]/div/div[2]/button').click()
    
    
    #ProceedBtn.click()
    sleep(3)
    print("click button : ",web.title)
    #parentwindow = web.current_window_handle 

    #return all the handle values of open browser window
    handles = web.window_handles
    print('get webdriver 01')
    for handle in handles:
        web.switch_to.window(handle)
        print("after click button : ",web.title)
        sleep(2)
        if web.title=="Authentication":
            print("inside Authentication 01 : ",web.title)
            SelectEmailBtn = web.find_element_by_xpath('//*[@id="queryLink"]').click()
            print("inside Authentication 02: ",web.title)
            if web.title=="Sign in - Google Accounts":
                print("inside Google 01: ",web.title)
                windows_before  = web.current_window_handle
                email = web.find_element_by_xpath('//*[@id="identifierId"]').send_keys("shanil@zkewed.com")
                NextBtn = web.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()
                web.implicitly_wait(4)
                password = web.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys("rpdsi@22076R")
                #password = web.find_element_by_name("password").send_keys("rpdsi@22076R")
                NextBtn2 = web.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()
                #windows_before  = web.current_window_handle
                print("inside Google 02: ",web.title)
                #sleep(4)
                web.implicitly_wait(40)
                WebDriverWait(web, 5).until(EC.number_of_windows_to_be(2))
                windows_after = web.window_handles
                new_window = [x for x in windows_after if x != windows_before][0]
                web.switch_to.window(new_window)
                print("after Google 02: ",web.title)

                NIC_no = WebDriverWait(web, 5).until(EC.presence_of_element_located((By.XPATH , '//*[@id="nicNumber"]')))
                NIC_no.send_keys("940473144V")
                Tell_NO = web.find_element_by_xpath('//*[@id="contactNumber"]').send_keys("0712461605")
                VehicleNo = web.find_element_by_xpath('//*[@id="vehicleRegistrationNumber"]').send_keys(text_Numberplate)
                Submit = web.find_element_by_xpath('//*[@id="es-content"]/div[6]/div[1]/form/div/div[5]/div/div[2]/button[1]').click()
                #sleep(2)
                web.switch_to.alert.accept()
                ReportDate = web.find_element_by_xpath('//*[@id="es-content"]/div[5]/div/div[2]/div/ul/li[1]/label')
                VehicleRegistrationNumber = web.find_element_by_xpath('//*[@id="es-content"]/div[5]/div/div[2]/div/ul/li[2]/label')
                ownership = web.find_element_by_xpath('//*[@id="es-content"]/div[6]/div/div[2]/div[1]/table/tbody/tr[1]/td[3]')
                EngineNumber = web.find_element_by_xpath('//*[@id="es-content"]/div[6]/div/div[2]/div[1]/table/tbody/tr[2]/td[3]')
                VehicleClass = web.find_element_by_xpath('//*[@id="es-content"]/div[6]/div/div[2]/div[1]/table/tbody/tr[3]/td[3]')
                ConditionsNotes = web.find_element_by_xpath('//*[@id="es-content"]/div[6]/div/div[2]/div[1]/table/tbody/tr[4]/td[3]')
                Make = web.find_element_by_xpath('//*[@id="es-content"]/div[6]/div/div[2]/div[1]/table/tbody/tr[5]/td[3]')
                Model = web.find_element_by_xpath('//*[@id="es-content"]/div[6]/div/div[2]/div[1]/table/tbody/tr[6]/td[3]')
                ManufacturedYear = web.find_element_by_xpath('//*[@id="es-content"]/div[6]/div/div[2]/div[1]/table/tbody/tr[7]/td[3]')

    
        
                results = {'ReportDate': ReportDate.text,
                    'VehicleRegistrationNumber':VehicleRegistrationNumber.text,
                    'ownership':ownership.text,
                    'EngineNumber':EngineNumber.text,
                    'VehicleClass':VehicleClass.text,
                    'ConditionsNotes':ConditionsNotes.text,
                    'Make':Make.text,
                    'Model':Model.text,
                    'ManufacturedYear':ManufacturedYear.text,
                    'errorMessage':ownership.text,
                    }
        
    
                return results

if __name__ == '__main__':
    im = DMTautomation("CAN-1744")
    print(im.get('VehicleRegistrationNumber'))
    print(im.get('ownership'))
    print(im.get('EngineNumber'))