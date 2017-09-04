# -*- coding: utf-8 -*-
import urllib
from HTMLParser import HTMLParser
from xml.dom import minidom
from xml.etree.ElementTree import XMLParser

def getTextSingle(node):
    parts = [child.data for child in node.childNodes if child.nodeType == node.TEXT_NODE]
    return u"".join(parts)

def getText(nodelist):
    return u"".join(getTextSingle(node) for node in nodelist)

def writeResult(strToWrite) :
    fileToWrite = open("actualite.txt", "w") 
    fileToWrite.write(strToWrite)
    fileToWrite.close()

page=urllib.urlopen('http://rss.lemonde.fr/c/205/f/3050/index.rss')
strpage=page.read()

allTitle=''
dom = minidom.parseString(strpage)
items = dom.getElementsByTagName("item")
for i in items:
    title = i.getElementsByTagName("title")
    #print getText(title)
    allTitle=allTitle+getText(title)+' .,.,. '
    description = i.getElementsByTagName("description")
    #print getText(description)[0:getText(description).find('.')]

writeResult(allTitle.encode('utf-8', 'ignore'))

    
       
