# libraries
import requests, json

# connection to API
response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
print(response_API.status_code)
##most know status of connection:
##    200 : OK. It means we have a healthy connection with the API on web.
##    204: It depicts that we can successfully made a connection to the API, but did not return any data from the service.
##    401 : Authentication failed!
##    403 : Access is forbidden by the API service.
##    404 : The requested API service is not found on the server/web.
##    500 : Internal Server Error has occurred.
##
##    for more see: https://httpstatusdogs.com/


# get text data
data = response_API.text
print(data[1:200])

### convert to JASON data (key:value pairs)
##parse_json = jason.loads(data)
##print(parse_json)

### accessing info
##parse_json['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
