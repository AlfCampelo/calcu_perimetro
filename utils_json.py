import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict


ARCHIVO_JSON = Path('perimetros.json')


def cargar_json(ruta: Path=ARCHIVO_JSON, default=None) -> List[Dict]:
    if ruta.exists():
        try:
            with ruta.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default or []
    return default or []


def guardar_json(dato: Dict, ruta: Path=ARCHIVO_JSON):
    datos = cargar_json(ruta, [])
    datos.append(dato)
    with ruta.open('w', encoding='utf-8')as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def mostrar_json():
    datos = cargar_json()
    if not datos:
        print('No hay datos guardados aún.')
    else:
        print(json.dumps(datos, indent=4, ensure_ascii=False))


def obtener_fecha():
    return datetime.now().strftime('%d/%m/%Y %H:%M:S')


def registrar_resultado(**kwargs):
    guardar_json({'fecha': obtener_fecha(), **kwargs})


