#!/usr/bin/python
import urllib, urllib2, cookielib
import os
import time
import sys

fichierALire=str(sys.argv[1])
bot= str(sys.argv[2])
fichierTemp= str(sys.argv[3])
fichierMessage= str(sys.argv[4])

#Ecrire dans le fichier
#fileToStr= open(fichierALire, "w")
#fileToStr.write("Premier test d'ecriture dans un fichier")
#fileToStr.close()

#lecture dans le fichier de la chaine d lire
fileStr= open(fichierALire,"r")
chaineADire=fileStr.read()
fileStr.close()

url = 'http://voxygen.fr/sites/all/modules/voxygen_voices/assets/proxy/index.php'
values = {'method' : 'redirect', 'text' : chaineADire, 'voice' : bot}

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#text = raw_input("Entrez le texte a convertir en audio : ")
#voice = raw_input("Entrez le nom du bot de lecture (ex: Eva): ")
#FileName = raw_input("Entrez le nom du fichier: ")
#data = urllib.urlencode({'method' : 'redirect', 'text': 'ok cool' ,'voice' : 'eva'})
data = urllib.urlencode(values)
#resp= opener.open('http://voxygen.fr/sites/all/modules/voxygen_voices/assets/proxy/index.php', data)
resp= opener.open(url,data)

#f = open(FileName, "wb")
f = open(fichierTemp,"wb") 

try:
    while True:
        data=resp.read(1)
        if len(data) != 1:
            break;
        f.write(data)
except IOError:
    pass
finally:
    f.close()

os.system('mpg123 -w '+ fichierMessage+ ' '+ fichierTemp)
#print 'mpg123 -w '+ fichierTemp+' '+ fichierMessage 
os.system('play '+ fichierMessage)
time.sleep(5)
os.system('rm '+ fichierTemp)
#os.system('rm '+ fichierMessage)
