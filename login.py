#/usr/bin/python3
#~/anaconda3/bin/python

#This script logs a user into the ArchivesSpace API

import requests,json

def login():
    api_url = input('Please enter the ArchivesSpace API URL: ')
    username = input('Please enter your username: ')
    password = input('Please enter your password: ')
    auth = requests.post(api_url+'/users/'+username+'/login?password='+password).json()
    #if session object is returned then login was successful; if not it failed.
    if 'session' in auth:
        session = auth["session"]
        headers = {'X-ArchivesSpace-Session':session, 'Content_Type': 'application/json'}
        print('Login successful!')
        return (api_url, headers)
    else:
        print('Login failed! Check credentials and try again')
        return

if __name__ == '__main__':
    login()
