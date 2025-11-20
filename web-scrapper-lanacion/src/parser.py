# src/parser.py

from bs4 import BeautifulSoup
from .config import URL_BASE

def parse_noticias (html: str) -> list[dict]:
    # Dado el HTML como str de la pagina ultimas noticias,
    # devuelve una lista de diccionarios separando la informacion de cada noticia
    soup = BeautifulSoup(html, "lxml")
    noticias = []
    
    articles = soup.find_all("article", class_="mod-article")
    
    for art in articles:
        # Fecha / hora
        time_tag = art.find("time", class_="com-hour")
        texto_hora = time_tag.get_text(strip=True) if time_tag else None
        
        hora = None
        if texto_hora and ":" in texto_hora:
            try:
                hora = int(texto_hora.split(":")[0].strip())
            except ValueError:
                hora = None
        
        descripcion = art.find("section", class_="mod-description")
        if not descripcion:
            continue
        
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
        
        # Tags y Autor
        
        tags = []
        autor = None
        
        for div in descripcion.find_all("div"):
            enlaces = div.find_all("a")
            
            for a in enlaces:
                titulo_attr = a.get("title", " ")
                
                if titulo_attr.startswith("Por "):
                    autor = a.get_text(strip = True)[4:]
                elif a.get_text(strip = True) != "LN+":
                    tags.append(a.get_text(strip = True))
        
        
        noticia = {
            "titulo": titulo,
            "url": url_completa,
            "hora": hora,
            "tags": tags,
            "autor": autor
        }
        
        if titulo and url_completa:
            noticias.append(noticia)
    
    return noticias

def parse_json_items(data: dict) -> list[dict]:
    # Extrae noticias desde el JSON de la API
        
    if "content_elements" not in data:
        return []

    noticias = []

    for item in data["content_elements"]:
        try:
            titulo = item["headlines"]["basic"]
            url = item["website_url"]
            autor = None
            tags = []

            # Autor
            try:
                autor = item["credits"]["by"][0]["name"]
            except:
                pass

            # Categoria principal
            try:
                categoria = item["taxonomy"]["primary_section"]["name"]
                tags.append(categoria)
            except:
                pass

            # Tags extra
            try:
                for t in item.get("tags", []):
                    tags.append(t["text"])
            except:
                pass

            # Hora como publish_date
            try:
                hora = int(item["publish_date"][11:13])
            except:
                hora = None

            noticia = {
                "titulo": titulo,
                "url": url,
                "hora": hora,
                "autor": autor,
                "tags": tags
            }

            noticias.append(noticia)

        except Exception:
            continue

    return noticias
