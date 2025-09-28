from flask import render_template

def init_routes(app):
    # Home
    @app.route('/')
    def home():
        return render_template('home.html')
    #carrinho
    @app.route('/carrinho')
    def carrinho():
         return render_template('carrinho.html')

    # Cliente
    @app.route('/cliente')
    def cliente():
        produtos = [
    {"nome": "Arroz Integral", "preco": 12.50, "categoria": "kg", "quantidade": 1, "img": "arroz.jpg"},
    {"nome": "Feijão Preto", "preco": 9.80, "categoria": "kg", "quantidade": 1, "img": "feijao.jpg"},
    {"nome": "Macarrão Espaguete", "preco": 6.40, "categoria": "kg", "quantidade": 0.5, "img": "macarrao.jpg"},
    {"nome": "Açúcar Refinado", "preco": 4.20, "categoria": "kg", "quantidade": 1, "img": "acucar.jpg"},
    {"nome": "Café Torrado", "preco": 15.90, "categoria": "kg", "quantidade": 0.5, "img": "cafe.jpg"},
    {"nome": "Leite Integral", "preco": 4.50, "categoria": "L", "quantidade": 1, "img": "leite.jpg"},
    {"nome": "Manteiga", "preco": 7.80, "categoria": "g", "quantidade": 200, "img": "manteiga.jpg"},
    {"nome": "Queijo Mussarela", "preco": 39.90, "categoria": "kg", "quantidade": 0.5, "img": "queijo.jpg"},
    {"nome": "Presunto", "preco": 32.50, "categoria": "kg", "quantidade": 0.5, "img": "presunto.jpg"},
    {"nome": "Ovos Brancos", "preco": 12.00, "categoria": "dúzia", "quantidade": 1, "img": "ovos.jpg"},
    {"nome": "Pão Francês", "preco": 14.00, "categoria": "kg", "quantidade": 1, "img": "pao.jpg"},
    {"nome": "Bolo de Chocolate", "preco": 25.00, "categoria": "unidade", "quantidade": 1, "img": "bolo.jpg"},
    {"nome": "Coca-Cola 2L", "preco": 9.50, "categoria": "L", "quantidade": 2, "img": "coca.jpg"},
    {"nome": "Suco de Laranja", "preco": 6.90, "categoria": "L", "quantidade": 1, "img": "suco.jpg"},
    {"nome": "Água Mineral", "preco": 2.50, "categoria": "L", "quantidade": 1, "img": "agua.jpg"},
    {"nome": "Cerveja Lata", "preco": 3.20, "categoria": "ml", "quantidade": 350, "img": "cerveja.jpg"},
    {"nome": "Banana Nanica", "preco": 6.00, "categoria": "kg", "quantidade": 1, "img": "banana.jpg"},
    {"nome": "Maçã Gala", "preco": 8.50, "categoria": "kg", "quantidade": 1, "img": "maca.jpg"},
    {"nome": "Laranja Pera", "preco": 5.90, "categoria": "kg", "quantidade": 1, "img": "laranja.jpg"},
    {"nome": "Melancia", "preco": 18.00, "categoria": "kg", "quantidade": 3, "img": "melancia.jpg"},
    {"nome": "Alface Crespa", "preco": 4.00, "categoria": "unidade", "quantidade": 1, "img": "alface.jpg"},
    {"nome": "Cenoura", "preco": 5.50, "categoria": "kg", "quantidade": 1, "img": "cenoura.jpg"},
    {"nome": "Tomate Italiano", "preco": 7.20, "categoria": "kg", "quantidade": 1, "img": "tomate.jpg"},
    {"nome": "Batata Inglesa", "preco": 6.80, "categoria": "kg", "quantidade": 1, "img": "batata.jpg"},
    {"nome": "Cebola", "preco": 4.90, "categoria": "kg", "quantidade": 1, "img": "cebola.jpg"},
    {"nome": "Frango Congelado", "preco": 18.90, "categoria": "kg", "quantidade": 1, "img": "frango.jpg"},
    {"nome": "Carne Moída", "preco": 29.90, "categoria": "kg", "quantidade": 1, "img": "carne.jpg"},
    {"nome": "Peixe Tilápia", "preco": 34.50, "categoria": "kg", "quantidade": 1, "img": "tilapia.jpg"},
    {"nome": "Salsicha Hot Dog", "preco": 12.90, "categoria": "kg", "quantidade": 1, "img": "salsicha.jpg"},
    {"nome": "Pizza Congelada", "preco": 19.90, "categoria": "unidade", "quantidade": 1, "img": "pizza.jpg"}
]

        return render_template('cliente.html', produtos=produtos)

    # Funcionário
    @app.route('/funcionario')
    def funcionario():
        return render_template('funcionario.html')

    # Gerente/Adm
    @app.route('/gerente')
    def gerente():
        return render_template('gerente.html')
