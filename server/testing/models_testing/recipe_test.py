import pytest
from sqlalchemy.exc import IntegrityError
from app import app
from models import db, User, Recipe

@pytest.fixture
def test_user():
    """Create and return a test user."""
    with app.app_context():
        Recipe.query.delete()
        User.query.delete()
        db.session.commit()

        user = User(username="RecipeTester")
        user.password_hash = "supersecret"
        db.session.add(user)
        db.session.commit()

        # Return a persistent user from the same session
        return User.query.get(user.id)


def test_recipe_has_attributes(test_user):
    """Recipe has title, instructions, and minutes_to_complete"""
    user = test_user
    with app.app_context():
        recipe = Recipe(
            title="Delicious Shed Ham",
            instructions=(
                "Or kind rest bred with am shed then. In raptures building an "
                "bringing be. Elderly is detract tedious assured private so to "
                "visited. Do travelling companions contrasted it."
            ),
            minutes_to_complete=60,
            user_id=user.id
        )

        db.session.add(recipe)
        db.session.commit()

        fetched = Recipe.query.get(recipe.id)
        assert fetched.title == "Delicious Shed Ham"
        assert fetched.instructions == recipe.instructions
        assert fetched.minutes_to_complete == 60


def test_requires_title(test_user):
    """Recipe requires a title"""
    user = test_user
    with app.app_context():
        long_instructions = (
            "This recipe has instructions that are definitely longer than 50 characters "
            "so it will pass the length validation."
        )
        recipe = Recipe(
            instructions=long_instructions,
            minutes_to_complete=30,
            user_id=user.id
        )

        db.session.add(recipe)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()


def test_requires_long_instructions(test_user):
    """Recipe instructions must be 50+ characters"""
    user = test_user
    short_instructions = "Too short"
    with pytest.raises(ValueError):
        Recipe(
            title="Short Recipe",
            instructions=short_instructions,
            minutes_to_complete=15,
            user_id=user.id
        )


def test_user_can_have_recipes():
    """User can have a list of recipes attached"""
    with app.app_context():
        # Clear database
        Recipe.query.delete()
        User.query.delete()
        db.session.commit()

        # Create user in the same session
        user = User(username="RecipeTester2")
        user.password_hash = "supersecret"
        db.session.add(user)
        db.session.commit()
        user = User.query.get(user.id)  # ensure persistent

        recipe_1 = Recipe(
            title="Delicious Shed Ham",
            instructions=(
                "Or kind rest bred with am shed then. In raptures building an "
                "bringing be. Elderly is detract tedious assured private so to "
                "visited. Do travelling companions contrasted it."
            ),
            minutes_to_complete=60,
            user_id=user.id
        )

        recipe_2 = Recipe(
            title="Hasty Party Ham",
            instructions=(
                "As am hastily invited settled at limited civilly fortune me. Really "
                "spring in extent an by. Judge but built gay party world."
            ),
            minutes_to_complete=30,
            user_id=user.id
        )

        db.session.add(recipe_1)
        db.session.add(recipe_2)
        db.session.commit()

        # Refresh user to get latest recipes
        db.session.refresh(user)
        assert len(user.recipes) == 2
        assert recipe_1 in user.recipes
        assert recipe_2 in user.recipes
