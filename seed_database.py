import os
import json
import crud
import model
import server

   
os.system("dropdb recipes-app")
os.system("createdb recipes-app")

model.connect_to_db(server.app)
with server.app.app_context():
    model.db.create_all()

    # JSON file
    with open("recipes.json") as f:
        recipe_data = json.loads(f.read())

    recipes_in_db = []
    for recipe in recipe_data:
        name, instructions, cook_time, prep_time, servings, ingredients = (
            recipe["name"],
            recipe["instructions"],
            recipe["cook_time"],
            recipe["prep_time"],
            recipe["servings"],
            recipe["ingredients"],
        )

        db_recipe = crud.create_recipe(
            name,
            instructions,
            cook_time,
            prep_time,
            servings,
            ingredients,
        )
        recipes_in_db.append(db_recipe)

        model.db.session.add_all(recipes_in_db)
        model.db.session.commit()

    for n in range(10):
        email = f"user{n}@test.com"
        password = "test"

        user = crud.create_user(email, password)
        model.db.session.add(user)

    favorite_recipe = crud.create_favorite_recipe(user, recipe)
    model.db.session.add(favorite_recipe)

model.db.session.commit()