# libraries
import pandas as pd
import json, re, chardet, string, time, requests


############################################
# match_format function
############################################
def match_format(file_dir, file_name, save_dir, save_name):
    
##  # full path for file
    full_path = file_dir + file_name + '.csv'
    
##  # check encoding of files: open first 10'000 bytes                 
    with open(full_path, 'rb') as rawdata:
        encoding = chardet.detect(rawdata.read(10000))
##    print(encoding)
##    # 73% of confidence
        
##  # load data
    df = pd.read_csv(full_path, sep=',', encoding=encoding['encoding'])

##  # put info in the right format    
##  # see https://permid.org/match:
##  # 'Organization' and 'Download Template' buttons
    df = df.drop(['COUPON_RATE','ISIN_CODE','ISSUER_NAME','MATURITY_DATE','NCB','file_date'], axis = 1)
##  # drop NCB (country) as it has missmatchs
    
##  # add empty info
    df['LocalID'] = ''
    df['Standard Identifier'] = ''
    df['Country'] = ''
    df['Street'] = ''
    df['City'] = ''
    df['PostalCode'] = ''
    df['State'] = ''
    df['Website'] = ''

##  # remove duplicates and sort
    df = df.drop_duplicates(subset=['Name1','Name2'])
    df = df.sort_values(by=['Name1'])
    
##  # re-order columns
##  # names with and without company designations
    df_main = df[['Name1','Name2']]
    
##  # names with company designations
    df_with = df[['LocalID','Standard Identifier','Name1','Country','Street','City','PostalCode','State','Website']]
    df_with.rename(columns={"Name1":"Name"}, inplace=True)

##  # names without company designations    
    df_without = df[['LocalID','Standard Identifier','Name2','Country','Street','City','PostalCode','State','Website']]
    df_without.rename(columns={"Name2":"Name"}, inplace=True)
    
##  # saving data
    full_path = '2_' + save_dir + 'main_' + save_name + '.csv'
    df_main.to_csv(full_path, index=False, encoding=encoding['encoding'])

    full_path = '2_' + save_dir + 'with_' + save_name + '.csv'
    df_with.to_csv(full_path, index=False, encoding=encoding['encoding'])

    full_path = '2_' + save_dir + 'without_' + save_name + '.csv'
    df_without.to_csv(full_path, index=False, encoding=encoding['encoding'])

    print('finished')



############################################
# match_info function
############################################
def match_info(file_dir, file_name, save_dir, save_name):

##  # paths for all files
    full_path1 = '2_' + file_dir + 'main_' + file_name + '.csv'
    full_path2 = '3_' + save_dir + 'with_match_' + file_name + '.csv'
    full_path3 = '3_' + save_dir + 'without_match_' + file_name + '.csv'

##  # check encoding of files: open first 10'000 bytes                 
    with open(full_path2, 'rb') as rawdata: # the most common file
        encoding = chardet.detect(rawdata.read(10000))
##    print(encoding)
##    # 73% of confidence
        
##  # load data
    df_main = pd.read_csv(full_path1, sep=',', encoding=encoding['encoding'])

    df_with = pd.read_csv(full_path2, sep=',', encoding=encoding['encoding'])
    df_with.rename(columns={"Match OpenPermID":'OpenPermID_1',
                            'Match OrgName':'OrgName_1',
                            'Match Score':'Score_1',
                            'Match Level':'Level_1'}, inplace=True)

    df_without = pd.read_csv(full_path3, sep=',', encoding=encoding['encoding'])
    df_without.rename(columns={"Match OpenPermID":'OpenPermID_2',
                               'Match OrgName':'OrgName_2',
                               'Match Score':'Score_2',
                               'Match Level':'Level_2'}, inplace=True)

##  # add columns of interest
    df_final = pd.DataFrame([])
    df_final['Name_1'] = df_main['Name1']
    df_final = df_final.join( df_with.iloc[:,1:5] )
    df_final['Name_2'] = df_main['Name2']
    df_final = df_final.join( df_without.iloc[:,1:5] )
    df_final['EqualOrgName'] = ( df_final['OrgName_1'] == df_final['OrgName_2'] )

##  # saving data
    full_path = '4_' + save_dir + 'main_match_' + save_name + '.csv'
    df_final.to_csv(full_path, index=False, encoding=encoding['encoding'])

    print('finished')
    
