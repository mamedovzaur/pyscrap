from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
import time
import mysql.connector
import re

mydb = mysql.connector.connect(
    host="mysql-server-ip",
    port="port",
    user="admin",
    password="dummypass",
    database="database"
    )

def main():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    ua = UserAgent()
    a = ua.random
    user_agent = ua.random
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    #driver = webdriver.Chrome("/Users/mamed/Documents/chromedriver", options=options)
    driver = webdriver.Chrome("chromedriver", options=options)
    
    

    for i in range(1,20):
        url = 'https://arenda.az/filtirli-axtaris/'+str(i)+'/?home_search=1&lang=1&site=1&home_s=1&price_min=&price_max=&otaq_min=0&otaq_max=0&sahe_min=&sahe_max=&mertebe_min=0&mertebe_max=0&y_mertebe_min=0&y_mertebe_max=0&axtar='
        driver.get(url)
        scrap_link(driver)

    #df = pd.DataFrame({"Title":title,"Address":address,"Price:":price,"Surface" : surface,"Description":desc})
    #df.to_csv("output.csv")


def scrap_link(driver):
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('a', href=True)
    surl=''
    mycursor = mydb.cursor()
    regexp1 = re.compile(r'az/satilir')
    regexp2 = re.compile(r'az/kiraye')
    for a in results:
        if regexp1.search(a['href']) or regexp2.search(a['href']):
            regexp1 = re.compile(r'evler')
            regexp2 = re.compile(r'ofisler')
            regexp3 = re.compile(r'kiraye-ev')
            if regexp1.search(a['href']) or regexp2.search(a['href']) or regexp3.search(a['href']):
                print ("Found the URL:", a['href'])
            else:
                print ("Found the URL:", a['href'])
                sql = "INSERT IGNORE INTO tb_arendaaz_url (siteurl, status) VALUES (%s, %s)"
                val = (a['href'], 0)
                mycursor.execute(sql, val)
                mydb.commit()
    mycursor.close


    ##get all inserted rows with status=0
    sql ="select siteurl from tb_arendaaz_url where status=0"
    mycursor.execute(sql)
    siteurls=mycursor.fetchall()
    for row in siteurls:
        driver.get(row[0])
        #print('url: '+row[0])
        scrap_data(driver,row[0])

    

        
def scrap_data(driver,surl):
    time.sleep(10)
    #print ("Found the URL:", driver)
    html = driver.page_source
    time.sleep(10)
    soup = BeautifulSoup(html, 'html.parser')
    #results = soup.find(id="container")
    #print(results)
    try:
        owner=soup.select_one('#elan_desc > section.elan_desc_sides.elan_desc_right_side.elan_in_right > div:nth-child(3) > div > p:nth-child(1)').text.strip()
    except:
        mycursor = mydb.cursor()
        sql = "update tb_arendaaz_url set status=%s where siteurl=%s"
        val = (12, surl)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close
        return None
    adi=''
    Kategoriya=''
    header=''
    qiymet=''
    valyuta=''
    elan=''
    phone=''
    Rayon=''
    Mertebe=''
    MertebeSayi=''
    Sahe=''
    Otaqsayi=''
    Kupca=''
    Ipoteka=''
    TorpaqSahesi=''
    Binanovu=''
    #print(owner)
    if 'Vasitəçi' in owner:
        print("vasiteci!")
        mycursor = mydb.cursor()
        sql = "update tb_arendaaz_url set status=%s where siteurl=%s"
        val = (11, surl)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close
    else:
        Kategoriya=soup.select_one('#elan_desc > section.elan_desc_sides.elan_desc_left_side > h2').text.strip()
        print("Kategoriya: "+Kategoriya)
        


if __name__ == '__main__':
    main()