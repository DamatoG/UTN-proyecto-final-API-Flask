from flask import Flask, json, jsonify, request
from http import HTTPStatus
import json
from flask_cors import CORS, cross_origin
from flask_jwt import JWT, jwt_required

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from tiene_comentario_ajeno import tiene_comentarios_ajenos



#jsonfy convierte cadenas de caracteres en formato json para poder enviarlo al cliente.

app = Flask(__name__)
# Configurar la extension Flask-JWT-Extended 
app.config["JWT_SECRET_KEY"] = "123456789" 
jwt = JWTManager(app)


#CORS
cors = CORS(app, resources={ r'*': { 'origins':'*'}})
#CORS(app)


data = open('data.json')
db=json.load(data)



@app.route('/', methods=["GET"])
def home():
    return ("Bienvenido a la api de peliculas")




#LOGIN
@app.route("/login", methods=["POST"])
def login():
    #recibo la data del usuario
    user = request.get_json()
    username = user["username"]
    password = user["password"]

    #recorro el json para saber si existe un usuario con username/password ingresado
    for us in db['users']:
        if username == us['username']  and password == us['password']:
            #Si existe creo el token y lo envio como respuesta
            access_token = create_access_token(identity=username)
            return jsonify({"token": access_token, "user":username}), HTTPStatus.OK
            #Si no existe retorno error
        else:
            return jsonify({'msg': 'Bad username or password'}), HTTPStatus.BAD_REQUEST


#MODULO PELICULAS
#endpoint retorna todas las peliculas -- GET

@app.route("/movies", methods=["GET"])  
def movies():
    return jsonify(db["movies"]), HTTPStatus.OK

#endpoint retorna un pelicula segun id
@app.route("/movie/<id>", methods=["GET"])
def movie(id):
    id = int(id)
    existe = False
    while not existe:
        for movie in db["movies"]:
            if movie["id_movie"] == id:
                existe = True
                return jsonify(movie), HTTPStatus.OK

    if existe: return jsonify({}), HTTPStatus.NOT_FOUND

#endpoint retorna pelicula by_director
@app.route("/movie_by_director/<id_director>", methods=["GET"])
def movie_by_director(id_director):
    id_director = int(id_director)
    directores = [ d['director_id'] for d in db['directores']]
    print (directores)
    if id_director not in directores:
        return jsonify({'msj':'Director inexistente'}), HTTPStatus.NOT_FOUND
    else:
        movies_by_director = [ m for m in db['movies'] if m['director'] == id_director]
        return jsonify(movies_by_director), HTTPStatus.OK


#endpoint crea una pelicula -- POST
@app.route("/movie", methods = ["POST"])
#@jwt_required()
def create_new_movie():
    data_client = request.get_json()

    if "name_movie" and "fecha_estreno" and "director" and "genero" and "sinopsis" and "url_img" in data_client:
        titulos = [movie["name_movie"] for movie in db["movies"]]
    
        if data_client["name_movie"] in titulos:
            return ("Ya existe una pelicula con este nombre en nuestra base de datos"), HTTPStatus.BAD_REQUEST
        else:
            new_movie_id = max([movie["id_movie"] for movie in db["movies"]]) + 1
            data_client["id_movie"] = new_movie_id
            db["movies"].append(data_client)
            return jsonify(data_client), HTTPStatus.OK
    


#endopoint modifica una pelucula -- PUT
@app.route("/movie/<id_movie>", methods = ["PUT"])
@jwt_required()
def modificar_pelicula(id_movie):
    id_movie = int(id_movie)
    data_client = request.get_json()

    ids_movies = [ m['id_movie'] for m in db['movies']]
    if id_movie not in ids_movies:
        return jsonify({'msj':'Pelicula no encontrada'}), HTTPStatus.NOT_FOUND
    elif 'name_movie' and "fecha_estreno" and "director" and "sinopsis" and "url_img" and "genero" in data_client:
        for i in range(len(db['movies'])):
            if db["movies"][i]['id_movie'] == id_movie:
                data_client['id_movie'] = db["movies"][i]['id_movie']
                data_client['id_user'] = db["movies"][i]['id_user']
                db["movies"][i] = data_client
                break
        return jsonify({'msj':'Pelicula modificada con exito'}), HTTPStatus.OK
    else:
        return jsonify({'msj':'Informacion insuficiente'}), HTTPStatus.BAD_REQUEST



