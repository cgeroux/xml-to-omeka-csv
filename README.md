This script creates a CSV file from an xml file which is compatible with CSV Import+. It was designed to work specifically with Curatescape story items in omeka. See https://github.com/Daniel-KM/CsvImportPlus. The format of the CSV file needs to be specified as:

CSV format
==========
Column delimiter: tabulation
Enclosure: (empty)
Element delimiter: pipe
Tag delimiter: pipe
File delimiter: pipe

Default values
==============
Item type: No default item type
Collection: No default collection

Process
=======
Identifier field: Identifer
Action: No default action
Contains extra data: Yes, so column names won't be checked


For an example input xml files see `xml2omekacsv/example-xml/`
