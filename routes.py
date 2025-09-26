from flask import Flask,render_template

app = Flask(__name__)


def init_routes(app):
    # Home
    @app.route('/')
    def home():
        return render_template('home.html')

    # Cliente
    @app.route('/cliente')
    def cliente():
        return render_template('cliente.html')

    # Funcionário
    @app.route('/funcionario')
    def funcionario():
        return render_template('funcionario.html')

    # Gerente/Adm
    @app.route('/gerente')
    def gerente():
        return render_template('gerente.html')
