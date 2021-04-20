# packages
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
import time


# handle StaleElementReferenceException
def handle_stale(b, e, cn, i):
    try:
        Select(e).select_by_index( i )
    except exceptions.StaleElementReferenceException:
        e = b.find_element_by_class_name( cn )
        Select( e ).select_by_index( i )


# handle ElementNotInteractableException
def handle_noclick(b, xp, id_):
    try:
        b.find_element_by_xpath( xp ).click()
        b.find_element_by_id( id_ ).click()
    except exceptions.ElementNotInteractableException:
        pass
    except exceptions.NoSuchElementException:
        pass
    


# bulk download
def bulk_download(webpage, save_dir, file_type, driver='Firefox'):

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
##      WORK IN PROGRESS
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


##  # get webpage
    browser.get(webpage)
    time.sleep(1)

##  # accept cookies
    browser.find_element_by_class_name("check").click()

##  # open dropdown historical
    browser.execute_script("window.scrollTo(0,7500)")
    browser.find_element_by_xpath("/html/body/div[2]/main/div[8]/div[1]").click()
    
##  # select years, months and days
##  # element: year
    yEl = browser.find_element_by_class_name("ui-datepicker-year")
    yOp = yEl.find_elements_by_tag_name("option")

    for y in range( len(yOp) ):
        year = 2017 + y
        handle_stale(b=browser, e=yEl, cn="ui-datepicker-year", i=y)
       
##      # element: month
        mEl = browser.find_element_by_class_name("ui-datepicker-month")
        mOp = mEl.find_elements_by_tag_name("option")

        for m in range( len(mOp) ):
            if y==0:
                month = m + 6
            else:
                month = m + 1
            
            handle_stale(b=browser, e=mEl, cn="ui-datepicker-month", i=m)

##          # element: day of the week
            main_xpath = "/html/body/div[2]/main/div[8]/div[2]/div/div/div/table/tbody/"

            for w in range(6):
                w_day = "tr[" + str(w + 1) + "]/td[5]" # '5' means active
                w_xpath = main_xpath + w_day
                calButton = "download_calendarButton"
                handle_noclick(b=browser, xp=w_xpath, id_=calButton)
       
##              # check
                print("donwload correspondos to: %s/%s, week: %s" % (year, month, w) )
                
    browser.quit()
    
