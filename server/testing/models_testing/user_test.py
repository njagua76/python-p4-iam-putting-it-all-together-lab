import pytest
from app import app
from models import db, User, Recipe

def test_user_can_have_recipes():
    """User can have a list of recipes attached"""
    with app.app_context():
        Recipe.query.delete()
        User.query.delete()
        db.session.commit()

        # Create user
        user = User(username="TestUser")
        user.password_hash = "supersecret"
        db.session.add(user)
        db.session.commit()  # user.id is now set

        # Create recipes attached to this user
        recipe_1 = Recipe(
            title="Delicious Shed Ham",
            instructions=("Or kind rest bred with am shed then. In raptures building "
                          "an bringing be. Elderly is detract tedious assured private."),
            minutes_to_complete=60,
            user_id=user.id
        )

        recipe_2 = Recipe(
            title="Hasty Party Ham",
            instructions=("As am hastily invited settled at limited civilly fortune me. "
                          "Really spring in extent an by. Judge but built gay party world."),
            minutes_to_complete=30,
            user_id=user.id
        )

        db.session.add_all([recipe_1, recipe_2])
        db.session.commit()

        # Refresh user from DB
        user = db.session.get(User, user.id)

        assert len(user.recipes) == 2
        assert recipe_1 in user.recipes
        assert recipe_2 in user.recipes
