import sys
from bulk_download import *
from merge_csv import *
from API_match import *
from API_pull import *

# change working path
sys.path.append('/home/jriveraespejo/Desktop/project_europa/notebooks')


# bulk download
# download all ECB files into raw folder
web1 = "https://www.ecb.europa.eu/mopo/implement/app/html/index.en.html#cspp"
save1 = '/home/jriveraespejo/Desktop/project_europa/data/raw'
##bulk_download(webpage=web1, save_dir=save1, file_type=filet)


# merge csv's
# produced files: '1_CSPPholdings_201706_2021.csv'
file2 = "/home/jriveraespejo/Desktop/project_europa/data/raw"
file3 = "/home/jriveraespejo/Desktop/project_europa/data/processed/"
name1 = "CSPPholdings_201706_2021"
##merge_csv(file_dir=file2, save_dir=file3, file_name=name1)


# produce csv in permitID format
# produced files: '2_main_', '2_with_', '2_without_'
##match_format(file_dir=file3, file_name=name1, save_dir=file3, save_name=name1)


# Manual matching in 'https://permid.org/match'
# produced files: '3_with_', '3_without_'


# combine information
# (DO NOT RUN BEFORE manual matching of companies)
# produced files: '4_main_'
file3 = "/home/jriveraespejo/Desktop/project_europa/data/processed/"
name1 = "CSPPholdings_201706_2021"
##match_info(file_dir=file3, file_name=name1, save_dir=file3, save_name=name1)


# extract information
# produced files: '5_info_match_round1_', '5_info_match_round2_'
user = 'your_username'
word = 'your_password'
web_main = 'https://permid.org/'

# first run
# it takes nerly 3 hours
match_data(wm=web_main, un=user, pw=word, rows=range(441), round_=1,
           file_dir=file3, file_name=name1, save_dir=file3, save_name=name1)

# re-check the ones not found (just as a precaution)
match_data(wm=web_main, un=user, pw=word, rows=range(441), round_=2,
           file_dir=file3, file_name=name1, save_dir=file3, save_name=name1)

