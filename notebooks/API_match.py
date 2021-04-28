# libraries
import pandas as pd
import json, re, chardet, string, time, requests


############################################
# clean_weird function
############################################
def clean_weird(vector_dirty, basic=1):
##  # remove weird symbols
    if basic==1:
        vector_clean = vector_dirty.str.strip()
        vector_clean = vector_clean.str.replace('-', ' ')
        vector_clean = vector_clean.str.replace('\s{2,}', ' ')
        vector_clean = vector_clean.str.replace('á', 'a')
        vector_clean = vector_clean.str.replace('ã', 'a')
        vector_clean = vector_clean.str.replace('ä', 'a')
        vector_clean = vector_clean.str.replace('é', 'e')
        vector_clean = vector_clean.str.replace('ë', 'e')
        vector_clean = vector_clean.str.replace('É', 'E')
        vector_clean = vector_clean.str.replace('í', 'i')
        vector_clean = vector_clean.str.replace('ó', 'o')
        vector_clean = vector_clean.str.replace('ö', 'o')
        vector_clean = vector_clean.str.replace('ü', 'u')
        vector_clean = vector_clean.str.replace('ñ', 'n')
        vector_clean = vector_clean.str.replace('(,\s\w+)$', '')
        vector_clean = vector_clean.str.replace('[{}]'.format(string.punctuation), '')

##      # to lower
        vector_clean = vector_clean.str.lower()

##  # remove company designations
##  # see:
##  # https://www.corporateinformation.com/Company-Extensions-Security-Identifiers.aspx
##  # https://www.nathantrust.com/insights/comprehensive-guide-to-a-designated-activity-company-dac
    elif basic==2:
##      # it assumes it is in 'lowercase'
        s_chars = r'(\s(ag|as|sa|sl|sas|spa|sca|sau|sanv|sarl|se|scs|nv|bv|nvsa|ltd|plc|oyj|dac|(g)mbh))$'
        vector_clean = vector_dirty.str.replace(s_chars, '')

        s_chars = r'(\s((sa\s\w+)|(socand\w+)))$'
        vector_clean = vector_clean.str.replace(s_chars, '')
        
    return(vector_clean)



############################################
# match_fromat function
############################################
def match_format(file_dir, file_name, save_dir, save_name):
##  # full path for file
    full_path = file_dir + file_name + '.csv'
    
    # check encoding of files: open first 10'000 bytes                 
    with open(full_path, 'rb') as rawdata:
        encoding = chardet.detect(rawdata.read(10000))
##    print(encoding)
##    # 73% of confidence
        
##  # load data
    df = pd.read_csv(full_path, sep=',', encoding=encoding['encoding'])

##  # clean names
    df["Name"] = clean_weird( df['ISSUER_NAME'], basic=1 )
##    df["Name"] = clean_weird( df["Name"], basic=2 ) # to decide on
    
##  # remove duplicates and sort
    df = df.drop_duplicates(subset=['Name'])
    df = df.sort_values(by=['Name'])

##  # put info in the right format    
##  # see https://permid.org/match: 'Organization' and 'Download Template' buttons
    df = df.drop(['COUPON_RATE','ISIN_CODE','MATURITY_DATE','NCB','file_date'], axis = 1)
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

##  # re-order columns  
    df = df[['LocalID','Standard Identifier','Name','Country','Street','City','PostalCode','State','Website']]

##  # saving data
    full_path = save_dir + save_name + '.csv'
    df.to_csv(full_path, index=False, encoding=encoding['encoding'])
    print('finished')




############################################
# record matching function
############################################
def match_api(webpage, api_key, file_dir, name_file, name_save):
##  # WORK IN PROGRESS
##  # WEB PAGE ONLY SHOWS HOW TO DO IT IN JAVA
    
##  # connection to API
##  # followed this (without success):
##  # https://www.geeksforgeeks.org/get-post-requests-using-python/

    # file location
    full_path = file_dir + file_name + '.csv'
  
    # data to be sent to api
    parameters = {'x-openmatch-dataType': 'Organization',
                  'X-AG-Access-Token': api_key,
                  'Content-Type': 'form-data',
                  'x-openmatchnumberOfMatchesPerRecord': 1}
  
    # sending post request and saving response as response object
    data = requests.post(url=webpage, data=parameters)
##  # most know status of connection:
##  # 200 : OK. It means we have a healthy connection with the API on web.
##  # 204: It depicts that we can successfully made a connection to the API, but did not return any data from the service.
##  # 401 : Authentication failed!
##  # 403 : Access is forbidden by the API service.
##  # 404 : The requested API service is not found on the server/web.
##  # 500 : Internal Server Error has occurred.
##
##  # for more see: https://httpstatusdogs.com/

  
    # extracting response text 
    print( data.text )
    


############################################
# data extraction function
############################################
