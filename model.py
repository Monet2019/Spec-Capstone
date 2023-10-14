from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import os



db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)


    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Recipe(db.Model):
    """A recipe."""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    instructions = db.Column(db.Text)
    cook_time = db.Column(db.Integer)
    prep_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)

# ingredients = a list of Ingredient objects
    ingredient = db.relationship("Ingredient", backref="recipe", lazy="dynamic")

    def __repr__(self):
        return f"<Recipe recipe_id={self.recipe_id} name={self.name}>"



class Ingredient(db.Model):
    """An ingredient in a recipe."""

    __tablename__ = "ingredient"

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ingredient_name = db.Column(db.String)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))



    def __repr__(self):
        return f"<Ingredient ingredient_id={self.ingredient_id} recipe_id={self.recipe_id}>"


class Fav(db.Model):
    """A Fav recipe."""

    __tablename__ = "fav"

    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
        return f"<Fav fav_id={self.fav_id} recipe_id={self.recipe_id} user_id={self.user_id}>"


def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

def my_function(obj):
    if not isinstance(obj, inspect(obj).mapper.mapped_class):
        raise TypeError("Object must be an SQLAlchemy object")



 # Create a new Fav object
    fav = Fav()

    # Get the Recipe object with the ID 1
    recipe = Recipe.query.get(1)

    # Add the Recipe object to the Fav object
    fav.recipe = recipe

    # Save the Fav object
    db.session.add(fav)
    db.session.commit()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)