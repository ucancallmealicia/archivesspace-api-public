#Python 3

#This script changes 'inclusive' dates to 'single' dates in resource records using a CSV of resource URIs as input

#Use get_dates SQL query to return URIs needed for this script

#TO-DO - write log to file

import requests
import json
import csv
import getpass

#login business
def login (api_url, username, password):
    '''This function logs into the ArchivesSpace REST API returning an acccess token'''
    auth = requests.post(api_url+'/users/'+username+'/login?password='+password).json()
    session = auth["session"]
    headers = {'X-ArchivesSpace-Session':session}
    return headers

if __name__ == '__main__':
    api_url = input('Please enter the URL for the ArchivesSpace API: ')
    username = getpass.getuser()
    check_username = input('Is your username ' + username + '?: ')
    if check_username.lower() not in ('y', 'yes', 'yep', 'you know it'):
        username = input('Please enter ArchivesSpace username:  ')
    password = getpass.getpass(prompt=username + ', please enter your ArchivesSpace Password: ', stream=None)
    print('Logging in', api_url)
    headers = login(api_url, username, password)
    if headers != '':
        print('Success!')
    else:
        print('Ooops! something went wrong')

    #enter full path to CSV file
    input_file = input("Please enter path to input CSV: ")

    with open(input_file, 'r', encoding='utf-8') as input_csv:
          csv_in = csv.reader(input_csv)
          #skips header row
          next(csv_in, None)
          #loops through each resource URI in the CSV file
          for row in csv_in:
              resource_uri = row[0]
              #looks up URI and stores JSON
              resource_to_update_json = requests.get(api_url + resource_uri, headers=headers).json()
              #loops through all dates in resource JSON 
              for date in resource_to_update_json['dates']:
                  #if there is no end date, change date type to single
                  if 'end' not in date:
                      date['date_type'] = 'single'
                  #if the end date is the same as the begin date, change date type to single
                  elif date['end'] == date['begin']:
                      date['date_type'] = 'single'
              #turn back into JSON, post to ArchivessSpace
              resource_update_data = json.dumps(resource_to_update_json)
              resource_update = requests.post(api_url+ resource_uri, headers=headers, data=resource_update_data).json()
              print(resource_update)
          
          
