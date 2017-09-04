#!/usr/bin/env python
# -*- coding: utf-8 -*-
#http://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
# Uniquement pour faire de l'imap
import poplib
import imaplib
from email import parser
import email
import datetime
import re
from email.header import decode_header, make_header
from email.Iterators import typed_subpart_iterator

"""Decode le header d'un mail"""
def getheader(header_text, default="ascii"):
    
    headers = decode_header(header_text)
    header_sections = [unicode(text, charset or default)
                       for text, charset in headers]
    return u"".join(header_sections)

"""Decode l'encodage d'un mail"""
def get_charset(message, default="ascii"):
    
    if message.get_content_charset():
        return message.get_content_charset()

    if message.get_charset():
        return message.get_charset()

    return default

"""Decode le corps d'un mail"""
def get_body(message):
   
    if message.is_multipart():
        #get the plain text version only
        text_parts = [part
                      for part in typed_subpart_iterator(message,
                                                         'text',
                                                         'plain')]
        body = []
        for part in text_parts:
            charset = get_charset(part, get_charset(message))
            body.append(unicode(part.get_payload(decode=True),
                                charset,
                                "replace"))

        return u"\n".join(body).strip()

    else: # if it is not multipart, the payload will be a string
          # representing the message body
        body = unicode(message.get_payload(decode=True),
                       get_charset(message),
                       "replace")
        return body.strip()

"""Recupère l'ensemble des mail à partir d'un imap, user et password de sa boite
inbox """
def getMailListFromUser(imap, login, password):
    mail = imaplib.IMAP4_SSL(imap)
    mail.login(login, password)
    mail.list()
    mail.select("inbox")
    
    return mail

"""Permet d'obtenir la liste des UID de mail par rapport à la recherche"""
def getListeUIDmail(mail,search):
    mail.select("inbox",readonly=True) # connect to inbox.
    # ALL ==> pour tout
    # (RFC822)
    #'(SENTSINCE {date})'.format(date=date) ==> pour une date données
    result, data = mail.uid('search', None, search)
    return data[0].split(' ')

""" Permet de valider le mail comme lu """
def setSeenMail(mail, uid) :   
    mail.uid('STORE', uid, '+FLAGS', '(SEEN)')
    #mail.store(i, '+FLAGS', '(UNSEEN)')
    #mail.store(i,'-FLAGS','\\Seen')

""" Permet de supprimer définitivement le mail
Attention, il n'est pas dans la corbeille (Trash) """
def setDeleteMail(mail, uid) :
     mail.uid('STORE', uid , '+FLAGS', '(\Deleted)')
     mail.expunge()

def writeResult(strToWrite) :
    fileToWrite = open("mailSandra.txt", "w") 
    fileToWrite.write(strToWrite.encode('utf-8', 'ignore'))
    fileToWrite.close()
    
  
#mail=getMailListFromUser('imap.gmail.com','**************', '**********')
mail=getMailListFromUser('imap.orange.fr','**********', '********')
date = (datetime.date.today() - datetime.timedelta(2)).strftime("%d-%b-%Y")
listeUID=getListeUIDmail(mail,'(SENTSINCE {date} UnSeen)'.format(date=date))
text=''

#Parcours l'ensemble des UID mails
for i in listeUID :

    #recupère le mail de l'uid
    result, data = mail.uid('fetch', i, '(RFC822)')

    #transformation en string
    email_message = email.message_from_string(data[0][1])

    #decodage de l'envoyeur, du sujet et du corps de messages
    subject, encoding = decode_header(email_message['Subject'])[0]
    author, encoding = decode_header(email_message['From'])[0]

    #Decode en fonction de l'encodage du mail
    if encoding==None:
           author=author.decode('iso-8859-1')
           author=author[0:author.find('<')]+author[author.find('>'):len(author)]
           text=text+u' Expéditeur : '+author+' . Sujet : '+ subject.decode('iso-8859-1')+'. '
    else:
           author=author.decode(encoding)
           author=author[0:author.find('<')]+author[author.find('>'):len(author)]
           text=text+u' Expéditeur : '+author+' . Sujet : '+ subject.decode(encoding)+'. '
       
    if subject.find('Information AXA Banque')!= -1 :
           pos=[m.start() for m in re.finditer(r".",get_body(email_message))][1]           
           pos=get_body(email_message).find('.',get_body(email_message).find('.')+1)
           text=text+' Contenu: '+ get_body(email_message)[0:pos]+' . '
    #text=text[0:text.find('<')]+text[text.find('>'):len(text)]   
    

writeResult(text.replace('<','').replace('>',' ').replace(u'Ã©',u'é').replace('&','et'))    
#print text.replace('<','').replace('>',' ').replace(u'Ã©',u'é'))

##lineFile=''
##ins = open( "test.txt", "r" )
##for line in ins:
##    lineFile=lineFile+line
##    #print line.decode('iso-8859-1').replace('?utf-8?QE282AC ','euros').replace('C3AA',u'é').replace('E28099','\'')
##ins.close()
##
##print lineFile.decode('iso-8859-1').replace('?utf-8?QE282AC ','euros').replace('C3AA',u'é').replace('E28099','\'')

""" Pour se connecter en POP """
##pop_conn = poplib.POP3_SSL('pop.gmail.com')
##pop_conn.user('************')
##pop_conn.pass_('******************')
##Get messages from server:
##messages = [pop_conn.retr(i) for i in range(1, 5)]
## Concat message pieces:
##messages = ["\n".join(mssg[1]) for mssg in messages]
##Parse message intom an email object:
##messages = [parser.Parser().parsestr(mssg) for mssg in messages]
##for message in messages:
##    print message['subject']
##pop_conn.quit()


