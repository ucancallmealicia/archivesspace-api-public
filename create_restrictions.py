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

def create_rights_restrictions():
    values = login()
    csvfile = opencsv()
    txtfile = opentxt()
    for row in csvfile:
        record_uri = row[0]
        persistent_id = row[1]
        begin = row[2]
        end = row[3]
        local_type = row[4]
        note_type = row[5]
        record_json = requests.get(values[0] + record_uri, headers=values[1]).json()
        new_restriction = {'begin': begin, 'end': end, 'local_access_restriction_type': [local_type],
                           'restriction_note_type': note_type, 'jsonmodel_type': 'rights_restriction'}
        for note in record_json['notes']:
            if note['persistent_id'] == persistent_id:
                note['rights_restriction'] = new_restriction
        record_data = json.dumps(record_json)
        record_update = requests.post(values[0] + record_uri, headers=values[1], data=record_data).json()
        writetxt(txtfile, record_update)
        print(record_update)