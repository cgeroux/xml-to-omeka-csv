#!/usr/bin/env python
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
    ,"Item Type Metadata:subtitle"
    ,"Item Type Metadata:lede"
    ,"Item Type Metadata:story"
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
    return xmlTemp.text
  return ""
def addRowToCSV(file,xmlItem):
  
  line=""
  
  #output ID
  line+=addXMLItemToLine(xmlItem,"id")
  
  #output Record type, ["Item","File"]
  line+="\t"+"Item"#no files yet
  
  #output Item type, if record type=="Item", ["Curatescape Story","Still Image",...]
  line+="\t"+"Curatescape Story"
  
  #output Public ["true","false"]
  line+="\t"+"true"
  
  #output Featured [1,0]
  line+="\t0"#not featured
  
  #output Item, ID of the item a file is associated with
  line+="\t"#nothing right now as all rows are items
  
  #output File, URL to the file if Record type=file
  line+="\t"#nothing right now, no files
  
  #output Dublin Core:Title
  line+="\t"+addXMLItemToLine(xmlItem,"title")
  
  #output Dublin Core:Creator
  line+="\t"+addXMLItemToLine(xmlItem,"creator")
  
  #output Dublin Core:Date
  line+="\t"
  
  #output Dublin Core:Subject
  line+="\t"+addXMLItemToLine(xmlItem,"subject")
  
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
  file.write(line)
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  #check we got the expected number of arguments
  if (len(args)<1):
    raise Exception("Expected at least one xml file.")
  
  #load schema to validate against
  schemaFileName=os.path.join(os.path.dirname(__file__),"xmlSchema/story.xsd")
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
    
    addRowToCSV(outputFile,xmlDoc)
    
  outputFile.close()
if __name__ == "__main__":
 main()