"""PERSISTENCIA: única parte del programa que lee y escribe el archivo JSON.
Recibe y devuelve listas de diccionarios; no sabe qué es un Estudiante."""

import json
import os


class GestorJSON:
    """Lee y guarda una lista de diccionarios en un archivo JSON."""

    def __init__(self, ruta):
        # Guarda la ruta del archivo y crea la carpeta (data/) si no existe
        self.ruta = ruta
        carpeta = os.path.dirname(ruta)

        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def leer(self):
        """Devuelve SIEMPRE una lista: vacía si el archivo no existe o está dañado."""
        if not os.path.exists(self.ruta):
            return []
        try:
            # with cierra el archivo automáticamente; utf-8 para tildes y ñ
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)    # JSON -> lista de diccionarios

            return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            # Se capturan errores concretos (JSON mal formado o archivo ilegible)
            return []

    def guardar(self, datos):
        """Escribe la lista en el archivo. Devuelve True si salió bien, False si falló."""
        try:
            # modo "w": reemplaza todo el contenido del archivo
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            return True
        except (TypeError, OSError):
            # TypeError aparece si se intenta guardar un set: JSON no lo conoce
            return False
