import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from rich.console import Console
from rich.json import JSON
from rich.table import Table
from rich.panel import Panel
from rich import box



console = Console()

ARCHIVO_JSON = Path('perimetros.json')


def cargar_json(ruta: Path=ARCHIVO_JSON, default=None) -> List[Dict]:
    if ruta.exists():
        try:
            with ruta.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default or []
    return default or []


def guardar_json(dato: Dict, ruta: Path=ARCHIVO_JSON) -> None:
    datos = cargar_json(ruta, [])
    datos.append(dato)
    with ruta.open('w', encoding='utf-8')as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def mostrar_json() -> None:
    datos = cargar_json()
        
    # FORMATO TABLA
    if not datos:
        console.print(Panel(
            '[yellow]📂 No hay datos guardados aún.[/yellow]',
            title='Historial vacío',
            border_style='yellow'
        ))
        return
    
    # Crear tabla principal
    table = Table(
        title=f'📊 HISTORIAL DE CÁLCULOS ({len(datos)} registros)',
        title_style='bold cyan',
        box=box.ROUNDED,
        show_header=True,
        header_style='bold magenta',
        border_style='cyan',
        expand=False
    )
    
    # Añadir columnas
    table.add_column('#', style='yellow', justify='right', width=4)
    table.add_column('Fecha', style='cyan', width=17)
    table.add_column('Figura', style='green', width=20)
    table.add_column('Perímetro', style='bold blue', justify='right', width=12)
    table.add_column('Parámetros', style='magenta', width=40)
    
    # Añadir filas con los datos
    for i, registro in enumerate(datos, 1):
        fecha = registro.get('fecha', 'N/D')
        figura = registro.get('figura', 'desconocida')
        perimetro = registro.get('perimetro', 'N/D')
        params = registro.get('parametros', {})
        
        # Formatear parámetros
        if isinstance(params, dict):
            params_str = '\n'.join([f'{k}: {v}' for k, v in params.items()])
        else:
            params_str = str(params)
        
        # Formatear perímetro
        perimetro_str = f'{perimetro:.2f}' if isinstance(perimetro, (int, float)) else str(perimetro)
        
        table.add_row(
            str(i),
            fecha,
            figura.replace('_', ' ').title(),
            perimetro_str,
            params_str
        )
    
    console.print(table)


def obtener_fecha() -> str:
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


def registrar_resultado(**kwargs):
    guardar_json({'fecha': obtener_fecha(), **kwargs})


def buscar_por_figura(figura: str, ruta: Path = ARCHIVO_JSON) -> None:
    """Busca y muestra registros de una figura específica con Rich"""
    datos = cargar_json(ruta)
    
    if not isinstance(datos, list):
        console.print(Panel(
            '[red]El formato del archivo JSON no es una lista de registros.[/red]',
            title='❌ Error',
            border_style='red'
        ))
        return
    
    figura = figura.lower().strip()
    
    # Filtrar resultados
    resultados = [
        registro for registro in datos
        if isinstance(registro, dict) and 
        'figura' in registro and 
        registro['figura'].lower() == figura
    ]
    
    if not resultados:
        console.print(Panel(
            f'[yellow]No se encuentran registros para la figura "[bold]{figura}[/bold]"[/yellow]',
            title='🔍 Búsqueda sin resultados',
            border_style='yellow'
        ))
        return
    
    # Crear tabla de resultados
    table = Table(
        title=f'🔍 Resultados para: [bold green]{figura.replace("_", " ").upper()}[/bold green]',
        title_style='bold cyan',
        box=box.DOUBLE,
        show_header=True,
        header_style='bold magenta',
        border_style='cyan',
        expand=False
    )
    
    table.add_column('#', style='yellow', justify='right', width=4)
    table.add_column('Fecha', style='cyan', width=17)
    table.add_column('Perímetro', style='bold green', justify='right', width=12)
    table.add_column('Parámetros', style='blue', width=45)
    
    for i, res in enumerate(resultados, 1):
        fecha = res.get('fecha', 'N/D')
        perimetro = res.get('perimetro', 'N/D')
        params = res.get('parametros', {})
        
        # Formatear parámetros
        if isinstance(params, dict):
            params_str = ', '.join([f'{k}: {v}' for k, v in params.items()])
        else:
            params_str = str(params)
        
        # Formatear perímetro
        perimetro_str = f'{perimetro:.2f}' if isinstance(perimetro, (int, float)) else str(perimetro)
        
        table.add_row(str(i), fecha, perimetro_str, params_str)
    
    console.print(table)
    
    # Panel con resumen
    console.print(Panel(
        f'[bold cyan]Total de registros encontrados:[/bold cyan] [yellow]{len(resultados)}[/yellow]',
        border_style='green',
        expand=False
    ))
    
    # Estadísticas específicas de la figura
    if resultados:
        perimetros = [
            r.get('perimetro', 0) 
            for r in resultados 
            if isinstance(r.get('perimetro'), (int, float))
        ]
        
        if perimetros:
            stats_table = Table(
                title='📊 Estadísticas de esta figura',
                box=box.SIMPLE,
                show_header=False,
                border_style='green',
                expand=False
            )
            
            stats_table.add_column(style='cyan')
            stats_table.add_column(style='yellow', justify='right')
            
            stats_table.add_row('Perímetro promedio:', f'{sum(perimetros)/len(perimetros):.2f}')
            stats_table.add_row('Perímetro máximo:', f'{max(perimetros):.2f}')
            stats_table.add_row('Perímetro mínimo:', f'{min(perimetros):.2f}')
            
            console.print('\n')
            console.print(stats_table)

            
    """ resultados = []

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
 """
    
   

                

    
