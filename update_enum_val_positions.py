#!/usr/bin/env python3
import requests
import json
import getpass
import csv

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

input_file = input('Please enter path to input CSV: ')

file = open(input_file, 'r', encoding='utf-8')
csvin = csv.reader(file)
next(csvin, None)
for row in csvin:
    enum_val_uri = row[0]
    desired_position = row[1]
    enum_vals = requests.get(api_url + enum_val_uri, headers=headers).json()
    enum_val_json = requests.post(api_url + enum_val_uri + '/position?position=' + desired_position, headers=headers, data=json.dumps(enum_vals)).json()
    print(enum_val_json)
