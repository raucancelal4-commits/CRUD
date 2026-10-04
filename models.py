"""MODELO: define qué es un Estudiante (sus datos y lo que puede hacer).
No pide datos, no imprime y no abre archivos: solo representa al estudiante."""

import json

# TUPLA: campos que se piden por teclado. Es fija, por eso no es lista.
# La usan main.py (formularios) y views.py (validaciones).
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet", "telefono", "ciudad")


class Estudiantes:
    """Representa a un estudiante con sus notas y materias."""

    def __init__(self, id_estudiante, nombre, apellido, email, carnet,
                 telefono="", ciudad="", notas=None, materias=None):
        # Constructor: se ejecuta al crear un estudiante y guarda sus datos.
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet
        self.telefono = telefono
        self.ciudad = ciudad
        # DICCIONARIO DE LISTAS: {"Matematica": [18, 19], "Ingles": [17]}
        self.notas = notas if notas else {}
        # CONJUNTO: materias inscritas, sin repetidos
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        """Devuelve 'Nombre Apellido' en un solo texto."""
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        """Agrega la materia al conjunto (add no duplica si ya estaba)."""
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        """Inscribe la materia y agrega la nota a la lista de esa materia."""
        self.inscribir_materia(materia)
        # setdefault crea la lista vacía la primera vez que aparece la materia
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        """Promedio de TODAS las notas de todas las materias (0 si no hay notas)."""
        todas = []
        for lista_notas in self.notas.values():
            todas.extend(lista_notas)      # junta todas las notas en una sola lista
        if not todas:
            return 0
        return round(sum(todas) / len(todas), 2)

    def materias_en_comun(self, otro_estudiante):
        """INTERSECCIÓN de conjuntos (&): materias que comparten los dos."""
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        """Objeto -> diccionario, listo para guardarse en JSON."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "notas": self.notas,
            # JSON no sabe guardar un set: lo convertimos a lista ordenada
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Diccionario -> objeto. Método de la CLASE (recibe cls, no self).
        Se usa así: Estudiantes.desde_diccionario({...})"""
        return cls(
            datos["id"], datos["nombre"], datos["apellido"], datos["email"],
            datos["carnet"],
            telefono=datos.get("telefono", ""),   # .get evita KeyError si falta
            ciudad=datos.get("ciudad", ""),
            notas=datos.get("notas", {}),
            materias=datos.get("materias", []),   # el __init__ la vuelve a convertir en set
        )

    def __str__(self):
        """Texto que se muestra al hacer print(estudiante)."""
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"
