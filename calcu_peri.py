import math
from typing import Union
from utils_json import registrar_resultado


def calcular_perimetro(figura: str, **kwargs: float) -> Union[float, str]:
    """
    Calcula el perímetro de distintas figuras geométricas según los argumentos pasados.

    Parámetros:
        figura (str): Tipo de figura ('rectangulo', 'triangulo_equilatero','triangulo_isosceles', 'triangulo_escaleno', 
            'triangulo_rectangulo', 'circulo', 'trapecio', 'cuadrado', 'poligono regular')
        **kwargs: Parámetros de cada figura (base, altura, radio, lado, etc.)

    Retorna:
        float: Área calculada redondeada a 2 decimales.
        str: Mensaje de error si falta un argumento o la figura no es válida.
    """ 


    def perimetro_cuadrado(lado: float) -> float:
        return 4 * lado
    
    
    def perimetro_rectangulo(base: float, altura: float) -> float:
        return 2 * (base + altura)
    

    def perimetro_trapecio(base_mayor: float, base_menor: float, lado: float) -> float:
        return base_mayor + base_menor + (lado * 2)
    

    def perimetro_circulo(radio: float) -> float:
        return 2 * math.pi * radio
    

    def perimetro_poligono_regular(num_lados: int, lado: float) -> float:
        return num_lados * lado


    def perimetro_triangulo_equilatero(lado: float) -> float:
        return 3 * lado


    def perimetro_triangulo_isosceles(lados_iguales: float, lado: float) -> float:
        return (2 * lados_iguales) + lado
    

    def perimetro_triangulo_escaleno(lado_1: float, lado_2: float, lado_3: float) -> float:
        if((lado_1 + lado_2) > lado_3) and ((lado_2 + lado_3) > lado_1) and ((lado_1 + lado_3) > lado_2):
            return lado_1 + lado_2 + lado_3
        else:
            return f'Un triángulo con esos valores no se puede construir'
        

    def perimetro_triangulo_rectangulo(cateto_1: float, cateto_2: float) -> float:
        return cateto_1 + cateto_2 + (math.hypot(cateto_1, cateto_2))


    figuras = {
        'cuadrado': perimetro_cuadrado,
        'rectangulo': perimetro_rectangulo,
        'trapecio': perimetro_trapecio,
        'circulo': perimetro_circulo,
        'poligono_regular': perimetro_poligono_regular,
        'triangulo_equilatero': perimetro_triangulo_equilatero,
        'triangulo_isosceles': perimetro_triangulo_isosceles,
        'triangulo_escaleno': perimetro_triangulo_escaleno,
        'triangulo_rectangulo': perimetro_triangulo_rectangulo
    } 

    if figura not in figuras:
        raise ValueError(f'Figura {figura} no valida. Usa: {",".join(figuras.keys())}')
    
    try:
        perimetro = round(figuras[figura](**kwargs), 2)
        datos = {
            'figura': figura,
            'perimetro': perimetro,
            'parametros': kwargs
        }
        registrar_resultado(**datos)
        return perimetro
    except TypeError:
        return f'Argumentos incorrectos para la figura {figura}'
    

        

            