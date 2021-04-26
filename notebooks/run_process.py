import sys
from bulk_download import *
from merge_csv import *
from API_match import *

# change working path
sys.path.append('/home/jriveraespejo/Desktop/project_europa/notebooks')

### bulk download
##web1 = "https://www.ecb.europa.eu/mopo/implement/app/html/index.en.html#cspp"
##save1 = '/home/jriveraespejo/Desktop/project_europa/data/raw'
##filet = "application/csv,text/csv,text/comma-separated-values"
##bulk_download(webpage=web1, save_dir=save1, file_type=filet, driver='Firefox')

### merge csv's
##file2 = "/home/jriveraespejo/Desktop/project_europa/data/raw"
file3 = "/home/jriveraespejo/Desktop/project_europa/data/processed/"
name1 = "CSPPholdings_201706_2021"
##merge_csv(file_dir=file2, save_dir=file3, file_name=name1)

# produce csv in permitID format
name2 = "format_CSPPcompanies_2017_2021"
match_format(file_dir=file3, file_name=name1, save_dir=file3, save_name=name2)

### match file
### WORK IN PROGRESS
##web2 = 'https://permid.org/match'
##name3 = 'matches_CSPPholdings_201706_2021'
##record_matching(webpage=web2, file_dir=file3, name_file=name2, name_save=name3, driver='Firefox')
