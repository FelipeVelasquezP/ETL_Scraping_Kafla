from bs4 import BeautifulSoup
import requests
import csv

# Newspaper url's
tiempoURL = "https://www.eltiempo.com"
publimetroURL = "https://www.publimetro.co"

# Newspaper HTML
tiempoHTML = requests.get(tiempoURL)
publimetroHTML = requests.get(publimetroURL)

# Conversion HTML to BS
tiempoBS = BeautifulSoup(tiempoHTML.content, 'html.parser')
publimetroBS = BeautifulSoup(publimetroHTML.content, 'html.parser')
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

def newsTitles (titleClass, nested_a = False):
    for title in titleClass:
        if nested_a:
            titleScraped = titles.find('a')
            titles.append(titleScraped.text)
        else: titles.append(title.text)

def newsCategories (categoryClass, newspaper = "", nested_a = False):
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


def newsUrls (urlClass, newspaper = "", nested_a = False):
    for url in urlClass: 
        if nested_a:
            scrapedURL = url.find('a')['href']
        else:
            scrapedURL = url.get('href','')
        if newspaper == "ET": urls.append(tiempoURL+scrapedURL)
        else:  urls.append(publimetroURL+scrapedURL)


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

""" El Tiempo """
communET = tiempoBS.find_all('a', class_='title')

# Begins the scraping for "El Tiempo"
newsTitles(communET)
newsCategories(communET, "ET")
newsUrls(communET, "ET")
generateCSV(categories, titles, urls, "El Tiempo.csv")

""" Publimetro """
titleClassv1 = publimetroBS.find_all('a', class_='headline')
titleClassv2 = publimetroBS.find_all('a', class_='card-list--headline-link')
titleClassv3 = publimetroBS.find_all('a', class_='sm-promo-headline')
titleClassv4 = publimetroBS.find_all('div', class_='results-list--headline-container')
titleClass = [titleClassv1, titleClassv2, titleClassv3, titleClassv4]

# Begins the scraping for "Publimetro"
neasted = False
for titleList in titleClass:
    if titleClass[3] == True: neasted = True
    newsTitles(titleList, nested_a = neasted)
    newsCategories(titleList, newspaper="PB", nested_a = neasted)
    newsUrls(titleList, nested_a = neasted)

generateCSV(categories, titles, urls, "Publimetro.csv")
