# Análisis del sitio

Antes de empezar con el desarrollo del scraper analicé el sitio de La Nación para entender qué secciones eran accesibles y si era ético automatizar la extracción. Lo primero fue revisar el archivo oficial de `robots.txt`, ubicado en:

[https://www.lanacion.com.ar/robots.txt](https://www.lanacion.com.ar/robots.txt)

Ese archivo especifica qué directorios permiten la presencia de bots y cuáles no. La sección que me interesa para este proyecto, “Últimas Noticias” ([https://www.lanacion.com.ar/ultimas-noticias/](https://www.lanacion.com.ar/ultimas-noticias/)), no está listada como restringida, así que el scraping sobre esa ruta es aceptable siempre y cuando se haga de forma responsable: sin abusar de la cantidad de requests, sin intentar acceder a contenido privado y sin afectar el funcionamiento normal del sitio.

---

## Análisis inicial del HTML

Al principio trabajé directamente sobre el HTML de la página de últimas noticias. Cada noticia aparece envuelta en un bloque similar a este:

```html
<article class="mod-article">
    <time class="com-hour ...">18:54</time>
    <section class="mod-description">
        <h2 class="com-title ...">
            <a href="/politica/...">Título de la noticia</a>
        </h2>
        <div>tags, autor, etc...</div>
    </section>
</article>
```

A partir de esta estructura se pueden extraer varios datos interesantes por noticia:

* El título, desde el `h2.com-title` y el enlace interno (`<a href="...">`).
* La hora de publicación, desde la etiqueta `<time class="com-hour ...">`.
* Tags o categorías, buscando enlaces y textos adicionales dentro del `<div>` interno.
* El autor, cuando aparece, también dentro de ese bloque, a través de enlaces con atributos como `title="Por (Autor)"`.
* La URL completa, construyendo `https://www.lanacion.com.ar` + la ruta relativa del link.

El problema de esta aproximación es que el HTML solo muestra un conjunto limitado de noticias (aprox. 30) y luego el sitio ofrece un botón de “Cargar más noticias”. No hay una paginación clásica con URLs del estilo `/page/2/`, lo que indica que el contenido adicional se carga dinámicamente vía JavaScript.

---

## Funcionamiento de la API interna

Para entender cómo se cargaban las noticias extra, abrí las herramientas de desarrollo del navegador y miré la pestaña de red (Network), filtrando por solicitudes del tipo fetch/XHR. Al hacer clic en “Cargar más noticias”, aparece una request a un endpoint interno de la Nación:

[https://www.lanacion.com.ar/pf/api/v3/content/fetch/acuArticlesSource](https://www.lanacion.com.ar/pf/api/v3/content/fetch/acuArticlesSource)

Este endpoint recibe un parámetro `query` muy largo, codificado en URL, que contiene un objeto JSON con todos los parámetros de la consulta. Cuando se decodifica, se ve algo parecido a lo siguiente (simplificado):

```json
{
  "authorId": null,
  "excludePreload": false,
  "excludeSectionId": false,
  "hasCollectionApertura": false,
  "imageConfig": "newBoxArticles",
  "page": 1,
  "promoItemsOnly": false,
  "sectionId": null,
  "sectionsIds": "(\"/economia\",\"/sociedad\",\"/deportes\",\"/politica\",...)",
  "shouldNotFilter": false,
  "size": 30,
  "sourceOrigin": "composer",
  "type": "",
  "website": "la-nacion-ar"
}
```

El parámetro clave es `page`, que controla qué tanda de noticias se devuelve (1, 2, 3, etc.), junto con `size`, que indica cuántos resultados trae por página (en este caso, 30). Gracias a esto deja de ser necesario depender del HTML inicial: se puede consumir directamente la API y obtener muchas más noticias que las visibles en la primera carga del DOM.

La ventaja de esta API es que devuelve la información en JSON, con mucha más estructura que el HTML. Por ejemplo, se puede acceder a campos como:

* `headlines.basic` para el título de la noticia.
* `website_url` para la URL (ya lista para usar).
* `publish_date` para la fecha y hora completa en formato timestamp.
* `credits.by` para la lista de autores.
* `taxonomy.primary_section` y `tags` para secciones y etiquetas.

Esto hace que el scraping sea más estable y menos frágil frente a cambios de diseño en el frontend.

---

## Cambio de estrategia: de HTML a API

Una vez entendida la existencia de esta API, la estrategia del scraper cambió. En lugar de extraer datos del HTML con BeautifulSoup, la versión final del proyecto se apoya exclusivamente en la API interna que La Nación utiliza para el botón de “Cargar más noticias”.

La lógica básica es:

1. Construir el JSON de `query` respetando la estructura original que usa el sitio.
2. Modificar dinámicamente el campo `"page"` para pedir página 1, 2, 3, etc.
3. Hacer requests consecutivas hasta que la API deje de devolver resultados.
4. Parsear cada respuesta JSON y transformarla en una estructura de Python más simple.

En el parser, cada noticia termina representada con una estructura similar a esta:

```python
noticia = {
    "titulo": item["headlines"]["basic"],
    "url": item["website_url"],
    "hora": int(item["publish_date"][11:13]),
    "autor": autor_extraido_o_None,
    "tags": lista_de_tags_y_categorias
}
```

De esta forma, la parte compleja se concentra en entender la estructura del JSON de la API y no en adivinar clases CSS o estructuras HTML cambiantes. Además, al poder paginar, se obtienen cientos de noticias en lugar de solo las últimas 30, lo que permite hacer análisis más interesantes (distribución por hora, ranking de autores, categorías más frecuentes, etc.).

---

## Conclusión

Se pueden ver tres cosas importantes: primero, que la sección “Últimas Noticias” no está bloqueada en el `robots.txt`, por lo que el scraping se puede hacer de forma ética y controlada. Segundo, que el HTML inicial sirve como referencia, pero es limitado y depende demasiado del diseño. Tercero, que la mejor forma de obtener datos fiables y en volumen es usar la API interna que el propio sitio expone para cargar más noticias.