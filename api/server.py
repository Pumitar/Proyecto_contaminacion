from flask import Flask, jsonify, render_template
from flask_cors import CORS


from api.controlers import get_ranking

app = Flask('Proyecto_Cosmo', template_folder='public/templates', static_folder='public/static')
CORS(app)  # Habilita CORS para toda la aplicación

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api")
def hello_world():
    return "<p>Bienvenido a Cosmo Api!</p>"

@app.route("/api/ranking", methods=['GET'])
def ranking():
    return jsonify(get_ranking())
