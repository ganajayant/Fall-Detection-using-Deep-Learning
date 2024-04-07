# Code for the subscriber to receive the sensor data and make predictions

import json
import os
import smtplib
import sqlite3
from os.path import dirname, join

import numpy as np
import pandas as pd
import pika
from dotenv import load_dotenv
from keras.models import load_model

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


url = os.getenv("CLOUDAMQP_URL")
params = pika.URLParameters(url)
model = load_model("Model.h5")
gmail_user = os.environ.get("EMAIL")
gmail_app_password = os.environ.get("PASSWORD")
send_from = os.environ.get("EMAIL")


def indextolabel(index):
    label = ['Stand', 'Fall', 'On Floor']
    return label[index[0]]


def get_db_connection(dir='db/database.db'):
    conn = sqlite3.connect(dir)
    conn.row_factory = sqlite3.Row
    return conn


def send_mailer(sender, body, subject="Alert there is a fall"):
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.ehlo()
            server.login(gmail_user, gmail_app_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(send_from, sender, message)
    except smtplib.SMTPAuthenticationError:
        print("Error: SMTP authentication failed! Please check your credentials.")
    except smtplib.SMTPException as e:
        print(f"Error: Failed to send email. {e}")


with pika.BlockingConnection(params) as connection:
    channel = connection.channel()
    channel.queue_declare(queue="sensor_data_queue")

    def callback(ch, method, properties, body):
        x = json.loads(body)
        ax = x['accelerometer_x']
        ay = x['accelerometer_y']
        az = x['accelerometer_z']
        gx = x['gyroscope_x']
        gy = x['gyroscope_y']
        gz = x['gyroscope_z']
        lat = x['lat']
        longi = x['longi']
        test = pd.DataFrame([[ax, ay, az, gx, gy, gz]], columns=[
                            'Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz'])
        y_pred = np.argmax(model.predict(test), axis=-1)
        prediction = indextolabel(y_pred)
        if prediction == "Fall":
            print(f"Prediction: {prediction}")
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Accidents(accelerometer_x, accelerometer_y, accelerometer_z, gyroscope_x, gyroscope_y, gyroscope_z, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ax, ay, az, gx, gy, gz, lat, longi))
            conn.commit()
            cursor.close()
            conn.close()
            location = f"https://www.google.com/maps/search/?api=1&query={
                lat:.6f},{longi:.6f}"
            send_mailer("ganajayant.s20@iiits.in",
                        f"Fall detected with accelerometer values: {ax}, {ay}, {az} and gyroscope values: {gx}, {gy}, {gz} at location {location} ")
    channel.basic_consume(queue="sensor_data_queue",
                          on_message_callback=callback, auto_ack=True)

    print("Waiting for messages...")
    channel.start_consuming()
