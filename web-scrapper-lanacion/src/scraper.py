# src/scraper.py

import requests

from .config import HEADERS

def fetch_page(url: str) -> str | None:
    # Hace una request GET a la URL y devuelve el HTML como string
    # Si hay un error, devuelve None"""

    try:
        response = requests.get(url, HEADERS, timeout=10)
    except requests.RequestException as e:
        print(f"[ERROR] Fallo la request {e}")
        return None
    
    if response.status_code != 200:
        print(f"[ERROR] Status code inesperado: {response.status_code}")
        return None
    
    return response.text