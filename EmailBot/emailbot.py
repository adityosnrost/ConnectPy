#!env/bin/python
from datetime import datetime

import pymysql
import pymysql.cursors

import random
import string
import smtplib
import os
import json

import time

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate

import schedule

with open('config.json') as data_file:
    dataConfig = json.load(data_file)

# Main Job that getting data from Analytics and store them in redis
def job():

    emails = [
        {"email" : "email1@gmail.com",  "password" : "password1"}
    ]

    emailNumber = 0

    db = pymysql.connect(dataConfig['database']['url'], dataConfig['database']['username'], dataConfig['database']['password'], dataConfig['database']['dbname'])

    # Prepare SQL query to INSERT a record into the database.
    cursor = db.cursor()
    try:
        # Execute the SQL command
        cursor.execute("SELECT filename, email, id FROM emailshare WHERE status = 1 ")
        data = cursor.fetchall()
        #print str(data)
        for row in data:
            pathFile = row[0].replace('-', '\\')
            emailaddress = row[1]
            idDB = row[2]
            print(pathFile + " " + row[1])

            if emailNumber >= len(emails):
                emailNumber = 0
                
            print(emailNumber)

            sender = emails[emailNumber]["email"]
            receiver = [emailaddress]

            img_data = open(pathFile, 'rb').read()
            msg = MIMEMultipart()
            msg['Subject'] = "Subject"
            msg['From'] = sender
            msg['To'] = receiver[0]

            text = MIMEText("Thank You for Coming to GSK")
            msg.attach(text)
            image = MIMEImage(img_data, name=os.path.basename(pathFile))
            msg.attach(image)


            try:
                session = smtplib.SMTP('smtp.gmail.com', 587)
                session.ehlo()
                session.starttls()
                session.ehlo()
                session.login(sender,emails[emailNumber]["password"])
                session.sendmail(sender,receiver,msg.as_string())
                session.quit()

                try:
                    # Execute the SQL command
                    cursor.execute('UPDATE emailshare SET status = 2 WHERE id = %s' % \
                    (idDB))
                    # Commit your changes in the database
                    db.commit()
                except:
                    # Rollback in case there is any error
                    db.rollback()

            except smtplib.SMTPException as e:
                print("Failed to sending email")

            emailNumber = emailNumber + 1
        
    except Exception as e:
        print(e)
        # Rollback in case there is any error
        print("Getting data from Database failed")
    
    db.close()

    print("Job End")

# schedule.every().day.at("23:59").do(job)
schedule.every(15).minutes.do(job)
# schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

# job()