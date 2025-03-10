from flask import Flask, render_template, request, url_for

app = Flask(__name__, static_folder="static")

# Hardcoded Recipe Database
RECIPE_DB = {
    "italian": {
        "tomato": "🍅 **Tomato Basil Pasta**: Cook pasta and mix with fresh tomato sauce and basil.",
        "cheese": "🧀 **Four Cheese Pizza**: A crispy pizza with mozzarella, parmesan, ricotta, and gorgonzola.",
        "chicken": "🍗 **Chicken Parmesan**: Breaded chicken baked with tomato sauce and cheese.",
        "pasta": "🍝 **Creamy Alfredo Pasta**: Cook pasta and mix with a rich white sauce.",
        "mushroom": "🍄 **Mushroom Risotto**: Creamy risotto with sautéed mushrooms and parmesan.",
        "olive": "🫒 **Mediterranean Olive Salad**: Fresh olives, feta, and herbs tossed in olive oil."
    },
    "chinese": {
        "rice": "🍚 **Fried Rice**: Stir-fry rice with soy sauce, eggs, and vegetables.",
        "chicken": "🐔 **Kung Pao Chicken**: Stir-fried chicken with peanuts and spicy sauce.",
        "mushroom": "🍄 **Mushroom Stir-Fry**: Sautéed mushrooms with garlic and soy sauce.",
        "noodles": "🍜 **Chow Mein**: Stir-fried noodles with vegetables and soy sauce.",
        "tofu": "🥢 **Mapo Tofu**: Spicy Sichuan-style tofu in a rich sauce.",
        "cabbage": "🥬 **Stir-Fried Cabbage**: Crunchy cabbage tossed with garlic and soy sauce."
    },
    "mexican": {
        "avocado": "🥑 **Guacamole**: Mashed avocado with lime, tomato, and onion.",
        "chicken": "🌮 **Chicken Tacos**: Grilled chicken in a tortilla with salsa and cheese.",
        "beans": "🌯 **Burrito Bowl**: Beans, rice, avocado, and grilled veggies in a bowl.",
        "cheese": "🧀 **Quesadilla**: Cheese-filled tortilla grilled to perfection.",
        "corn": "🌽 **Elote (Mexican Street Corn)**: Grilled corn with mayo, cheese, and chili powder.",
        "beef": "🥩 **Carne Asada**: Marinated grilled beef with lime and spices."
    },
    "indian": {
        "rice": "🍛 **Biryani**: Spiced rice with vegetables or chicken.",
        "chicken": "🍗 **Butter Chicken**: Creamy tomato-based curry with tender chicken.",
        "lentils": "🥣 **Dal Tadka**: Spiced lentil soup with garlic and ghee.",
        "potato": "🥔 **Aloo Gobi**: Spiced potato and cauliflower stir-fry.",
        "paneer": "🧀 **Palak Paneer**: Spinach-based curry with soft paneer cheese.",
        "chickpeas": "🍛 **Chana Masala**: Spiced chickpea curry with tomatoes and onions."
    },
    "american": {
        "beef": "🍔 **Classic Burger**: Grilled beef patty with cheese, lettuce, and tomato.",
        "potato": "🍟 **French Fries**: Crispy golden fries with a pinch of salt.",
        "cheese": "🧀 **Mac & Cheese**: Creamy pasta with melted cheese.",
        "chicken": "🍗 **BBQ Chicken Wings**: Chicken wings glazed in BBQ sauce.",
        "egg": "🍳 **Omelet**: Fluffy eggs cooked with cheese and vegetables.",
        "bacon": "🥓 **Bacon Cheeseburger**: A juicy burger with crispy bacon and melted cheese."
    }
}

# Function to get recipe images (Fix for url_for issue)
def get_recipe_images():
    """Generate image URLs dynamically within Flask's context."""
    with app.app_context():
        return {
            "italian": url_for('static', filename='italian.png'),
            "chinese": url_for('static', filename='chinese.png'),
            "mexican": url_for('static', filename='mexican.png'),
            "indian": url_for('static', filename='indian.png'),
            "american": url_for('static', filename='american.png')
        }

def get_recipe(ingredients, cuisine):
    """Generate recipe based on user-selected ingredients and cuisine."""
    cuisine = cuisine.lower()
    
    if cuisine not in RECIPE_DB:
        return "⚠️ No recipes available for this cuisine.", url_for('static', filename='default.jpg')

    recipes = [RECIPE_DB[cuisine].get(ingredient.strip().lower(), None) for ingredient in ingredients]
    recipes = [r for r in recipes if r]  # Filter out None values

    if not recipes:
        return "⚠️ Sorry, no recipes found for these ingredients.", url_for('static', filename='default.jpg')

    recipe_images = get_recipe_images()  # Get images dynamically
    return "<br><br>".join(recipes), recipe_images.get(cuisine, url_for('static', filename='default.jpg'))

@app.route('/')
def home():
    """Render homepage."""
    return render_template('index.html')

@app.route('/generate_recipe', methods=['POST'])
def generate():
    """Generate recipe based on user input."""
    ingredients = request.form['ingredients'].split(',')
    cuisine = request.form.get('restaurant', 'italian')

    recipe, image_url = get_recipe(ingredients, cuisine)
    
    return render_template('recipe.html', recipe=recipe, restaurant=cuisine.capitalize(), image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
