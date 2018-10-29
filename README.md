# archivesspace-api-public

A collection of Python scripts for interacting with the ArchivesSpace API.

## Requirements
* Python 3.4+
* `requests` module
* ArchivesSpace 2.4+
* Access to ArchivesSpace database (not required but important)

## Getting Started

### Installation

__NOTE:__ You must clone or download the entire repository, as the main scripts call functions within the `utilities.py` and `login.py` scripts.

__Mac__

1. Open Terminal
2. Navigate to directory where you wish to store the repository `cd /Users/username/direcorypath`
3. Enter `git clone https://github.com/ucancallmealicia/archivesspace-api-public`
4. Enter `cd archivesspace-api-public`
5. To work with the scripts interactively, open the Python interpreter `python`
6. To run a particular script, enter `python script_to_run.py`
7. Follow prompts in Terminal 

__Windows__

1. Open command prompt
2. Navigate to directory where you wish to store the repository  `cd C:\Users\username\directorypath`
3. Enter `git clone https://github.com/ucancallmealicia/archivesspace-api-public`
4. Enter `cd archivesspace-api-public`
5. To work with the scripts interactively, open the Python interpreter `python`
6. To run a particular script, enter `python myscript.py`
7. Follow prompts in command window

### Suggested Workflow

These scripts use CSV files as inputs for making bulk metadata updates via the ArchivesSpace API. The easiest way to retrieve the data required for the updates is by querying the ArchivesSpace database. A repository of queries written for use with these scripts can be found [here](http://github.com/ucancallmealicia/archivesspace-sql).  

 Below is a suggested workflow for gathering and re-using data from the ArchivesSpace database. It is highly recommended to first test all work in a non-production instance of ArchivesSpace.

1. Open an SQL file in a MySQL client such as MySQL Workbench or Sequel Pro.
2. Execute query and export results in CSV format.
3. Make a copy of the query export
4. Process this query output in whatever way suits your needs, making sure to retain the URIs.
5. Use the modified query output as input for the scripts in this repository

### Resources

* [ArchivesSpace Data Dictionary (Database Documentation)](https://desolate-tundra-60608.herokuapp.com)
* [ArchivesSpace API Documentation](http://archivesspace.github.io/archivesspace/api/)

## Repository Contents

### utilities.py

Holds file handling and other utility functions used in various scripts.

### login.py

Simple script for logging into the ArchivesSpace API.

### barcode_search.py

Searches for a user-provided list of barcodes and returns data about the associated top container in CSV format.

### create_restrictions.py

Creates machine-actionable conditions governing access or conditions governing use notes.

### delete_notes.py

Deletes notes using a CSV of record URIs and note persistent IDs.

### delete_records.py

Deletes top-level records using a CSV of record URIs as input.

### ex_tra_val_ead.py

Exports a set of EAD files and transforms and validates them using user-supplied schemas.

### file_version_update.py

Add file versions to digital object records.

### link_records.py

Create links between top-level records and subrecords (i.e. link a top container as an instance), top-level records and other top-level records (i.e. link an agent to a resource).

### merge_agents.py

Merges duplicate agent records using a CSV of "target" (the records to accept the merge) and "victim" (the records to be merged) URIs. 

### merge_subjects.py

Merges subject records.

### position_enum_vals.py

Repositions enumeration values. [Query](https://github.com/ucancallmealicia/archivesspace-sql).

### update_multipart_notes.py

Updates multipart notes using URIs and persistent IDs extracted from the ArchivesSpace database. [Query](https://github.com/ucancallmealicia/archivesspace-sql).

### update_record_components.py

Updates any top-level  record component (resource, archival object, digital object, etc.). To use, ...

### update_record_publish.py

Publishes or unpublishes a set of top-level records.

### update_subrecord_components.py

Updates any subrecord (date, extent, instance, etc.). To use, ...

### update_subsubrecord_components.py

Updates any subrecord‘s subrecord (i.e. subcontainers within an instance record).

### asnake_implement.py

Test script to implement create and update functions using ArchivesSnake.