#endpoint elimina una pelicula
#DELETE
@app.route("/movie/<id_user>/<id_movie>", methods = ["DELETE"])
@jwt_required()
def eliminar_pelicula(id_user, id_movie):
    id_user = int(id_user)
    elimino = False
    for movie in db['movies']:
        if movie['id_movie'] == int(id_movie) and movie['id_user'] == int(id_user):
            if tiene_comentarios_ajenos(movie, db['comentarios'], id_user) != True:
                db['movies'] = [movie for movie in db['movies'] if movie['id_movie'] != int(id_movie)]
                elimino = True
            else:
                return jsonify({'msj': 'No es posible eliminar la pelicula, tiene comentarios de otros usuarios'})

    if elimino:
        return jsonify({'msj':'Pelicula eliminada con exito'}), HTTPStatus.OK
    else:
        return jsonify({}), HTTPStatus.BAD_REQUEST


#endpoint crea un usuario nuevo
@app.route("/register", methods = ["POST"])
def register():
    data_client = request.get_json()

    for user in db["users"]:
        if data_client["name_user"] == user["name_user"]:
            return jsonify({'msj':'Ya existe un usuario registrado con ese nombre en nuestra base de datos'}), HTTPStatus.OK
    
    new_user_id = max([user["id_user"] for user in db["users"]]) + 1 
    data_client["id_users"] = new_user_id
    db["users"].append(data_client)
    return jsonify({}), HTTPStatus.OK



#MODULO DIRECTORES
#Endpoint retorna lista de directores
@app.route("/directores", methods = ['GET'])
def directores():
    return jsonify(db["directores"]), HTTPStatus.OK


#MODULO GENERO
#Endpoint retorna lista de genero
@app.route("/genero", methods = ['GET'])
def generos():
    return jsonify(db["generos"]), HTTPStatus.OK



#MODULO COMENTARIOS
#endpoint retorna todos los comentarios de una pelicula segun idMovie
#GET
@app.route("/comentarios/<id_movie>", methods = ['GET'])
def comentarios_movie(id_movie):
    ids_movies = [ m['id_movie'] for m in db['movies']]
    if int(id_movie) not in ids_movies:
        return jsonify({'msj':'Pelicula no encontrada'}), HTTPStatus.NOT_FOUND
    else:
        comentarios_movie = [c for c in db['comentarios'] if c['id_movie'] == int(id_movie)]
        print(comentarios_movie)
        return jsonify(comentarios_movie), HTTPStatus.OK


#endpoint crea nuevo comentario en una pelicula
#POST
@app.route('/movie/<id_movie>/comentario', methods = ['POST'])
#@jwt_required()
def crear_comentario(id_movie):
    id_movie = int(id_movie)
    data_client = request.get_json()
    ids_movies = [m['id_movie'] for m in db['movies']]

    #Valido data y que el id_movie exista
    if ('body' in data_client and 'id_user' in data_client):
        if id_movie in ids_movies:
            new_comentario_id = max([c["id_comentario"] for c in db["comentarios"]]) + 1 
            for m in db['movies']:
                if m['id_movie'] == id_movie:
                    m['id_comentarios'].append(new_comentario_id)
            data_client['id_comentario'] = new_comentario_id
            data_client['id_movie'] = id_movie
            db['comentarios'].append(data_client)

            return jsonify(data_client), HTTPStatus.OK
        else:
            return jsonify({'msj':'Pelicula inexistente'}), HTTPStatus.NO_CONTENT
    else:
        return jsonify({}), HTTPStatus.BAD_REQUEST





if __name__ == '__main__':
    app.run(debug = True, port = 5000)