# src/config.py

URL_BASE = "https://www.lanacion.com.ar"
URL_ULTIMAS_NOTICIAS = f"{URL_BASE}/ultimas-noticias/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}