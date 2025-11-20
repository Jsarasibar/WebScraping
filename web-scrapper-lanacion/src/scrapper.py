import requests
from bs4 import BeautifulSoup

URL_BASE = "https://www.lanacion.com.ar"
URL_ULTIMAS_NOTICIAS = f"{URL_BASE}/ultimas-noticias/"

HEADERS = {
    "user-agent": "Mozilla/5.0 (compatible; WebScraperPortafolio/0.1; +https://github.com/jsarasibar)"
}

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

def parse_noticias (html: str) -> list[dict]:
    # Dado el HTML como str de la pagina ultimas noticias,
    # devuelve una lista de diccionarios separando la informacion de cada noticia
    soup = BeautifulSoup(html, "lxml")
    noticias = []
    
    articles = soup.find_all("article", class_="mod-article")
    
    for art in articles:
        descripcion = art.find("section", class_="mod-description")
        if not descripcion:
            continue
        
        # Fecha / hora
        time_tag = descripcion.find("time", class_="com_hour")
        fecha_hora = time_tag.get_text(strip = True) if time_tag else None
        
        # Titulo y URL
        h2_tag = descripcion.find("h2", class_="com-title")
        a_tag = h2_tag.find("a") if h2_tag else None
        
        titulo = a_tag.get_text(strip = True) if a_tag else None
        href = a_tag.get("href") if a_tag else None
        
        # Armamos URL completa si es relativa
        if href and href.startswith("http"):
            url_completa = href
        elif href:
            url_completa = URL_BASE + href
        else:
            url_completa = None
            
        noticia = {
            "titulo": titulo,
            "url": url_completa,
            "fecha_hora": fecha_hora
        }
        
        if titulo and url_completa:
            noticias.append(noticia)
    
    return noticias


def main():
    print(f"[INFO] Obteniendo pagina: {URL_ULTIMAS_NOTICIAS}")
    html = fetch_page(URL_ULTIMAS_NOTICIAS)
    
    if html is None:
        print("[ERROR] No se pudo obtener el html")
        return
    
    noticias = parse_noticias(html)
    print(f"[INFO] Se obtuvieron {len(noticias)} noticias")
    
    # Mostrar las primeras 5
    for i,n in enumerate(noticias[:5], start=1):
        print(f"\nNoticia #{i}")
        print(f"  Título     : {n['titulo']}")
        print(f"  Fecha/Hora : {n['fecha_hora']}")
        print(f"  URL        : {n['url']}")
        
if __name__ == "__main__":
    main()