# src/utils.py

import json
import csv
from pathlib import Path

def save_json(data: list[dict], path: str):
    # Guarda la lista de noticias en un json
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[INFO] json guardado en: {path}")
        
def save_csv(data: list[dict], path: str):
    # Guarda la lista de noticias en un csv
    
    path = Path(path)
    path.parent.mkdir(parents = True, exist_ok = True)
    
    if not data:
        print("[ALERTA] No hay datos para guardar en CSV.")
        return
    
    columnas = data[0].keys()
    
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(data)

        print(f"[INFO] CSV guardado en: {path}")