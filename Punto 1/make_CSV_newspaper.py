from datetime import datetime, timedelta
from io import StringIO
import json
import boto3
from bs4 import BeautifulSoup
import csv
import ntpath

def dowloand_structure(periodic):
    today = datetime.now()
    year=today.year
    month=today.month
    day=today.day
    archivo=f'{periodic}.html'
    ruta=f'headlines/raw/periodico={periodic}/year={year}/month={month}/day={day-1}/{periodic}.html'
    s3 = boto3.resource('s3')
    s3.meta.client.download_file('newspaperstructure', ruta, f'/tmp/{periodic}.html')
    file = open(f'/tmp/{periodic}.html',"r",encoding='utf-8')
    archivoBS = BeautifulSoup(file.read(), 'html.parser')
    titles = list()
    categories = list()
    urls = list()
    ind=""
    if archivo=='El_Tiempo.html': 
        executeTiempo(archivoBS,archivo)
        ind="ET"
    else:
        executeEspectador(archivoBS,archivo)
 
def executeTiempo(archivoBS,archivo):
    titles = list()
    categories = list()
    urls = list()
    communET = archivoBS.find_all('a', class_='title')

    # Begins the scraping for "El Tiempo"
    newsTitles(communET)
    newsCategories(communET, "ET")
    newsUrls(communET, "ET")
    generateCSV(categories, titles, urls, "El Tiempo.csv")
    
    urlSave="/tmp/"+archivo.replace('html','csv')
    generateCSV(categories, titles, urls, urlSave)
    saveS3(archivo.replace('html','csv'))


def executePublimetro(archivoBS,archivo):
    titles = list()
    categories = list()
    urls = list()
    print('Starting publimetro scraping')
    titleClassv1 = archivoBS.find_all('a', class_='headline')
    titleClassv2 = archivoBS.find_all('a', class_='card-list--headline-link')
    titleClassv3 = archivoBS.find_all('a', class_='sm-promo-headline')
    titleClassv4 = archivoBS.find_all('div', class_='results-list--headline-container')
    titleClass = [titleClassv1, titleClassv2, titleClassv3, titleClassv4]

    # Begins the scraping for "Publimetro"
    neasted = False
    for titleList in titleClass:
        if titleClass[3] == True: neasted = True
        newsTitles(titleList, nested_a = neasted)
        newsCategories(titleList, newspaper="PB", nested_a = neasted)
        newsUrls(titleList, nested_a = neasted)
    print('Starting publimetro scraping')
    urlSave="/tmp/"+archivo.replace('html','csv')
    generateCSV(categories, titles, urls, urlSave)
    saveS3(archivo.replace('html','csv'))

# Newspaper url's
tiempoURL = "https://www.eltiempo.com"
publimetroURL = "https://www.publimetro.co"

def newsTitles (titleClass, titles, nested_a = False):
    for title in titleClass:
        if nested_a:
            titleScraped = titles.find('a')
            titles.append(titleScraped.text)
        else: titles.append(title.text)
    return titles

def newsCategories (categoryClass, categories, newspaper = "", nested_a = False):
    for category in categoryClass:
        if nested_a:
            scrapedCategory = category.find('a')['href']
        else:
            scrapedCategory = category.get('href','')
        txt = scrapedCategory.split(sep='/')
        if newspaper == "PB":
            if len(txt) > 2:
                if txt[0] == "https:": categories.append("banner publicitario")
                else: categories.append(txt[1])
            else: categories.append("No category")
        else: categories.append(txt[1]+"/"+txt[2])
    return categories


def newsUrls (urlClass, urls, newspaper = "", nested_a = False):
    for url in urlClass: 
        if nested_a:
            scrapedURL = url.find('a')['href']
        else:
            scrapedURL = url.get('href','')
        if newspaper == "ET": urls.append(tiempoURL+scrapedURL)
        else:  urls.append(publimetroURL+scrapedURL)
    return urls

def generateCSV(categories, titles, urls, fileName):
    print(len(categories),len(titles), len(urls))
    fields = ['Category', 'Title', 'Url']
    rows = []

    for i in range(len(categories)):
        row = [categories[i], titles[i], urls[i]]
        rows.append(row)

    with open(fileName, 'w', encoding="utf-8") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
        print("Scraping successful.\nFinal file: ", fileName)

    titles.clear()
    categories.clear()
    urls.clear()

def saveS3(filename):
    nameNews=filename.replace('csv','')
    today = datetime.now()
    year=today.year
    month=today.month
    day=today.day
    urlsave= f'headlines/final/periodico={nameNews}/year={year}/month={month}/day={day-1}/{filename}'
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(f'/tmp/{filename}', 'csvnews',urlsave)
    

dowloand_structure('El_Tiempo')
dowloand_structure('Publimetro')