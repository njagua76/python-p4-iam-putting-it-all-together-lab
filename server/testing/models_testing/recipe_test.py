import pytest
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Recipe

class TestRecipe:
    '''User in models.py'''

def test_has_attributes(self):
    '''has attributes title, instructions, and minutes_to_complete.'''
    
    with app.app_context():
        # Clear previous data
        Recipe.query.delete()
        User.query.delete()
        db.session.commit()

        # Create a user first
        from models import User
        user = User(username="TestUser")
        user.password_hash = "supersecret"
        db.session.add(user)
        db.session.commit()

        # Create a recipe linked to user
        recipe = Recipe(
            title="Delicious Shed Ham",
            instructions=(
                "Or kind rest bred with am shed then. In raptures building an bringing be. "
                "Elderly is detract tedious assured private so to visited. Do travelling "
                "companions contrasted it. Mistress strongly remember up to. Ham him compass "
                "you proceed calling detract. Better of always missed we person mr. September "
                "smallness northward situation few her certainty something."
            ),
            minutes_to_complete=60
        )
        user.recipes.append(recipe)  # <-- link to user

        db.session.add(user)  # only need to add the user; recipes are auto-added
        db.session.commit()

        new_recipe = Recipe.query.filter_by(title="Delicious Shed Ham").first()

        assert new_recipe.title == "Delicious Shed Ham"
        assert new_recipe.minutes_to_complete == 60
        assert new_recipe in user.recipes
 