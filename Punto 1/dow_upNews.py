from datetime import datetime, timedelta
import boto3
import csv

def dowloand_upload_structure(periodic):
    today = datetime.now()
    year=today.year
    month=today.month
    day=today.day
    ruta=f'headlines/final/periodico={periodic}/year={year}/month={month}/day={day-1}/{periodic}.csv'
    print('hola 1')
    print(ruta)
    s3 = boto3.resource('s3')
    s3.meta.client.download_file('csvnews', ruta, f'/tmp/{periodic}.csv')
    print('hola 2')
    urlsave=f'news/raw/periodico={periodic}/year={year}/month={month}/day={day-1}/{periodic}.csv'
    print('hola 3')
    s3.meta.client.upload_file(f'/tmp/{periodic}.csv', 'rawnew',urlsave)
    print('hola 4')

dowloand_upload_structure('El_Tiempo')

