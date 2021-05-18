import os, glob, re, chardet
import pandas as pd
from statistics import mode


############################################
# clean_weird function
############################################
def clean_weird(vector_dirty, extra=False):

##  # ============================        
##  # ORDER MATTERS HERE
##  # ============================ 
##  # strip and to lower
    vector_clean = vector_dirty.str.strip()
    vector_clean = vector_clean.str.lower()

##  # city names at the end
    vector_clean = vector_clean.str.replace(r'(,\s\w+(\s\w+)?)$', '', regex=True)

##  # ============================
##  # remove weird symbols
##  # ============================
    vector_clean = vector_clean.str.replace(r'á','a', regex=True)
    vector_clean = vector_clean.str.replace(r'ã','a', regex=True)
    vector_clean = vector_clean.str.replace(r'ä','a', regex=True)
    vector_clean = vector_clean.str.replace(r'é','e', regex=True)
    vector_clean = vector_clean.str.replace(r'ë','e', regex=True)
    vector_clean = vector_clean.str.replace(r'É','E', regex=True)
    vector_clean = vector_clean.str.replace(r'í','i', regex=True)
    vector_clean = vector_clean.str.replace(r'ó','o', regex=True)
    vector_clean = vector_clean.str.replace(r'ö','o', regex=True)
    vector_clean = vector_clean.str.replace(r'ü','u', regex=True)
    vector_clean = vector_clean.str.replace(r'ñ','n', regex=True)
    
##  # ============================
##  # remove company designations
##  # ============================
##  # see:
##  # https://www.corporateinformation.com/Company-Extensions-Security-Identifiers.aspx
##  # https://www.nathantrust.com/insights/comprehensive-guide-to-a-designated-activity-company-dac
    if extra==True:

##      # combos: as,sl,scs,sa,sac,sau,sas,spa,sanv, etc. (with and without intermediate . or /)
        s_chars = r'(a\W?s\W?|s\W?((a|e|p|c|l)\W?)?((a|s|u)\W?)?\W?(n\W?v\W?)?(r\W?l\W?)?)$'
        vector_clean = vector_clean.str.replace(s_chars, '', regex=True)

##      # combos: nv,nvsa,bv,oyj,ltd, etc. (with and without intermediate . or /)
        s_chars = r'((n|b)\W?v\W{0,2}?(s\W?a\W?)?|o\W?y\W?j\W?|l\W?t\W?d\W?)$'
        vector_clean = vector_clean.str.replace(s_chars, '', regex=True)

##      # combos: cvba,ag,plc,dac, etc. (with and without intermediate . or /)
        s_chars = r'(c\W?v\W?b\W?a\W?|a\W?g\W?|p\W?l\W?c\W?|d\W?a\W?c\W?)$'
        vector_clean = vector_clean.str.replace(s_chars, '', regex=True)

##      # combos: ,(g)mbh, kgaa, etc. (with and without intermediate . or /)
        s_chars = r'((g\W?)?m\W?b\W?h\W?|k\W?g\W?a\W?a\W?)$'
        vector_clean = vector_clean.str.replace(s_chars, '', regex=True)

##      # specifics
        s_chars = r'(\W(sa)\s(\wt)\W(expl)\W(p)\W(g)\W(cl)\W)$'
        vector_clean = vector_clean.str.replace(s_chars, '', regex=True)
        
        s_chars = r'(\W(soc)\W(an)\W(d)\W(gest)\W(st)\W(d)\W(sec)\W)$'
        vector_clean = vector_clean.str.replace(s_chars, '', regex=True)

    vector_clean = vector_clean.str.replace(r'-',' ', regex=True)
    vector_clean = vector_clean.str.replace(r'\s{2,}',' ', regex=True)
    vector_clean = vector_clean.str.replace(r'[^\w\s]','', regex=True)
    vector_clean = vector_clean.str.strip()
    
    return(vector_clean)



############################################
# function merge_csv
############################################
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
                idxNum = df[ df.ISSUER_NAME.isnull() ].index
                df = df.drop(index=idxNum)

                idxNum = df.ISSUER_NAME.str.contains('(d|D)ummy')
                idxNum = idxNum.fillna(False)
                idxNum = df[ idxNum ].index
                df = df.drop(index=idxNum)
                
##              # adding file date
                df['file_date'] = regex.findall(file) * df.shape[0]

##              # merging
                all_df.append(df)
                merged_df = pd.concat(all_df, ignore_index=True, sort=True)

##      # sorting by date
        merged_df = merged_df.sort_values(by='file_date')

##      # creting column with new names
        merged_df["Name1"] = clean_weird( merged_df['ISSUER_NAME'], extra=False)
        merged_df["Name2"] = clean_weird( merged_df['ISSUER_NAME'], extra=True)
        
##      # saving data
##      # use most repeated encoding
        final_encode = mode(encode)
        full_path = '1_' + save_dir + file_name + '.csv'
        merged_df.to_csv(full_path, index=False, encoding=final_encode)
        
        print('finished')



############################################
# function merge_taxonomy
############################################
def merge_taxonomy(file_match, file_taxonomy, file_main, save_dir):

##  #-----------------------
##  # taxonomy data files
##  #-----------------------
##  # path for file
    full_path = file_taxonomy + 'sustainable-taxonomy_renewable.csv'
        
##  # load data
    df_green = pd.read_csv(full_path, sep=',')
    df_green['TRBC_6'] = df_green['TRBC_6'].astype(float).astype(str)
    # print( df_green )
    
##  #-----------------------
##  # match data files
##  #-----------------------
##  # path for file
    full_path1 = file_match + '5_info_match_round2_complete.csv'
    full_path2 = file_match + '6_info_match_round2_missing.csv'
        
##  # load data
    df_comp = pd.read_csv(full_path1, sep=',')
    df_miss = pd.read_csv(full_path2, sep=',')
##    print(df_comp)
##    print(df_miss)

##  # append data
    df_comp = df_comp.append(df_miss)
    df_comp['TRBC code'] = df_comp['TRBC code'].astype(float).astype(str)
##    print(df_comp)

##  # create 'green' economy column
    df_comp = df_comp.assign( green=df_comp['TRBC code'].isin(df_green.TRBC_6).astype(int) )
##    print( sum(df_comp.green) )

##  # save dataFrame
    full_path = save_dir + '7_info_match_round3_complete.csv'
    df_comp.to_csv(full_path, index=False)
    

##  #-----------------------
##  # main data files
##  #-----------------------
##  # path for file
    full_path = file_main + '1_CSPPholdings_201706_2021.csv'
        
##  # load data
    df_main = pd.read_csv(full_path, sep=',')

##  # merge 'TRBC code' and 'green' columns
    right_df = df_comp[['Name_1','Name_2','TRBC code','green']]
    right_df = right_df.rename(columns={"Name_1":"Name1", "Name_2":"Name2"})
    df_main = df_main.merge(right_df, on=['Name1','Name2'], how='left')
##    print(df_main)

##  # save dataFrame
    full_path = save_dir + '7_CSPPholdings_201706_2021.csv'
    df_main.to_csv(full_path, index=False)

    print('finished')
