import requests
import sqlalchemy #pour faire du CRUD sur une base sql 
from tqdm import tqdm # progress bar: https://tqdm.github.io/
import os #pour créer un dossier sur le disque 
import pandas as pd
from bs4 import BeautifulSoup

#le nom du livre
Title = []
#la note moyenne des avis (le nombre d'étoiles)
Rating = []
#scraper de lien du livre
Link = []
Categorie = []
#le nombre de livres en stock
Stock = []
#le prix
Price = []
#l'UPC (le numéro d'edition)
Upc = []
#Le lien de l'image du livre 
Image = []

#folder_name = "Images_livres"
#os.makedirs(folder_name)

#acceder à chacune des 50 pages et des 20 livres
for i in tqdm(range(1, 51)):
    page = f'http://books.toscrape.com/catalogue/page-{i}.html'
    req = requests.get(page) 
    soup5 = BeautifulSoup(req.content, 'html.parser')
    allbooks = soup5.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    #page_livre=
    for book in allbooks: 
        title = book.h3.a['title']
        price = float((book.find('p',{'class': 'price_color'})).text[2:])
        rating= book.find('p', class_="star-rating").attrs['class'][1]
        url = book.h3.a['href']
        #On explore chacune des pages des livres du catalogue
        #pour extraire la categorie, le résumé et l'upc
        link = f'http://books.toscrape.com/catalogue/{url}'
        requette = requests.get(link)
        soup6 = BeautifulSoup(requette.content, 'html.parser')
        Category = soup6.find_all('li')[2].text
        table = soup6.find('table',{'class': 'table table-striped'})
        upc_find = table.tr.find('td').text

        #Pour les données de stock on navigue jusqu'à l'élément Table Header(TH) contenant "availability"
        availability_row = table.find('th', string='Availability').find_next('td').text
        #On extrait uniquement la valeur et on strip() le texte, on effectue une conversion en integer
        stock_qt = int(availability_row.strip('In stock ( available)'))

        #extraction de l'image
        div_active = soup6.find('div',{'class': 'item active'})
        #on trouve l'element image
        img = div_active.find('img')
        img_url = img['src']
        #pour obtenir l'url complète et non l'url relative on update la variable avec le chemin complet
        img_url = 'http://books.toscrape.com/' + img_url.strip('../../')

        Title.append(title)
        Price.append(price)
        Rating.append(rating)
        Categorie.append(Category)
        Stock.append(stock_qt)
        Upc.append(upc_find)
        Image.append(img_url)
        #on peut telecharger l'image localement
        #image_raw = requests.get(img_url).content
        # Enregistrer l'image dans le dossier créé
        #img_name = os.path.join(folder_name, "book_image.jpg")  # Chemin du fichier image
        #with open(img_name, 'wb') as handler:
        #    handler.write(image_raw)
        Link.append(link)

df = pd.DataFrame({'Titre':Title, 'Prix':Price, 'Rating':Rating, 'Stock': Stock, 'Lien': Link, 'Categorie': Categorie, 'UPC': Upc, 'Image': Image})

# Using shape to get the size of the dataframe
rows, columns = df.shape
print(f"Number of rows: {rows}, Number of columns: {columns}")
infos = df.info()
#describe = df.describe()
#On exporte le datagramme au format csv
df.to_csv('book_scraping.csv', index=False) 

#On peut également exporter au format excel:
datatoexcel = pd.ExcelWriter('book_scrapping.xlsx')

# write DataFrame to excel
df.to_excel(datatoexcel)

# save the excel
datatoexcel.close()

