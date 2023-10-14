from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db, Fav
from jinja2 import StrictUndefined
import crud


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():

    return render_template("homepage.html")


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/recipes")


@app.route("/recipes")
def all_recipes():
    """View all recipes."""

    recipes = crud.get_recipes()

    return render_template("all_recipes.html", recipes=recipes)


@app.route("/recipes/<recipe_id>")
def show_recipe(recipe_id):

    """Show details on a particular recipe."""
    recipe = crud.get_recipe_by_id(recipe_id)

    return render_template("recipe_details.html", recipe=recipe)


@app.route("/add-recipe", methods=["GET", "POST"])
def add_recipe():
    """Add a new recipe."""

    if request.method == "POST":
        name = request.form.get("name")
        instructions = request.form.get("instructions")
        cook_time = request.form.get("cook_time")
        prep_time = request.form.get("prep_time")
        servings = request.form.get("servings")
       

        recipe = crud.create_recipe(
            name, instructions, cook_time, prep_time, servings, 
        )
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe added successfully!")

        return redirect("/add-recipe")


    return render_template("add-recipe.html", flash=flash)





@app.route("/fav", methods=["GET"])
def fav():
    """List the user's favorites."""

    user_id = session.get("user_id")
    
    
   
    # Get the user's favorites
    favs = Fav.query.filter_by(user_id=user_id).all()

    return render_template("fav.html", favs=favs)


   
@app.route("/add_favorite", methods=["GET"])
def add_favorite_handler():
    """Add a recipe to favorites."""

    recipe_id = request.form.get("recipe_id")
    user_id = session.get("user_id")

  
  
    
    # Add the recipe to the user's favorites
    favorite = Fav(user_id=user_id, recipe_id=recipe_id)
    db.session.add(favorite)
    db.session.commit()
    flash("Recipe added to favorites.")
    return redirect("/fav")
    
    

@app.route("/search", methods=["GET"])
def search_recipe():
    """Search for Recipes"""

    if request.method == "GET":
        query = request.args.get("query")
        
    recipe= crud.search_recipes(query)
    recipes=crud.get_recipes   
        

    return render_template("search.html", recipes=recipes)







if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost", port=8000, debug=True)