import openai
import speech_recognition as sr
import pyttsx3
import threading
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("ERROR: Missing OpenAI API Key. Add it to a .env file or environment variables.")

# Initialize Flask app
app = Flask(__name__)

# Initialize Speech Recognition
recognizer = sr.Recognizer()

# Function to generate recipes using OpenAI API
def generate_recipe(ingredients, restaurant, chef, dietary_restrictions=None):
    """Generate a healthy recipe using OpenAI API."""
    prompt = f"Generate a healthy recipe using these ingredients: {', '.join(ingredients)}."

    if dietary_restrictions:
        prompt += f" Ensure it suits these dietary restrictions: {dietary_restrictions}."

    if restaurant:
        prompt += f" The recipe should be inspired by {restaurant} restaurant."

    if chef:
        prompt += f" Make it in the style of Chef {chef}."

    prompt += " Provide the recipe steps and a short description of its health benefits."

    try:
        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a professional chef providing delicious recipes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )

        return response["choices"][0]["message"]["content"].strip()
    
    except openai.error.OpenAIError as e:
        return f"Error generating recipe: {str(e)}"

# Function to handle voice input
def voice_input():
    """Capture voice input and convert it to text."""
    with sr.Microphone() as source:
        print("Listening for ingredients...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        return recognizer.recognize_google(audio)
    except Exception:
        print("Sorry, I did not catch that.")
        return ""

# Function for voice output using threading
def voice_output(text):
    """Convert text to voice output in a separate thread."""
    def speak():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=speak, daemon=True).start()

# Flask Routes
@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/generate_recipe', methods=['POST'])
def generate():
    """Generate a recipe based on user input."""
    ingredients = request.form['ingredients'].split(',')
    restaurant = request.form.get('restaurant', '')
    chef = request.form.get('chef', '')
    dietary_restrictions = request.form.get('dietary_restrictions', '')

    recipe = generate_recipe(ingredients, restaurant, chef, dietary_restrictions)
    voice_output(f"Here is a recipe from {restaurant} by {chef}: {recipe}")
    
    return render_template('recipe.html', recipe=recipe, restaurant=restaurant, chef=chef)

@app.route('/voice_ingredients', methods=['GET'])
def voice_ingredients():
    """Handle voice input to capture ingredients and display recipes."""
    ingredients = voice_input().split(',')
    restaurant = "Chef's Choice"
    chef = "Master Chef"
    dietary_restrictions = 'healthy'  # Default dietary preference

    recipe = generate_recipe(ingredients, restaurant, chef, dietary_restrictions)
    voice_output(f"Here is a recipe from {restaurant} by {chef}: {recipe}")

    return render_template('recipe.html', recipe=recipe, restaurant=restaurant, chef=chef)

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
