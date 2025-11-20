# run.py

from src.scraper import fetch_page
from src.parser import parse_noticias, parse_json_items
from src.utils import save_json, save_csv
from src.config import URL_ULTIMAS_NOTICIAS
from src.api_client import fetch_json_page

def fetch_all_pages(max_pages=10):
    todas = []

    for page in range(2, max_pages + 1):
        print(f"[INFO] Fetching page {page}...")
        data = fetch_json_page(page)

        if not data or not data.get("content_elements"):
            print("[INFO] No hay mas datos")
            break

        items = parse_json_items(data)
        todas.extend(items)

    return todas

def main():
    print(f"[INFO] Obteniendo página HTML inicial: {URL_ULTIMAS_NOTICIAS}")
    html = fetch_page(URL_ULTIMAS_NOTICIAS)

    if html is None:
        print("[ERROR] No se pudo obtener el HTML inicial")
        return

    # Parseo del html inicial
    noticias_html = parse_noticias(html)
    print(f"[INFO] Noticias obtenidas del HTML inicial: {len(noticias_html)}")

    # Parsear mediante API resto de noticias
    print("[INFO] Descargando más páginas vía API...")
    noticias_json = fetch_all_pages(max_pages=15)
    print(f"[INFO] Noticias obtenidas de la API: {len(noticias_json)}")

    # Juntar resultados
    noticias = noticias_html + noticias_json
    print(f"[INFO] Total de noticias obtenidas: {len(noticias)}")

    # Mostrar 3 ultimas noticias
    for i, n in enumerate(noticias[:3], start=1):
        print(f"\n--- Noticia #{i} ---")
        print("Título:", n["titulo"])
        print("Hora:", n["hora"])
        print("URL:", n["url"])
        print("Tags:", n["tags"])
        print("Autor:", n["autor"])

    save_json(noticias, "data/processed/noticias.json")
    save_csv(noticias, "data/processed/noticias.csv")

    print("\n[INFO] Archivos guardados correctamente.")
        
if __name__ == "__main__":
    main()