This script creates a CSV file from an xml file which is compatible with CSV Import+. It was designed to work specifically with Curatescape story items in omeka. See https://github.com/Daniel-KM/CsvImportPlus. The format of the CSV file needs to be specified as described in example 10 on the CsvImportPlus github readme copied below:

test_extra_data.csv

Show import of extra data that are not managed as elements, but as data in a specific table. The mechanism processes data as post, so it can uses the default hooks, specially after_save_item.

To try this test file, install Geolocation first. Set tabulation as column delimiter, no enclosure, and | as element, file and tag delimiters. You should set the required identifier to "Dublin Core : Identifier", the option "Contains extra data" to "Yes" too (or "Perhaps" to check manually). Use the update below to get full data for all items.

The last row of this file shows an example to import one item with attached files on one row (unused columns, specially Identifier and Record Type, can be removed). This simpler format can be used if you don't need files metadata or if you don't have a lot of files attached to each item.