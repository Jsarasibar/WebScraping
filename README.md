# WebScraping

Este repositorio reúne una colección de proyectos de web scraping desarrollados con un enfoque profesional, modular y ético. Cada scraper implementa prácticas recomendadas de análisis del sitio, respeto por los términos de uso y robots.txt, recolección robusta de datos, validación, procesamiento y generación de resultados útiles en formatos estándar.

Los objetivos generales son:

* automatización de extracción de datos,
* interacción con APIs públicas o no documentadas,
* procesamiento y normalización de información estructurada,
* análisis exploratorio y visualización,
* diseño modular de software en Python,
* buenas prácticas de versionado, documentación y testing.

Cada scraper se desarrolla en su propio subdirectorio.

---

## Proyectos incluidos

### 1. Scraper La Nación (noticias)

Scraper que obtiene las últimas noticias del sitio La Nación utilizando la misma API interna que usa el frontend para cargar contenido dinámico. Incluye:

* manejo de paginación
* extracción de título, hora, autor, categorías y URL
* almacenamiento en CSV y JSON
* generación de análisis estadísticos y gráficos
* documentación técnica del análisis del sitio y del funcionamiento interno

Directorio:
`web-scrapper-la-nacion/`

Documentación principal:

* `analisis_del_sitio.md`
* `funcionamiento.md`
* `README.md` del subproyecto

---

### 2. Scraper Mercado Libre (productos)

En desarrollo. Este scraper tendrá como objetivo extraer datos públicos de productos, precios, categorías y vendedores desde Mercado Libre, respetando las limitaciones de su robots.txt y usando un enfoque responsable.

El proyecto incluirá:

* análisis previo del sitio,
* estrategias de paginación o consulta (HTML, API, filters),
* extracción de productos,
* normalización de precios,
* análisis comparativo y gráficos.

Directorio proyectado:
`web-scraper-mercado-libre/`

---

## Estructura general del repositorio

```
WebScraping/
├── web-scraper-la-nacion/
│   ├── src/
│   ├── data/
│   ├── output/
│   ├── docs/
│   ├── tests/
│   └── README.md
├── web-scraper-mercado-libre/   # se agregará cuando el proyecto esté desarrollado
└── README.md (este archivo)
```

Cada subproyecto contiene:

* documentación propia,
* un `README.md` específico,
* un entorno modular en `src/`,
* scripts de ejecución,
* datos generados,
* análisis y gráficos.

---

## Instalación y uso general

Cada scraper incluye su propio archivo `requirements.txt`.

Ejemplo de instalación:

```bash
cd web-scraper-la-nacion
python3 -m venv venv
pip install -r requirements.txt
python3 run.py
```

Cada subproyecto tiene sus propios pasos y documentación detallada.

---

## Licencia y uso responsable

Los scrapers están diseñados con fines de estudio y no deben utilizarse para generar tráfico abusivo sobre los sitios analizados ni para redistribuir contenido sin autorización.