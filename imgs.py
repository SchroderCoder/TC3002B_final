import requests
import os
import re
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_service = Service('./chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

urls_and_folders = [
    {
        "url": "https://www.google.com/search?sca_esv=a0cb478d38178b5b&sxsrf=AE3TifMxTyDUhZl_QTSMouRh2lAM4FOZUA:1748120619297&q=paul+mccartney+face&udm=2&fbs=AIIjpHx4nJjfGojPVHhEACUHPiMQht6_BFq6vBIoFFRK7qchKBv8IM7dq8CEqHDU3BN7lbmYnvYQ6rIhpD6d6bj_VyqCDVICi0aYslRFVg6x8lIId9pHGh2yQ6AdokkDbdE8SxSwaP0197JzBQG9sSBJhByVo6IpBOwfTRZZt8edZB86SlTk7kxQvKCq5MeCv2tXBkNvjUEPTws5ZeDyErZbxVJ1rXpAYA&sa=X&ved=2ahUKEwjquKbkgL2NAxUtmO4BHXpMPMgQtKgLegQIExAB&biw=1536&bih=643&dpr=1.25",
        "folder": "./dataset/paul",
        "source": "google"
    },
    {
        "url": "https://www.google.com/search?q=John+Lennon+Face&sca_esv=a0cb478d38178b5b&udm=2&biw=1536&bih=643&sxsrf=AE3TifPR8NUKHqe8cQuRNl8ThF2jksQrEg%3A1748120735041&ei=nzQyaKyrApnHkPIP-f-muQk&ved=0ahUKEwjs9r6bgb2NAxWZI0QIHfm_KZcQ4dUDCBE&uact=5&oq=John+Lennon+Face&gs_lp=EgNpbWciEEpvaG4gTGVubm9uIEZhY2UyBxAjGCcYyQIyBBAAGB4yBBAAGB4yBBAAGB4yBBAAGB4yBBAAGB4yBBAAGB4yBBAAGB4yBhAAGAoYHjIEEAAYHkipI1AAWJAicAd4AJABAJgBVaABkQuqAQIxObgBA8gBAPgBAZgCFqACvgrCAgoQABiABBhDGIoFwgIGEAAYAxgKwgILEAAYgAQYsQMYgwHCAg0QABiABBixAxhDGIoFwgIIEAAYgAQYsQPCAgUQABiABMICBhAAGAgYHpgDAJIHAjIyoAeKeLIHAjE3uAezCsIHBjIuNC4xNsgHPw&sclient=img",
        "folder": "./dataset/john",
        "source": "google"
    },
    {
        "url": "https://www.google.com/search?q=george+harrison+face&sca_esv=a0cb478d38178b5b&udm=2&biw=1536&bih=643&sxsrf=AE3TifOx-2ERMzn5nfNpQ9TuZAuZPJBoaw%3A1748120771312&ei=wzQyaK70EtbRkPIP9r3pqQo&ved=0ahUKEwju4eSsgb2NAxXWKEQIHfZeOqUQ4dUDCBE&uact=5&oq=george+harrison+face&gs_lp=EgNpbWciFGdlb3JnZSBoYXJyaXNvbiBmYWNlMgcQABiABBgTMgcQABiABBgTMgcQABiABBgTMgYQABgTGB4yCBAAGBMYCBgeMggQABgTGAgYHjIGEAAYExgeSMMKUFxY6AVwAXgAkAEAmAFUoAGBA6oBATW4AQPIAQD4AQGYAgagApUDwgINEAAYgAQYsQMYQxiKBcICBhAAGAcYHsICCxAAGIAEGLEDGIMBwgIKEAAYgAQYQxiKBcICBRAAGIAEwgIEEAAYHpgDAIgGAZIHATagB-0asgcBNbgHkQPCBwUwLjEuNcgHEg&sclient=img",
        "folder": "./dataset/george",
        "source": "google"
    },
    {
        "url": "https://www.google.com/search?q=Ringo+Starr+Face&sca_esv=a0cb478d38178b5b&udm=2&biw=1536&bih=643&sxsrf=AE3TifPuv_xOKtQfHAtCOBtrJa4BITDE2w%3A1748120776366&ei=yDQyaOqRFoPDkPIP6tjksQ0&ved=0ahUKEwjqlZmvgb2NAxWDIUQIHWosOdYQ4dUDCBE&uact=5&oq=Ringo+Starr+Face&gs_lp=EgNpbWciEFJpbmdvIFN0YXJyIEZhY2UyBxAAGIAEGBMyBxAAGIAEGBMyBxAAGIAEGBMyBxAAGIAEGBMyBhAAGBMYHjIIEAAYExgIGB5IhBtQAFiIGnADeACQAQCYAV2gAdALqgECMTm4AQPIAQD4AQGYAhOgAvoKwgIHECMYJxjJAsICChAAGIAEGEMYigXCAgsQABiABBixAxiDAcICDhAAGIAEGLEDGIMBGIoFwgIIEAAYgAQYsQPCAg0QABiABBixAxhDGIoFwgIFEAAYgATCAgYQABgIGB7CAgQQABgewgIIEAAYExgFGB6YAwCSBwIxOaAHo3SyBwIxN7gH9grCBwYxLjMuMTXIBzo&sclient=img",
        "folder": "./dataset/ringo",
        "source": "google"
    },
]

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_images(url, source):
    driver.get(url)
    scroll_to_bottom(driver)

    if source == "google":
        images = driver.execute_script("""
            return Array.from(document.querySelectorAll('.YQ4gaf:not(.zr758c)')).map(e => e.src);
        """)
    elif source == "pinterest":
        images = set()
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            new_images = driver.execute_script("""
                return Array.from(document.querySelectorAll('img')).map(e => e.src);
            """)
            images.update(new_images)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        images = list(images)
    r = input(f"lon images: {len(images)}. Proced? (y/n)")
    if r == "y": return images
    else: exit(0)

def download_image(url, folder, file_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers['Content-Type']
            if 'image' in content_type:
                extension = content_type.split('/')[-1]
                if extension in ['jpeg', 'jpg', 'png']:
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    filename = os.path.join(folder, f"{file_name}.{extension}")
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f"Imagen descargada: {filename}")
                else:
                    print(f"Tipo de imagen no soportado: {content_type}")
            else:
                print(f"No es una imagen válida: {url}")
        else:
            print(f"No se pudo descargar la imagen {url}")
    except Exception as e:
        print(f"Error al descargar la imagen {url}: {e}")

def download_image_from_base64(base64_string, folder, file_name):
    match = re.match(r'data:image/(.*?);base64,(.*)', base64_string)
    if match:
        image_type = match.group(1)
        image_data = match.group(2)
        image_bytes = base64.b64decode(image_data)
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_path = os.path.join(folder, f"{file_name}.{image_type}")
        with open(file_path, 'wb') as image_file:
            image_file.write(image_bytes)
        print(f"Imagen guardada en {file_path}")
    else:
        download_image(base64_string, folder, file_name)

def get_initial_index(folder):
    existing_files = os.listdir(folder)
    image_files = [f for f in existing_files if f.endswith(('.jpeg', '.jpg', '.png'))]
    indices = [int(f.split('.')[0]) for f in image_files if f.split('.')[0].isdigit()]
    return max(indices, default=-1) + 1

for entry in urls_and_folders:
    url = entry["url"]
    folder = entry["folder"]
    source = entry["source"]
    
    images = scrape_images(url, source)
    
    i = get_initial_index(folder)
    for img_url in images:
        download_image_from_base64(img_url, folder, i)
        i += 1

driver.quit()
