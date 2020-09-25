#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import RPi.GPIO as GPIO
import time
import os
pir_sensor = 7
#piezo = 7
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(piezo,GPIO.OUT)
#GPIO.setup(pir_sensor, GPIO.IN)
GPIO.setup(pir_sensor, GPIO.IN, GPIO.PUD_DOWN)
current_state = 0
#time.sleep(2)
try:
    while True:
        time.sleep(0.5)
        current_state = GPIO.input(pir_sensor)
        if current_state == 1:
            print("GPIO pin %s is %s" % (pir_sensor, current_state))
            print("About to take a picture")
            os.system("raspistill -o test1.jpg")
            print("Picture taken")
            os.system("curl -X POST --form \"images_file=@test1.jpg\" --form \"classifier_ids=TKH_849252517\" \"https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=95cf029c3e74886abcdff799eea1165f72c24079&version=2018-03-19\""         
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

