"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, g, make_response, request, Flask, redirect, url_for, abort
from flask.json import jsonify
from flask_cors import CORS
from FlaskEmail import app

import MySQLdb
import MySQLdb.cursors

import random
import string
import smtplib
import os
import json

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate

import sys
from PIL import Image, ImageWin

with open('config.json') as data_file:
    dataConfig = json.load(data_file)

emails = [
	    {"email" : "email1@gmail.com",  "password" : "password1"}
	]

emailNumber = 0

@app.before_request
def beginning():
    g.db = MySQLdb.connect(dataConfig['database']['url'], dataConfig['database']['username'], dataConfig['database']['password'], dataConfig['database']['dbname'])

@app.after_request
def endingreq(response):
    g.db.close()
    return response

@app.route('/email2', methods=['POST', 'GET'])
def home():
        # print str(request.form["pathFile"])
        sender = "email1"
        receiver = ["email2"]
        message = "\r\n".join([
             "From: email1",
             "To: email2",
             "Subject: Photo.",
             "",
             "Hello,",
             "Thank You"
             ])

        try:
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.ehlo()
            session.starttls()
            session.ehlo()
            session.login(sender,'password')
            session.sendmail(sender,receiver,message)
            session.quit()
        except smtplib.SMTPException as e:
            # print str(e)
            return jsonify({'status':"failed"}), 400

        return jsonify({'status':"success"}), 200


@app.route('/email', methods=['POST', 'GET'])
def home2():
		pathFile = str(request.form["pathFile"])
		emailaddress = str(request.form["emailaddr"])
		name = str(request.form["name"])
		city = str(request.form["city"])
		age = str(request.form["age"])
		photoName = str(request.form["photoName"])
		telephone = str(request.form["telephone"])


		file_name = pathFile
		file_name_out = photoName
		img = Image.open (file_name)
		result_width = 1080
		result_height = 1080

		# 1920x1080 to 1080x1080
		# border_height = (img.height-result_height)/2
		# border_width = (img.width-result_width)/2
		# print border_height
		# print border_width
		# img = img.crop((border_width, border_height, img.width-border_width, img.height-border_height))

		# Custom calculation
		# border_width = (img.width-result_width)/2
		# img = img.crop((border_width, 340, img.width-border_width, 1350))

		# img.save(file_name_out)

		#Custum Resolution version 2
		border_width = (img.width - result_width)/2
		border_height = (img.height - result_height)/2
		img = img.crop((border_width, border_height, img.width - border_width, img.height - border_height))
			
		img.save(file_name_out)

		global emails
		global emailNumber

		print(emailNumber)
		print(emails[emailNumber]["email"])

		if emailNumber >= len(emails):
			emailNumber = 0

		sender = emails[emailNumber]["email"]
		receiver = [emailaddress]


		img_data = open(file_name_out, 'rb').read()
		msg = MIMEMultipart()
		msg['Subject'] = "Subject"
		msg['From'] = "ALIAS <" + sender + ">"
		msg['To'] = receiver[0]

		text = MIMEText("Thank You")
		msg.attach(text)
		image = MIMEImage(img_data, name=os.path.basename(file_name_out))
		msg.attach(image)

		# Prepare SQL query to INSERT a record into the database.
		db = g.db
		cursor = db.cursor()
		try:
			# Execute the SQL command
			cursor.execute('INSERT INTO emailshare(filename, email, name, city, age, telephone) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")' % \
						 (photoName, emailaddress, name, city, age, telephone))
			# Commit your changes in the database
			db.commit()
			
			lastid = cursor.lastrowid
			
		except:
			# Rollback in case there is any error
			db.rollback()
			print("error db insert")
			emailNumber = emailNumber + 1
			return jsonify({'status':"failed"}), 400

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
							 (lastid))
				# Commit your changes in the database
				db.commit()
			except:
				# Rollback in case there is any error
				db.rollback()
				print("error db update")
				emailNumber = emailNumber + 1
				return jsonify({'status':"failed"}), 400
			
		except smtplib.SMTPException as e:
			print(str(e))
			emailNumber = emailNumber + 1
			return jsonify({'status':"failed"}), 400

		emailNumber = emailNumber + 1
		return jsonify({'status':"success"}), 200
