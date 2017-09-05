#!/usr/bin/python
#*- coding: utf-8 -*-
     
import binascii
import os
import socket
     
# Opening mirror.
mirror = open("/dev/usb/hiddev0", "rb")
i=0    
adresse=('192.168.1.17',31000)

send_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

quelquunMaison= False

while 1:
    donnee = mirror.read(16)
    rfid_id = binascii.hexlify(donnee)[0:]
     # print "donnee %s" % rfid_id	
    if donnee != '\x01\x00\x00\xff\x00\x00\x00\x00\x01\x00\x00\xff\x00\x00\x00\x00':
  	  rfid_id = binascii.hexlify(donnee)[4:]
	  i=i+1

	  if i==1 and rfid_id[21]=='1' and not quelquunMaison :
	       print "Tag pose "
	       quelquunMaison = True	
	       #os.system('./bash_ps.sh')
	       #os.system('./radioEmission 0 12325261 1 on')	
	       os.system('./action_arrivee.sh')	
               send_socket.sendto('kikitounette', adresse)		
	  elif i==1 and rfid_id[21]=='2' :
	       os.system('./action_depart.sh')	
	       #os.system('./radioEmission 0 12325261 1 off')	
	       print "Tag enlevee"
	       quelquunMaison = False	
		
          print "donnee non nul  %s" %rfid_id

    	  if i == 5 :
		print rfid_id[20:22]
	        if rfid_id[20:22] == '2d' : 
    			print "Puce identifiee kikitounet"
		if rfid_id[20:22] == '21' :
			print "Puce identifiee kikitouentte"
     
          elif donnee[0:2] == '\x02\x02': 
    		print "Puce identifiee %s retiree." % rfid_id
   	
	  if i == 6 :
		print "fin"
		i=0
print("Fermeture connexion")
send_socket.close()
