from flask import Flask, request, session, jsonify
from flask_restful import Api, Resource
from models import db, bcrypt, User, Recipe
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

# --------------------- RESOURCES ---------------------

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        bio = data.get("bio")
        image_url = data.get("image_url")

        if not username or not password:
            return {"error": "Username and password required"}, 422

        try:
            user = User(username=username, bio=bio, image_url=image_url)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            return {"error": "Username must be unique"}, 422

        session['user_id'] = user.id
        return {
            "id": user.id,
            "username": user.username,
            "bio": user.bio,
            "image_url": user.image_url
        }, 201

class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401
        user = User.query.get(user_id)
        return {
            "id": user.id,
            "username": user.username,
            "bio": user.bio,
            "image_url": user.image_url
        }

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if not user or not user.authenticate(password):
            return {"error": "Invalid credentials"}, 401

        session['user_id'] = user.id
        return {
            "id": user.id,
            "username": user.username,
            "bio": user.bio,
            "image_url": user.image_url
        }

class Logout(Resource):
    def delete(self):
        if not session.get("user_id"):
            return {"error": "Unauthorized"}, 401
        session['user_id'] = None
        return {}, 204

class RecipeIndex(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401
        recipes = Recipe.query.filter_by(user_id=user_id).all()
        return [{
            "id": r.id,
            "title": r.title,
            "instructions": r.instructions,
            "minutes_to_complete": r.minutes_to_complete
        } for r in recipes]

    def post(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        try:
            recipe = Recipe(
                title=data.get("title"),
                instructions=data.get("instructions"),
                minutes_to_complete=data.get("minutes_to_complete"),
                user_id=user_id
            )
            db.session.add(recipe)
            db.session.commit()
        except:
            db.session.rollback()
            return {"error": "Invalid recipe"}, 422

        return {
            "id": recipe.id,
            "title": recipe.title,
            "instructions": recipe.instructions,
            "minutes_to_complete": recipe.minutes_to_complete
        }, 201

# --------------------- ROUTES ---------------------

api.add_resource(Signup, "/signup")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(RecipeIndex, "/recipes")

if __name__ == "__main__":
    app.run(debug=True)
