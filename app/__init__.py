# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configurações do app
    app.config['SECRET_KEY'] = 'minha_chave_secreta'
    
    # Importa as rotas
    from app.routes import init_routes
    init_routes(app)
    
    return app
