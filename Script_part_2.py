import pandas as pd
from bs4 import BeautifulSoup
import requests as req
import time

# loaded previously extracted product data
df = pd.read_csv('dataset_part_1.csv')

# Stored product links 
Urls=df['product_link']

# part 2 output parameters
parameters=['product_url','ASIN','product_description','product_manufacturer']

# storing links that are failed to load
failed_urls=[]

# empty part 2 file
df1=pd.read_csv('dataset_part_2.csv')
check=1
for iterations in range(2):
    # dictionary to store parameter values
    dataset={key: [] for key in parameters}
    for index,url in enumerate(Urls):
        # url='https://www.amazon.in/Skybags-Brat-Black-Casual-Backpack/dp/B08Z1HHHTD'

        print(index+1,'url:',url)

        # fetching data from url using requests
        time.sleep(4)
        r=req.get(url)
        limit=5
        while r.status_code==503 and limit>0:
            time.sleep(4)
            r=req.get(url)
            limit-=1

        if r.status_code==200:
            # extracting content from requests in lxml format
            soup=BeautifulSoup(r.content,'lxml')

            # ASIN parameter
            try:
                ASIN_table=soup.find('table',id='productDetails_detailBullets_sections1')
                ASIN=ASIN_table.find('td',class_='a-size-base prodDetAttrValue').get_text()
            except:
                try:
                    ASIN_table=soup.find('div',id='detailBullets_feature_div')
                    for content in ASIN_table.find_all('li'):
                        section=str(content.find('span',class_='a-text-bold').get_text()).replace(" ","").replace("\n","")[:-3]
                        if section=="ASIN":
                            ASIN=str(content.find('span',class_='a-text-bold').find_next('span').get_text()).replace(" ","").replace("\n","")
                            break
                except:
                    ASIN='Not Availble'
            
            # Manufacturer parameter
            try:
                Manufacturer_table=soup.find('table',id='productDetails_techSpec_section_1').find_all('tr')
                for content in Manufacturer_table:
                    section=str(content.find('th').get_text()).replace(" ","").replace("\n","")
                    if section=="Manufacturer":
                        Manufacturer=str(content.find('td').get_text()).replace(" ","").replace("\n","")
                        break
            except:
                try:
                    Manufacturer_table=soup.find('div',id='detailBullets_feature_div').find_all('li')
                    for content in Manufacturer_table:
                        section=str(content.find('span',class_="a-text-bold").get_text()).replace(" ","").replace("\n","")[:-3]
                        if section=="Manufacturer":
                            Manufacturer=str(content.find('span',class_="a-text-bold").find_next('span').get_text()).replace(" ","").replace("\n","")
                            break
                except:
                    Manufacturer='Not Available'
            
            # product Information paramter
            Info=soup.find('ul',class_='a-unordered-list a-vertical a-spacing-mini').find_all('li',class_='a-spacing-mini')
            Merged_desc=''
            for point in Info:
                Merged_desc+=point.find('span').get_text()+'\n'

            print('ASIN',ASIN)
            print('Manufacturer',Manufacturer)
            print('Merged_desc',Merged_desc)

            # adding the parameters into dictionary
            dataset['product_url'].append(url)
            dataset['ASIN'].append(ASIN)
            dataset['product_description'].append(Merged_desc)
            dataset['product_manufacturer'].append(Manufacturer)
            print('Success')
            pass
        else:
            # site didn't load
            print(f'site {url} was not hit. Code:',r.status_code)

            # adding url in failed_urls array
            if check==1:
                failed_urls.append(url)
    
    # saving data into csv file
    df2 = pd.DataFrame(dataset)
    df1=pd.concat([df1,df2],ignore_index=True)
    df1.to_csv('dataset_part_2.csv', index=False)

    # retrying failed urls
    if check==1:
        print(len(failed_urls),'urls failed.\n Retrying.....')
    Urls=failed_urls
    check=0
    failed_urls=[]