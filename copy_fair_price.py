import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.request import urlopen

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

Fairprice_data=[]
count=0

url = 'https://fairprice.com.sg/categories'
html_page = session.get(url,headers=headers)
soup = BeautifulSoup(html_page.content,'html.parser')
mai = soup.find_all("ul",class_="sc-qg4l23-7 gcQtZV")

for kl,i in enumerate(mai):
    for t in range(10,20):

        if kl==t:
            kp = i.find_all('li',class_="sc-qg4l23-8 ekvzaK")
            for ty,tu in enumerate(kp):
                if tu.find('a',class_="sc-qg4l23-9 jYHTwT"):
                    count+=1
            print(count)
            for lo,kr in enumerate(kp):
                for u in range(count):
                    if lo==u:
                        category_link = kr.find('a',class_="sc-qg4l23-9 jYHTwT")['href']
                        base_category_link = f"https://fairprice.com.sg{category_link}"
                        print(base_category_link)

                        print("I am loop of category",t)
                        html_page1 = session.get(base_category_link)
                        soup1 = BeautifulSoup(html_page1.content,'html.parser')
                        try:
                            product_lim = soup1.find('span',class_="sc-1bsd7ul-1 kouteV").text
                            product_limit = int(product_lim[:2])
                        except:
                            product_limit = 50
                        print(product_limit)

                        link_of_div = soup1.find_all('div',class_="sc-1plwklf-0 iknXK product-container")

                        for ap,k in enumerate (link_of_div):
                            for akl in range(product_limit):
                                if ap == akl:
                                    print(f"I am loop of Product {akl} of category {t}")
                                    link_of_pro = k.find('a',class_="sc-1plwklf-3 bmUXOR")['href']
                                    base_link_of_pro = f"https://fairprice.com.sg{link_of_pro}"
                                    
                                    html_page2 = session.get(base_link_of_pro)
                                    soup2 = BeautifulSoup(html_page2.content,'html.parser')
                                    try:
                                        price = soup2.find('span',class_="sc-1bsd7ul-1 sc-13n2dsm-5 kxEbZl deQJPo").text
                                    except:
                                        price='None'
                                    try:
                                        name = soup2.find('span',class_="sc-1bsd7ul-1 cZuPIJ").text
                                    except:
                                        name="None"
                                    try:
                                        brand = soup2.find('a',class_="sc-13n2dsm-1 jLtMNk").text
                                    except:
                                        brand="None"
                                    try:
                                        sold_by = soup2.find('div',class_="sc-16yemxd-0 gOtEQZ").text
                                    except:
                                        sold_by='None'
                                    try:
                                        Net = soup2.find('span',class_="sc-1bsd7ul-1 sc-13n2dsm-13 gDxsDx liuneL").text
                                    except:
                                        Net='None'
                                    # try:
                                    #     Country_origin = soup2.find('span',class_="sc-1bsd7ul-1 sc-3zvnd-10 kEUDke hpuhl").text
                                    # except:
                                    #     Country_origin="None"
                                    images = soup2.find_all('li',class_="sc-10zw1uf-14")
                                    img1='None'
                                    img2='None'
                                    img3='None'
                                    img4='None'
                                    for p,image in enumerate(images):
                                        if p==0:
                                            img1 = image.find('img',class_="sc-10zw1uf-11 gyQcYf")['src']
                                        elif p==1:
                                            img2 = image.find('img',class_="sc-10zw1uf-11 gyQcYf")['src']
                                        elif p==2:
                                            img3 = image.find('img',class_="sc-10zw1uf-11 gyQcYf")['src']
                                        elif p==3:
                                            img4 = image.find('img',class_="sc-10zw1uf-11 gyQcYf")['src']
                                    fair_price_data = {
                                        'Product Name':name.strip(),
                                        'Price':price.strip(),
                                        'Net':Net.strip(),
                                        'Brand':brand.strip(),
                                        'IMG1':img1.strip(),
                                        'IMG2':img2.strip(),
                                        'IMG3':img3.strip(),
                                        'IMG4':img4.strip(),
                                        # 'Country Origin':Country_origin.strip(),
                                        'Sold By':sold_by.strip()
                                    }   
                                    Fairprice_data.append(fair_price_data)
                                    print(name)

                                    with open('Fairprice_data_1.csv','a') as f:
                                        df = pd.DataFrame(Fairprice_data)
                                        df.to_csv('Fair_price_data_1.csv')
                                        
                
# df = pd.DataFrame(Fairprice_data)
# df.to_csv('Fair_price_data.csv')

