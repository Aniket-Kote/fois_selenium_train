import os
import requests
from captcha import read_captcha
from db_connect import connect_to_db
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv


# fnr_d=['23072013899']
# fnr_d=['23072105978','23072013899']
# fnr_d=['23072117432','23072009203','23071801534','23071803930','23071608566','23072105978','23072013899']
# fnr_d=['23070702342']

# fnr_d=['23072304560','23072319100','23072402020','23072402011','23072420035']
# fnr_d=['23072009203']
# fnr_d=['23072117432','23072009203','23071801534','23071803930','23071608566','23072304560','23072319100','23072402020','23072402011','23072420035']
# fnr_d=['23072304560','23072319100','23072402020','23072402011']
# fnr_d=['23081301927','23081317867','23081501961']
# fnr_d=['23081501961']
# fnr_d=['23081401005','23081400990']
fnr_d=['23081400990','23081401005','23081301927','23081317867','23081501961']
# fnr_d=['23081501961']


def get_data(f):
    load_dotenv()


    PATH = "C:\Program Files (x86)\chromedriver.exe"
    serv_obj = Service(PATH)
    driver = webdriver.Chrome(service=serv_obj)


    # fnr="23061821885"
    # fnr="23070702342"
    # fnr="23062400980"
    # fnr="23061821867"
    fnr=f



    location_details=[]

    # Maximize the window
    driver.maximize_window()


    # open url
    driver.get("https://www.fois.indianrail.gov.in/FOISWebPortal/pages/FWP_FNREnq.jsp")
    # wait for 5sec after url is loaded


    time.sleep(1)


    # Enter FNR Number
    driver.find_element(By.XPATH,"/html/body/div[4]/center/div/div/div/div[2]/form/div[1]/span/span/input").send_keys(fnr)
    try:
        time.sleep(5)
        # get captcha
        captcha_resolved=read_captcha()
    except Exception as e:
        
        print(e)
        
        
    captcha_err_msg=driver.find_element(By.XPATH,"/html/body/div[5]/div")
    if captcha_err_msg:
        try:
        # get captcha
            captcha_resolved=read_captcha()
            # Enter Captcha
            driver.find_element(By.XPATH,"/html/body/div[4]/center/div/div/div/div[2]/form/div[2]/input").send_keys(captcha_resolved)

        except Exception as e:
            time.sleep(5)
            captcha_resolved=read_captcha()
    # time.sleep(5)
            


    # Click submit button
    driver.find_element(By.XPATH,"/html/body/div[4]/center/div/div/div/div[2]/form/div[4]/button").click()

    time.sleep(8)
    # switch to 1st frame
    iframe=driver.switch_to.frame('frmDtls')
    # click on view on map
    try:
        driver.find_element(By.XPATH,"/html/body/div[2]/div/ul/button").click()
    except NoSuchElementException:
        captcha_resolved=read_captcha()
        time.sleep(10)
        # Click submit button
        driver.find_element(By.XPATH,"/html/body/div[4]/center/div/div/div/div[2]/form/div[4]/button").click()
    # arrival_data=''
    # departure_data=''
    # date_time=''
    # click on full screen
    time.sleep(3)
    driver.find_element(By.XPATH,"/html/body/button[1]").click()

    time.sleep(7)
    img_src_arr=[]
    main_div=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div[5]")
    if main_div.is_displayed():
        time.sleep(2)
        i=1
        while True:
            try:
                element=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div[5]/div["+str(i)+"]")
                driver.execute_script("arguments[0].click();", element)
                departure=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div[6]/div/div[1]/div/table/tbody/tr[5]/td[2]")
                if i==1 and departure.is_displayed():
                    departure_data=departure.text
                    print("DEparture",departure_data)
                
                # else:
                #     continue
                i+=1
                img_src=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div[5]/div["+str(i)+"]/img").get_attribute("src")
                img_src_arr.append(str(img_src))
                time.sleep(1)
            except NoSuchElementException:
                # arrival=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div[6]/div/div[1]/div/table/tbody/tr[8]/td[2]")
                # if arrival.is_displayed():
                #     arrival_data =arrival.text
                #     print("Arrival",arrival_data)
                break
                
            
            
        print("DONE")
        
        
        # Find elements with the same XPath
        elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div//div/div[1]/div/table/tbody/tr[1]/td/b")
        
        
        
        # Iterate over the elements and retrieve the inner text
        for en,element_d in enumerate(elements):
            inner_text = element_d.text
            
            # if arrival.is_displayed():
            #     arrival_data=arrival.text
            # else:
            #     arrival_data='NA'
            
            # if departure.is_displayed():
            #     departure_data=departure.text
            # else:
            #     departure_data='NA'
            
            # print(en,'-->',inner_text)
            location_details.append([fnr,inner_text])
        
        
        # print(location_details)
        # print(len(elements))
        print(type(location_details))
        
        
        # print(img_src_arr)
        # print(len(img_src_arr))
        
        
        
        for a in img_src_arr:
            t=a.split('/')
            # print(t)
            if t[len(t)-1]=='greenicon.png':
                img_src_arr[img_src_arr.index(a)]="waypoint"
            elif t[len(t)-1]=='bMapIcon.png':
                img_src_arr[img_src_arr.index(a)]="current"
            elif t[len(t)-1]=='dstn.png':
                img_src_arr[img_src_arr.index(a)]="destination"
            elif t[len(t)-1]=='src.png':
                img_src_arr[img_src_arr.index(a)]="current"
                
            if img_src_arr[len(img_src_arr)-1]=="current":
                    img_src_arr[len(img_src_arr)-1]="destination" 
                    
        # img_src_arr[0]="Start"
        img_src_arr.insert(0, 'source')
        # print(img_src_arr) 
        img_src_arr[len(img_src_arr)-1]="destination" 
        status=[]


        for l,im in zip(location_details,img_src_arr):
        
            
            l.append(im)



        for l,im in zip(location_details,img_src_arr):
        
            if im=="current":
                for s in range(img_src_arr.index(im),len(location_details)):
                    status.append("pending")
                break
            else:    
                status.append("passed")
            


        for ss,iim in zip(status,location_details):
            iim.append(ss)
            
        # print(location_details)
        
        # for i in range(1,10):
        #     element=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div[5]/div["+str(i)+"]")
        #     if element.is_displayed():
        #         print("FOUNDDDDDDDDDD")
        #         driver.execute_script("arguments[0].click();", element)
        #         time.sleep(1)
            
                
    else:
        print("NOT FOUND")   


    connect_to_db(os.getenv('DB_HOST'),os.getenv('DB_NAME'),os.getenv('DB_USER'),os.getenv('DB_PASS'),5432,location_details,fnr)
    print(len(location_details))

    # card_path="/html/body/div[1]/div[2]/div[1]/div//div/div[1]"
    # while card_path.is_displayed():
    #     print("yes")


    # location=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div//div/div[1]/div/table/tbody/tr[1]/td/b")
    # while location.is_displayed():
    #     print(location.get_property('innerText'))
    # time.sleep(10)
    # Find the element to click on using XPath
    # element=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div[5]/div[6]")

    # iframe_html = driver.page_source




    # # Get the src attribute value of the iframe
    # iframe_src = iframe.get_attribute("src")

    # # Use requests library to fetch the source code of the iframe
    # response = requests.get(iframe_src)
    # iframe_source_code = response.text

    # Print the iframe source code
    # print(iframe_html)


    # with open ('d.txt', 'w') as file:  
    #     file.write(iframe_html) 



















    # # driver.execute_script("arguments[0].click();", element)
    # element=driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div[5]/div[2]')
    # # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[5]/div[7]/img"))).click()

    # # Check if the element is displayed
    # if element.is_displayed():

    #     # Check if the element is enabled
    #     if element.is_enabled():

    #         # The element is interactable
    #         print("The element is interactable")
    #         element.click()
    #         time.sleep(10)
    #     else:

    #         # The element is not enabled
    #         print("The element is not enabled")
    # else:

    #     # The element is not displayed
    #     print("The element is not displayed")


    # time.sleep(10)




    # time.sleep(5)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
for f in fnr_d:
    get_data(f)
    time.sleep(10)
