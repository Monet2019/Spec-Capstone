from model import db, connect_to_db, User, Recipe, Fav 

if __name__ == '__main__':
    from server import app
    connect_to_db(app)


def create_user(email, password):
    """Create and return a new user."""
    user = User(email=email, password=password)
    return user

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def create_recipe(name, ingredient, instructions, cook_time, prep_time, servings):
  """Create and return a new recipe."""

  recipe = Recipe(
    name=name,
    ingredient=ingredient,
    instructions=instructions,
    cook_time=cook_time,
    prep_time=prep_time,
    servings=servings,
  )
  return recipe


def get_recipes():
  """Return all recipes."""

  return Recipe.query.all()


def get_recipe_by_id(recipe_id):
  """Return a recipe by ID."""

  return Recipe.query.get(recipe_id)


def search_recipes(query):
  """Search for recipes by query."""

  return Recipe.query.filter(Recipe.name.contains(query) | Recipe.ingredient.contains(query))

def fav(recipe_id, user_id):
    """Add a new favorite to the database."""

    fav = Fav(recipe_id=recipe_id, user_id=user_id)
    db.session.add(fav)
    db.session.commit()

def add_favorite(recipe_id, user_id):
    """Add a recipe to favorites."""

    fav = Fav(recipe_id=recipe_id, user_id=user_id)

    db.session.add(fav)
    db.session.commit()


