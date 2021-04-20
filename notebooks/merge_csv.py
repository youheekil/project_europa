import os
import glob
import pandas as pd
import re



# function merge_csv
def merge_csv(save_dir, file_dir, file_ext, file_name):
##      # location
        os.chdir(file_dir)
                
        # list files
        all_files = [i for i in glob.glob(f"*{file_ext}")]

        all_df = []
        for file in all_files:
            df = pd.read_csv(file, sep=',')
##            print(file)
            df['date'] = os.path.split(file)[-1]
            print(os.path.split(file)[-1])
##            all_df.append(df)
##
##      combined_csv_data.to_csv('combined_csv_data.csv')


file_ = "/home/jriveraespejo/Desktop/project_europa/data/raw"
save_ = "/home/jriveraespejo/Desktop/project_europa/data/processed"
name_ = "CSPPholdings"
ext_ = ".csv"
merge_csv(save_dir=save_, file_dir=file_, file_ext=ext_, file_name=name_)
