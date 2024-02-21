import os   
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Download_from_source_link import Download
d={}
download_folder = input('Donwload Folder Path: ')
if os.name == 'nt':
    clear = 'cls'
else:
    clear = "clear"
os.system(clear)
real_manga_name = input('Manga Name: ')
os.system(clear)
manga_name = real_manga_name.replace(' ','+')
def manga_domain(manga_name):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    drive = webdriver.Chrome(options=option)
    search_domain = f'https://www.mngdoom.com/advanced-search?term={manga_name}'
    drive.get(search_domain)
    WebDriverWait(drive,10).until(ec.element_to_be_clickable((By.CSS_SELECTOR,"div[class='col-md-6']"))).click()
    WebDriverWait(drive,10).until(ec.element_to_be_clickable((By.CSS_SELECTOR,"dt[class='manga-title']")))
    titles = drive.find_elements(By.CSS_SELECTOR,"dt[class='manga-title']")
    print('Search results:  \n')
    for n,i in enumerate(titles):
        title = i.text
        shit = i.find_elements(By.CSS_SELECTOR,'a')
        for k in shit:
            domain = k.get_attribute('href')
        d.setdefault(n,domain)
        print(f'{n}-{title}')
    if title:
        Domain=d[int(input('\nPick your manga(number): '))]
        os.system('clear')
        print('Downloading...')
        return Domain
    else:
        print('Somthing went Wrong!!!')

def manga_download(Domain,manga_name,chapters=10000):
    os.mkdir(f'{download_folder}/{real_manga_name}')
    for chapter in range(1,chapters):
        for page in range(1,300):
            try:
                pages_domain = f'{Domain}/{str(chapter)}/{str(page)}'
                re = requests.get(pages_domain)
                soup = BeautifulSoup(re.text,'html.parser')
                image = soup.find(id = 'chapter_img').get('src')
                Download(image,f'{download_folder}/{manga_name}/{manga_name}_{chapter}_{page}')
            except:
                break
manga_download(manga_domain(manga_name),manga_name)