import os
import sqlite3

try:
    """Verificar la existencia de la base de datos en el repositorio"""
    if os.path.exists("sql_db/chinook.db"):
        print("correcto")
    else:
        print("fail")

except FileNotFoundError:
    print("archivo no encontrado")
