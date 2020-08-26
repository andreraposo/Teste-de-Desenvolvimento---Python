from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)

# LIDA COM ROTAS
from noticias.routes import *

# LIDA COM BANCO DE DADOS
app.config['MONGODB_SETTINGS'] = {
    'db': 'noticias',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine(app)

if __name__ == '__main__':
    app.run(debug=True)
