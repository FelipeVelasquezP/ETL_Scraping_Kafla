from bs4 import BeautifulSoup
import requests
import csv

# Newspaper url's
tiempoURL = "https://www.eltiempo.com"

# Newspaper HTML
tiempoHTML = requests.get(tiempoURL)

# Conversion HTML to BS
tiempoBS = BeautifulSoup(tiempoHTML.content, 'html.parser')

# Utils
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

# Lists
titles = list()
categories = list()
urls = list()

def newsTitles (titleClass):
    for title in titleClass:
        titles.append(title.text)

def newsCategories (categoryClass, newspaper = ""):
    for category in categoryClass:
        scrapedCategory = category['href']
        txt = scrapedCategory.split(sep='/')
        categories.append(txt[1]+"/"+txt[2])

def newsUrls (urlClass, newspaper = ""):
    for url in urlClass: 
        scrapedURL = url['href']
        if newspaper == "ET": urls.append(tiempoURL+scrapedURL)
        else:  urls.append(scrapedURL)


def generateCSV(categories, titles, urls, fileName):
    print(len(categories),len(titles), len(urls))
    fields = ['Category', 'Title', 'Url']
    rows = []

    for i in range(len(categories)):
        row = [categories[i], titles[i], urls[i]]
        rows.append(row)

    with open(fileName, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
        print("Scraping successful.\nFinal file: ", fileName)

    titles.clear()
    categories.clear()
    urls.clear()

""" El Tiempo """
communET = tiempoBS.find_all('a', class_='title')
titleClass = communET
categoryClass = communET
urlClass = communET

# Begins the scraping for "El Tiempo"
newsTitles(titleClass)
newsCategories(categoryClass, "ET")
newsUrls(urlClass, "ET")
generateCSV(categories, titles, urls, "El Tiempo.csv")



