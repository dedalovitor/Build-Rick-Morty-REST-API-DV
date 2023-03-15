from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    alive = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    species = db.Column(db.String(250),unique=False, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "gender": self.gender,
            "alive": self.alive,
            "species": self.species
        }

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(120), unique=True, nullable=False)
    location_type = db.Column(db.String(250), unique=False, nullable=False)
    dimension = db.Column(db.String(250), unique=False, nullable=False)

    def serialize(self):
        location = None
        character = None
        if self.location is not None:
            location=self.location.serialize()
        if self.character is not None:
            character = self.character.serialize()
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "location_id": self.location_id,
        }  

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episode_name = db.Column(db.String(120), unique=True, nullable=False)
    air_date = db.Column(db.String(250), unique=False, nullable=False)
    episode = db.Column(db.String(120), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "episode_name": self.episode_name,
            "air_date": self.air_date,
            "episode": self.episode,
        }  

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))  
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))   
    user = db.relationship("User", foreign_keys=[user_id])
    character = db.relationship('Character')
    location = db.relationship('Location')
    episode = db.relationship('Episode')




