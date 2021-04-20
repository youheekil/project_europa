import sys
sys.path.append('/home/jriveraespejo/Desktop/project_europa/notebooks')
from bulk_download import *
from merge_csv import *

### bulk download
##web = "https://www.ecb.europa.eu/mopo/implement/app/html/index.en.html#cspp"
##save = '/home/jriveraespejo/Desktop/project_europa/data/raw'
##files = "application/csv,text/csv,text/comma-separated-values"
##bulk_download(webpage=web, save_dir=save, file_type=files, driver='Firefox')

# join data
file_ = "/home/jriveraespejo/Desktop/project_europa/data/raw"
save_ = "/home/jriveraespejo/Desktop/project_europa/data/processed/"
name_ = "CSPPholdings_201706_2021"
merge_csv(save_dir=save_, file_dir=file_, file_name=name_)
