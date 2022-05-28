#Esta funcion recibe una pelicula y un id_user y verifica si existe un comentario con id_user distinto al 

pel = {
            "id_movie":1,
            "id_user":0,
            "name_movie":"avengers endgame",
            "fecha_estreno":"10/12/2029",
            "director":"stan lee",
            "genero":"",
            "sinopsis":"Después de los eventos devastadores de 'Avengers: Infinity War', el universo está en ruinas debido a las acciones de Thanos, el Titán Loco. Con la ayuda de los aliados que quedaron, los Vengadores deberán reunirse una vez más para intentar detenerlo y restaurar el orden en el universo de una vez por todas.",
            "url_img":"https://cdn.pixabay.com/photo/2020/11/28/03/19/iron-man-5783522_960_720.png",
            "id_comentarios":[1,2,3]
            
        }

us = 0

com = [
        {
        "id_comentario":1,
        "id_movie":1,
        "id_user":0,
        "cuerpo":"Hola que tal"
        },
        {
        "id_comentario":2,
        "id_movie":1,
        "id_user":0,
        "cuerpo":"Hola que tal"
        },
        {
        "id_comentario":3,
        "id_movie":1,
        "id_user":0,
        "cuerpo":"Hola que tal"
        }]


def tiene_comentarios_ajenos(movie, comentarios, id_user):
    comentarios_otro_user = [c['id_comentario'] for c in comentarios if c['id_user'] != id_user]
    
    encontro = False
    for c in comentarios_otro_user:
        if c in movie['id_comentarios']:
            encontro = True
            break
    return encontro