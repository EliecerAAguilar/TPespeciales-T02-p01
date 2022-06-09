import os
import sqlite3
import pandas as pd

def cleaning_list(lista):
    """busca los nombres alternativos de los subgenros y lo añade como un nuevo elemento
    en la sublista que contiene los subgeneros.
    ademas elimina la parte innecesaria del nombre del subgenero
    """
    for x in range(len(lista)):
        for y in range(len(lista[x])):
            search = lista[x][y].find("(")
            if search != (-1):
                temp_str = lista[x][y][lista[x][y].find(':')+2:-1]
                #print("found ", temp_str,)
                temp_str2 = lista[x][y][0:search]
                #print("y", lista[x][y], "temp2 ", temp_str2)
                lista[x][y] = temp_str2
                lista[x].append(temp_str)
    #print(lista)
    return lista

def main():
    try:
        """Verificar la existencia de la base de datos en el repositorio"""
        if os.path.exists("sql_db/chinook.db"):
            pass
            # print("correcto")
        else:
            raise FileNotFoundError
        """cargar los datos desde el archivo .txt"""
        subgenres_txt = pd.read_csv("resources/subgenres.txt", header=None)
        subgen_list = subgenres_txt.values.tolist()

        subgen_list = cleaning_list(subgen_list)
        print(subgen_list)

        """conexion a la base de datos"""
        chinook_db = sqlite3.connect("sql_db/chinook.db")
        cursor = chinook_db.cursor()

        """query"""
        # cursor.execute("""CREATE TABLE IF NOT EXISTS subgenres (
        #                 subgenreid INTEGER PRIMARY KEY NOT NULL,subgenrename VARCHAR(150) NOT NULL,
        #                 subgenrealtname VARCHAR(150), FOREIGN KEY(genreid) REFERENCES genres(genreid)""")

        # """retornar los valores consultados"""
        # first = cursor.fetchone()
        #
        # """imprimir los valores seleccionados"""
        # print("{0} {1}".format(first[0], first[1]))

        """cerrar conexion a la base de datos"""
        chinook_db.close()

    except FileNotFoundError:
        print("archivo no encontrado")
    except sqlite3.Error as sql_e:
        print("SQLite3 Error\n", sql_e)
    except sqlite3.OperationalError as sql_op_e:
        print("Operational Error\n", sql_op_e)


if __name__ == "__main__":
    main()