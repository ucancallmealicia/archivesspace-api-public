#Python 3

#This script updates locations which were incorrectly migrated into AS

#TO-DO - write log to file

import requests
import json
import csv
import getpass

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

#input so don't have to change path every time - DO NOT FORM AS A STRING, just input as is
input_file = input("Please enter path to input CSV: ")
#asks user to input path and file name for log file; name the file using a consistent format
outfile = input("Please enter path to output text file: ")

with open(input_file, 'r') as input_csv:
      csv_in = csv.reader(input_csv)
      next(csv_in, None)
      for row in csv_in:
            location_id = row[0]
            coordinate_1_label = row[1]
            coordinate_1_indicator = row[2]
            coordinate_2_label = row[3]
            coordinate_2_indicator = row[4]
            coordinate_3_label = row[5]
            coordinate_3_indicator = row[6]
            locations_to_update_json = requests.get(api_url + location_id, headers=headers).json()
            #Formulate updated json
            locations_to_update_json['building'] = 'SML'
            locations_to_update_json['coordinate_1_indicator'] = coordinate_1_indicator
            locations_to_update_json['coordinate_1_label'] = coordinate_1_label
            locations_to_update_json['coordinate_2_indicator'] = coordinate_2_indicator
            locations_to_update_json['coordinate_2_label'] = coordinate_2_label
            locations_to_update_json['coordinate_3_indicator'] = coordinate_3_indicator
            locations_to_update_json['coordinate_3_label'] = coordinate_3_label
            location_update_data = json.dumps(locations_to_update_json)
            location_update = requests.post(api_url+location_id, headers=headers, data=location_update_data).json()
            with open(outfile, 'a') as txtout:
                for key, value in location_update.items():
                      if key == 'status':
                            txtout.write('%s:%s\n' % (key, value))
                            print(key, value)
                      if key == 'uri':
                            txtout.write('%s:%s\n' % (key, value) + '\n')
                            print(key, value)
                      if key == 'error':
                            txtout.write('%s:%s\n' % (key, value))
                            print(key, value)
            txtout.close()

print('All Done!')
