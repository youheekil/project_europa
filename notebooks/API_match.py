# libraries
import pandas as pd
from selenium import webdriver as wd
import json, re, chardet, string, time


# match_fromat function
def match_format(file_dir, file_name, save_dir, save_name):
##  # full path for file
    full_path = file_dir + file_name + '.csv'
    
    # check encoding of files: open first 10'000 bytes                 
    with open(full_path, 'rb') as rawdata:
        encoding = chardet.detect(rawdata.read(10000))
##    print(encoding)
##    # 73% of confidence
        
##  # load data
    df = pd.read_csv(full_path, sep=',', encoding=encoding['encoding'])

##  # clean names
    df["Name"] = df['ISSUER_NAME'].str.strip()
    df["Name"] = df['Name'].str.replace('á', 'a')
    df["Name"] = df['Name'].str.replace('ã', 'a')
    df["Name"] = df['Name'].str.replace('ä', 'a')
    df["Name"] = df['Name'].str.replace('é', 'e')
    df["Name"] = df['Name'].str.replace('ë', 'e')
    df["Name"] = df['Name'].str.replace('É', 'E')
    df["Name"] = df['Name'].str.replace('í', 'i')
    df["Name"] = df['Name'].str.replace('ó', 'o')
    df["Name"] = df['Name'].str.replace('ö', 'o')
    df["Name"] = df['Name'].str.replace('ü', 'u')
    df["Name"] = df['Name'].str.replace('ñ', 'n')
    df["Name"] = df['Name'].str.replace('(,\s\w+)$', '')
    df["Name"] = df['Name'].str.replace('[{}]'.format(string.punctuation), '')

##  # to lower
    df["Name"] = df['Name'].str.lower()
    
##  # remove duplicates and sort
    df = df.drop_duplicates(subset=['Name'])
    df = df.sort_values(by=['Name'])

##  # put info in the right format    
##  # see https://permid.org/match: 'Organization' and 'Download Template' buttons
##  # drop NCB (country) as it has missmatchs
    df = df.drop(['COUPON_RATE','ISIN_CODE','MATURITY_DATE','NCB','file_date'], axis = 1)

##  # add empty info
    df['LocalID'] = ''
    df['Standard Identifier'] = ''
    df['Country'] = ''
    df['Street'] = ''
    df['City'] = ''
    df['PostalCode'] = ''
    df['State'] = ''
    df['Website'] = ''

##  # re-order columns  
    df = df[['LocalID','Standard Identifier','Name','Country','Street','City','PostalCode','State','Website']]

##  # saving data
    full_path = save_dir + save_name + '.csv'
    df.to_csv(full_path, index=False, encoding=encoding['encoding'])
    print('finished')





# record matching function
def record_matching(webpage, file_dir, name_file, name_save, driver='Firefox'):

    # THIS IS WITH SELENIUM, BUT IT WOULD BE MORE CONVENIENT WITH THE API
    
    ##  # defines profile and browser
    if driver=='Firefox':
        
##      # profile for autosaving (Firefox)
        profile = wd.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", file_dir)

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
                 "download.default_directory": file_dir,
                 'download.directory_upgrade': True,}
        profile.add_experimental_option('prefs', prefs)

##      # start webdriver 
        browser = wd.Chrome(profile)
        
    else:
        raise SystemExit

##  # get webpage
    browser.get(webpage)
    time.sleep(5)

##  # accept cookies
    browser.find_element_by_class_name("btn-continue").click()

##  # select match by organization
    browser.find_element_by_id("type-organization").click()

##  # input csv for search
    file_input = browser.find_element_by_xpath("/html/body/div[3]/section/div/div[2]/div[1]/form/div[1]/input[2]")

    full_path = file_dir + name_file + '.csv'
    file_input.send_keys( full_path )
    time.sleep(1)

##  # start matching
    browser.find_element_by_id("show-matchresults").click()
    time.sleep(20) # wait enough

####  # download file of matches
##    file_output = browser.find_element_by_xpath('/html/body/div[3]/section/div/div[2]/div[3]/div[5]/div/button')
##
##    full_path = file_dir + name_save + '.csv'
##    file_output.send_keys( os.path.abspath(full_path) )

    
    
##def record_donwload():
##    

### connection to API
##response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
##print(response_API.status_code)
####most know status of connection:
####    200 : OK. It means we have a healthy connection with the API on web.
####    204: It depicts that we can successfully made a connection to the API, but did not return any data from the service.
####    401 : Authentication failed!
####    403 : Access is forbidden by the API service.
####    404 : The requested API service is not found on the server/web.
####    500 : Internal Server Error has occurred.
####
####    for more see: https://httpstatusdogs.com/
##
##
### get text data
##data = response_API.text
##print(data[1:200])
##
##### convert to JASON data (key:value pairs)
####parse_json = json.loads(data)
####print(parse_json)
##
##### accessing info
####parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
