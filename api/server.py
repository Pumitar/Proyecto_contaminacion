from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os


from api.controlers import get_ranking

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(BASE_DIR, 'public', 'templates')
STATIC = os.path.join(BASE_DIR, 'public', 'static')

app = Flask(__name__, template_folder=TEMPLATES, static_folder=STATIC)


CORS(app)  # Habilita CORS para toda la aplicación

@app.route("/")
def index():
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:3000")
    return render_template('index.html', api_base_url=api_base_url)

@app.route("/api")
def hello_world():
    return "<p>Bienvenido a Cosmo Api!</p>"

@app.route("/api/ranking", methods=['GET'])
def ranking():
    return jsonify(get_ranking())
