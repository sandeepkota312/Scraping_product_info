import requests as req
from bs4 import BeautifulSoup
import time
import pandas as pd 

# URL of the Amazon site
amazon_base_url = 'https://www.amazon.in'
parameters=['product_link','product_name','product_price','product_rating','product_No_of_reviews']
dataset={key: [] for key in parameters}
for index in range(1,21):
    print('page',index)
    r=req.get(f'https://www.amazon.in/s?k=bags&ref=sr_pg_{index}')
    limit=7
    time.sleep(2)
    while r.status_code==503 and limit>0:
        r=req.get(f'https://www.amazon.in/s?k=bags&ref=sr_pg_{index}')
        time.sleep(3)
        limit-=1
    if r.status_code==200:
        soup=BeautifulSoup(r.content,'lxml')
        products=soup.find_all('div',class_ ="a-section a-spacing-small a-spacing-top-small")
        print(len(products),'products')
        key=0
        for product in products:
            # dataset['product_link'].append(product.find_all('a',class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal", href=True))
            try:
                dataset['product_name'].append(product.find('span',class_='a-size-medium a-color-base a-text-normal').get_text())
                dataset['product_price'].append(product.find('span',class_='a-offscreen').get_text())
                dataset['product_rating'].append(product.find('span',class_="a-icon-alt").get_text())
                dataset['product_No_of_reviews'].append(product.find('span',class_="a-size-base s-underline-text").get_text())
                for product_link in product.find_all('a',class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal", href=True):
                    try:
                        dataset['product_link'].append(amazon_base_url + product_link['href'])
                    except:
                        pass
            except:
                pass
    else:
        print('site '+ f'https://www.amazon.in/s?k=bags&ref=sr_pg_{index}' + ' was not hit. Code:',r.status_code)

# Convert the dictionary to a DataFrame
df = pd.DataFrame(dataset)
df.to_csv('dataset_part_1.csv', index=False)
print('output',df)

