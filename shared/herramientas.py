"""Funciones reutilizables para la interfaz de consola."""

import os

# DICCIONARIO: cada color tiene su etiqueta y su código de consola
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}

# TUPLA: respuestas afirmativas aceptadas. Es fija, por eso no es lista.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    """Limpia la consola usando el comando correspondiente al sistema operativo."""
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color):
    """Imprime texto con un color ANSI y después restaura el color normal."""
    codigo = COLORES.get(color, COLORES["BLANCO"])   # .get evita el error si el color no existe
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto):
    """Limpia la pantalla y dibuja un encabezado para una sección del menú."""
    limpiar_pantalla()
    imprimir_color("=" * 60, "AZUL")
    print(f"  {texto}".center(60))
    imprimir_color("=" * 60, "AZUL")
    print()


def imprimir_exito(mensaje):
    """Muestra un mensaje de operación exitosa en verde."""
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    """Muestra un mensaje de error en rojo."""
    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje):
    """Muestra información general en cyan."""
    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta):
    """Pregunta una confirmación y devuelve True solo para respuestas afirmativas."""
    # Devuelve True si el usuario respondió algo de la tupla RESPUESTAS_SI
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    texto = texto.strip()
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")