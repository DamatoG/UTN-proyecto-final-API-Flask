#Esta funcion recibe una pelicula y un id_user y verifica si existe un comentario con id_user distinto al 

def tiene_comentarios_ajenos(movie, comentarios, id_user):
    comentarios_otro_user = [c['id_comentario'] for c in comentarios if c['id_user'] != id_user]
    
    encontro = False
    for c in comentarios_otro_user:
        if c in movie['id_comentarios']:
            encontro = True
            break
    return encontro