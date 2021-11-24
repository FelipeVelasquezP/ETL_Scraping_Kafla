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

    titleClass = archivoBS.find_all('a', class_='title')
    categoryClass = archivoBS.find_all('a', class_='category')
    urlClass = archivoBS.find_all('h3', class_='title-container')
    titles=newsTitles(titleClass,titles)
    categories=newsCategories(categoryClass,"ET",categories)
    urls,categories=newsUrls(urlClass,urls,categories)
    urlSave="/tmp/"+archivo.replace('html','csv')
    generateCSV(categories, titles, urls, urlSave)
    saveS3(archivo.replace('html','csv'))


def executeEspectador(archivoBS,archivo):
    titles = list()
    categories = list()
    urls = list()
    print('hola0')
    titleClass = archivoBS.find_all('h2', class_='Card-Title')
    categoryClass = archivoBS.find_all('h4', class_='Card-Section')
    titles=newsTitles(titleClass,titles)
    categories=newsCategories(categoryClass,"",categories)
    urls,categories=newsUrls(titleClass,urls,categories)
    # urlSave="/tmp/"+archivo.replace('html','csv')
    # generateCSV(categories, titles, urls, urlSave)
    print('chao')
    # saveS3(archivo.replace('html','csv'))

def normalize(s): #Function to 
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def newsTitles (titleClass,titles):
    for title in titleClass:
        titles.append(title.text)
    return titles

def newsCategories (categoryClass, newspaper , categories):
    for category in categoryClass:
        if newspaper == "ET": category = category.text
        else: category = category.find('a').text
        if category != category.upper():
            categories.append(category)
    return categories

def newsUrls (urlClass, urls, categories):
    for index, url in enumerate(urlClass): 
        scrapedURL = url.find('a')['href']
        urls.append(scrapedURL)
        # Process to check if a news has category
        txt = scrapedURL.split(sep='/')
        hasCategory = True
        for texto in txt:
            normalizeCatedory = normalize(categories[index].lower())
            newTxt = texto.replace('-', ' ')
            if normalizeCatedory in newTxt.split() or normalizeCatedory.split()[0] in newTxt.split():
                hasCategory = False
                break
        if hasCategory: 
            categories.insert(index, "Category Null")
    return urls,categories

def generateCSV(categories, titles, urls, fileName):
    print(len(categories),len(titles), len(urls))
    minTam=min([len(categories),len(titles), len(urls)])
    print(minTam)
    fields = ['Category', 'Title', 'Url']
    rows = []
    for i in range((minTam)-1):
        row = [categories[i], titles[i], urls[i]]
        rows.append(row)
    with open(fileName, 'w',newline='',encoding='utf-8') as f:
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
    urlsave= f'headlines/final/periodico={nameNews}/year={year}/month={month}/day={day}/{filename}'
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(f'/tmp/{filename}', 'csvnews',urlsave)
    

# dowloand_structure('El_Espectador')
dowloand_structure('El_Tiempo')