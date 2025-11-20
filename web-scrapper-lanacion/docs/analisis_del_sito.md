El link https://www.lanacion.com.ar/robots.txt informa cuales son los sitios que no estan permotidos para el uso de bots.
El link que interesa para hacer el scrapping es https://www.lanacion.com.ar/ultimas-noticias/ y no está incluido en robots.txt,
por lo que se mantiene etico.

Qué datos me interesan extraer por noticia:
 - Titulo
 - Fecha
 - Categorias/tags
 - Descripcion breve
 - Autor
 - URL completa

analizando el html, veo que cada articulo esta dentro de la clase:
article class="mod-article"
y la informacion que me interesa dentro de (Titulo, Fecha, Categorias/tags, Descripcion breve, Autor(si se ve desde el html), URL completa):
section class="mod-description"
en <time class="com-hour --font-primary --font-black --m"> obtengo la fecha (hora)
dentro, de <h2 class="com-title --font-primary --m --font-medium"> se ve el titulo, url completo 
y en <div> obtengo los tags y el autor si se ve desde la pagina ultimas noticias

no tiene paginacion en cuanto a un boton para pasar, sino que la misma pagina tiene un boton para cargar mas paginas