#!/usr/bin/env python3

#deletes notes from a resource using a CSV containing the resource URI and the persistent ID of the note to be deleted

#import modules we need in script
import requests
import json
import getpass
import csv

#ArchivesSpace API login script from Mark Custer - asks for login info and connects to API
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

input_csv = input('Please enter path to CSV: ')

with open(input_csv, 'r', encoding='utf-8') as csvfile:
    csvin = csv.reader(csvfile)
    next(csvin, None)
    for row in csvin:
        resource_uri = row[0]
        persistent_id = row[1]
        resource_json = requests.get(api_url + resource_uri, headers=headers).json()
        for key, valuelist in resource_json.items():
            if key == 'notes':
                for i in valuelist:
                    newdict = {k:v for k,v in i.items()}
                    for key, value in newdict.items():
                        if value == persistent_id:
                            i.clear()
        resource_data = json.dumps(resource_json)
        resource_update = requests.post(api_url + resource_uri, headers=headers, data=resource_data).json()
        print(resource_update)
