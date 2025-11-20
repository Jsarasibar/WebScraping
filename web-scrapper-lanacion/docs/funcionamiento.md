# Funcionamiento del scraper

## Estructura general del proyecto

El proyecto está organizado con una estructura modular. Los componentes principales están dentro del directorio `src/`, dividido por responsabilidades:

```

src/
├── api_client.py     # Maneja las requests a la API de La Nación
├── parser.py         # Convierte la respuesta JSON en diccionarios Python
├── scraper.py        # Lógica de paginación y recolección de todas las noticias
├── analysis.py       # Funciones de análisis y gráficos
├── utils.py          # Funciones auxiliares (guardar en CSV/JSON, validaciones…)
└── config.py         # Variables globales, URLs y parámetros del scraper

```

Carpetas para datos crudos, datos procesados y salidas visuales:

```

data/raw/         # Requests opcionales guardadas para depuración (no se sube a GitHub)
data/processed/   # CSV y JSON finales con las noticias procesadas
output/           # Gráficos generados durante el análisis
docs/             # Documentación del proyecto
tests/            # Tests unitarios

```

Script principal que ejecuta todo el proceso es:

```

run.py

```

---

## Cómo se conecta a la API

El archivo `api_client.py` es el encargado de construir la solicitud hacia la API interna de La Nación. Lo que hace básicamente es preparar el parámetro `query` respetando la estructura que el frontend del sitio utiliza, y luego enviarlo a la URL:

```

https://www.lanacion.com.ar/pf/api/v3/content/fetch/acuArticlesSource

````

Cada request incluye un JSON:

```python
QUERY_BASE = {
    "authorId": None,
    "excludePreload": False,
    "excludeSectionId": False,
    "hasCollectionApertura": False,
    "imageConfig": "newBoxArticles",
    "page": 1,
    "promoItemsOnly": False,
    "sectionId": None,
    "sectionsIds": "(\"/economia\",\"/sociedad\", ... )",
    "shouldNotFilter": False,
    "size": 30,
    "sourceOrigin": "composer",
    "type": "",
    "website": "la-nacion-ar"
}
````

Durante la ejecución simplemente actualiza el campo `"page"` para obtener la página 1, 2, 3… hasta que la API no devuelva más elementos.

---

## Proceso de scraping

La coordinacion del scraping está en `scraper.py`. Esa parte hace tres cosas:

- **Genera una request por página**, cambiando el campo `"page"` del `query`.
- **Invoca al parser** para transformar el JSON crudo en un diccionario limpio.
- **Corta el proceso automáticamente** cuando la API devuelve cero resultados.

El código esencial del flujo es algo así:

```python
def fetch_all_pages(max_pages=15):
    noticias = []

    for page in range(1, max_pages + 1):
        print(f"[INFO] Fetching page {page}...")
        data = fetch_json_page(page)

        if not data:
            print("[ALERTA] No hay mas datos")
            break

        items = parse_items(data)

        if not items:
            break

        noticias.extend(items)

    return noticias
```

De esta forma, el scraper puede llegar a recolectar cientos de noticias sin depender del HTML inicial.

---

## Cómo se parsean las noticias

El archivo `parser.py` recibe la estructura JSON que La Nación envía y la convierte en un formato estandarizado. En la práctica significa transformar un JSON grande en un diccionario Python mucho más simple:

```python
{
    "titulo": item["headlines"]["basic"],
    "url": item["website_url"],
    "hora": int(item["publish_date"][11:13]),
    "autor": autor_extraido_o_None,
    "tags": lista_de_tags
}
```

El parser también maneja casos donde el autor no existe, donde no hay tags o donde el dato viene incompleto.

---

## Guardado de datos

El módulo `utils.py` contiene funciones para guardar la información procesada en formatos JSON y CSV:

### Guardado en JSON

```python
save_json(noticias, "data/processed/noticias.json")
```

### Guardado en CSV

```python
save_csv(noticias, "data/processed/noticias.csv")
```

Si el archivo esta vacío, se emite una advertencia para evitar guardar basura.

---

## Generación de gráficos y análisis

Luego de tener el dataset con todas las noticias, el archivo `analysis.py` permite hacer gráficos como:

* **Distribución de noticias por hora**
* **Autores más frecuentes**
* **Categorías más mencionadas**

Por ejemplo, el gráfico de autores usa un simple conteo:

```python
counter_autores = Counter([n["autor"] for n in noticias if n["autor"]])
plt.bar(etiquetas, valores)
```

Y lo guarda en:

```
output/top_autores.png
```

---

## Ejecución del scraper

El script principal, `run.py`, coordina todas las etapas:

1. Descarga todas las noticias usando la API.
2. Muestra un pequeño resumen por consola.
3. Guarda los datos en CSV y JSON.
4. Ejecuta el análisis para generar gráficos.
5. Informa dónde se guardó todo.

La ejecución es simplemente:

```bash
python3 run.py
```

Y al finalizar aparecen en:

* `data/processed/noticias.json`
* `data/processed/noticias.csv`
* `output/*.png`