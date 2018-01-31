import csv
import requests
import json


def login():
    api_url = input('Please enter the ArchivesSpace API URL: ')
    username = input('Please enter your username: ')
    password = input('Please enter your password: ')
    auth = requests.post(api_url+'/users/'+username+'/login?password='+password).json()
    #if session object is returned then login was successful; if not it failed.
    if 'session' in auth:
        session = auth["session"]
        headers = {'X-ArchivesSpace-Session':session}
        print('Login successful!')
        return (api_url, headers)
    else:
        print('Login failed! Check credentials and try again')
        return

def opencsv():
    '''This function opens a csv file'''
    input_csv = input('Please enter path to CSV: ')
    file = open(input_csv, 'r', encoding='utf-8')
    csvin = csv.reader(file)
    next(csvin, None)
    return csvin

def opentxt():
    filepath = input('Please enter path to output text file: ')
    filename = open(filepath, 'a' )
    return filename

def writetxt(file, jsonname):
    for key, value in jsonname.items():
        if key == 'status':
            file.write('%s:%s\n' % (key, value))
        if key == 'uri':
            file.write('%s:%s\n' % (key, value) + '\n')
        if key == 'error':
            file.write('%s:%s\n' % (key, value) + '\n')

def replace_note_by_id():
    #replaces a note's content in ArchivesSpace using a persistent ID
    values = login()
    csvfile = opencsv()
    txtfile = opentxt()
    for row in csvfile:
        record_uri = row[0]
        persistent_id = row[1]
        note_text = row[2]
        resource_json = requests.get(values[0] + record_uri, headers=values[1]).json()
        for note in resource_json['notes']:
            if note['jsonmodel_type'] == 'note_multipart':
                if note['persistent_id'] == persistent_id:
                    note['subnotes'][0]['content'] = note_text
            elif note['jsonmodel_type'] == 'note_singlepart':
                if note['persistent_id'] == persistent_id:
                    note['content'] = [note_text]
        resource_data = json.dumps(resource_json)
        resource_update = requests.post(values[0] + record_uri, headers=values[1], data=resource_data).json()
        writetxt(txtfile, resource_update)
        print(resource_update)

replace_note_by_id()
