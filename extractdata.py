from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
import time
import mysql.connector



def main():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    ua = UserAgent()
    a = ua.random
    user_agent = ua.random
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome("chromedriver", options=options)

    mydb = mysql.connector.connect(
    host="mysql-server-ip",
    port="port",
    user="admin",
    password="dummypass",
    database="database"
    )

    mycursor = mydb.cursor()

    sql ="select siteurl from tb_tutaz_url where status=0"
    mycursor.execute(sql)
    siteurls=mycursor.fetchall()
    for row in siteurls:
        driver.get(row[0])
        scrap_data(driver,row[0])


        
def scrap_data(driver,surl):
    time.sleep(10)
    #print ("Found the URL:", driver)
    html = driver.page_source
    try:
        driver.find_element_by_id('showContact').click()
    except:
        mydb = mysql.connector.connect(
        host="144.91.81.143",
        port="53306",
        user="admin",
        password="RtyFgh123!@#",
        database="rltr"
        )
        mycursor = mydb.cursor()
        sql = "update tb_tutaz_url set status=%s where siteurl=%s"
        val = (12, surl)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close
        return None
    time.sleep(10)
    soup = BeautifulSoup(html, 'html.parser')
    #results = soup.find(id="container")
    #print(results)
    #owner=soup.select_one('#js-item-show > div.item_show_content > div.info > section > div.name').text.strip()
    #print(owner)
    #phone=driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[2]/div[1]/div[1]/div[3]/div/div[1]/div/div[2]/ul/li[1]/a/span[1]').text
    #print('phone: '+phone)    
    #Unvan=soup.select_one('#_leftProductPart > div._flexSlider > div._advertsInfoContainer > ul > li:nth-child(1) > span.second_part').text.strip()
    #print('Unvan: '+Unvan) 
    mulkiyyetci='Mülküyətci'  
    for ultag in soup.find_all('ul', {'class': 'list-inline'}):
         for litag in ultag.find_all('li'):
            if 'Vasitəçi' in litag.text:
                 #print('Vasitəçi')
                 mulkiyyetci='Vasitəçi'
                
    print(mulkiyyetci)
    if 'Vasitəçi' in mulkiyyetci:
        mydb = mysql.connector.connect(
        host="144.91.81.143",
        port="53306",
        user="admin",
        password="RtyFgh123!@#",
        database="rltr"
        )
        mycursor = mydb.cursor()
        sql = "update tb_tutaz_url set status=%s where siteurl=%s"
        val = (11, surl)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close
    
            





if __name__ == '__main__':
    main()