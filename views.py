"""CONTROLADOR: reglas del negocio (validar, buscar, decidir y guardar).
Nunca usa print() ni input(). Cada operación devuelve una tupla (exito, mensaje)
o datos, y main.py decide cómo mostrarlos."""

import os
from models import CAMPOS_ESTUDIANTE, Estudiantes
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

# Un solo gestor para todo el módulo. Ruta absoluta: funciona desde cualquier carpeta.
gestor = GestorJSON(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "estudiantes.json"))

# TUPLAS de configuración: fijas, nadie las modifica mientras corre el programa
CAMPO_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")


# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """CONJUNTO con los emails ya usados (en minúscula). Sirve para detectar duplicados.
    excepto_id permite ignorar al propio estudiante cuando se edita."""
    return {
        estudiante["email"].lower()
        for estudiante in gestor.leer()
        if estudiante["id"] != excepto_id
    }


def carnets_registrados(excepto_id=None):
    """CONJUNTO con los carnets ya usados (en minúscula). Evita carnets repetidos."""
    return {
        estudiante["carnet"].lower()
        for estudiante in gestor.leer()
        if estudiante["id"] != excepto_id
    }


def siguiente_id():
    """Calcula el próximo id: el mayor existente + 1 (o 1 si no hay estudiantes)."""
    ids = [estudiante["id"] for estudiante in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    """Valida los datos y guarda un nuevo estudiante. Devuelve (exito, mensaje).
    datos: diccionario con las claves de CAMPOS_ESTUDIANTE."""
    try:
        # 1) Normaliza: diccionario con todos los campos y sin espacios sobrantes
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        # 2) Revisa que los campos obligatorios no estén vacíos
        faltantes = [campo for campo in CAMPO_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # 3) Formato del email
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no es válido."

        # 4) Email duplicado: búsqueda instantánea dentro del CONJUNTO
        if valores["email"].lower() in emails_registrados():
            return False, "El email ya está registrado."

        # 5) Carnet duplicado: mismo método con otro conjunto
        if valores["carnet"].lower() in carnets_registrados():
            return False, "El carnet ya está registrado."

        # 6) Crea el objeto del modelo; ** convierte el diccionario en argumentos con nombre
        estudiante = Estudiantes(siguiente_id(), **valores)

        # 7) Agrega a la LISTA de registros y guarda todo en el archivo
        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        if not gestor.guardar(registros):
            return False, "Error al guardar el estudiante."

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} creado exitosamente."

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """Devuelve una LISTA de objetos Estudiantes (uno por cada registro del archivo)."""
    return [Estudiantes.desde_diccionario(estudiante) for estudiante in gestor.leer()]


def obtener_por_id(id_estudiante):
    """Busca un estudiante por id. Devuelve el objeto o None si no existe."""
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(criterio):
    """Búsqueda lineal: devuelve los estudiantes que contengan el texto en
    nombre, apellido, email, teléfono o ciudad (sin importar mayúsculas)."""
    criterio = criterio.strip().lower()
    if not criterio:
        return []

    encontrados = []
    for estudiante in gestor.leer():
        for campo in CAMPOS_BUSCABLES:          # recorre la TUPLA de campos
            if criterio in str(estudiante.get(campo, "")).lower():
                encontrados.append(Estudiantes.desde_diccionario(estudiante))
                break                            # ya coincidió: pasa al siguiente estudiante
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    """Modifica solo los campos recibidos en el diccionario cambios. Devuelve (exito, mensaje)."""
    try:
        # DIFERENCIA DE CONJUNTOS: detecta claves que no existen en el modelo
        desconocido = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocido:
            return False, f"Campos no validos: {', '.join(desconocido)}"

        if not cambios:
            return False, "No se proporcionaron cambios."

        # El email se valida igual que al crear (formato y duplicado en otros estudiantes)
        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, f"El email '{cambios['email']}' no es válido."
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "El email ya lo tiene otro estudiante."

        # El carnet tampoco puede repetirse
        if "carnet" in cambios and cambios["carnet"].strip().lower() in carnets_registrados(excepto_id=id_estudiante):
            return False, "El carnet ya lo tiene otro estudiante."

        # Busca la posición del registro dentro de la lista (enumerate da índice y valor)
        registros = gestor.leer()
        posicion = None
        for indice, reg in enumerate(registros):
            if reg["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No se encontró estudiante con ID {id_estudiante}."

        # update() reemplaza solo las claves recibidas y conserva las demás
        registros[posicion].update({k: str(c).strip() for k, c in cambios.items()})
        if not gestor.guardar(registros):
            return False, "Error al guardar los cambios."
        return True, f"Estudiante con ID {id_estudiante} actualizado exitosamente."

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    """Elimina un estudiante por id. Devuelve (exito, mensaje)."""
    registros = gestor.leer()
    # Construye una LISTA NUEVA sin ese registro: nunca se borra mientras se recorre
    quedan = [r for r in registros if r["id"] != id_estudiante]
    if len(quedan) == len(registros):          # si el tamaño no cambió, no existía
        return False, f"No se encontró estudiante con ID {id_estudiante}."
    gestor.guardar(quedan)
    return True, f"Estudiante con ID {id_estudiante} eliminado exitosamente."


# ===================== EXTRA: estadísticas =====================

def estadisticas():
    """Devuelve un DICCIONARIO resumen: total, ciudades distintas y dominios de email."""
    registros = gestor.leer()
    # Los CONJUNTOS eliminan ciudades y dominios repetidos automáticamente
    ciudades = {r.get("ciudad", "").title() for r in registros if r.get("ciudad")}
    dominios = {r.get("email", "").split("@")[1].lower() for r in registros if "@" in r.get("email", "")}

    return {
        "total": len(registros),
        "ciudades": sorted(ciudades),     # sorted convierte el set en lista ordenada
        "dominios": sorted(dominios),
    }


# ===================== MATERIAS Y NOTAS =====================

def inscribir_materia(id_estudiante, materia):
    """Inscribe al estudiante en una materia. Devuelve (exito, mensaje)."""
    materia = materia.strip().title()          # "matematica" y "Matematica" son la misma
    if not materia:
        return False, "La materia no puede estar vacía."
    registros = gestor.leer()
    for reg in registros:
        if reg["id"] == id_estudiante:
            materias = set(reg.get("materias", []))   # lista -> set para no duplicar
            materias.add(materia)
            reg["materias"] = sorted(materias)         # set -> lista ordenada para JSON
            if not gestor.guardar(registros):
                return False, "Error al guardar."
            return True, f"Inscrito en {materia}."
    return False, f"No se encontró estudiante con ID {id_estudiante}."


def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota (0 a 20) a una materia del estudiante. Devuelve (exito, mensaje)."""
    materia = materia.strip().title()
    if not materia:
        return False, "La materia no puede estar vacía."
    try:
        nota = float(nota)                     # convierte el texto a número
    except ValueError:
        return False, "La nota debe ser un número."
    if not 0 <= nota <= 20:                    # validación de rango
        return False, "La nota debe estar entre 0 y 20."
    registros = gestor.leer()
    for reg in registros:
        if reg["id"] == id_estudiante:
            # setdefault crea el diccionario/lista la primera vez; append agrega la nota
            reg.setdefault("notas", {}).setdefault(materia, []).append(nota)
            materias = set(reg.get("materias", []))
            materias.add(materia)              # si tiene nota, queda inscrito en la materia
            reg["materias"] = sorted(materias)
            if not gestor.guardar(registros):
                return False, "Error al guardar."
            return True, f"Nota {nota} agregada en {materia}."
    return False, f"No se encontró estudiante con ID {id_estudiante}."


def obtener_promedio(id_estudiante):
    """Devuelve (True, promedio) o (False, mensaje) si el estudiante no existe."""
    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        return False, f"No se encontró estudiante con ID {id_estudiante}."
    return True, estudiante.obtener_promedio()


def materias_ofertadas():
    """Devuelve un CONJUNTO con las materias inscritas por todos los estudiantes, sin repetir."""
    ofertadas = set()
    for estudiante in obtener_todos():
        ofertadas |= estudiante.materias       # |= es la UNIÓN de conjuntos
    return ofertadas


def estudiantes_en_comun(id_a, id_b):
    """Materias que comparten dos estudiantes. Devuelve (True, lista) o (False, mensaje)."""
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)
    if not estudiante_a or not estudiante_b:
        return False, "Alguno de los dos ids no existe."
    # INTERSECCIÓN de conjuntos (la hace el método del modelo)
    return True, sorted(estudiante_a.materias_en_comun(estudiante_b))
