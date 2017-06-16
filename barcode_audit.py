import pymysql
import csv
import pprint

print('Connecting to database...')

pw = #yourpassword

connection = pymysql.connect(host=#yourhost,
                             port = #yourport,
                             user=#yourusername,
                             password=pw,
                             db=#yourdb)

print('Connected!')

cursor = connection.cursor()

#create list from barcodes in text file

outfile = input('input the name of the file: ')

barcodelist = open(outfile, 'r')

barcodelisty = barcodelist.read().split('\n')

#print(barcodelisty)


#CAREFUL WITH THIS!!
#should do something like: if barcodelisty[-1] = '', else...
del barcodelisty[-1]

pprint.pprint(barcodelisty)

moveon = input('Please press enter to run query...')
print(moveon)

textfile = input('Please enter path to outputfile: ')

output = open(textfile, 'a')

csvfile = input('Please enter path to CSV: ')

for barcode in barcodelisty:
    print('querying ' + str(barcode))
    cursor.execute("""
        Select resource.ead_id AS EAD_ID
            , resource.title AS Collection
            , ao.display_string AS Archival_Object
            , cp.name AS Container_Type
            , tc.indicator AS Container_Number
            , tc.barcode AS Barcode
        FROM sub_container sc
        left join enumeration_value on enumeration_value.id = sc.type_2_id
        left join top_container_link_rlshp tclr on tclr.sub_container_id = sc.id
        left join top_container tc on tclr.top_container_id = tc.id
        left join top_container_profile_rlshp tcpr on tcpr.top_container_id = tc.id
        left join container_profile cp on cp.id = tcpr.container_profile_id
        join instance on sc.instance_id = instance.id
        join archival_object ao on instance.archival_object_id = ao.id
        join resource on ao.root_record_id = resource.id
        WHERE tc.barcode LIKE """ + str(barcode))
    columns = cursor.description
    result = cursor.fetchall()
#    results = [{columns[index][0]:column for index, column in enumerate(value)} for value in result - doesn't work yet
    if not cursor.rowcount:
        print('No results found for: ' + str(barcode))
        output.write(str(barcode) + '\n')
    else:
#        print(results)
#        output.write(results)
        for row in result:
            print(row)
            with open(csvfile, 'a', newline='') as c:
                writer = csv.writer(c)
                writer.writerows([row])

output.close()
cursor.close()

#add series designation to output? Parent name and parent level id? Not exactly sure - less important I think than having AOs and coll
#still need to add headers
#error handling as per usual
