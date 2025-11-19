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


def buscar_por_figura(figura: str, ruta: Path=ARCHIVO_JSON):
    datos = cargar_json(ruta)
    if not isinstance(datos, list):
        print('El formato del archivo JSON no es una lista de registros.')
        return
    
    figura = figura.lower().strip()

    resultados = []

    for registro in datos:
        if isinstance(registro, dict) and 'figura' in registro and registro['figura'].lower() == figura:
            resultado = {
                'fecha': registro.get('fecha', 'N/D'),
                'parametros': registro.get('parametros', 'N/D'),
                'perimetro': registro.get('perimetro', 'N/D')
                }
            resultados.append(resultado)

        if resultados:
            print(f'\nResultados de búsqueda para la figura: {figura}')
            for i, res in enumerate(resultados):
                print(f'\nRegistro #{i + 1} ({res["fecha"]}):')
                print(f'Perimetro: {res["perimetro"]}')
                params_str = ', '.join([f'{k}: {v}' for k, v in res['parametros'].items()]) if isinstance(res['parametros'], dict) else res['parametros']
                print(f'Parámetros: {{{params_str}}}')
                print('---------------------------------------------------------------------------------------')
        else:
            print(f'\nNo se encuentran registros para la figura {figura}')


   

                

    
