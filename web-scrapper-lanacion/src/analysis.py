# src/analysis.py

import json
from collections import Counter
import matplotlib.pyplot as plt
from pathlib import Path

# Cargar datos (noticias del json)

def load_noticias(path = "data/processed/noticias.json") -> list[dict]:
    path = Path(path)
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
    
# Genera contador con tags mas comunes
def contar_tags(noticias: list[dict]) -> Counter:
    todos_los_tags = []
    for n in noticias:
        todos_los_tags.extend(n["tags"])
    
    return Counter(todos_los_tags)


# Genera contador de autores
def contar_autores(noticias: list[dict]) -> Counter:
    autores = [n["autor"] for n in noticias if n["autor"]]
    return Counter(autores)

def extraer_horas(noticias: list[dict]) -> list[dict]:
    return [n["hora"] for n in noticias if isinstance(n["hora"], int)]


# Grafica en barras las categorias con mas publicaciones
def grafico_tags(counter_tags: Counter, top=10):
    # Grafico de barras tags/categorias mas frecuentes
    
    etiquetas = [tag for tag, _ in counter_tags.most_common(top)]
    valores = [count for _, count in counter_tags.most_common(top)]

    plt.figure(figsize=(10, 5))
    plt.bar(etiquetas, valores, color = "#D61031")
    plt.xticks(rotation=45, ha="right")
    plt.title("Top categorías de noticias")
    plt.tight_layout()
    plt.savefig("output/top_categorias.png")
    plt.close()
    print("[INFO] Gráfico guardado en output/top_categorias.png")

def grafico_autores(counter_autores: Counter, top=10):
    # Grafico de barras autores mas frecuentes
    
    etiquetas = [aut for aut, _ in counter_autores.most_common(top)]
    valores = [count for _, count in counter_autores.most_common(top)]

    plt.figure(figsize=(10, 5))
    plt.bar(etiquetas, valores, color = "#D61095")
    plt.xticks(rotation=45, ha="right")
    plt.title("Autores más frecuentes")
    plt.tight_layout()
    plt.savefig("output/top_autores.png")
    plt.close()
    print("[INFO] Gráfico guardado en output/top_autores.png")


def grafico_horas(horas: list[int]):
    # Grafico de linea cantidad de noticias por hora (0 a 23)

    counter = Counter(horas)

    horas_completas = list(range(24))
    cantidades = [counter.get(h, 0) for h in horas_completas]

    # Calcular hora con mas noticias
    max_count = max(cantidades)
    hora_max = cantidades.index(max_count)

    plt.figure(figsize=(12, 5))
    plt.plot(horas_completas, cantidades, marker="o", color = "#B510D6")

    # resalta el punto maximo
    plt.scatter(hora_max, max_count, s=40, color="#D61031", zorder=5)

    # añade texto sobre el punto maximo de noticias
    plt.text(
        hora_max,
        max_count + 0.7,  # arriba del punto
        f"Hora con más noticias: {hora_max} ({max_count})",
        ha="center",
        fontsize=10,
        fontweight="bold"
    )

    # Ajustes del grafico
    plt.title("Distribución de noticias por hora del día")
    plt.xlabel("Hora del día (0–23)")
    plt.ylabel("Cantidad de noticias")
    plt.xticks(horas_completas)  # Mostrar las 24 horas
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("output/noticias_por_hora.png")
    plt.close()

    print("[INFO] Gráfico de horas guardado en output/noticias_por_hora.png")

    
    
def main():
    noticias = load_noticias()

    # Analisis
    counter_tags = contar_tags(noticias)
    counter_autores = contar_autores(noticias)
    horas = extraer_horas(noticias)

    # Resumen en consola
    print("\nTOP TAGS:")
    print(counter_tags.most_common(5))

    print("\nTOP AUTORES:")
    print(counter_autores.most_common(5))

    print("\nHORAS MÁS FRECUENTES:")
    print(Counter(horas).most_common(5))

    # Graficos
    grafico_tags(counter_tags)
    grafico_autores(counter_autores)
    grafico_horas(horas)


if __name__ == "__main__":
    main()