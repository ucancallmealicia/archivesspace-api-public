import pymysql
import csv
import pprint

#connect to DB
print('Connecting to database...')

connection = pymysql.connect(host='',
                             port = '',
                             user='',
                             password='',
                             db='')

print('Connected!')

cursor = connection.cursor()

#create list from ead ids in text file
outfile = input('input the name of the file: ')

eadlist = open(outfile, 'r')

eadlisty = eadlist.read().split('\n')

#sometimes a newline gets stuck in there - this takes care of that
if eadlisty[-1] == '':
    del eadlisty[-1]

#check to make sure all is well...
pprint.pprint(eadlisty)

#don't want to be too hasty...
moveon = input('Please press enter to run query...')
print(moveon)

#text file to store eads that don't have any restrictions
textfile = input('Please enter path to outputfile: ')

output = open(textfile, 'a')

#CSV file to store query data
csvfile = input('Please enter path to CSV: ')

#needs headers in output CSV
for ead in eadlisty:
    print('querying ' + ead)
    cursor.execute("""
    SELECT DISTINCT resource.ead_id AS EAD_ID
        , resource.identifier AS Identifier
        , resource.title AS Resource_Title
        , ev.value AS LEVEL
        , rr.restriction_note_type AS Restriction_Type
        , rr.begin AS BEGIN_DATE
        , rr.end AS END_DATE
        , CAST(note.notes as CHAR (10000) CHARACTER SET UTF8) AS restriction_text
        , CONCAT('/repositories/', resource.repo_id, '/resources/', resource.id) AS Resource_URL
    FROM rights_restriction rr
    LEFT JOIN resource on resource.id = rr.resource_id
    LEFT JOIN enumeration_value ev on ev.id = resource.level_id
    LEFT JOIN note on resource.id = note.resource_id
    WHERE resource.repo_id = 12 #enter your repo_id here
    AND rr.restriction_note_type LIKE '%accessrestrict%'
    AND note.notes LIKE '%accessrestrict%'
    AND resource.ead_id LIKE '%""" + ead + """%'""")
    columns = cursor.description
    result = cursor.fetchall()
    #if no results, write ead id to text file
    if not cursor.rowcount:
        print('No results found for: ' + ead)
        output.write(ead + '\n')
    #if results, write to CSV
    else:
        for row in result:
            print(row)
            with open(csvfile, 'a', newline='') as c:
                writer = csv.writer(c)
                writer.writerows([row])

output.close()
cursor.close()

