def search_barcodes():
    values = login()
    csvfile = opencsv()
    csvoutfile = opencsvout()
    for row in csvfile:
        barcode = row[0]
        try:
            search = requests.get(values[0] + '/repositories/12/top_containers/search?q=barcode_u_sstr:' +  barcode, headers=values[1]).json()
            identifier = search['response']['docs'][0]['collection_identifier_stored_u_sstr'][0]
            title = search['response']['docs'][0]['collection_display_string_u_sstr'][0]
            if 'series_identifier_stored_u_sstr' in search['response']['docs'][0].keys():
                series = search['response']['docs'][0]['series_identifier_stored_u_sstr'][0]
            else:
                series = 'no_series'
            record_json = json.loads(search['response']['docs'][0]['json'])
            container_number = record_json['indicator']
            if 'container_profile_display_string_u_sstr' in search['response']['docs'][0].keys():
                container_profile = search['response']['docs'][0]['container_profile_display_string_u_sstr'][0]
            else:
                container_profile = 'no_container_profile'
            newrow = row + [barcode, series, identifier, title, container_profile, container_number]
            print(newrow)
            csvoutfile.writerow(newrow)
        except:
            print('Error! Could not retrieve record ' + str(row))
            csvoutfile.writerow(row)