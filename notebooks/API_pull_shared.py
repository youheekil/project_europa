# libraries
import pandas as pd
import numpy as np
import json, re, chardet, string, time, requests

from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions


############################################
# handle ElementNotInteractableException
############################################
def handle_noclick_xp(b, xp):
    try:
        b.find_element_by_xpath( xp ).click()
    except exceptions.ElementNotInteractableException:
        pass
    except exceptions.NoSuchElementException:
        pass


def handle_noclick_extra(b, xp_start, xp_end, divs):
    for div in divs:
        try:
            xp = xp_start + str(div) + xp_end
            b.find_element_by_xpath( xp ).click()
        except exceptions.ElementNotInteractableException:
            next
        except exceptions.NoSuchElementException:
            next
        else:
            break



############################################
# match_data function
############################################
def match_data(wm, un, pw, file_dir, file_name, save_dir, save_name,
               driver='Firefox',
               ft="application/csv,text/csv,text/comma-separated-values"):

##  # ==========================
##  # open file of pages
##  # ==========================
##  # paths for all files
    full_path = file_dir + 'main_match_' + file_name + '.csv'
    
##  # check encoding of files: open first 10'000 bytes                 
    with open(full_path, 'rb') as rawdata:
        encoding = chardet.detect(rawdata.read(10000))
##    print(encoding)
##    # 73% of confidence
        
##  # load data
    df = pd.read_csv(full_path, sep=',', encoding=encoding['encoding'])

##  # creating storage
    df["Primary Industry"] = '0'
    df["Primary Bussiness"] = '0'
    df["Primary Economic"] = '0'
    df["Domiciled"] = '0'
    df["Incorporated"] = '0'
    df["Primary Industry description"] = '0'

##  # save path
    full_path = save_dir + 'info_match_' + save_name + '.csv'   

##  # ==========================
##  # webscrapping
##  # ==========================
##  # defines profile and browser
    if driver=='Firefox':
##      # profile for autosaving (Firefox)
        pf = wd.FirefoxProfile()
        pf.set_preference("browser.download.folderList", 2)
        pf.set_preference("browser.download.manager.showWhenStarting", False)
        pf.set_preference("browser.download.dir", save_dir)
        pf.set_preference("browser.helperApps.neverAsk.saveToDisk", ft)
        pf.set_preference("browser.link.open_newwindow", 1)
        
##      # start webdriver
        browser = wd.Firefox(pf)

    elif driver=='Chrome':
##      # WORK IN PROGRESS
##      # profile for autosaving (Chrome)
        pf = wd.ChromeOptions()
        prefs = {'download.prompt_for_download': False,
                 'safebrowsing.enabled': False,
                 'safebrowsing.disable_download_protection': True,
                 "profile.default_content_settings.popups": 0,
                 "download.default_directory": save_dir,
                 'download.directory_upgrade': True,}
        pf.add_experimental_option('prefs', prefs)

##      # start webdriver 
        browser = wd.Chrome(pf)
        
    else:
        raise SystemExit

##  # enter main page
    browser.get(wm)
    time.sleep(10)
    
    xp = "/html/body/navbar/header[1]/nav/div/ul/li[2]/a"
    handle_noclick_xp(b=browser, xp=xp)
    time.sleep(10)
    
    username = browser.find_element_by_id("AAA-AS-SI1-SE003")
    password = browser.find_element_by_id("AAA-AS-SI1-SE006")
    username.send_keys(un)
    password.send_keys(pw)
    time.sleep(1)
    browser.find_element_by_id("AAA-AS-SI1-SE014").click()
    time.sleep(10)

    xp = "/html/body/div[2]/div/div/div[2]/a"
    browser.find_element_by_xpath(xp).click()
    time.sleep(10)

##  # to check 'nan' first
    nan_org1 = df.OpenPermID_1.isna()
    nan_org2 = df.OpenPermID_2.isna()
    nan_org = nan_org1 & nan_org2

##  # run through all info available
    for i in range(df.shape[0]): # df.shape[0]
        
##      # to check evolution
        print('start ' + str(i) + ' of ' + str(df.shape[0]) )
        
##      # skip no info
        if not( nan_org[i] ):
            
##          # get the web (depending on the quality of match)
            if not(nan_org1[i]) and nan_org2[i]:
                web = df.OpenPermID_1[i]
            elif nan_org1[i] and not(nan_org2[i]):
                web = df.OpenPermID_2[i]
            elif df.Score_1[i] >= df.Score_2[i]:
                web = df.OpenPermID_1[i]
            else:
                web = df.OpenPermID_2[i]
                
##          # enter page (in the same windows)
            browser.get(web)
            time.sleep(10)

##          # get main info
            web_source = browser.page_source
            soup = bs(web_source, 'html.parser')
            
            full_class = soup.find_all('a', class_='link ng-binding')
            full_info = []
            for each_class in full_class:
                full_info.append(each_class.text)
            if len(full_info) > 5: # when public, there is more info
                del full_info[5:]

##          # click section of interest
            xp_s = "/html/body/div[3]/section/div/div[2]/div[1]/div["
            xp_e = "]/div[2]/a"
            handle_noclick_extra(b=browser, xp_start=xp_s, xp_end=xp_e,
                                 divs=range(5,8))
            time.sleep(10)

##          # get primary industry description
            web_source = browser.page_source
            soup = bs(web_source, 'html.parser')
            full_class = soup.find_all('div', class_='col-md-8 ng-binding')
            full_info.append(full_class[3].text) # always located in [3]
            print(full_info)

##          # save the info in df
            df.iloc[i, range(11,17)] = full_info
            
##          # save data
            df.to_csv(full_path, index=False, encoding=encoding['encoding'])

##  # close user session
    handle_noclick_id(b=browser, id_='profile-toggle')
            
##  # finish the page
    browser.quit()

    print('finished')



file3 = "/home/jriveraespejo/Desktop/project_europa/data/processed/"
name1 = "CSPPholdings_201706_2021"
web_main = 'https://permid.org/'
user = 'your_username'
word = 'your_password'
match_data(wm=web_main, un=user, pw=word,
           file_dir=file3, file_name=name1, save_dir=file3, save_name=name1)


