from app import app
from models import db, User, Recipe

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(username="Ash", bio="I wanna be the very best!", image_url="https://example.com/ash.png")
    user.password_hash = "pikachu"
    db.session.add(user)
    db.session.commit()

    recipe = Recipe(
        title="PokeSnack",
        instructions="Mix ingredients thoroughly and bake for 20 minutes at 180C. Serve warm. Delicious!",
        minutes_to_complete=25,
        user_id=user.id
    )
    db.session.add(recipe)
    db.session.commit()

    print("Seeded database successfully!")
