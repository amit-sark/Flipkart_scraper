import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import csv
import time 
class FlipScrape: 
    def __init__(self, link):
        self.link = link
        self.re = requests.get(url=self.link)

    def data_parser(self):
        context = BeautifulSoup(self.re.text, 'lxml')

        def get_text(selector, default="N/A"):
            element = context.find(*selector)
            return element.text.strip() if element else default
        
        brand = get_text(('span', {'class': 'mEh187'}))
        title = get_text(('span', {'class': 'VU-ZEz'}))
        mark = "Assured Product!" if context.find('span', {'class': '+N9xME hxqV2A'}) else "Not Assured"
        mrp = get_text(('div', {'class': 'yRaY8j A6+E6v'}))
        price = get_text(('div', {'class': 'Nx9bqj CxhGGd'}))
        discount = get_text(('div', {'class': 'UkUFwK WW8yVX dB67CR'}), "0%")
        ratting = get_text(('span', {'class': 'Wphh3N'}), "ZERO RATING")
        stock_status = "STOCK OUT" if context.find('div', {'class': 'Z8JjpR'}) else "IN STOCK"
        
        image_element = context.find('img', {'class': '_53J4C- utBuJY'})
        image = image_element['src'] if image_element else "No Image Available"
        
        product_data = {
            "Brand": brand,
            "Title": title,
            "Assurity": mark,
            "MRP": mrp,
            "Stock": stock_status,
            "Price": price,
            "Discount": discount,
            "Rating": ratting,
            "Image": image,
            "Product Link": self.link
        }
        print(product_data,"\n")
        return product_data

def fetch_product_data(product_id):
    link = f"https://www.flipkart.com/product/p/item?pid={product_id.strip()}"
    scraper = FlipScrape(link)
    return scraper.data_parser()

def main():
    start_time = time.time()
    with open('ffsid.txt', mode='r') as file:
        product_ids = file.readlines()

    with open('flipkart_products.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Brand", "Title", "Assurity", "MRP", "Stock", "Price", "Discount", "Rating", "Image", "Product Link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = executor.map(fetch_product_data, product_ids)

        for product in results:
            writer.writerow(product)
    end_time = time.time()        

    print(f"\nTotal Consumed time: {start_time-end_time}✅ Data  successfully in flipkart_products.csv")

if __name__ == "__main__":

    main()
