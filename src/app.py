"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Episode, Location, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)    

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# --- Routes USER ---
@app.route('/user', methods=['GET'])
def get_users():
    usersDb = User.query.all()
    user_list = list(map(lambda user: user.serialize(), usersDb))
    response_body = {
        "success": True,
        "results": user_list,
    }
    return jsonify(response_body), 200

@app.route('/user', methods=['POST'])
def create_user():
    body = json.loads(request.data)
    newUser = User(email = body["email"], password = body["password"])
    db.session.add(newUser)
    db.session.commit()
    response_body = {        
        "success": True,
        "message": ("User created", newUser.serialize())
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_single(user_id):
    userDb = User.query.get(user_id)
    return jsonify(userDb.serialize()), 200

# --- ROUTES FAVORITES ---
@app.route('/user/favorite', methods=['GET'])
def get_favorite():
    favoritesDb = Favorite.query.all()
    favorites_list = list(map(lambda favorite: favorite.serialize(), favoritesDb))
    response_body = {
        "msg": ("Favorite items:", favorites_list)
    }
    return jsonify(response_body), 200
    
@app.route('/user/favorite/character/<int:character_id>', methods=['POST'])
def add_FavoriteCharacter(character_id):
    request_body_user = request.get_json()
    print(request_body_user)
    favoriteCharacter = Favorite(user_id=request_body_user["user_id"], character_id=character_id)
    db.session.add(favoriteCharacter)
    db.session.commit()
    response_body = {
        "msg": ("Character added:", favoriteCharacter.serialize())
    }
    return jsonify(response_body), 200

@app.route('/user/favorite/location/<int:location_id>', methods=['POST'])
def add_FavoriteLocation(location_id):
    request_body_user = request.get_json()
    print(request_body_user)
    favoriteLocation = Favorite(user_id=request_body_user["user_id"], location_id=location_id)
    db.session.add(favoriteLocation)
    db.session.commit()
    response_body = {
        "msg": ("Location added:", favoriteLocation.serialize())
    }
    return jsonify(response_body), 200

@app.route('/user/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_FavoriteCharacter(character_id):
    favCharacter = Favorite.query.filter_by(character_id = character_id).first()
    db.session.delete(favCharacter)
    db.session.commit()
    return "Succesfully deleted", 200

@app.route('/user/favorite/location/<int:location_id>', methods=['DELETE'])
def delete_FavoriteLocation(location_id):
    favLocation = Favorite.query.filter_by(location_id = location_id).first()
    db.session.delete(favLocation)
    db.session.commit()
    return "Succesfully deleted", 200
    
# --- Routes CHARACTER ---
@app.route('/character', methods=['GET'])
def get_characters():
    characterDb = Character.query.all()
    character_list = list(map(lambda character: character.serialize(), characterDb))
    response_body = {        
        "success": True,
        "results": character_list
    }
    return jsonify(response_body), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_id(character_id):
    characterId = Character.query.get(character_id)    
    return jsonify(characterId.serialize()), 200

# # --- Routes LOCATION ---
@app.route('/location', methods=['GET'])
def get_locations():
    locationDb = Location.query.all()
    location_list = list(map(lambda location: location.serialize(), locationDb))
    response_body = {        
        "success": True,
        "results": location_list
    }
    return jsonify(response_body), 200

@app.route('/location/<int:location_id>', methods=['GET'])
def get_location_id(location_id):
    locationId = Location.query.get(location_id)    
    return jsonify(locationId.serialize()), 200


# # --- Routes EPISODE ---
@app.route('/episode', methods=['GET'])
def get_episodes():
    episodeDb = Episode.query.all()
    episode_list = list(map(lambda episode: episode.serialize(), episodeDb))
    response_body = {        
        "success": True,
        "results": episode_list
    }
    return jsonify(response_body), 200

@app.route('/episode/<int:episode_id>', methods=['GET'])
def get_episode_id(episode_id):
    episodeId = Episode.query.get(episode_id)    
    return jsonify(episodeId.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
