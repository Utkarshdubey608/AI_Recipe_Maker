import openai
import speech_recognition as sr
import pyttsx3
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Initialize Text-to-Speech Engine (for voice output)
engine = pyttsx3.init()

def generate_recipe(ingredients, dietary_restrictions=None):
    """Generate a healthy recipe using GPT-3/4 based on ingredients and dietary constraints."""
    prompt = f"Generate a healthy recipe using the following ingredients: {', '.join(ingredients)}."
    
    if dietary_restrictions:
        prompt += f" Please make sure it is suitable for people with the following dietary restrictions: {dietary_restrictions}."
    
    prompt += " Provide the recipe steps and include a brief description of the health benefits of the dish."

    response = openai.Completion.create(
        engine="text-davinci-003",  # Use GPT-4 if available
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

def voice_input():
    """Capture voice input and convert it to text."""
    recognizer = sr.Recognizer()
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

def voice_output(text):
    """Convert text to voice output."""
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/generate_recipe', methods=['POST'])
def generate():
    """Generate a recipe based on user input."""
    ingredients = request.form['ingredients'].split(',')
    dietary_restrictions = request.form.get('dietary_restrictions', '')
    recipe = generate_recipe(ingredients, dietary_restrictions)
    voice_output(f"Here is a recipe based on your ingredients: {recipe}")
    return render_template('recipe.html', recipe=recipe)

@app.route('/voice_ingredients', methods=['GET'])
def voice_ingredients():
    """Handle voice input to capture ingredients and display recipes."""
    ingredients = voice_input().split(',')
    dietary_restrictions = 'healthy'  # Default dietary preference
    recipe = generate_recipe(ingredients, dietary_restrictions)
    voice_output(f"Here is a recipe based on your ingredients: {recipe}")
    return render_template('recipe.html', recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)