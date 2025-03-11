from flask import Flask, render_template, request, url_for

app = Flask(__name__, static_folder="static")

# Recipe Database
RECIPE_DB = {
    "italian": {
    "tomato": "🍅 Tomato Basil Pasta: Cook pasta and mix with fresh tomato sauce and basil.",
    "cheese": "🧀 Four Cheese Pizza: A crispy pizza with mozzarella, parmesan, ricotta, and gorgonzola.",
    "chicken": "🍗 Chicken Parmesan: Breaded chicken baked with tomato sauce and cheese.",
    "pasta": "🍝 Creamy Alfredo Pasta: Cook pasta and mix with a rich white sauce.",
    "mushroom": "🍄 Mushroom Risotto: Creamy risotto with sautéed mushrooms and parmesan.",
    "olive": "🫒 Mediterranean Olive Salad: Fresh olives, feta, and herbs tossed in olive oil."
},
"chinese": {
    "rice": "🍚 Fried Rice: Stir-fry rice with soy sauce, eggs, and vegetables.",
    "chicken": "🐔 Kung Pao Chicken: Stir-fried chicken with peanuts and spicy sauce.",
    "mushroom": "🍄 Mushroom Stir-Fry: Sautéed mushrooms with garlic and soy sauce.",
    "noodles": "🍜 Chow Mein: Stir-fried noodles with vegetables and soy sauce.",
    "tofu": "🥢 Mapo Tofu: Spicy Sichuan-style tofu in a rich sauce.",
    "cabbage": "🥬 Stir-Fried Cabbage: Crunchy cabbage tossed with garlic and soy sauce."
},
"mexican": {
    "avocado": "🥑 Guacamole: Mashed avocado with lime, tomato, and onion.",
    "chicken": "🌮 Chicken Tacos: Grilled chicken in a tortilla with salsa and cheese.",
    "beans": "🌯 Burrito Bowl: Beans, rice, avocado, and grilled veggies in a bowl.",
    "cheese": "🧀 Quesadilla: Cheese-filled tortilla grilled to perfection.",
    "corn": "🌽 Elote (Mexican Street Corn): Grilled corn with mayo, cheese, and chili powder.",
    "beef": "🥩 Carne Asada: Marinated grilled beef with lime and spices."
},
"indian": {
    "rice": "🍛 Biryani: Spiced rice with vegetables or chicken.",
    "chicken": "🍗 Butter Chicken: Creamy tomato-based curry with tender chicken.",
    "lentils": "🥣 Dal Tadka: Spiced lentil soup with garlic and ghee.",
    "potato": "🥔 Aloo Gobi: Spiced potato and cauliflower stir-fry.",
    "paneer": "🧀 Palak Paneer: Spinach-based curry with soft paneer cheese.",
    "chickpeas": "🍛 Chana Masala: Spiced chickpea curry with tomatoes and onions."
},
"american": {
    "beef": "🍔 Classic Burger: Grilled beef patty with cheese, lettuce, and tomato.",
    "potato": "🍟 French Fries: Crispy golden fries with a pinch of salt.",
    "cheese": "🧀 Mac & Cheese: Creamy pasta with melted cheese.",
    "chicken": "🍗 BBQ Chicken Wings: Chicken wings glazed in BBQ sauce.",
    "egg": "🍳 Omelet: Fluffy eggs cooked with cheese and vegetables.",
    "bacon": "🥓 Bacon Cheeseburger: A juicy burger with crispy bacon and melted cheese."
}

}

# Function to generate recipe images
def get_recipe_images():
    with app.app_context():
        return {
            "italian": url_for('static', filename='italian.png'),
            "chinese": url_for('static', filename='chinese.png'),
            "mexican": url_for('static', filename='mexican.png'),
            "indian": url_for('static', filename='indian.png'),
            "american": url_for('static', filename='american.png')
        }

# ✅ Final Improved Function
def get_recipe(ingredients, allergies):
    matched_recipes = []

    # Check every cuisine for matching ingredients
    for cuisine, dishes in RECIPE_DB.items():
        for ingredient in ingredients:
            ingredient = ingredient.strip().lower()
            if ingredient in dishes:
                matched_recipes.append((dishes[ingredient], cuisine))
    
    # Remove duplicates
    matched_recipes = list(set(matched_recipes))

    # Filter out recipes with allergens if provided
    if allergies:
        filtered_recipes = []
        for recipe, cuisine in matched_recipes:
            if not any(allergen.lower() in recipe.lower() for allergen in allergies):
                filtered_recipes.append((recipe, cuisine))
        matched_recipes = filtered_recipes

    # Handle no recipes found
    if not matched_recipes:
        if allergies: 
            return "⚠️ No suitable recipes found. All contain allergens.", url_for('static', filename='default.png')
        else:
            return "⚠️ No suitable recipes found.", url_for('static', filename='default.png')
    
    # Combine recipes as HTML
    recipes_html = "<br><br>".join([f"{recipe[0]}" for recipe in matched_recipes])
    image_url = get_recipe_images().get(matched_recipes[0][1], url_for('static', filename='default.png'))
    
    return recipes_html, image_url

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_recipe', methods=['POST'])
def generate():
    ingredients = request.form['ingredients'].split(',')
    allergies = request.form['allergies'].split(',')
    
    # Handle case where no allergies are provided
    if allergies == ['']:
        allergies = []
    
    recipe, image_url = get_recipe(ingredients, allergies)
    
    return render_template('recipe.html', recipe=recipe, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
