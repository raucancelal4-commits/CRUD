import sys

sys.stdout.reconfigure(encoding="utf-8")

from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, estadisticas,
    inscribir_materia, agregar_nota
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CIUDAD':<15}")
    print("-" * 85)
    for estudiante in estudiantes:
        print(f"{estudiante.id:<5}{estudiante.obtener_nombre_completo():<25}"
              f"{estudiante.email:<28}{estudiante.ciudad:<15}")
    print("-" * 85)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


# ---------- C · CREAR ----------
def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)     
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- R · LEER TODOS ----------
def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1 para crear el primero.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


# ---------- S · BUSCAR ----------
def opcion_buscar():
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
        for clave, valor in estudiante.a_diccionario().items():
            print(f"  {clave.capitalize():<12}: {valor}")
        print(f"  {'Promedio':<12}: {estudiante.obtener_promedio()}")
    pausa()


# ---------- U · ACTUALIZAR ----------
def opcion_actualizar():
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

    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(estudiante, campo)
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

    imprimir_titulo("ESTADÍSTICAS")
    datos = estadisticas()
    print(f"  Estudiantes registrados : {datos['total']}")
    print(f"  Ciudades distintas   : {len(datos['ciudades'])} -> {', '.join(datos['ciudades'])}")
    print(f"  Dominios de email    : {', '.join(datos['dominios'])}")
    pausa()


def _pedir_estudiante():
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return None
    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return None
    imprimir_info(f"Estudiante: {estudiante.obtener_nombre_completo()}")
    return id_estudiante


def opcion_inscribir_materia():
    imprimir_titulo("INSCRIBIR EN MATERIA")
    id_estudiante = _pedir_estudiante()
    if id_estudiante is not None:
        exito, mensaje = inscribir_materia(id_estudiante, input("Materia: "))
        (imprimir_exito if exito else imprimir_error)(mensaje)
    pausa()


def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")
    id_estudiante = _pedir_estudiante()
    if id_estudiante is not None:
        materia = input("Materia: ")
        nota = input("Nota (0-20): ")
        exito, mensaje = agregar_nota(id_estudiante, materia, nota)
        (imprimir_exito if exito else imprimir_error)(mensaje)
    pausa()


def salir():
    imprimir_info("¡Hasta luego! 👋")
    return "salir"



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
    "0": ("Salir", salir),
}


def mostrar_menu():
    
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():

    while True:
        mostrar_menu()
       
        tecla = input("Seleccione una opción: ").strip()

       
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

       
        _texto, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break

if __name__ == "__main__":
   
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")