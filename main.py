from selenium import webdriver
import gspread
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


gc = gspread.service_account('json файл, нужно скачать когда будете создавать API для работы с гугл таблицами')
sh = gc.open_by_url('Ссылка на таблицу куда будут загружаться данные')
worksheet = sh.worksheet('Лист1')


urls = [x.replace('\n','') for x in open('url.txt')]


def get_html_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=HelloWorl:')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(url)
    time.sleep(5)
    main_page = driver.page_source
    with open('wb_html.html','w',encoding="utf-8") as file:
        file.write(main_page)
    file.close()

def update_gs(row):
    html = open('wb_html.html',encoding='utf-8')
    soup = bs(html,'lxml')
    price = soup.find('ins',class_='price-block__final-price')
    name = soup.find('div',class_='product-page__header')
    worksheet.update_cell(row+1,1,name.text.strip())
    worksheet.update_cell(row+1,2,price.text.strip())
    html.close()
    os.remove('wb_html.html')

for i in range(len(urls)):
    try:
        get_html_page(urls[i])
    except:
        pass
    finally:
        update_gs(i)
