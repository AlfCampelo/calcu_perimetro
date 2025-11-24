from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from calcu_peri import calcular_perimetro
from utils_json import mostrar_json, buscar_por_figura, mostrar_ultimos_calculos, limpiar_historial

console = Console()

# ======================================
# ====== CONFIGURACIÓN DE FIGURAS ======
# ======================================

FIGURAS_CONFIG = {
    '1': {
        'nombre': 'cuadrado',
        'titulo': 'Cuadrado',
        'params': [
            ('lado', 'Introduce el lado', 'float')
        ]
    },
    '2': {
        'nombre': 'rectangulo',
        'titulo': 'Rectángulo',
        'params': [
            ('base', 'Introduce la base', 'float'),
            ('altura', 'Introduce la altura', 'float')
        ]
    },
    '3': {
        'nombre': 'trapecio',
        'titulo': 'Trapecio',
        'params': [
            ('base_mayor', 'Introduce la base mayor', 'float'),
            ('base_menor', 'Introduce la base menor', 'float'),
            ('lado', 'Introduce los lados', 'float')
        ]
    },
    '4': {
        'nombre': 'circulo',
        'titulo': 'Circulo',
        'params': [
            ('radio', 'Introduce el radio', 'float')
        ]
    },
    '5': {
        'nombre': 'poligono_regular',
        'titulo': 'Polígono regular',
        'params': [
            ('num_lados', 'Introduce el número de lados', 'int'),
            ('lado', 'Introduce el lado', 'float'),
        ]
    },
    '6': {
        'nombre': 'triangulo_equilatero',
        'titulo': 'Triángulo equilátero',
        'params': [
            ('lado', 'Introduce el lado', 'float')
        ]
    },
    '7': {
        'nombre': 'triangulo_isosceles',
        'titulo': 'Triángulo isósceles',
        'params': [
            ('lados_iguales', 'Introduce los lados iguales', 'float'),
            ('lado', 'Introduce el otro lado', 'float'),
        ]
    },
    '8': {
        'nombre': 'triangulo_escaleno',
        'titulo': 'Triángulo escaleno',
        'params': [
            ('lado_1', 'Introduce el primer lado', 'float'),
            ('lado_2', 'Introduce el segundo lado', 'float'),
            ('lado_3', 'Introduce el tercer lado', 'float')
        ]
    },
    '9': {
        'nombre': 'triangulo_rectangulo',
        'titulo': 'Triángulo rectángulo',
        'params': [
            ('cateto_1', 'Introduce el primer cateto', 'float'),
            ('cateto_2', 'Introduce el segundo cateto', 'float'),
        ]
    }
}


# ======================================
# ======== FUNCIONES AUXILIARES ========
# ======================================


def pedir_float(mensaje: str) -> float:
    ''' Solicita un número float positivo al usuario '''
    while True:
        try:
            valor = float(Prompt.ask(mensaje))
            if valor <= 0:
                raise ValueError
            return valor
        except ValueError:
            console.print('[red]Ingresa un número válido mayor que cero.')


def pedir_int(mensaje: str) -> int:
    ''' Solicita un número entero positivo al usuario '''
    while True:
        try:
            valor = int(Prompt.ask(mensaje))
            if valor <= 0:
                raise ValueError
            return valor
        except ValueError:
            console.print('[red]Ingresa un número entero válido mayor que cero[/red]')


def procesar_figura(config: dict) -> None:
    '''
        Procesa el cálculo de perímetro para cualquier figura según su configuración.

        Args:
            config: Diccionario con la configuración de la figura
                (nombre, titulo, params)
    '''
    try:
        # Recopilar parámetros dinámicamente
        parametros = {}

        for paran_name, mensaje, tipo in config['params']:
            if tipo == 'int':
                parametros[paran_name] = pedir_int(mensaje)
            elif tipo == 'float':
                parametros[paran_name] = pedir_float(mensaje)

        # Calcular perímetro
        perimetro = calcular_perimetro(config['nombre'], **parametros)

        # Mostrar resultado
        mostrar_resultado(config['titulo'], perimetro=perimetro)
    
    except ValueError as e:
        console.print(Panel(f'[bold red]⚠️ Error: {e}[/bold red]', border_style='red'))
    except Exception as e:
        console.print(Panel(f'[bold red]❌ Error inesperado: {e}[/bold red]', border_style='red'))



def mostrar_resultado(nombre_figura: str, perimetro: float) -> None:
    ''' Muestra el resultado del cálculo de forma atractiva. '''
    console.print(Panel.fit(
        f'[bold cyan]Perímetro del {nombre_figura.lower()}[/bold cyan]'
        f'[bold green] 📏 {perimetro} unidades[/bold green]',
        border_style='green'
    ))


