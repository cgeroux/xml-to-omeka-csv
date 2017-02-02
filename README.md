

This script creates a CSV file from an xml file which is compatible with [CSVImport+](https://github.com/Daniel-KM/CsvImportPlus). It was designed to work specifically with Curatescape story items in omeka. 

Installation
============
As root user run:

`python setup.py install`

or to install to your home directory under `.local` directory do:

`python setup.py install --user`

Usage
=====
`xml2omekacsv -h` shows help message and how to use program.
`xml2omekacsv input_xml_file.xml` will create a csv file from the input xml file which can be imported into omeka

Importing into Omeka
====================
The format of the CSV file needs to be specified as:

CSV format
----------
Column delimiter: tabulation
Enclosure: (empty)
Element delimiter: pipe
Tag delimiter: pipe
File delimiter: pipe

Default values
----------
Item type: No default item type
Collection: No default collection

Process
----------
Identifier field: Identifer
Action: No default action
Contains extra data: Yes, so column names won't be checked


For an example input xml files see `xml2omekacsv/example-xml/`
