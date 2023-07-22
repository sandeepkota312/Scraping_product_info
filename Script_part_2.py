import pandas as pd
from bs4 import BeautifulSoup
import requests as req
import time

df = pd.read_csv('dataset_part_1.csv')
# print(df)

Urls=df['product_link']
# print(len(Urls))
parameters=['Description','ASIN','product_description','product_manufacturer']
dataset={key: [] for key in parameters}

# for url in Urls:
url='https://www.amazon.in/American-Tourister-AMT-SCH-02/dp/B07CJCGM1M'
print('url:',url)
r=req.get(url)
limit=7
time.sleep(2)
while r.status_code==503 and limit>0:
    time.sleep(3)
    r=req.get(url)
    limit-=1
if r.status_code==200:
    soup=BeautifulSoup(r.content,'lxml')
    ASIN_table=soup.find('table',id='productDetails_detailBullets_sections1')
    ASIN=ASIN_table.find('td',class_='a-size-base prodDetAttrValue').get_text()
    print('ASIN',ASIN)

    Manufacturer_table=soup.find('table',id='productDetails_techSpec_section_1').find_all('tr')
    Manufacturer=Manufacturer_table[10].find('td').get_text()
    Manufacturer=str(Manufacturer).replace(" ","").replace("\n","")
    print('Manufacturer',Manufacturer,len(Manufacturer))
    
    Info=soup.find('ul',class_='a-unordered-list a-vertical a-spacing-mini').find_all('li',class_='a-spacing-mini')
    Merged_desc=''
    for point in Info:
        Merged_desc+=point.find('span').get_text()+'\n'
    print('Merged_desc',Merged_desc)
    print('Success')
    pass
else:
    print(f'site {url} was not hit. Code:',r.status_code)