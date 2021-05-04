# libraries
import pandas as pd
import numpy as np
import json, re, chardet, string, time, requests

from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions

from bulk_download import *

############################################
# match_data function
############################################
def match_data(file_dir, file_name, save_dir, save_name, driver='Firefox',
               file_type="application/csv,text/csv,text/comma-separated-values"):

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

##  # ==========================
##  # webscrapping
##  # ==========================
##  # defines profile and browser
    if driver=='Firefox':
        
##      # profile for autosaving (Firefox)
        profile = wd.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", save_dir)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", file_type)

##      # start webdriver
        browser = wd.Firefox(profile)

    elif driver=='Chrome':
##      # WORK IN PROGRESS
##      # profile for autosaving (Chrome)
        profile = wd.ChromeOptions()
        prefs = {'download.prompt_for_download': False,
                 'safebrowsing.enabled': False,
                 'safebrowsing.disable_download_protection': True,
                 "profile.default_content_settings.popups": 0,
                 "download.default_directory": save_dir,
                 'download.directory_upgrade': True,}
        profile.add_experimental_option('prefs', prefs)

##      # start webdriver 
        browser = wd.Chrome(profile)
        
    else:
        raise SystemExit


##  # to check 'nan' first
    nan_org1 = df.OpenPermID_1.isna()
    nan_org2 = df.OpenPermID_2.isna()
    nan_org = nan_org1 & nan_org2

##  # run through all info available
    for i in range(1): # df.shape[0]
        
##      # get the web
        webpage = df.OpenPermID_1[i]
        if nan_org1[i]:
            webpage = df.OpenPermID_2[i]

##      # skip no info
        if nan_org[i]:
            next
        else:
##            print(webpage, nan_org[i], nan_org1[i], nan_org2[i])
            browser.get(webpage)
            time.sleep(1)
            


