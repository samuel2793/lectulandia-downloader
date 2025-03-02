import os
import requests
from bs4 import BeautifulSoup
import time
import urllib3
from dotenv import load_dotenv

# Desactivar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cargar variables de entorno desde .env
load_dotenv()

# Proxy configurado desde las variables de entorno
proxy = {
    "http": os.getenv("HTTP_PROXY"),
    "https": os.getenv("HTTPS_PROXY"),
}

# URL base de la paginación
base_url = "https://ww3.lectulandia.com/book/page/"

# Configuración de cabecera para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Número de páginas a recorrer
num_pages = 5

# Lista para almacenar enlaces de libros
book_links = []

for page in range(1, num_pages + 1):
    url = f"{base_url}{page}/"
    print(f"Extrayendo libros de: {url}")

    try:
        response = requests.get(url, headers=headers, proxies=proxy, verify=False, timeout=10)
        if response.status_code != 200:
            print(f"Error al acceder a la página {url}, código: {response.status_code}")
            continue  # Pasar a la siguiente página si falla
        
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar los enlaces a los libros
        for a in soup.select("a.card-click-target"):
            book_url = "https://ww3.lectulandia.com" + a["href"]
            book_links.append(book_url)

        time.sleep(2)  # Evitar bloqueos por peticiones rápidas

    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        continue

# Guardamos los enlaces de los libros
with open("libros.txt", "w") as f:
    for link in book_links:
        f.write(link + "\n")

print(f"Se encontraron {len(book_links)} libros.")
