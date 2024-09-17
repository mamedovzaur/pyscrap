from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
import time
import mysql.connector

mydb = mysql.connector.connect(
    host="mysql-server-ip",
    port="port",
    user="admin",
    password="dummypass",
    database="database"
    )

def main():
    options = Options()
    options = Options()
    #options.add_argument("window-size=0,0")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    ua = UserAgent()
    a = ua.random
    user_agent = ua.random
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    #driver = webdriver.Chrome("/Users/mamed/Documents/chromedriver", options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    

    for i in range(1,10):
        url = 'https://mulk.az/?get='+str(i)
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

    for a in results:
        if '.mulk' in a['href']:
            #print ("Found the URL:", a['href'])
            sql = "INSERT IGNORE INTO tb_mulkaz_url (siteurl, status) VALUES (%s, %s)"
            val = (a['href'], 0)
            mycursor.execute(sql, val)
            mydb.commit()
    mycursor.close

    sql ="select siteurl from tb_mulkaz_url where status=0"
    mycursor.execute(sql)
    siteurls=mycursor.fetchall()
    for row in siteurls:
        driver.get('https:/mulk.az/'+row[0])
        scrap_data(driver,row[0])

        
def scrap_data(driver,surl):
    time.sleep(10)
    #print ("Found the URL:", driver)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #results = soup.find(id="container")
    #print(results)
    adi=soup.select('#content > div.newsContentPage > div.col-md-4 > i.fa.fa-user')[0].next_sibling.strip()
    print('https://mulk.az/'+surl)
    print('adi:'+adi)
    if 'vasitəçi' in adi:
        print("vasiteci!")
        mycursor = mydb.cursor()
        sql = "update tb_mulkaz_url set status=%s where siteurl=%s"
        val = (11, surl)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close
    else:
        print("mulkiyetci!")
        try:
            Kategoriya = soup.select_one('#desc > tbody > tr:nth-child(2) > td:nth-child(2)').text
            print('Kategoriya:'+Kategoriya)
        except:
            Kategoriya=''
            print('Kategoriya ex:'+Kategoriya)
        if 'Torpaq' in Kategoriya or 'Qaraj' in Kategoriya:
            try:
                header = soup.select_one('#content > div.newsTitle > strong:nth-child(1)').text.strip()
                print("header:"+header)
            except:
                header=''
                print("header ex:"+header)
            try:    
                elan = soup.select('#content > div.newsContentPage > div.col-md-4 > br:nth-child(2)')[0].next_sibling.strip()
                print('elan:'+elan)
            except:
                elan=''
                print('elan ex:'+elan)
            try:
                qiymet = soup.select_one('#desc > tbody > tr:nth-child(1) > td:nth-child(2)').text.split(" ")
                valyuta=qiymet[1]
                qiymet=qiymet[0]
                print("qiymet:"+qiymet)
                print('valyuta:'+valyuta)
            except:
                qiymet=''
                valyuta=''
        
            try:
                Mertebe = ''
                MertebeSayi=''
            except:
                Mertebe=''
                print('Mertebe ex:')
            try:
                Sahe=soup.select_one('#desc > tbody > tr:nth-child(3) > td:nth-child(2)').text.replace(' sot','')
                print('Sahe:'+Sahe)
            except:
                Sahe=''
                print('Sahe ex:'+Sahe)
            try:
                Otaqsayi=''
                print('Otaqsayi:'+Otaqsayi)
            except:
                Otaqsayi=''
                print('Otaqsayi ex:'+Otaqsayi)
            try:
                Kupca=soup.select_one('#desc > tbody > tr:nth-child(4) > td:nth-child(2)').text
                print('Kupca:'+Kupca)
            except:
                Kupca=''
                print('Kupca ex:'+Kupca)
            try:
                phone=soup.select('#content > div.newsContentPage > div.col-md-4 > i.fa.fa-phone')[0].next_sibling.strip().replace('Telefon : ','')
                print('phone:'+phone)
            except:
                phone=''
            
            try:
                try:
                    Rayon0=soup.select_one('#content > div.newsContentPage > div.col-md-4 > b:nth-child(8)').text
                except:
                    Rayon0=''
                try:
                    Rayon1=soup.select_one('#content > div.newsContentPage > div.col-md-4 > b:nth-child(9)').text
                except:
                    Rayon1=''
                try:
                    Rayon2=soup.select_one('#content > div.newsContentPage > div.col-md-4 > b:nth-child(10)').text
                except:
                    Rayon2=''
                try:
                    Rayon3=soup.select_one('#content > div.newsContentPage > div.col-md-4 > br:nth-child(12)').text
                except:
                    Rayon3=''
                if len(Rayon1)>1:
                    Rayon0=Rayon0+', '+Rayon1
                if len(Rayon2)>1:
                    Rayon0=Rayon0+', '+Rayon2
                if len(Rayon3)>1:
                    Rayon0=Rayon0+', '+Rayon3
                Rayon=Rayon0    
            except:
                print('Yerleshme1 ex')
        else:
            try:
                header = soup.select_one('#content > div.newsTitle > strong:nth-child(1)').text.strip()
                print("header:"+header)
            except:
                header=''
                print("header ex:"+header)
            try:    
                elan = soup.select('#content > div.newsContentPage > div.col-md-4 > br:nth-child(2)')[0].next_sibling.strip()
                print('elan:'+elan)
            except:
                elan=''
                print('elan ex:'+elan)
            try:
                qiymet = soup.select_one('#desc > tbody > tr:nth-child(1) > td:nth-child(2)').text.split(" ")
                valyuta=qiymet[1]
                qiymet=qiymet[0]
                print("qiymet:"+qiymet)
                print('valyuta:'+valyuta)
            except:
                qiymet=''
                valyuta=''
        
            try:
                Mertebe0 = soup.select_one('#desc > tbody > tr:nth-child(3) > td:nth-child(2)').text.split(" / ")
                try:
                    print('Mertebe:'+Mertebe0[0])
                    Mertebe=Mertebe0[0]
                except:
                    print('Mertebe ex0:')
                try:
                    print('MertebeSayi:'+Mertebe0[1])
                    MertebeSayi=Mertebe0[1]
                except:
                    print('Mertebe ex1:')
            except:
                Mertebe=''
                print('Mertebe ex:')
            try:
                Sahe=soup.select_one('#desc > tbody > tr:nth-child(4) > td:nth-child(2)').text.replace(' m²','')
                print('Sahe:'+Sahe)
            except:
                Sahe=''
                print('Sahe ex:'+Sahe)
            try:
                Otaqsayi=soup.select_one('#desc > tbody > tr:nth-child(5) > td:nth-child(2)').text
                print('Otaqsayi:'+Otaqsayi)
            except:
                Otaqsayi=''
                print('Otaqsayi ex:'+Otaqsayi)
            try:
                Kupca=soup.select_one('#desc > tbody > tr:nth-child(6) > td:nth-child(2)').text
                print('Kupca:'+Kupca)
            except:
                Kupca=''
                print('Kupca ex:'+Kupca)
            try:
                phone=soup.select('#content > div.newsContentPage > div.col-md-4 > i.fa.fa-phone')[0].next_sibling.strip().replace('Telefon : ','')
                print('phone:'+phone)
            except:
                phone=''
            
            try:
                try:
                    Rayon0=soup.select_one('#content > div.newsContentPage > div.col-md-4 > b:nth-child(8)').text
                except:
                    Rayon0=''
                try:
                    Rayon1=soup.select_one('#content > div.newsContentPage > div.col-md-4 > b:nth-child(9)').text
                except:
                    Rayon1=''
                try:
                    Rayon2=soup.select_one('#content > div.newsContentPage > div.col-md-4 > b:nth-child(10)').text
                except:
                    Rayon2=''
                try:
                    Rayon3=soup.select_one('#content > div.newsContentPage > div.col-md-4 > br:nth-child(12)').text
                except:
                    Rayon3=''
                if len(Rayon1)>1:
                    Rayon0=Rayon0+', '+Rayon1
                if len(Rayon2)>1:
                    Rayon0=Rayon0+', '+Rayon2
                if len(Rayon3)>1:
                    Rayon0=Rayon0+', '+Rayon3
                Rayon=Rayon0    
            except:
                print('Yerleshme1 ex')
        mycursor = mydb.cursor()
        sql = "insert ignore into tb_mulkaz (siteurl,Kateqoriya,Mertebe,Sahe,OtaqSayi,Kupca,Qiymet,Valyuta,phone,elanmetni,TorpagSahesi,Rayon,Header,MertebeSayi,adi) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = ('https://mulk.az/'+surl,Kategoriya,Mertebe,Sahe,Otaqsayi,Kupca,qiymet,valyuta,phone,elan,Sahe,Rayon,header,MertebeSayi,adi)
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "update tb_mulkaz_url set status=%s where siteurl=%s"
        val = (10, surl)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close


if __name__ == '__main__':
    main()