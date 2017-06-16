#!/usr/bin/env python3

#This is a script to link existing top container instances from Yale's microfilm collections (HM XXX)
#to the MS/RU archival objects with which they are associated.

#use at your own risk - work in progress

#import modules we need in script
import requests
import json
import getpass
import csv
import time

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

startit = True
def start():

    #starts runtime calculation
    startTime = time.time()

    #input so don't have to change path every time - DO NOT FORM AS A STRING, just input as is
    input_csv = input("Please enter path to input CSV: ")
    #asks user to input path and file name for log file; name the file using a consistent format i.e ms.xxxx.hm.xxx_log
    output_txt = input("Please enter path to output text file: ")

    #opens input spreadsheet for collection and log file
    with open((input_csv), 'r', encoding='UTF8') as csvfile, open(output_txt, 'w') as txtout:
        #reads CSV file into memory so we can act on it
        csvin = csv.reader(csvfile)
        #skips header row in CSV
        next(csvin, None)
        #variable to hold count of update attempts
        i = 0
        #variable to hold count of objects successfully updated
        x = 0
        #iterates through each row of the CSV containing archival object URIs matched with their HM reel data and
        #performs all of the actions in the indented area on each archival object
        for row in csvin:
                #need location URI for HM top containers to build JSON - this is in column 7 in CSV
                location = row[8]
                #also barcode for reel of HM microfilm for JSON - in column 5 of CSV
                barcode = row[6]
                #indicator (reel number) of HM top containers - column 4 of CSV
                indicator = row[5]
                #URI for HM film top container - column 6 of CSV
                top_container_uri = row[7]
                #URI for archival object to which HM reels are associated with
                archival_object_uri = row[4]
                #get MS/RU archival object JSON from API using archival object URI, decode it into a data type we can act upon in Python
                archival_object_json = requests.get(api_url+archival_object_uri, headers=headers).json()
                #create new JSON of top container instance from CSV data; uses HM data from spreadsheet
                #start date change
                new_instance = {"container": {"barcode_1": barcode, "container_locations": [{"jsonmodel_type": "container_location", 
                            "ref": location, "start_date": "2015-06-02", "status": "current"}], "indicator_1": indicator, "type_1": "box"}, 
                            "instance_type": "mixed_materials", "jsonmodel_type": "instance", "sub_container": {"jsonmodel_type": "sub_container", 
                            "top_container": {"ref": top_container_uri}}}
                #append HM instance data to MS/RU archival object JSON we pulled from API
                archival_object_json["instances"].append(new_instance)
                #delete child or grandchild instance - NEXT UP - will have to modify depending on whether microfilm was imported as a child
                #or grandchild. Don't want to delete indicator 2s if the film was imported as a grandchild, as this would delete folder refs
                for key, valuelist in archival_object_json.items():
                    if key == 'instances':
                        for datadict in valuelist:
                            for subkey, subvalue in datadict.items():
                                if type(subvalue) is dict:
                                    newdict = {k:v for k,v in subvalue.items()}
                                    for subsubkey, subsubvalue in newdict.items():
                                        if subsubkey == 'indicator_3':
                                            del subvalue['indicator_3']
                                        if subsubkey == 'type_3':
                                            del subvalue['type_3']
                #print(type(archival_object_json))
                #turn the data we've been working with back into JSON that the API can read
                archival_object_data = json.dumps(archival_object_json)
                #print(archival_object_data)# - can comment out post and uncomment this to check to make sure everything looks ok before we do stuff
                #if all looks good above, this will post update back to AS 
                archival_object_update = requests.post(api_url+archival_object_uri, headers=headers, data=archival_object_data).json()
                #another for loop which writes what's happening to a text file and counts number of updated records
                for key, value in archival_object_update.items():
                    if key == 'status':
                        txtout.write('%s:%s\n' % (key, value))
                        x = x +1
                    if key == 'uri':
                        txtout.write('%s:%s\n' % (key, value) + '\n')
                    if key == 'error':
                        txtout.write('%s:%s\n' % (key, value))
                #prints what's happening in IDLE window
                print(archival_object_update)
                #each time the loop runs through it adds to this variable - a count of archival objects acted upon
                i = i + 1
        #add total count of apdate attempts to log file
        txtout.write('\n' + 'Total update attempts: ' + str(i) + '\n')
        #add count of successful updates to log file
        txtout.write('Records updated successfully: ' + str(x) + '\n')
        #finish calculating script runtime - including login and input time
        elapsedTime = time.time() - startTime
        m, s = divmod(elapsedTime, 60)
        h, m = divmod(m, 60)
        #add runtime to log file
        txtout.write('Total time elapsed, including login and input: ')
        txtout.write('%d:%02d:%02d' % (h, m, s))
        #recspermin = x/int(m,s)
        #txtout.write(recspermin)
        #close log file
        txtout.close()

    print('All Done!')

while startit:
    start()
