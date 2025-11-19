from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from calcu_peri import calcular_perimetro
from utils_json import mostrar_json, buscar_por_figura

console = Console()

def pedir_float(mensaje: str) -> float:
    while True:
        try:
            valor = float(Prompt.ask(mensaje))
            if valor <= 0:
                raise ValueError
            return valor
        except ValueError:
            console.print('[red]Ingresa un número válido mayor que cero.')


def mostrar_menu():
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
            console.print(Panel(f'[bold red]⛔ Opción no valida[/bold red]'))