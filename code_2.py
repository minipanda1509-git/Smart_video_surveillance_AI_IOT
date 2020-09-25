#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def EditZipFile():
    from zipfile import *
    with ZipFile('/home/pi/tkhSir photos.zip', 'a') as myzip:
     myzip.write('test1.jpg')
     myzip.close()
    os.system("curl -X POST --form \"Sir_positive_examples=@tkhSir photos.zip\" \"https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classifiers/TKH_849252517?api_key=95cf029c3e74886abcdff799eea1165f72c24079&version=2018-03-19\"")
    time.sleep(5)
    os.system("curl -X GET \"https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classifiers/TKH_849252517?api_key=95cf029c3e74886abcdff799eea1165f72c24079&version=2018-03-19\"")
    #print("done adding")
    return

def RingBuzzer():
   import RPi.GPIO as gpio
   import time
   piezo=40
   gpio.setwarnings(False)
   gpio.setmode(gpio.BOARD)
   gpio.setup(piezo, gpio.OUT) 
   try:
    while True:
        gpio.output(piezo,1)
        time.sleep(0.2)  
        gpio.output(piezo,0)
        time.sleep(0.3)

   finally:
    gpio.cleanup()
    return


import RPi.GPIO as GPIO
import smtplib
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import subprocess
with open("output.txt", "w+") as output:
    subprocess.call(["python", "./FYP_part1.py"], stdout=output);    

with open('output.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')
    
str="score"
j=data.find(str,0, len(data))
if j>=0 :
 i=data.index(str)
 score= data[i+8:i+12]
if j== -1 or (j>=0 and float(score)<0.75)  :
            attachment ='/home/pi/test1.jpg'
            fp= open(attachment, 'rb')
            img= MIMEImage(fp.read())
            fp.close()
            msg=MIMEMultipart()
            msg.attach(img)
            content = 'Hi python'
            mail= smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            mail.login('sudwapone@gmail.com','password')
            mail.sendmail('sudwapone@gmail.com','sudeshna1509@gmail.com',msg.as_string())
            mail.close()        

else :
    EditZipFile()
    
myfile.close()

import imaplib
import email
time.sleep(50)

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('sudwapone@gmail.com', 'password')
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox", True) # connect to inbox.
count=len(mail.search(None,'UnSeen')[1][0].split())
if count==0:
    RingBuzzer()
else:     
 result, data = mail.search(None, '(FROM "sudeshna1509@gmail.com")')

 ids = data[0] # data is a list.
 id_list = ids.split() # ids is a space separated string
 latest_email_id = id_list[-1] # get the latest

 result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

 raw_email = data[0][1] # here's the body, which is raw text of the whole email
 # including headers and alternate payloads
 raw_email_string = raw_email.decode('utf-8')

 b = email.message_from_string(raw_email_string)
 if b.is_multipart():
  for payload in b.get_payload():
        body=payload.get_payload()
    
#print(body) 

j=body.find("Ignore",0, len(body))
if j!= -1 :
   EditZipFile()
   print("Known person")
elif body.find("Ring",0, len(body)) != -1 :   #  ring burglary alarm
   print("Ring")
   RingBuzzer()

