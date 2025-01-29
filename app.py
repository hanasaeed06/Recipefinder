from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'bc196b30da3a4413ba02f29963f55edb'
API_URL = 'https://api.spoonacular.com/recipes/findByIngredients'


@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []
    if request.method == 'POST':
        ingredients = request.form['ingredients']

        response = requests.get(API_URL, params={
            'ingredients': ingredients,
            'number': 5,  
            'apiKey': API_KEY
        })
        
        if response.status_code == 200:
            recipes = response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")  
    
    return render_template('index.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)