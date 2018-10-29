#/usr/bin/python3
#~/anaconda3/bin/python

import utilities, requests, json, logging

def merge_records(record_type):
    starttime = time.time()
    values = utilities.login()
    csvfile = utilities.opencsv()
    dirpath = utilities.setdirectory()
    x = 0
    for i, row in enumerate(csvfile, 1):
        try:
            target = row[0]
            victims = row[1]
            victim_backup = requests.get(values[0] + victims, headers=values[1]).json()
            if 'error' in victim_backup:
                logging.debug('error: could not retrieve ' + str(victim_backup))
                logging.debug(str(victim_backup.get('error')))
            outfile = utilities.openjson(dirpath, victims[1:].replace('/','_'))
            json.dump(victim_backup, outfile)
            victim_refs = [{'ref': victim} for victim in victims.split(', ')]
            merge_json = {'target': {'ref': target}, 
                          'victims': victim_refs, 
                          'jsonmodel_type': 'merge_request'}
            merge_dump = json.dumps(merge_json)
            merge_request = requests.post(values[0] + '/merge_requests/' + str(record_type), headers=values[1], data=merge_dump).json()
            print(merge_request)
            if 'status' in merge_request:
                    x += 1
            if 'error' in merge_request:
                    logging.debug(str(target))
                    logging.debug('log: ' + str(merge_request.get('error')))   
        except Exception as exc:
            print(target)
            print(traceback.format_exc())
            logging.debug(target)
            logging.exception('Error: ')
            continue
    logging.debug('Total update attempts: ' + str(i))
    #add count of successful updates to log file
    logging.debug('Records updated successfully: ' + str(x))
    utilities.keeptime(starttime)
    print('All Done!')

if __name__ == "__main__":
    utilities.error_log()
    merge_records()