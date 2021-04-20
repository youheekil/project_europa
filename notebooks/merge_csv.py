import os, glob, re
import pandas as pd
import re

# function merge_csv
def merge_csv(save_dir, file_dir, file_name):
##      # location
        os.chdir(file_dir)
                
##      # list files
        all_files = [i for i in glob.glob("*.csv")]

##      # regular expression for date
        regex = re.compile(r'\d+')       

##      # iterating through data
        all_df = []
        for file in all_files:
##              # load data frame
                df = pd.read_csv(file, sep=',', encoding='latin1')

##              # eliminating unnecessary columns
                if df.shape[1] > 5:
                        df.drop(df.iloc[:, 5:], inplace=True, axis=1)

##              # equalizing column names
                df.columns = ['NCB','ISIN_CODE','ISSUER_NAME','MATURITY_DATE','COUPON_RATE']

##              # adding file date
                df['file_date'] = regex.findall(file) * df.shape[0]

##              # merging
                all_df.append(df)
                merged_df = pd.concat(all_df, ignore_index=True, sort=True)

##      # saving data
        full_path = save_dir + file_name + '.csv'
        merged_df.to_csv(full_path, index=False)
        print('finished')
        
