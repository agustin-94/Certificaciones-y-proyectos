"""
_rutas.py

Helper compartido: calcula la carpeta raíz del proyecto a partir de la
ubicación de este archivo (no del directorio desde el que se ejecuta
python), para que los scripts funcionen sin importar desde dónde los
corras (VS Code, terminal, doble clic, etc.).

Uso en los demás scripts:
    from _rutas import ruta

    ruta("assets/muestra.jpg")   -> ruta absoluta a esa carpeta/archivo,
                                     calculada siempre desde la raíz del
                                     proyecto (donde están las carpetas
                                     assets/, output/, modelos/, etc.)
"""
import os

DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
DIR_PROYECTO = os.path.dirname(DIR_SCRIPT)  # un nivel arriba de src/


def ruta(*partes):
    return os.path.join(DIR_PROYECTO, *partes)
