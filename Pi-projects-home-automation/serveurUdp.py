#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Serveur UDP utilisant le module socket
 
# import nécessaire au fonctionnement du serveur
import socket
import threading
import time
 
# imports seulement nécessaires à l'exemple (=calcul d'expression par eval())
import sys
import os
from math import *


fileToWrite = open("logSrvUdp.txt", "w") 
fileToWrite.write('sleep')
    

time.sleep(50)
 
buf=1024


UDP_IP = "192.168.1.25"
UDP_PORT = 31100

def doActionOnLight(nb, state, nom=' '):
    os.system('./radioEmission 0 12325261 '+nb+' '+state)
    print 'done'
    
def doActionReadMail(nom=' '):
    os.system('play mailSandra.wav')
    print 'done'
    
def doActionMeteo( nom=' '):
    os.system('play meteo.wav')
    print 'done'

def doActionActualite( nom=' '):
    os.system('play actualite.wav')
    print 'done'


socketserveur=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketserveur.bind((UDP_IP, UDP_PORT))
print "serveur actif"
fileToWrite.write('serveur actif')
 
# boucle de service du serveur
while True:
    # attente d'une nouvelle connexion
    # et enregistrement de la requete et de l'adresse du demandeur
    
    #print "attente req"
    requete, adresseclient = socketserveur.recvfrom(buf)
    #requete=str (requete.strip())
    
    requete=requete.strip().decode(encoding='UTF-8')
    
    print requete
    fileToWrite.write(requete)
 
    # préparation de la réponse
   
        
    if requete =='allumer un' :
        print 'ok'
       # os.system('./radioEmission 0 12325261 1 on')
        threading.Thread(None, doActionOnLight, None, ('1','on'), {'nom':''}).start()
        
    if requete =='eteindre un' :
        #os.system('./radioEmission 0 12325261 1 off')
        threading.Thread(None, doActionOnLight, None, ('1','off'), {'nom':''}).start()
    
    if requete =='allumer deux' :
        #os.system('./radioEmission 0 12325261 2 on')
        threading.Thread(None, doActionOnLight, None, ('2','on'), {'nom':''}).start()
        
    if requete =='eteindre deux' :
        #os.system('./radioEmission 0 12325261 2 off')
        threading.Thread(None, doActionOnLight, None, ('2','off'), {'nom':''}).start()
        
    if requete =='meteo' :
        #os.system('./radioEmission 0 12325261 2 off')
        threading.Thread(None, doActionMeteo, None, {'nom':''}).start()
        
    if requete =='mail' :
        #os.system('./radioEmission 0 12325261 2 off')
        threading.Thread(None, doActionReadMail, None, {'nom':''}).start()
        
    if requete =='info' :
        #os.system('./radioEmission 0 12325261 2 off')
        threading.Thread(None, doActionActualite, None, {'nom':''}).start()
        
      
    print requete.strip().decode(encoding='UTF-8')

fileToWrite.close()
 
    # envoi de la réponse au demandeur
    #socketserveur.sendto("%s" % reponse,adresseclient)
    
    