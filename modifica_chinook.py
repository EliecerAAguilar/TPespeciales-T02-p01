import os
import sqlite3
import pandas as pd
import traceback as t


def cleaning_list(lista):
    """ busca los nombres alternativos de los subgenros y lo añade como un nuevo elemento
        en la sublista que contiene los subgeneros.
        ademas elimina la parte innecesaria del nombre del subgenero
    """
    for x in range(len(lista)):
        for y in range(len(lista[x])):
            search = lista[x][y].find("(")
            if search != (-1):
                temp_str = lista[x][y][lista[x][y].find(':')+2:-1]
                temp_str2 = lista[x][y][0:search]
                lista[x][y] = temp_str2
                lista[x].append(temp_str)
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

        """conexion a la base de datos"""
        chinook_db = sqlite3.connect("sql_db/chinook.db")
        cursor = chinook_db.cursor()
        cursor.execute("""BEGIN""")
        """query CREAR  la tabla de subgeneros en la db"""
        cursor.execute("""CREATE TABLE IF NOT EXISTS subgenres (
                        subgenreid INTEGER PRIMARY KEY NOT NULL,
                        subgenrename VARCHAR(150) NOT NULL,
                        subgenrealtname VARCHAR(150),
                        genreid INTEGER NOT NULL, 
                        FOREIGN KEY(genreid) REFERENCES genres(GenreId))""")

        """insertando los valores solicitados dependiendo de si tiene o no un nombre alternativo"""
        for x in range(len(subgen_list)):
            if len(subgen_list[x]) < 2:
                cursor.execute("""INSERT OR REPLACE INTO subgenres(subgenrename,subgenrealtname,genreid) 
                                VALUES(
                                        :subgenrename,
                                        NULL,
                                        (SELECT GenreId FROM genres WHERE Name LIKE '%punk%')
                                       )""",
                               {
                                   'subgenrename': subgen_list[x][0]
                               }
                               )
            else:
                cursor.execute("""INSERT OR REPLACE INTO subgenres(subgenrename,subgenrealtname,genreid) 
                            VALUES(
                                    :subgenrename,
                                    :subgenrealtname,
                                    (SELECT GenreId FROM genres WHERE Name LIKE '%punk%')
                            )""",
                            {
                                'subgenrename':subgen_list[x][0],
                                'subgenrealtname':subgen_list[x][1]
                            }
                            )

        """ejecutar el query"""
        chinook_db.commit()

        """agregar una nueva columna a la tabla tracks """
        cursor.execute("""ALTER TABLE tracks ADD subgenere VARCHAR(150)""")
        chinook_db.commit()

        """generar 5 nuevas canciones en la tablas tracks"""
        artist_name = "Joe Lally"
        cursor.execute("""INSERT INTO artists(Name)
                        VALUES(:Name)""",
                       {'Name': artist_name}
                       )
        cursor.execute("""SELECT last_insert_rowid()""")
        artist_id = cursor.fetchone()

        chinook_db.commit()

        album_title = "13 Songs"
        cursor.execute("""INSERT INTO albums(Title,ArtistId)
                        VALUES(:Title, :ArtistId)""",
                       {'Title' : album_title, 'ArtistId': artist_id[0]})
        cursor.execute("""SELECT last_insert_rowid()""")
        album_id = cursor.fetchone()
        chinook_db.commit()

        subgenre_name = "punk rock"
        cursor.execute("""INSERT INTO subgenres(subgenrename,subgenrealtname,genreid)
                                VALUES(:subgenrename,NULL,4)""",
                       {'subgenrename' : subgenre_name}
                       )

        cursor.execute("""SELECT last_insert_rowid()""")
        subgenre_id = cursor.fetchone()
        chinook_db.commit()

        """
            TIPOS DE MEDIA... Media_types table
            1,MPEG audio file
            2,Protected AAC audio file
            3,Protected MPEG-4 video file
            4,Purchased AAC audio file
            5,AAC audio file
        """

        """
            genres table
            id, Name
            4,Alternative & Punk
        """

        """https://music.apple.com/us/album/waiting-room/49249845?i=49249816"""
        data = [
                    ("Waiting Room", album_id[0], 1, 4, "Ted Niceley", 2530, 47000000, 5.99, subgenre_id[0]),
                    ("Bulldog Front", album_id[0], 1, 4, "Ted Niceley", 2530, 47000000, 5.99, subgenre_id[0]),
                    ("Bad Mouth", album_id[0], 1, 4, "Ted Niceley", 2350, 28000000, 5.99, subgenre_id[0]),
                    ("Burning", album_id[0], 1, 4, "Ted Niceley", 2390, 30000000, 5.99, subgenre_id[0]),
                    ("Give Me the Cure", album_id[0], 1, 4, "Ted Niceley", 2580, 47000000, 5.99, subgenre_id[0]),
                ]
        cursor.executemany("""INSERT INTO tracks(Name, AlbumId, MediaTypeId,GenreId,
                                                Composer,Milliseconds,Bytes,UnitPrice,subgenere)
                            VALUES(?, ?, ?,?,?,?,?,?,?)""", data)
        chinook_db.commit()
        """cerrar conexion a la base de datos"""
        chinook_db.close()

    except FileNotFoundError:
        print("archivo no encontrado")
        print(t.format_exc())
    except sqlite3.Error as sql_e:
        print("SQLite3 Error\n", sql_e)
        print(t.format_exc())
    except sqlite3.OperationalError as sql_op_e:
        print("Operational Error\n", sql_op_e)
        print(t.format_exc())
        cursor.execute("""ROLLBACK""")


if __name__ == "__main__":
    main()
