"""VISTA: punto de entrada y menú. Pide datos con input(), muestra con print()
y llama a views.py para las reglas. No valida reglas del negocio ni abre archivos."""

import sys

# Fuerza UTF-8 en la consola para que se vean bien ✓ ✗ y las tildes en Windows
sys.stdout.reconfigure(encoding="utf-8")

from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, estadisticas,
    inscribir_materia, agregar_nota, obtener_promedio,
    materias_ofertadas, estudiantes_en_comun
)


def pausa():
    """Detiene la pantalla hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    """Imprime una lista de estudiantes en formato de tabla (los números son el ancho de cada columna)."""
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CIUDAD':<15}")
    print("-" * 85)
    for estudiante in estudiantes:
        print(f"{estudiante.id:<5}{estudiante.obtener_nombre_completo():<25}"
              f"{estudiante.email:<28}{estudiante.ciudad:<15}")
    print("-" * 85)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


def _pedir_estudiante():
    """Pide un id y comprueba que exista. Devuelve el id, o None si es inválido o no existe."""
    try:
        id_estudiante = int(input("Id del estudiante: "))   # int() convierte el texto a entero
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return None
    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return None
    imprimir_info(f"Estudiante: {estudiante.obtener_nombre_completo()}")
    return id_estudiante


# ---------- C · CREAR ----------
def opcion_crear():
    """Opción 1: pide cada campo del estudiante y solicita su creación."""
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    # Recorre la TUPLA de campos: si se agrega un campo al modelo, el formulario se actualiza solo
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)     # desempaqueta la TUPLA que devuelve
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- R · LEER TODOS ----------
def opcion_ver_todos():
    """Opción 2: muestra la tabla con todos los estudiantes."""
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1 para crear el primero.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


# ---------- S · BUSCAR ----------
def opcion_buscar():
    """Opción 3: busca por nombre, apellido, email, teléfono o ciudad."""
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, email, teléfono o ciudad: ")
    encontrados = buscar_estudiantes(termino)

    if not encontrados:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


# ---------- R · LEER UNO ----------
def opcion_ver_por_id():
    """Opción 4: muestra todos los datos de un estudiante, incluido su promedio."""
    imprimir_titulo("VER ESTUDIANTE POR ID")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        # Recorre el DICCIONARIO del estudiante: clave y valor a la vez
        for clave, valor in estudiante.a_diccionario().items():
            print(f"  {clave.capitalize():<12}: {valor}")
        print(f"  {'Promedio':<12}: {estudiante.obtener_promedio()}")
    pausa()


# ---------- U · ACTUALIZAR ----------
def opcion_actualizar():
    """Opción 5: cambia solo los campos que el usuario escribe (Enter vacío = no cambiar)."""
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Editando a {estudiante.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no quiera cambiar.\n")

    # Arma un DICCIONARIO solo con lo que el usuario escribió
    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(estudiante, campo)      # getattr lee un atributo por su nombre (texto)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- D · ELIMINAR ----------
def opcion_eliminar():
    """Opción 6: elimina un estudiante después de pedir confirmación."""
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


# ---------- EXTRA · ESTADÍSTICAS ----------
def opcion_estadisticas():
    """Opción 7: muestra el resumen (total, ciudades y dominios de email)."""
    imprimir_titulo("ESTADÍSTICAS")
    datos = estadisticas()
    print(f"  Estudiantes registrados : {datos['total']}")
    print(f"  Ciudades distintas   : {len(datos['ciudades'])} -> {', '.join(datos['ciudades'])}")
    print(f"  Dominios de email    : {', '.join(datos['dominios'])}")
    pausa()


# ---------- MATERIAS Y NOTAS ----------
def opcion_inscribir_materia():
    """Opción 8: inscribe a un estudiante en una materia."""
    imprimir_titulo("INSCRIBIR EN MATERIA")
    id_estudiante = _pedir_estudiante()
    if id_estudiante is not None:
        exito, mensaje = inscribir_materia(id_estudiante, input("Materia: "))
        (imprimir_exito if exito else imprimir_error)(mensaje)   # elige la función según el resultado
    pausa()


def opcion_agregar_nota():
    """Opción 9: agrega una nota (0 a 20) a una materia del estudiante."""
    imprimir_titulo("AGREGAR NOTA")
    id_estudiante = _pedir_estudiante()
    if id_estudiante is not None:
        materia = input("Materia: ")
        nota = input("Nota (0-20): ")
        exito, mensaje = agregar_nota(id_estudiante, materia, nota)
        (imprimir_exito if exito else imprimir_error)(mensaje)
    pausa()


def opcion_ver_promedio():
    """Opción 10: muestra el promedio general de un estudiante."""
    imprimir_titulo("VER PROMEDIO")
    id_estudiante = _pedir_estudiante()
    if id_estudiante is not None:
        exito, resultado = obtener_promedio(id_estudiante)
        if exito:
            imprimir_exito(f"Promedio: {resultado}")
        else:
            imprimir_error(resultado)
    pausa()


def opcion_materias_en_comun():
    """Opción 11: muestra las materias que comparten dos estudiantes (intersección de conjuntos)."""
    imprimir_titulo("MATERIAS EN COMÚN")
    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los ids deben ser números enteros")
        return pausa()
    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    elif not resultado:
        imprimir_info("No comparten ninguna materia.")
    else:
        imprimir_exito(f"Materias en común: {', '.join(resultado)}")
    pausa()


def opcion_materias_ofertadas():
    """Opción 12: lista todas las materias inscritas por algún estudiante, sin repetir."""
    imprimir_titulo("MATERIAS OFERTADAS")
    materias = materias_ofertadas()
    if not materias:
        imprimir_info("Todavía no hay materias inscritas.")
    else:
        imprimir_info(f"{len(materias)} materia(s): {', '.join(sorted(materias))}")
    pausa()


def salir():
    """Opción 0: despide al usuario y devuelve 'salir' para que main() termine el bucle."""
    imprimir_info("¡Hasta luego! 👋")
    return "salir"


# DICCIONARIO de opciones: tecla -> (texto del menú, función que se ejecuta)
OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Estadísticas", opcion_estadisticas),
    "8": ("Inscribir en materia", opcion_inscribir_materia),
    "9": ("Agregar nota", opcion_agregar_nota),
    "10": ("Ver promedio", opcion_ver_promedio),
    "11": ("Materias en común", opcion_materias_en_comun),
    "12": ("Materias ofertadas", opcion_materias_ofertadas),
    "0": ("Salir", salir),
}


def mostrar_menu():
    """Dibuja el menú a partir del diccionario OPCIONES (se actualiza solo)."""
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    # _funcion se ignora al imprimir: solo se necesita el texto
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    """Ciclo principal: muestra el menú, lee la opción y ejecuta su función hasta que se elija salir."""
    while True:
        mostrar_menu()
        # strip() quita espacios accidentales antes y después
        tecla = input("Seleccione una opción: ").strip()

        # 'in' sobre un diccionario comprueba si la tecla existe como clave
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = OPCIONES[tecla]
        if funcion() == "salir":      # ejecuta la función; si devuelve "salir", rompe el bucle
            break


# Solo se ejecuta si el archivo se corre directamente (python main.py), no al importarlo
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:       # Ctrl+C
        print("\nPrograma interrumpido por el usuario.")
