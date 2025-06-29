import requests
import json
from bs4 import BeautifulSoup
git add .
import csv



url="https://books.toscrape.com"

def scrape_books(url):
    response= requests.get(url)
    #print(response)
    #print(response.status_code)
    if response.status_code !=200:
        print("failed to load page")
        return []

    response.encoding = response.apparent_encoding
    #print(response.text)
    soup= BeautifulSoup(response.text, 'html.parser')
    books= soup.find_all('article', class_='product_pod')
    #print(books) 

    book_list=[]
    for book in books:
        title= book.h3.a['title'] 
        #print(title)
        price_text= book.find('p', class_='price_color').text
        #print(price_text)
        currency= price_text[0]
        price= float(price_text[1:])
        #print(title, currency, price)
        book_list.append({
            'title': title,
            'currency': currency,
            'price': price
        })
    #print(book_list)
    return book_list
    
all_books= scrape_books(url)

with open('books.json', 'w', encoding='utf-8') as f:
    json.dump(all_books, f, indent=4, ensure_ascii=False)

with open('books.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'currency', 'price'])
    writer.writeheader()
    writer.writerows(all_books)