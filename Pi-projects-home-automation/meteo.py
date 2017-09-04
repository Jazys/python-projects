# -*- coding: utf-8 -*-
import urllib
from HTMLParser import HTMLParser
from xml.dom import minidom
from xml.etree.ElementTree import XMLParser

def deleteBaliseNoDiv(replaceStr):
    replaceStr=replaceStr.replace("<strong>","");
    replaceStr=replaceStr.replace("</strong>","");
    replaceStr=replaceStr.replace("<strong>","");
    replaceStr=replaceStr.replace("</strong>","");
    replaceStr=replaceStr.replace("h4","div");
    replaceStr=replaceStr.replace("h3","div");
    replaceStr=replaceStr.replace("span","div");
    replaceStr=replaceStr.replace("img","div");

    return replaceStr

def deletePicVent(replaceStr):
    #print replaceStr
    
    for i in range(1,5) :    
        picVent=replaceStr.find('picVent')
        strToReplace='picVent'       
    
        if picVent !=-1 :
           cpt=0
           for z in range(picVent+7,picVent+20) :
                if replaceStr[z]=='"':
                    cpt=z
                    break
                #print replaceStr[i]
                strToReplace+=replaceStr[z]

           #print strToReplace
           #replaceStr=replaceStr[picVent-1:picVent+20].replace(strToReplace,'vent-direction')
           replaceStr=replaceStr[0:picVent]+'vent-direction'+replaceStr[cpt:len(replaceStr)]
           #print replaceStr[0:picVent]+'vent-direction';
           #print replaceStr[cpt:len(replaceStr)]
           #print replaceStr.find(strToReplace)
        #picVent=replaceStr.find('picVent')

    #print replaceStr
    return replaceStr

def parseGlobalJour(jour):
    xmldoc = minidom.parseString(jour)
    itemlist = xmldoc.getElementsByTagName('div') 
    for s in itemlist :        

        if s.attributes['class'].value=='day-summary-temperature' :
           print s.firstChild.nodeValue.replace("|","a")

        if s.attributes['class'].value=='day-summary-broad' :
           print s.firstChild.nodeValue

        if s.attributes['class'].value=='day-summary-uv' :
           print s.firstChild.nodeValue

        if s.attributes['class'].value=='day-summary-wind-info' :
           print s.firstChild.nodeValue

        if s.attributes['class'].value=='day-summary-title' :
           print s.firstChild.nodeValue

        return ''

def getDay(jour):
    xmldoc = minidom.parseString(jour)
    itemlist = xmldoc.getElementsByTagName('div') 
  
    for s in itemlist :
        if s.attributes['class'].value=='day-summary-title' :
           return s.firstChild.nodeValue

def deleteImgBalise(chaine):
    indice=chaine.find('title="Indice de confiance')
    chaineToReturn=chaine[0:indice]+'/'+chaine[indice+33:len(chaine)]
    return chaineToReturn
           

def parseDetailJour(jourXDetail):

    #Parser minidom
    xmldocDetail = minidom.parseString(jourXDetail)
    #on recupère les div
    itemlistDetail = xmldocDetail.getElementsByTagName('div') 
    #print len(itemlistDetail)
    
    # Pour stocker le resultat
    jouXText='';
    
    #print itemlistDetail[0].attributes['class'].value
   

    #Parcours
    for s in itemlistDetail :
        #print s.attributes['class'].value  

        if s.attributes['class'].value=='day-summary-title' :
           #print s.firstChild.nodeValue
           jouXText+=s.firstChild.nodeValue+' : '
        
        if s.attributes['class'].value=='day-summary-temperature' :
           #print s.firstChild.nodeValue.replace("|","a").replace("°C","degré")
           text=s.firstChild.nodeValue.replace("|",u"à")
           text=text.replace(u"°C",u" degré")
           jouXText+=u'Température de '+text+' , '

        if s.attributes['class'].value=='day-summary-broad'  :
           #print s.firstChild.nodeValue
           if len(s.firstChild.nodeValue)>1 :
               jouXText+= 'avec la tendance : '+s.firstChild.nodeValue+' , '       

        #if s.attributes['class'].value=='day-summary-uv' :
           #print s.firstChild.nodeValue

        if s.attributes['class'].value=='vent-detail-vitesse' :
           #print s.firstChild.nodeValue
           jouXText+=s.firstChild.nodeValue.replace("Vent"," de").replace("km/h",u" kilomètre par heure")+' . '

        if s.attributes['class'].value=='vent-direction'  :
           #print s.firstChild.nodeValue
           jouXText+='pour un '+s.firstChild.nodeValue 

        #if s.attributes['class'].value=='day-summary-wind-info' :
           #print s.firstChild.nodeValue
           #print s.attributes['class'].getElementsByTagName('span')[0].attributes['class'].value 

        if s.attributes['class'].value=='day-summary-ressentie' :
           #print s.firstChild.nodeValue.replace("|","a")
           text=s.firstChild.nodeValue.replace("|",u"à")
           text=text.replace(u"°C",u"degré")
           text=text.replace("Ressentie","ressentie de")
           jouXText+='avec un '+text +' , '

        if s.attributes['class'].value=='proba-pluie' :
            jouXText+=s.firstChild.nodeValue +' , '

        if s.attributes['class'].value=='proba-gel' :
            jouXText+=s.firstChild.nodeValue +' . '
        

    return jouXText