def mostrar_menu() -> None:
    ''' Muestra el menú principal con todas las opciones '''
    table = Table(title='MENÚ PERÍMETRO', style='bold blue')

    table.add_column('Opción', style='yellow', justify='center')
    table.add_column('Descripción')

    # Agregar opciones de figuras desde la configuración
    for opcion, config in FIGURAS_CONFIG.items():
        table.add_row(opcion, config['titulo'])

    # Agregar opciones adicionales
    table.add_row('10', 'Mostrar JSON')
    table.add_row('11', 'Buscar historial por figura')
    table.add_row('12', 'Últimos 5 cálculos')
    table.add_row('13', 'Limpiar historial')
    table.add_row('14', 'Salir')
    
    console.print(table)


def buscar_historial() -> None:
    ''' Permite al usuario buscar en el historial por figura '''

    # Crear lista de figuras para búsqueda
    figuras_busqueda = [
        (str(i), config['nombre'], config['titulo'])
        for i, (_, config) in enumerate(FIGURAS_CONFIG.items(), 1)
    ]

    # Mostrar tabla de opciones
    table = Table(title='Buscar en el historial', style='bold blue')
    table.add_column('Opción', style='yellow', justify='center')

    for opcion, _, titulo in figuras_busqueda:
        table.add_row(opcion, titulo)

    console.print(table)

    # Solicitar opción
    try:
        index_str = Prompt.ask(
            'Introduce el número de figura a buscar',
            choices=[str(i) for i in range(1, len(figuras_busqueda) + 1)]
        )
        index = int(index_str) -1
        nombre_figura = figuras_busqueda[index][1]
        buscar_por_figura(figura=nombre_figura)

    except (ValueError, IndexError) as e:
        console.print(Panel(f'[bold red]Errror: {e}[/bold red]', border_style='red'))

    
# ======================================
# =========== MENÚ PRINCIPAL ===========
# ======================================

def menu() -> None:
    ''' Menú principal de la aplicación '''
    while True:
        try:
            mostrar_menu()

            opcion = Prompt.ask(
                '\n[bold cyan]Elige una opción[/bold cyan]',
                choices=[str(i) for i in range(1, 15)])
            
            # Procesar figuras geométricas (opciones 1-9)
            if opcion in FIGURAS_CONFIG:
                procesar_figura(FIGURAS_CONFIG[opcion])
            
            # Mostrar JSON (opción 10)
            elif opcion == '10':
                console.print('\n[bold cyan]=== HISTORIAL DE CÁLCULOS ===[/bold cyan]\n')
                mostrar_json()

            # Buscar historial (opción 11)
            elif opcion == '11':
                buscar_historial()

            # Mostrar últimos 5 cálculos (opción 12)
            elif opcion == '12':
                console.print('\n[bold cyan]=== ÚLTIMOS CÁLCULOS ===[/bold cyan]\n')
                mostrar_ultimos_calculos(5)

            # Limpiar historial (opción 13)
            elif opcion == '13':
                confirmacion = Prompt.ask(
                    '[bold yellow]⚠️ ¿Estás seguro de que deseas limpiar todo el historial? (s/n)[/bold yellow]',
                    choices=['s', 'n', 'S', 'N'],
                    default='n'                    
                )
                if confirmacion.lower() == 's':
                    limpiar_historial()

            # Salir (opción 14)
            elif opcion == '14':
                console.print(Panel(
                    '[bold green]✋ Hasta pronto[/bold green]',
                    border_style= 'green'
                ))
                break
            
            # Pausa antes de mostrar el menú nuevamente
            if opcion != '14':
                console.print('\n[dim]Presiona ENTER para continuar...[/dim]')
                input()
                console.clear()
        
        except KeyboardInterrupt:
            console.print('\n')
            console.print(Panel(
                '[bold yellow]⚠️ Operación cancelada por el usuario[/bold yellow]',
                border_style='yellow'
            ))
            break

        except Exception as e:
             console.print(Panel(
                f'[bold red]❌ Error inesperado: {e}[/bold red]',
                border_style='red'
            ))
            


