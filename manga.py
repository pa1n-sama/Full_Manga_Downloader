from PIL import Image,ImageFile
import requests
import os
import shutil

ImageFile.LOAD_TRUNCATED_IMAGES = True

def transform_topdf(folder_path):
    folder_items = sorted(os.listdir(folder_path))
    image = [Image.open(os.path.join(folder_path,f)) for f in folder_items]
    pdf_path = folder_path+".pdf"
    image[0].save(pdf_path,"PDF",resolution=100.0,save_all=True,append_images=image[1:])
    print("PDF Created.")
    shutil.rmtree(folder_path)
def getting_domain(manga_name):
    api_url = "https://api.mangadex.org/manga"
    search_parameter = {
        "title": manga_name,
        "limit": 10,
    }
    response = requests.get(api_url, params=search_parameter)
    if response.status_code != 200:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return None
    
    search_results = response.json()
    data = search_results.get("data", [])
    if not data:
        print("No results found.")
        return None
    
    print("Search Results: \n")
    ids = []

    for index, manga in enumerate(data):
        title = manga["attributes"]["title"].get("en", "Unknown Title")
        manga_id = manga["id"]
        print(f"{index}: {title}\n")
        ids.append(manga_id)

    try:
        element = ids[int(input("Input the Manga Number: "))]
        os.system("clear")
        return element
    except (ValueError, IndexError):
        print("Invalid Number")
        return None


def getting_chapters(manga_name):
    manga_id = getting_domain(manga_name)
    if not manga_id:
        return
    
    api_url = f"https://api.mangadex.org/manga/{manga_id}/feed"
    limit = 100
    offset = 0
    all_manga_chap=[]
    lang = input("English or Arabic? (en,ar...): ").strip().lower()
        
    while True:
        params = {"translatedLanguage[]": lang, "limit": limit, "offset": offset, "order[chapter]": "asc"}

        response = requests.get(api_url, params=params)
        if response.status_code != 200:
            print(f"Failed to retrieve manga details. Status code: {response.status_code}")
            return

        manga_chapters = response.json().get("data", [])
        if not manga_chapters:
            break
        all_manga_chap.extend(manga_chapters)
        offset+=limit
    
    check = input("Do you want to download all the chapters? (y/n): ").strip().lower()
    start = len(os.listdir(download_dir))
    if start!=0:
        print(f"Starting from chapter {start} ")
    if check == "n":
        stop = int(input("How many chapters?: "))
        all_manga_chap = all_manga_chap[start:stop]
    else:
        all_manga_chap = all_manga_chap[start:]
    for chapter in all_manga_chap:
        chapter_id = chapter["id"]
        chapter_number = chapter["attributes"].get("chapter", "Unknown")
        print(f"Downloading chapter {chapter_number}")
        download_chapter_images(chapter_id, f"Chapter_{chapter_number}")


def download_chapter_images(chapter_id, chapter_title):
    api_url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to retrieve chapter details. Status code: {response.status_code}")
        return
    
    try:
        chapter_data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Failed to decode JSON. Response content: {response.content}")
        return
    
    base_url = chapter_data.get('baseUrl')
    if not base_url:
        print(f"Invalid chapter data: {chapter_data}")
        return
    
    chapter_hash = chapter_data['chapter']['hash']
    page_filenames = chapter_data['chapter']['data']
    
    chapter_folder = os.path.join(download_dir, chapter_title)
    os.makedirs(chapter_folder, exist_ok=True)
    
    for page_number, page_filename in enumerate(page_filenames, start=1):
        page_url = f"{base_url}/data/{chapter_hash}/{page_filename}"
        download_image(page_url, chapter_folder, f"page_{page_number}.jpg")
    transform_topdf(chapter_folder)


def download_image(url, folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        print(f"Downloaded: {file_name}")
    else:
        print(f"Failed to download image from {url}")


manga_name = input("Enter the Manga name: ")
try:
    with open("download_folder.txt",'r') as file:
        path=os.path.join(file.readline(),manga_name)
except:
    download_dir = input("Enter the download folder path: ")
    with open("download_folder.txt",'w') as file:
        file.write(download_dir)
    download_dir = os.path.join(download_dir,manga_name)

os.makedirs(download_dir,exist_ok=True)
getting_chapters(manga_name)
