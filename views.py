import os
from models import CAMPOS_ESTUDIANTE, Estudiantes
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "estudiantes.json"))

CAMPO_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")


def emails_registrados(excepto_id=None):
    return {
        estudiante["email"].lower()
        for estudiante in gestor.leer()
        if estudiante["id"] != excepto_id
    }

def siguiente_id():
    ids =[estudiante["id"] for estudiante in gestor.leer()]
    return max(ids) + 1 if ids else 1

def crear_estudiante(datos):
    try:
        valores ={campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        faltantes = [campo for campo in CAMPO_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no es válido."

        if valores["email"].lower() in emails_registrados():
            return False, "El email ya está registrado."

        estudantes = Estudiantes(siguiente_id(), **valores)

        registro = gestor.leer()
        registro.append(estudantes.a_diccionario())
        if not gestor.guardar(registro):
            return False, "Error al guardar el estudiante."

        return True, f"Estudiante {estudantes.obtener_nombre_completo()} creado exitosamente."

    except Exception as error:
        return False, f"Error inesperado: {error}"


def obtener_todos():
    return [Estudiantes.desde_diccionario(estudiante) for estudiante in gestor.leer()]

def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


def buscar_estudiantes(criterio):
    criterio = criterio.strip().lower()
    if not criterio:
        return []

    econtrados = []
    for estudiante in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if criterio in str(estudiante.get(campo, "")).lower():
                econtrados.append(Estudiantes.desde_diccionario(estudiante))
                break
    return econtrados


def actualizar_estudiante(id_estudiante, cambios):
    try:
        desconocido = set(cambios)-set(CAMPOS_ESTUDIANTE)
        if desconocido:
            return False, f"Campos no validos: {', '.join(desconocido)}"

        if not cambios:
            return False, "No se proporcionaron cambios."

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, f"El email '{cambios['email']}' no es válido."
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "El email ya lo tiene otro estudiante."


        registros = gestor.leer()
        posicion = None
        for indice, reg in enumerate(registros):
            if reg["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No se encontró estudiante con ID {id_estudiante}."

        registros[posicion].update({k: str(c).strip() for k, c in cambios.items()})
        if not gestor.guardar(registros):
            return False, "Error al guardar los cambios."
        return True, f"Estudiante con ID {id_estudiante} actualizado exitosamente."

    except Exception as error:
        return False, f"Error inesperado: {error}"


def eliminar_estudiante(id_estudiante):
    registro = gestor.leer()
    quedan = [r for r in registro if r["id"] != id_estudiante]
    if len(quedan) == len(registro):
        return False, f"No se encontró estudiante con ID {id_estudiante}."
    gestor.guardar(quedan)
    return True, f"Estudiante con ID {id_estudiante} eliminado exitosamente."

def estadisticas():
    registor = gestor.leer()
    ciudades = {r.get("ciudad", "").title() for r in registor if r.get("ciudad")}
    dominios = {r.get("email", "").split("@")[1].lower() for r in registor if "@" in r.get("email", "")}

    return {
        "total": len(registor),
        "ciudades": sorted(ciudades),
        "dominios": sorted(dominios),
    }


def inscribir_materia(id_estudiante, materia):
    materia = materia.strip().title()
    if not materia:
        return False, "La materia no puede estar vacía."
    registros = gestor.leer()
    for reg in registros:
        if reg["id"] == id_estudiante:
            materias = set(reg.get("materias", []))
            materias.add(materia)
            reg["materias"] = sorted(materias)
            if not gestor.guardar(registros):
                return False, "Error al guardar."
            return True, f"Inscrito en {materia}."
    return False, f"No se encontró estudiante con ID {id_estudiante}."


def agregar_nota(id_estudiante, materia, nota):
    materia = materia.strip().title()
    if not materia:
        return False, "La materia no puede estar vacía."
    try:
        nota = float(nota)
    except ValueError:
        return False, "La nota debe ser un número."
    if not 0 <= nota <= 20:
        return False, "La nota debe estar entre 0 y 20."
    registros = gestor.leer()
    for reg in registros:
        if reg["id"] == id_estudiante:
            reg.setdefault("notas", {}).setdefault(materia, []).append(nota)
            materias = set(reg.get("materias", []))
            materias.add(materia)
            reg["materias"] = sorted(materias)
            if not gestor.guardar(registros):
                return False, "Error al guardar."
            return True, f"Nota {nota} agregada en {materia}."
    return False, f"No se encontró estudiante con ID {id_estudiante}."
