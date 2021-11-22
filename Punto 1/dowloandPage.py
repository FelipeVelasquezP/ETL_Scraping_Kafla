from datetime import datetime
import csv
import json
import boto3
import requests


#Fecha de hoy
today = datetime.now()
year=today.year
month=today.month
day=today.day

# Newspaper url's
news=[('El_Tiempo','https://www.eltiempo.com/'),('El_Espectador','https://www.elespectador.com/')]
for i in news:
        # Newspaper HTML
        page = requests.get(i[1])
        # espectadorHTML = requests.get(espectadorURL, timeout=5000, stream=True)
        filesave = '/tmp/'+i[0]+'.html'

        with open(filesave, 'w', encoding='utf-8') as web:
            web.write(page.text)

        #save in s3
        ruta=f'headlines/raw/periodico={i[0]}/year={year}/month={month}/day={day-1}/{i[0]}.html'
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(filesave, 'newspaperstructure', ruta)
