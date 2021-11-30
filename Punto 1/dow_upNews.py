from datetime import datetime, timedelta
import boto3
import csv

def dowloand_upload_structure(periodic):
    today = datetime.now()
    year=today.year
    month=today.month
    day=today.day
    ruta=f'headlines/final/periodico={periodic}/year={year}/month={month}/day={day}/{periodic}.csv'
    s3 = boto3.resource('s3')
    s3.meta.client.download_file('csvnews', ruta, f'/tmp/{periodic}.csv')
    urlsave=f'news/raw/periodico={periodic}/year={year}/month={month}/day={day}/{periodic}.csv'
    s3.meta.client.upload_file(f'/tmp/{periodic}.csv', 'rawnew',urlsave)


dowloand_upload_structure('El_Tiempo')
dowloand_upload_structure('Publimetro')


