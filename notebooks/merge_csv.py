import os, glob, re, chardet
import pandas as pd
from statistics import mode

# function merge_csv
def merge_csv(save_dir, file_dir, file_name):
##      # location
        os.chdir(file_dir)
                
##      # list files
        all_files = [i for i in glob.glob("*.csv")]

##      # regular expression for date
        regex = re.compile(r'\d+')

##      # iterating through data
        all_df = [] # to concatenate all data
        encode = [] # to save all encodings
        
        for file in all_files:
##              # check encoding of files: open first 10'000 bytes                 
                with open(file, 'rb') as rawdata:
                        encoding = chardet.detect(rawdata.read(10000))
##                print(encoding)
##                # 73% of confidence in each file
                        
                encode.append(encoding['encoding']) # to use in final file

##              # load data frame
                df = pd.read_csv(file, sep=',', encoding=encoding['encoding'])

##              # eliminating unnecessary columns
##              # some files have extra empty colums
                if df.shape[1] > 5:
                        df.drop(df.iloc[:, 5:], axis=1, inplace=True)

##              # equalizing column names
                df.columns = ['NCB','ISIN_CODE','ISSUER_NAME','MATURITY_DATE','COUPON_RATE']
                
##              # eliminating noninformative rows
                idxNum = df[ df.ISIN_CODE.isnull() & df.ISSUER_NAME.isnull() & df.MATURITY_DATE.isnull() ].index
                df = df.drop(index=idxNum)
                
##              # adding file date
                df['file_date'] = regex.findall(file) * df.shape[0]

##              # merging
                all_df.append(df)
                merged_df = pd.concat(all_df, ignore_index=True, sort=True)

##      # sorting by date
        merged_df = merged_df.sort_values(by='file_date')
        
##      # saving data
##      # use most repeated encoding
        final_encode = mode(encode)
        full_path = save_dir + file_name + '.csv'
        merged_df.to_csv(full_path, index=False, encoding=final_encode)
        print('finished')
