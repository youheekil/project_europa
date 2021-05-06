# libraries
import pandas as pd
import numpy as np
import json, re, chardet, string, time, requests, lightrdf

from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions


############################################
# handlers
############################################

## if the xpath is not clickable
def handle_noclick_xp(b, xp_):
    try:
        b.find_element_by_xpath( xp_ ).click()
    except exceptions.ElementNotInteractableException:
        pass
    except exceptions.NoSuchElementException:
        pass

## if the id is not clickable
def handle_noclick_id(b, id_):
    try:
        b.find_element_by_id( id_ ).click()
    except exceptions.ElementNotInteractableException:
        pass
    except exceptions.NoSuchElementException:
        pass

## test the existence of the multiple 'divs'
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

## handle error by xpath
def handle_error_css(b, css_):
    try:
        text = b.find_element_by_css_selector(css_).text
    except exceptions.ElementNotInteractableException:
        text = 'No error'
    except exceptions.NoSuchElementException:
        text = 'No error'
    return(text)


## reload page with 'Unexpected error occurred'
## NEEDS REVIEWING
def handle_web(b, w):
##    xpath = "/html/body/div[3]/section/div/div/div/div/div[1]/div/div/h1"
    csspath = "div.About-title h1.heading-2.ng-binding"
    error_text = handle_error_css(b=b, css_=csspath)
    print(error_text)

    j = 1
    while error_text == 'Unexpected error occurred':
        j += 1
        b.get(w)
        time.sleep(10)
        error_text = handle_error_css(b=b, css_=csspath)
        print(error_text + " at " + str(j) + " try" )


############################################
# match_data function
############################################
def match_data(wm, un, pw, file_dir, file_name, save_dir, save_name,
               rows, round_=1, driver='Firefox',
               ft="application/csv,text/csv,text/comma-separated-values"):

##  # ==========================
##  # open file of pages
##  # ==========================

##  # first time of retrieving
    if round_==1:
        
##      # path for file
        full_path = file_dir + 'main_match_' + file_name + '.csv'
    
##      # check encoding of files: open first 10'000 bytes                 
        with open(full_path, 'rb') as rawdata:
            encoding = chardet.detect(rawdata.read(10000))
##      print(encoding)
##      # 73% of confidence
        
##      # load data
        df = pd.read_csv(full_path, sep=',', encoding=encoding['encoding'])

##      # creating storage
        df["Primary Industry"] = '0'
        df["Primary Bussiness"] = '0'
        df["Primary Economic"] = '0'
        df["Domiciled"] = '0'
        df["Incorporated"] = '0'
        df["Primary Industry description"] = '0'
        obs = rows

##      # to check 'nan' first
        nan_org1 = df.OpenPermID_1.isna()
        nan_org2 = df.OpenPermID_2.isna()
        nan_org = nan_org1 & nan_org2

##      # save path
        full_path = save_dir + 'info_match_round1_' + save_name + '.csv'
        
##  # second time of retrieving
    elif round_==2:

##      # path for file
        full_path = file_dir + 'info_match_round1_' + file_name + '.csv'
    
##      # check encoding of files: open first 10'000 bytes                 
        with open(full_path, 'rb') as rawdata:
            encoding = chardet.detect(rawdata.read(10000))
##      print(encoding)
##      # 73% of confidence
        
##      # load data
        df = pd.read_csv(full_path, sep=',', encoding=encoding['encoding'])
        print()
        
##      # check for empty values
        nan_org1 = df.OpenPermID_1.isna()
        nan_org2 = df.OpenPermID_2.isna()
        nan_org = nan_org1 & nan_org2
        obs = df[ (df["Primary Industry"] == '0') & (nan_org!=True) ].index.tolist()
        print('checking for ' + str( len(obs) ) + ' observations')

##      # save path
        full_path = save_dir + 'info_match_round2_' + save_name + '.csv'
    
##  # no other time is allowed
    else: 
        raise SystemExit


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
    handle_noclick_xp(b=browser, xp_=xp)
    time.sleep(10)
    
    username = browser.find_element_by_id("AAA-AS-SI1-SE003")
    password = browser.find_element_by_id("AAA-AS-SI1-SE006")
    username.send_keys(un)
    password.send_keys(pw)
    time.sleep(1)
    browser.find_element_by_id("AAA-AS-SI1-SE014").click()
    time.sleep(10)

##  # accept cookies
    xp = "/html/body/div[2]/div/div/div[2]/a"
    browser.find_element_by_xpath(xp).click()
    time.sleep(3)

##  # run through all info available
    for i in obs: # df.shape[0]
        
##      # to check evolution
        print('start ' + str(i) + ' of ' + str(df.shape[0]) + ':',
              df.OrgName_1[i] )
        
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
                
##          # enter web
            browser.get(web)
            time.sleep(10)

##          # check for error
            handle_web(b=browser, w=web)

##          # get main info           
            web_source = browser.page_source
            soup = bs(web_source, 'html.parser')
            full_class = soup.find_all('a', class_='link ng-binding')

##          # if there is info go in                                    
            if len(full_class) > 0:
                full_info = []
                for each_class in full_class:
                    full_info.append(each_class.text)
                if len(full_info) > 5: # when public, there is more info
                    del full_info[5:]
                if len(full_info) == 4:
                    full_info.append('')

##              # click section of interest
                xp_s = "/html/body/div[3]/section/div/div[2]/div[1]/div["
                xp_e = "]/div[2]/a"
                handle_noclick_extra(b=browser,
                                     xp_start=xp_s,
                                     xp_end=xp_e,
                                     divs=range(5,8))
                time.sleep(15)

##              # get primary industry description
                web_source = browser.page_source
##                handle_web(b=browser, w=web) # not implemented yet
                soup = bs(web_source, 'html.parser')
                full_class = soup.find_all('div', class_='col-md-8 ng-binding')

##              # if there is info go in                                  
                if len(full_class) > 0:
##                  # save info
                    full_info.append(full_class[3].text) # always located in [3]
                    df.iloc[i, range(11,17)] = full_info
            
##                  # save data
                    df.to_csv(full_path, index=False, encoding=encoding['encoding'])
##                    print(full_info)
                    
##  # close user session
    handle_noclick_id(b=browser, id_='profile-toggle')
    handle_noclick_xp(b=browser, xp_='/html/body/navbar/header[1]/nav/div/div[2]/ul/li[3]/a')
    time.sleep(3)
    print('session closed')
            
##  # finish the page
    browser.quit()
    print('finished')
