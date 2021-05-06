import sys, time
from API_match import *
from API_pull import *

# change working path
sys.path.append('/home/jriveraespejo/Desktop/project_europa/notebooks')

# combine information
# (DO NOT RUN BEFORE manual matching of companies)
file3 = "/home/jriveraespejo/Desktop/project_europa/data/processed/"
name1 = "CSPPholdings_201706_2021"
##match_info(file_dir=file3, file_name=name1, save_dir=file3, save_name=name1)

### extract information (1st form)
user = 'your_username'
word = 'your_password'
web_main = 'https://permid.org/'

### first run
### it takes nerly 3 hours
##match_data(wm=web_main, un=user, pw=word, rows=range(441), round_=1,
##           file_dir=file3, file_name=name1, save_dir=file3, save_name=name1)

### re-check the ones not found (just as a precaution)
match_data(wm=web_main, un=user, pw=word, rows=range(441), round_=2,
           file_dir=file3, file_name=name1, save_dir=file3, save_name=name1)
