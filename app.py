from flask import Flask
from routes import init_routes   # importando as rotas

app = Flask(__name__)
init_routes(app)                # inicializando rotas

if __name__ == '__main__':
    app.run(debug=True)
