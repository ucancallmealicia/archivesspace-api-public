#python 3

#This script adds a container type - "reel" - to each top container of microfilm
#This test was done only on the use copies for now, since that's what I am primarily
#working on.

import csv
import requests
import json
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

filepath = input('Please enter path to input CSV: ')
outfile = input('Please enter path to output TXT: ')

with open(filepath, 'r', encoding= 'utf-8') as f:
    csvin = csv.reader(f)
    next(csvin, None)
    x = 0
    i = 0
    for row in csvin:
        top_container_uri = row[5]
        top_container_json = requests.get(api_url + top_container_uri, headers=headers).json()
        top_container_json['type'] = 'reel'
        top_container_data = json.dumps(top_container_json)
        top_container_update = requests.post(api_url + top_container_uri, headers=headers, data=top_container_data).json()
        with open(outfile, 'a') as txtout:
            for key, value in top_container_update.items():
                if key == 'status':
                    txtout.write('%s:%s\n' % (key, value))
                    x = x + 1
                    print(key, value)
                if key == 'uri':
                    txtout.write('%s:%s\n' % (key, value) + '\n')
                    print(key, value)
                if key == 'error':
                    txtout.write('%s:%s\n' % (key, value))
                    print(key, value)
            i = i + 1
            txtout.write('\n' + 'Total update attempts: ' + str(i) + '\n')
            txtout.write('Records updated successfully: ' + str(x) + '\n')
        txtout.close()

                                             
    