def writeFile(strToWrite):
    mon_fichier = open("meteo.txt", "w") 
    mon_fichier.write(strToWrite)
    mon_fichier.close()

     


#adresse sur la page meteo france
adresseMeteo='http://www.meteofrance.com/previsions-meteo-france/marcilloles/38260'

#fait une requete HTTP
page=urllib.urlopen(adresseMeteo)

#recupère le html
strpage=page.read()

#print strpage.find('<div class="bloc-day-summary first active" id="day-symmary-id-00001">')
#print strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00002">')
# strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00003">')
#print strpage.find('<div class="bloc-day-summary last " id="day-symmary-id-00004">')
#print strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00005">')
#print strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00006">')
#print strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00007">')
#print strpage.find('<div class="bloc-day-summary last " id="day-symmary-id-00008">')
#print strpage.find('<div id="ajax-day-detail" class="ajax-day-detail ">')
#print strpage.find('<div class="group-day-more-info" id="more-info-day-symmary-id-00001">')

jourX=strpage[strpage.find('<div class="bloc-day-summary first active" id="day-symmary-id-00001">'):strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00002">')]
jourXDetail=strpage[strpage.find('<div class="group-day-detail " id="detail-day-symmary-id-00001" >'):strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00002" style="display: none;">')]
jourX2=strpage[strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00002">'):strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00003">')]
jourX2Detail=strpage[strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00002" style="display: none;">'):strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00003" style="display: none;">')]
jourX3=strpage[strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00003">'):strpage.find('<div class="bloc-day-summary last " id="day-symmary-id-00004">')]
jourX3Detail=strpage[strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00003" style="display: none;">'):strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00004" style="display: none;">')]
jourX4=strpage[strpage.find('<div class="bloc-day-summary last " id="day-symmary-id-00004">'):strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00005">')-51]
jourX4Detail=strpage[strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00004" style="display: none;">'):strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00005" style="display: none;">')]
jourX5=strpage[strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00005">'):strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00006">')]
jourX5Detail=strpage[strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00005" style="display: none;">'):strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00006" style="display: none;">')]
jourX6=strpage[strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00006">'):strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00007">')]
jourX6Detail=strpage[strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00006" style="display: none;">'):strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00007" style="display: none;">')]
jourX7=strpage[strpage.find('<div class="bloc-day-summary " id="day-symmary-id-00007">'):strpage.find('<div class="bloc-day-summary last " id="day-symmary-id-00008">')]
jourX7Detail=strpage[strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00007" style="display: none;">'):strpage.find('<div class="group-day-detail hide-id-js" id="detail-day-symmary-id-00008" style="display: none;">')]


jourX=deleteBaliseNoDiv(jourX)
jourX=deletePicVent(jourX)

jourX2=deleteBaliseNoDiv(jourX2)
jourX2=deletePicVent(jourX2)

jourX3=deleteBaliseNoDiv(jourX3)
jourX3=deletePicVent(jourX3)

jourX4=deleteBaliseNoDiv(jourX4)
jourX4=deletePicVent(jourX4)

jourX5=deleteBaliseNoDiv(jourX5)
jourX5=deletePicVent(jourX5)

jourX6=deleteBaliseNoDiv(jourX6)
jourX6=deletePicVent(jourX6)

jourXDetail=deleteBaliseNoDiv(jourXDetail)
jourXDetail=deletePicVent(jourXDetail)
jourXDetail=parseDetailJour(jourXDetail)

jourX2Detail=deleteBaliseNoDiv(jourX2Detail)
jourX2Detail=deletePicVent(jourX2Detail)
jourX2Detail=parseDetailJour(jourX2Detail)

jourX3Detail=deleteBaliseNoDiv(jourX3Detail)
jourX3Detail=deletePicVent(jourX3Detail)
jourX3Detail=parseDetailJour(jourX3Detail)

jourX4Detail=deleteBaliseNoDiv(jourX4Detail)
jourX4Detail=deletePicVent(jourX4Detail)
jourX4Detail=parseDetailJour(jourX4Detail)

jourX5Detail=deleteBaliseNoDiv(jourX5Detail)
jourX5Detail=deletePicVent(jourX5Detail)
jourX5Detail=parseDetailJour(jourX5Detail)

jourX6Detail=deleteBaliseNoDiv(jourX6Detail)
jourX6Detail=deletePicVent(jourX6Detail)
jourX6Detail=parseDetailJour(jourX6Detail)

jourX5=deleteImgBalise(jourX5)
jourX6=deleteImgBalise(jourX6)

dataTowrite = getDay(jourX).encode('utf8') +' . '+jourXDetail.encode('utf8') +getDay(jourX2).encode('utf8') +' . '+jourX2Detail.encode('utf8')+getDay(jourX3).encode('utf8') +' . '+jourX3Detail.encode('utf8') + getDay(jourX4).encode('utf8') +' . '+jourX4Detail.encode('utf8') 

writeFile(dataTowrite)

#print getDay(jourX).encode('utf8') +' . '+jourXDetail.encode('utf8') 
#print getDay(jourX2).encode('utf8') +' . '+jourX2Detail.encode('utf8') 
#print getDay(jourX3).encode('utf8') +' . '+jourX3Detail.encode('utf8') 
#print getDay(jourX4).encode('utf8') +' . '+jourX4Detail.encode('utf8') 