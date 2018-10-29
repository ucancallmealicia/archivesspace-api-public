#!/usr/bin/env python3

#deletes notes from a resource using a CSV containing the resource URI and the persistent ID of the note to be deleted

import utilities, time, requests, json

def delete_notes():
    starttime = time.time()
    csvfile = utilities.opencsv()
    api_url, headers = utilities.login()
    dirpath = utilities.setdirectory()
    for i, row in enumerate(csvfile, 1):
        try:
            record_uri = row[0]
            persistent_id = row[1]
            record_json = requests.get(api_url + record_uri, headers=headers).json()
            if 'error' in record_json:
                logging.debug('error: could not retrieve ' + str(record_uri))
                logging.debug(str(record_json.get('error')))
            outfile = openjson(dirpath, record_uri[1:].replace('/','_'))
            json.dump(record_json, outfile)
            for note in record_json['notes']:
                if note['persistent_id'] == persistent_id:
                    #which one is right? should be clear, since it's a dict?
                    #del note
                    note.clear()
            record_data = json.dumps(record_json)
            record_update = requests.post(api_url + record_uri, headers=headers, data=record_data).json()
        except Exception as exc:
            logging.debug(record_uri)
            logging.exception('Error: ')
            print(record_uri)
            print(traceback.format_exc())
    logging.debug('Total update attempts: ' + str(i))
    logging.debug('Records updated successfully: ' + str(x))
    print('All Done!')
    print('Total update attempts: ' + str(i))
    print('Records updated successfully: ' + str(x))
    utilities.keeptime(starttime)

if __name__ == "__main__":
    utilities.error_log()
    delete_notes()
