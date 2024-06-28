from flask import Flask, render_template, request, redirect, url_for
from models import db, Recipe
import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()




@app.route('/home')
def home():
    dishes = Recipe.query.all()
    return render_template("home.html", dishes=dishes)


@app.route("/uploads", methods=["GET", "POST"])
def uploads():
    if request.method == "POST":
        # Handle form submission
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        difficulty = request.form.get('difficulty')
        cost = request.form.get('cost')
        image = request.files['image']  # Uploaded file - Tentative



        # Create a new Recipe object and add to the database
        new_recipe = Recipe(
            title=title, description=description,
            ingredients=ingredients,
            instructions=instructions,
            difficulty=difficulty, cost=cost)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('success'))

    return render_template("uploads.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/dishes/<int:dish_id>")
def dish(dish_id):
    recipe = Recipe.query.get_or_404(dish_id)
    print(recipe)
    return render_template("dish.html", recipe=recipe)


if __name__ == '__main__':
    app.run(debug=True)
