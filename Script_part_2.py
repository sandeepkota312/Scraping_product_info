import pandas as pd
from bs4 import BeautifulSoup
import requests as req
import time

df = pd.read_csv('dataset_part_1.csv')
# print(df)

Urls=df['product_link']
# print(len(Urls))
parameters=['product_url','ASIN','product_description','product_manufacturer']
dataset={key: [] for key in parameters}

for index,url in enumerate(Urls):
    # url='https://www.amazon.in/Skybags-Brat-Black-Casual-Backpack/dp/B08Z1HHHTD'
    print(index+1,'url:',url)
    time.sleep(3)
    r=req.get(url)
    limit=7
    while r.status_code==503 and limit>0:
        time.sleep(4)
        r=req.get(url)
        limit-=1
    if r.status_code==200:
        soup=BeautifulSoup(r.content,'lxml')
        try:
            ASIN_table=soup.find('table',id='productDetails_detailBullets_sections1')
            ASIN=ASIN_table.find('td',class_='a-size-base prodDetAttrValue').get_text()
        except:
            ASIN_table=soup.find('div',id='detailBullets_feature_div')
            for content in ASIN_table.find_all('li'):
                section=str(content.find('span',class_='a-text-bold').get_text()).replace(" ","").replace("\n","")[:-3]
                # print('section',section,len(section))
                if section=="ASIN":
                    ASIN=str(content.find('span',class_='a-text-bold').find_next('span').get_text()).replace(" ","").replace("\n","")
                    break
        print('ASIN',ASIN)
        try:
            Manufacturer_table=soup.find('table',id='productDetails_techSpec_section_1').find_all('tr')
            for content in Manufacturer_table:
                section=str(content.find('th').get_text()).replace(" ","").replace("\n","")
                if section=="Manufacturer":
                    Manufacturer=str(content.find('td').get_text()).replace(" ","").replace("\n","")
                    break
        except:
            Manufacturer_table=soup.find('div',id='detailBullets_feature_div').find_all('li')
            for content in Manufacturer_table:
                section=str(content.find('span',class_="a-text-bold").get_text()).replace(" ","").replace("\n","")[:-3]
                # print('section',section)
                if section=="Manufacturer":
                    Manufacturer=str(content.find('span',class_="a-text-bold").find_next('span').get_text()).replace(" ","").replace("\n","")
                    break
        print('Manufacturer',Manufacturer)
        
        Info=soup.find('ul',class_='a-unordered-list a-vertical a-spacing-mini').find_all('li',class_='a-spacing-mini')
        Merged_desc=''
        for point in Info:
            Merged_desc+=point.find('span').get_text()+'\n'
        print('Merged_desc',Merged_desc)
        dataset['product_url'].append(url)
        dataset['ASIN'].append(ASIN)
        dataset['product_description'].append(Merged_desc)
        dataset['product_manufacturer'].append(Manufacturer)
        print('Success')
        pass
    else:
        print(f'site {url} was not hit. Code:',r.status_code)

df2 = pd.DataFrame(dataset)
df2.to_csv('dataset_part_2.csv', index=False)
print('output',df2)