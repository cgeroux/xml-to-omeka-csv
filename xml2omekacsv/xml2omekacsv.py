#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import optparse as op
from lxml import etree
import os

__version__="1.0.0"

def parseOptions():
  """Parses command line options
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options] XMLINPUT"
    ,version="%prog 1.0"
    ,description="Converts a set of XML files to a single CSV file importable by Omeka")
  
  parser.add_option("-o",action="store"
    ,dest="outputFileName"
    ,help="Sets the output file name. "
    +"[default: %default].",default="omeka_items.csv")
  
  #parse command line options
  return parser.parse_args()
def addCSVHeader(file):
  headers=["Dublin Core:Identifier"
    ,"Record Type"
    ,"Item Type"
    ,"Public"
    ,"Featured"
    ,"Item"
    ,"File"
    ,"Dublin Core:Title"
    ,"Dublin Core:Creator"
    ,"Dublin Core:Date"
    ,"Dublin Core:Subject"
    ,"Tags"
    ,"Dublin Core:Rights"
    ,"Item Type Metadata:Subtitle"
    ,"Item Type Metadata:Lede"
    ,"Item Type Metadata:Story"
    ,"Item Type Metadata:Street Address"
    ,"Item Type Metadata:Access Information"
    ,"Item Type Metadata:Related Resources"
    ,"geolocation:latitude"
    ,"geolocation:longitude"
    ,"geolocation:zoom_level"
    ,"geolocation:map_type"
    ,"geolocation:address"]
  line=headers[0]
  for header in headers[1:]:
    line+="\t"+header
  line+="\n"
  file.write(line)
def addXMLItemToLine(node,name):
  xmlTemp=node.find(name)
  if xmlTemp!=None:
    return xmlTemp.text.replace('\n',"")#remove newlines as it will break csv file format
  else:
    return ""
def addStoryToCSV(file,xmlItem):
  line=""
  
  #output ID
  id=addXMLItemToLine(xmlItem,"id")
  line+=id
  
  print("adding story \""+id+"\" to csv file ...")
  
  #output Record type, it is "Item" for curatescape story
  line+="\t"+"Item"
  
  #output Item type, if record type=="Item", ["Curatescape Story","Still Image",...]
  line+="\t"+"Curatescape Story"
  
  #output Public ["true","false"]
  line+="\t"+"true"
  
  #output Featured [1,0]
  line+="\t0"#not featured
  
  #output Item, ID of the item a file is associated with
  line+="\t"#this is a story, not needed
  
  #output File, URL to the file if Record type=file
  line+="\t"#this is a story, not needed
  
  #output Dublin Core:Title
  line+="\t"+addXMLItemToLine(xmlItem,"title")
  
  #output Dublin Core:Creator
  line+="\t"+addXMLItemToLine(xmlItem,"creator")
  
  #output Dublin Core:Date
  line+="\t"
  
  #output Dublin Core:Subject
  xmlSubjects=xmlItem.find("subjects")
  line+="\t"
  if xmlSubjects!=None:
    if len(xmlSubjects)>0:
      xmlSubject=xmlSubjects[0]
      line+=xmlSubject.text
      for xmlSubject in xmlSubjects[1:]:
        line+="|"+xmlSubject.text
  
  #output Tags, separated by pipes
  xmlTags=xmlItem.find("tags")
  line+="\t"
  if xmlTags!=None:
    if len(xmlTags)>0:
      xmlTag=xmlTags[0]
      line+=xmlTag.text
      for xmlTag in xmlTags[1:]:
        line+="|"+xmlTag.text
  
  #output Dublin Core:Rights
  line+="\t"
  
  #output Item Type Metadata:Subtitle
  line+="\t"+addXMLItemToLine(xmlItem,"subtitle")
  
  #output Item Type Metadata:Lede
  line+="\t"+addXMLItemToLine(xmlItem,"lede")
  
  #output Item Type Metadata:Story
  line+="\t"+addXMLItemToLine(xmlItem,"story")
  
  #output Item Type Metadata:Street Address
  line+="\t"+addXMLItemToLine(xmlItem,"street-address")
  
  #output Item Type Metadata:Access Information
  line+="\t"
  
  #output Item Type Metadata:Related Resources
  line+="\t"+addXMLItemToLine(xmlItem,"related-resources")
  
  xmlGeo=xmlItem.find("geolocation")
  if xmlGeo!=None:
    
    #output geolocation:latitude
    line+="\t"+addXMLItemToLine(xmlGeo,"latitude")
    
    #output geolocaiton:longitude
    line+="\t"+addXMLItemToLine(xmlGeo,"longitude")
    
    #output geolocaiton:zoom_level
    line+="\t"+addXMLItemToLine(xmlGeo,"zoom-level")
    
    #output geolocaiton:map_type
    line+="\t"
    
    #output geolocation:address
    line+="\t"
  else:
    line+="\t\t\t\t\t"
  line+="\n"
  file.write(line.encode("UTF-8"))
  
  #get files node
  xmlFiles=xmlItem.find("files")
  if xmlFiles!=None:
    for xmlFile in xmlFiles:
      addFileToCSV(file,xmlFile,id)
def addFileToCSV(file,xmlItem,parentItem):
  line=""
  
  #"Dublin Core:Identifier"
  id=addXMLItemToLine(xmlItem,"id")
  line+=id
  print("  adding file \""+id+"\" to csv file ...")
  
  #"Record Type", is "File" for files
  line+="\t"+"File"
  
  #"Item Type"
  line+="\t"
  
  #"Public"
  line+="\t"
  
  #"Featured"
  line+="\t"
  
  #"Item"
  line+="\t"+parentItem
  
  #"File"
  line+="\t"+addXMLItemToLine(xmlItem,"file")
  
  #"Dublin Core:Title"
  line+="\t"+addXMLItemToLine(xmlItem,"title")
  
  #"Dublin Core:Creator"
  line+="\t"
  
  #"Dublin Core:Date"
  line+="\t"+addXMLItemToLine(xmlItem,"date")
  
  #"Dublin Core:Subject"
  line+="\t"
  
  #"Tags"
  line+="\t"
  
  #"Dublin Core:Rights"
  line+="\t"+addXMLItemToLine(xmlItem,"rights")
  
  #"Item Type Metadata:Subtitle"
  line+="\t"
  
  #"Item Type Metadata:Lede"
  line+="\t"
  
  #"Item Type Metadata:Story"
  line+="\t"
  
  #"Item Type Metadata:Street Address"
  line+="\t"
  
  #"Item Type Metadata:Access Information"
  line+="\t"
  
  #"Item Type Metadata:Related Resources"
  line+="\t"
  
  #"geolocation:latitude"
  line+="\t"
  
  #"geolocation:longitude"
  line+="\t"
  
  #"geolocation:zoom_level"
  line+="\t"
  
  #"geolocation:map_type"
  line+="\t"
  
  #"geolocation:address"
  line+="\t"
  
  line+="\n"
  file.write(line.encode("UTF-8"))
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  #check we got the expected number of arguments
  if (len(args)<1):
    raise Exception("Expected at least one xml file.")
  
  #load schema to validate against
  schemaFileName=os.path.join(os.path.dirname(__file__),"xmlSchema/item.xsd")
  schema=etree.XMLSchema(file=schemaFileName)
  
  #open output file
  outputFile=open(options.outputFileName,'w')
  
  #add header
  addCSVHeader(outputFile)
  
  for xmlFileName in args:
    
    #parse xml file
    tree=etree.parse(xmlFileName)
    
    #strip out any comments in xml
    comments=tree.xpath('//comment()')
    for c in comments:
      p=c.getparent()
      p.remove(c)
    
    #validate against schema
    schema.assertValid(tree)
    
    #Parse XML 
    xmlDoc=tree.getroot()
    
    addStoryToCSV(outputFile,xmlDoc)
    
  outputFile.close()
if __name__ == "__main__":
 main()