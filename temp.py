#!/usr/bin/python

import os
import glob
import re
import time
import smtplib
import json

# http://www.d3noob.org/2015/02/raspberry-pi-multiple-temperature_4.html for mysql
# https://stackoverflow.com/questions/15839124/python-pyrrd-and-rrd-with-while-loop for rrdtool
# https://github.com/timofurrer/w1thermsensor library for working with sensor already done.

def check_temp(warning=[]):
    string = ''
    sensorNumber = 0
    if (len(warning) == 0):
        for i in range(len(device_folder)):
            warning.append(0)
    for i in device_folder:
        device_file = i + '/w1_slave'
        line = read_temp(device_file)
        for j in line:
            string += j
    temps = re.findall(r't=(\d+)', string)
    for i in range(len(temps)):
        temp_C = float(temps[i]) / 1000.0 # temperature is displayed as degree in C times 1000 initially
        temp_F = temp_C * 9.0 / 5.0 + 32.0 # convert C to F
        if (temp_F > 79.0 and warning[sensorNumber] < 5):
            warning[sensorNumber] += 1
            print time.strftime("%c") + ": Sensor Number " + str(sensorNumber + 1) + ": " + str(temp_F) + " " # log current temp
            message = "Subject: [#hostname#] Temperature Threshold Warning\n\nSensor number: " + str(sensorNumber + 1) + "\nCurrent temperature reading: "
            message += str(temp_F) + "F\nThreshold: 79.0F\nTimes seen: " + str(warning[sensorNumber]) + "\n\nTesting again in 60sec"
            sendEmail(message)
            time.sleep(60)
            check_temp(warning)
        elif (temp_F > 79.0 and warning[sensorNumber] >= 5):
            warning[sensorNumber] += 1
            print time.strftime("%c") + ": Sensor Number " + str(sensorNumber + 1) + ": " + str(temp_F) + " " # log current temp
            message = "Subject: [#hostname#] Temperature Threshold Warning\n\nSensor number: " + str(sensorNumber + 1) + "\nCurrent temperature reading: "
            message += str(temp_F) + "F\nThreshold: 79.0F\nTimes seen: " + str(warning[sensorNumber]) + "\n\nTesting again in 5min"
            sendEmail(message)
            time.sleep(300)
            check_temp(warning)
        elif (temp_F <= 79.0 and warning[sensorNumber] >= 1):
            print time.strftime("%c") + ": Sensor Number " + str(sensorNumber + 1) + ": " + str(temp_F) + " has recovered!" # log current temp
            message = "Subject: [#hostname#] Temperature Threshold OK\n\nSensor number: " + str(sensorNumber + 1) + "\nCurrent temperature reading: "
            message += str(temp_F) + "F\nThreshold: 79.0F\nWarnings sent prior to recovery: " + str(warning)
            sendEmail(message)
            warning[sensorNumber] = 0
    sensorNumber += 1
    print "\n"
    return

def read_temp(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def sendEmail(message):
    # assuming passwords are kept in a json file
    with open('/home/pi/passwords.json') as f:
        data = json.load(f)
    sender = 'from@example.com'
    receivers = 'to@example.com'
    try:
        smtpObj = smtplib.SMTP('mail.example.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(sender, data["Email"]["from"]) #login to account you're sending from
        smtpObj.sendmail(sender, receivers, message)
        smtpObj.quit()
        print "Successfully sent email"
    except:
        print "Error: unable to send email"
    return

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')
while True:
    check_temp()
    time.sleep(3)
