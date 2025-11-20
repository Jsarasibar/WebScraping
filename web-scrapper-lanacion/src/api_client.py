# src/api_client.py

import json
import requests
from urllib.parse import quote
from .config import HEADERS

API_URL = "https://www.lanacion.com.ar/pf/api/v3/content/fetch/acuArticlesSource"

# Query original base
BASE_QUERY = {
    "authorId": None,
    "excludePreload": False,
    "excludeSectionId": False,
    "hasCollectionApertura": False,
    "imageConfig": "newBoxArticles",
    "page": 1,
    "promoItemsOnly": False,
    "sectionId": None,
    "sectionsIds": "(\"/economia\",\"/sociedad\",\"/deportes\",\"/politica\",\"/espectaculos\",\"/el-mundo\",\"/tecnologia\",\"/propiedades\",\"/dolar-hoy\",\"/buenos-aires\",\"/seguridad\",\"/educacion\",\"/cultura\",\"/salud\",\"/ciencia\",\"\")",
    "shouldNotFilter": False,
    "size": 30,
    "sourceOrigin": "composer",
    "type": "",
    "website": "la-nacion-ar"
}


def fetch_json_page(page: int) -> dict | None:
    # Obtiene la pagina pedida de noticias desde la API interna
    
    query = BASE_QUERY.copy()
    query["page"] = page

    # No usar json.dumps con sort_keys. Respetar estructura string.
    encoded_query = quote(json.dumps(query, separators=(',', ':')))

    url = f"{API_URL}?query={encoded_query}&d=1919&mxId=00000000&_website=la-nacion-ar"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print(f"[ALERTA] Código {r.status_code} en page={page}")
            return None
        return r.json()
    except Exception as e:
        print(f"[ERROR] page {page}: {e}")
        return None