""" def mostrar_menu():
    table = Table(title='MENÚ PERÍMETRO', style='bold blue')

    table.add_column('Opción', style='yellow')
    table.add_column('Descripción')

    opciones = [
        ('1', 'Cuadrado'),
        ('2', 'Rectángulo'),
        ('3', 'Trapecio'),
        ('4', 'Circulo'),
        ('5', 'Poligono regular'),
        ('6', 'Triángulo equilatero'),
        ('7', 'Triángulo isósceles'),
        ('8', 'Triángulo escaleno'),
        ('9', 'Triángulo rectángulo'),
        ('10', 'Mostrar JSON'),
        ('11', 'Buscar historial por figura'),
        ('12', 'Salir')
    ]

    for op, desc in opciones:
        table.add_row(op, desc)

    console.print(table)

def menu() -> None:  
    while True:
        mostrar_menu()
        opcion = Prompt.ask('Elige una opción', choices=[str(i) for i in range(1,13)])

        # ================ OPCIÓN 1 ================
        # ==============  CUADRADO  ================
        if opcion == '1':
            lado = pedir_float('Introduce el lado')
            perimetro = calcular_perimetro('cuadrado',lado=lado)
            console.print(Panel(f'Perímetro del cuadrado = [bold green] {perimetro} [/bold green]'))

        # ================ OPCIÓN 2 ================
        # ==============  RECTÁNGULO  ==============
        elif opcion == '2':
            base = pedir_float('Introduce la base')
            altura = pedir_float('Introduce la altura')
            perimetro = calcular_perimetro('rectangulo', base=base, altura=altura)
            console.print(Panel(f'Perímetro del rectángulo = [bold green] {perimetro} [/bold green]'))
        
        # ================ OPCIÓN 3 ================
        # ===============  TRAPECIO  ===============
        elif opcion == '3':
            base_mayor = pedir_float('Introduce la base mayor')
            base_menor = pedir_float('Introduce la base menor')
            lado = pedir_float('Introduce los lados')
            perimetro = calcular_perimetro('trapecio', base_mayor=base_mayor, base_menor=base_menor, lado=lado)
            console.print(Panel(f'Perímetro del trapecio = [bold green] {perimetro} [/bold green]'))

        # ================ OPCIÓN 4 ================
        # ===============  CIRCULO  ================
        elif opcion == '4':
            radio = pedir_float('Introduce el radio')
            perimetro = calcular_perimetro('circulo', radio=radio)
            console.print(Panel(f'Perímetro del circulo = [bold green] {perimetro} [/bold green]'))
            
        # ================ OPCIÓN 5 ================
        # ===========  POLIGONO REGULAR  ===========
        elif opcion == '5':
            num_lados = int(Prompt.ask('Introduce el número de lados'))
            lado = pedir_float('Introduce el lado')
            perimetro = calcular_perimetro('poligono_regular', num_lados=num_lados, lado=lado)
            console.print(Panel(f'Perímetro del poligono regular de {num_lados} = [bold green] {perimetro} [/bold green]'))
            
        # ================ OPCIÓN 6 ================
        # =========  TRIÁNGULO EQUILATERO  =========
        elif opcion == '6':
            lado = pedir_float('Introduce el lado')
            perimetro = calcular_perimetro('triangulo_equilatero', lado=lado)
            console.print(Panel(f'Perímetro del triangulo equilatero = [bold green] {perimetro} [/bold green]'))

        # ================ OPCIÓN 7 ================
        # =========  TRIÁNGULO ISÓSCELES  ==========
        elif opcion == '7':
            lados_iguales = pedir_float('Introduce los lados iguales')
            lado = pedir_float('Introduce el otro lado')
            perimetro = calcular_perimetro('triangulo_isosceles', lados_iguales=lados_iguales, lado=lado)
            console.print(Panel(f'Perímetro del triángulo isósceles = [bold green] {perimetro} [/bold green]'))

        # ================ OPCIÓN 8 ================
        # ==========  TRIÁNGULO ESCALENO  ==========
        elif opcion == '8':
            lado_1 = pedir_float('Introduce el primer lado')
            lado_2 = pedir_float('Introduce el segundo lado')
            lado_3 = pedir_float('Introduce el tercer lado')
            perimetro = calcular_perimetro('triangulo_escaleno', lado_1=lado_1, lado_2=lado_2, lado_3=lado_3)
            console.print(Panel(f'Perímetro del triángulo escaleno = [bold green] {perimetro} [/bold green]'))

        # ================ OPCIÓN 9 ================
        # =========  TRIÁNGULO RECTÁNGULO  =========
        elif opcion == '9':
            cateto_1 = pedir_float('Introduce el primer cateto')
            cateto_2 = pedir_float('Introduce el segundo cateto')
            perimetro = calcular_perimetro('triangulo_rectangulo', cateto_1=cateto_1, cateto_2=cateto_2)
            console.print(Panel(f'Perímetro del triángulo rectangulo = [bold green] {perimetro} [/bold green]'))

        # ================ OPCIÓN 10 ================
        # ==============  MOSTRAR JSON  =============
        elif opcion == '10':
            mostrar_json()

        # ================ OPCIÓN 11 ================
        # ============  BUSCAR HISTORIAL  ===========
        elif opcion == '11':
            figuras = [
                ('1','cuadrado'), ('2','rectangulo'), ('3','trapecio'), ('4','circulo'),
                ('5','poligono_regular'), ('6','triangulo_equilatero'), ('7','triangulo_isosceles'),
                ('8','triangulo_escaleno'), ('9','triangulo_rectangulo')
                ]
            
            table = Table('Busqueda', style='bold blue')
            table.add_column('Opción', style='yellow')
            table.add_column('Descripción')
            for op, desc in figuras:
                table.add_row(op, desc)
            
            console.print(table)
            index_str = Prompt.ask('Introduce el número de la figura a buscar', choices=[str(i) for i in range(1, 10)])
            index = int(index_str) - 1 
            nombre_figura = figuras[index][1]
            buscar_por_figura(figura=nombre_figura)
        
        # ================ OPCIÓN 12 ================
        # =================  SALIR  =================
        elif opcion == '12':
            console.print(Panel(f'[bold red]✋ Hasta pronto [/bold red]'))
            break
        
        else:
            console.print(Panel(f'[bold red]⛔ Opción no valida[/bold red]')) """