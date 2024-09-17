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
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    ua = UserAgent()
    a = ua.random
    user_agent = ua.random
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    #driver = webdriver.Chrome("/Users/mamed/Documents/chromedriver", options=options)
    driver = webdriver.Chrome("chromedriver", options=options)

    mycursor = mydb.cursor()

    sql ="select siteurl from tb_binaaz_url where status=10"
    mycursor.execute(sql)
    siteurls=mycursor.fetchall()
    for row in siteurls:
        driver.get('https:/bina.az'+row[0])
        scrap_data(driver)


        
def scrap_data(driver):
    time.sleep(10)
    #print ("Found the URL:", driver)
    html = driver.page_source
    driver.find_element_by_id('show-phones').click()
    time.sleep(10)
    soup = BeautifulSoup(html, 'html.parser')
    #results = soup.find(id="container")
    #print(results)
    owner=soup.select_one('#js-item-show > div.item_show_content > div.info > section > div.name').text.strip()
    #print(owner)
    if 'vasitəçi' in owner:
        print("vasiteci!")
    else:
        Kategoriya=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(1) > td:nth-child(2)').text.strip()
        header=soup.select_one('#js-item-show > div.price_header > div > h1').text.strip()
        qiymet=soup.select_one('#js-item-show > div.price_header > section > p > span.price-val').text.strip().replace(' ','')
        valyuta=soup.select_one('#js-item-show > div.price_header > section > p > span.price-cur').text.strip()
        elanmetni=soup.select_one('#js-item-show > div.item_show_content > div.side > article > p').text.strip()
        phone=driver.find_element_by_xpath('//*[@id="js-item-show"]/div[3]/div[1]/section/div[2]/div[2]/ul/li').text
        Rayon1=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > div > ul > li:nth-child(1) > a').text.strip()
        try:
            Rayon2=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > div > ul > li:nth-child(2) > a').text.strip()
        except:
            Rayon2=''
        try:
            Rayon3=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > div > ul > li:nth-child(3) > a').text.strip()
        except:
            Rayon3=''
        try:
            Rayon4=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > div > ul > li:nth-child(4) > a').text.strip()
        except:
            Rayon4=''
        try:
            Rayon5=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > div > ul > li:nth-child(5) > a').text.strip()
        except:
            Rayon5=''
        Rayon=Rayon1+' '+Rayon2 +' '+Rayon3 +' '+Rayon4 +' '+Rayon5    
        print('Kategoriya: '+Kategoriya)
        print('phone: '+phone)
        print("header: "+header)
        print("adi: "+owner.replace('mülkiyyətçi',' mülkiyyətçi'))
        print("qiymet: "+qiymet)
        print("valyuta: "+valyuta)
        print("elanmetni: "+elanmetni)
        print("Rayon: "+Rayon)
        if ('Yeni tikili' in Kategoriya) or ('Köhnə tikili' in Kategoriya):
            Mertebe0=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(2) > td:nth-child(2)').text.split(" / ")
            Sahe=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(3) > td:nth-child(2)').text.strip().replace(' m²','')
            Otaqsayi=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(4) > td:nth-child(2)').text.strip()
            Kupcha=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(5) > td:nth-child(2)').text.strip()
            try:
                Ipoteka=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(6) > td:nth-child(2)').text.strip()
            except:
                Ipoteka=''
            print("Mertebe: "+Mertebe0[0])
            print("Mertebesayi: "+Mertebe0[1])
            print("Sahe: "+Sahe)
            print("Otaqsayi: "+Otaqsayi)
            print("Kupcha: "+Kupcha)
            print("Ipoteka: "+Ipoteka)
            
        if ('Ev / Villa' in Kategoriya):
            Sahe=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(2) > td:nth-child(2)').text.strip().replace(' m²','')
            TorpaqSahesi=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(3) > td:nth-child(2)').text.strip().replace(' sot','')
            Otaqsayi=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(4) > td:nth-child(2)').text.strip()
            Kupcha=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(5) > td:nth-child(2)').text.strip()
            try:
                Ipoteka=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(6) > td:nth-child(2)').text.strip()
            except:
                Ipoteka=''
            print("Sahe: "+Sahe)
            print("TorpaqSahesi: "+TorpaqSahesi)
            print("Otaqsayi: "+Otaqsayi)
            print("Kupcha: "+Kupcha)
            print("Ipoteka: "+Ipoteka)
        if ('Bağ' in Kategoriya):
            Sahe=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(2) > td:nth-child(2)').text.strip().replace(' m²','')
            TorpaqSahesi=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(3) > td:nth-child(2)').text.strip().replace(' sot','')
            Kupcha=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(4) > td:nth-child(2)').text.strip()
            try:
                Ipoteka=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(5) > td:nth-child(2)').text.strip()
            except:
                Ipoteka=''
            print("Sahe: "+Sahe)
            print("TorpaqSahesi: "+TorpaqSahesi)
            print("Kupcha: "+Kupcha)
            print("Ipoteka: "+Ipoteka)
        if ('Ofis' in Kategoriya):
            Sahe=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(2) > td:nth-child(2)').text.strip().replace(' m²','')
            Binanovu=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(3) > td:nth-child(2)').text.strip()
            Otaqsayi=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(4) > td:nth-child(2)').text.strip()
            Kupcha=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(5) > td:nth-child(2)').text.strip()
            try:
                Ipoteka=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(6) > td:nth-child(2)').text.strip()
            except:
                Ipoteka=''
            print("Sahe: "+Sahe)
            print("Binanovu: "+Binanovu)
            print("Otaqsayi: "+Otaqsayi)
            print("Kupcha: "+Kupcha)
            print("Ipoteka: "+Ipoteka)
        if ('Torpaq' in Kategoriya):
            TorpaqSahesi=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(2) > td:nth-child(2)').text.strip().replace(' sot','')
            Kupcha=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(3) > td:nth-child(2)').text.strip()
            try:
                Ipoteka=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(4) > td:nth-child(2)').text.strip()
            except:
                Ipoteka=''
            print("TorpaqSahesi: "+TorpaqSahesi)
            print("Kupcha: "+Kupcha)
            print("Ipoteka: "+Ipoteka)
        if ('Obyekt' in Kategoriya) or ('Qaraj' in Kategoriya):
            Sahe=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(2) > td:nth-child(2)').text.strip().replace(' m²','')
            Kupcha=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(3) > td:nth-child(2)').text.strip()
            try:
                Ipoteka=soup.select_one('#js-item-show > div.item_show_content > div.side > div.parameters_section > div.param_info > table > tbody > tr:nth-child(4) > td:nth-child(2)').text.strip()
            except:
                Ipoteka=''
            print("Sahe: "+Sahe)
            print("Kupcha: "+Kupcha)
            print("Ipoteka: "+Ipoteka)
    

if __name__ == '__main__':
    main()