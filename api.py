from flask import Flask, json, jsonify, request
from http import HTTPStatus
import json
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

#jsonfy convierte cadenas de caracteres en formato json para poder enviarlo al cliente.

app = Flask(__name__)
# Configurar la extension Flask-JWT-Extended 
app.config["JWT_SECRET_KEY"] = "123456789" 
jwt = JWTManager(app)


#CORS
cors = CORS(app, resources={ r'*': { 'origins':'*'}})
CORS(app)


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
    print (user)

    #recorro el json para saber si existe un usuario con username/password ingresado
    for us in db['users']:
        if username == us['username']  and password == us['password']:
            #Si existe creo el token y lo envio como respuesta
            access_token = create_access_token(identity=username)
            return jsonify({"token": access_token})
            #Si no existe retorno error
        else:
            return jsonify({"msg": "Bad username or password"}), HTTPStatus.BAD_REQUEST


#MODULO PELICULAS
#endpoint retorna todas las peliculas
@app.route("/movies", methods=["GET"])
def movies():
    return jsonify(db["movies"]), HTTPStatus.OK

#endpoint retorna un pelicula segun id
@app.route("/movie/<id>", methods=["GET"])
def movie(id):
    
    #el parametro id viene desde el cliente con el type = str. Hay que convertirlo a int
    id = int(id)
    for movie in db["movies"]:
        if movie["id_movie"] == id:
            return jsonify(movie), HTTPStatus.OK
        else:
            return jsonify({}), HTTPStatus.NOT_FOUND

#endpoint crea una pelicula
@app.route("/movie", methods = ["POST"])
def create_new_movie():
    data_client = request.get_json()
    for movie in db["movies"]:
        if data_client["name_movie"] == movie["name_movie"]:
            return ("Ya existe una pelicula con este nombre en nuestra base de datos"), HTTPStatus.OK
    
    new_movie_id = max([movie["id_movie"] for movie in db["movies"]]) + 1 
    data_client["id_movie"] = new_movie_id
    db["movies"].append(data_client)
    return jsonify(data_client), HTTPStatus.OK



#endopoint modifica una pelucula
#PUT
@app.route("/movie/<id_movie>", methods = ["PUT"])
def modificar_pelicula(id_movie):
    id_movie = int(id_movie)
    data_client = request.get_json()
    
    for movie in  db["movies"]:
        if movie["id_movie"] == id_movie:
            if data_client["name_movie"] != "":
                movie["name_movie"] = data_client["name_movie"]
            
            if data_client["fecha_estreno"] != "":
                movie["fecha_estreno"] = data_client["fecha_estreno"]

            if data_client["director"] != "":
                movie["director"] = data_client["director"]

            if data_client["sinopsis"] != "":
                movie["sinopsis"] = data_client["sinopsis"]
                
            if data_client["url_img"] != "":
                movie["url_img"] = data_client["url_img"]

            if data_client["genero"] != "":
                movie["genero"] = data_client["genero"]

            return jsonify(movie), HTTPStatus.OK
        
        else:
            return jsonify({}), HTTPStatus.NOT_MODIFIED

#endpoint elimina una pelicula
#DELETE
"""@app.route("/movie/<id_movie>", methods = ["DELETE"])
def modificar_pelicula(id_movie):
    id_movie = int(id_movie)
    data_client = request.get_json()
    """




#MODULO USUARIO
#endpoint devuelve todos los users
@app.route("/users", methods=["GET"])
def users():
    return jsonify(db["users"]), HTTPStatus.OK


#endpoint devuelve un usuario segun id
#GET
@app.route("/user/<id>", methods = ["GET"])
def user(id):
    #el parametro id viene desde el cliente con el type = str. Hay que convertirlo a int
    id = int(id)
    for user in db["users"]:
        if user["id_user"] == id:
            return jsonify(user)
    else:
        return jsonify({}), HTTPStatus.NOT_FOUND

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



#endpoint modifica los datos de un usuario 
#Put


#endpoint elimina un usuario
#DELETE



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

#endpoint retorna un unico comentario de una pelicula segun idMOvie y idComentario
#GET

#endpoint modifica un comentario de una pelicula segun idMovie y idComentario

#endpoint elimina un comentario de una pelicula, si solo si, el usuario que la elimina esta registrado



if __name__ == '__main__':
    app.run(debug = True, port = 5000)