#!/usr/bin/env python3

from faker import Faker
import pytest
from random import randint

from app import app, db
from models import User, Recipe

fake = Faker()

# --------------------- PYTEST CUSTOMIZATION ---------------------
def pytest_itemcollected(item):
    """Make test output display class docstrings + test docstrings nicely."""
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

# --------------------- FIXTURES ---------------------
@pytest.fixture(scope="function")
def test_client():
    """Yields a test client with fresh database for each test."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def new_user():
    """Returns a User instance with a hashed password."""
    user = User(
        username=fake.user_name(),
        bio=fake.text(max_nb_chars=200),
        image_url=fake.image_url()
    )
    user.password_hash = "secret"
    return user

@pytest.fixture
def new_recipe(new_user):
    """Returns a Recipe instance associated with a user."""
    recipe = Recipe(
        title=fake.sentence(),
        instructions=fake.paragraph(nb_sentences=8),
        minutes_to_complete=randint(15, 90),
        user=new_user
    )
    return recipe
