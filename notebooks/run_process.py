import sys
from bulk_download import *
from merge_csv import *
from API_match import *

# change working path
sys.path.append('/home/jriveraespejo/Desktop/project_europa/notebooks')

### bulk download
##web1 = "https://www.ecb.europa.eu/mopo/implement/app/html/index.en.html#cspp"
##save1 = '/home/jriveraespejo/Desktop/project_europa/data/raw'
##bulk_download(webpage=web1, save_dir=save1, file_type=filet)

### merge csv's
##file2 = "/home/jriveraespejo/Desktop/project_europa/data/raw"
file3 = "/home/jriveraespejo/Desktop/project_europa/data/processed/"
name1 = "CSPPholdings_201706_2021"
##merge_csv(file_dir=file2, save_dir=file3, file_name=name1)

# produce csv in permitID format
match_format(file_dir=file3, file_name=name1, save_dir=file3, save_name=name1)
