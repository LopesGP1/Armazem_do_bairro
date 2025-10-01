from flask import render_template, jsonify,request
from app.models.produto import Produto
from app.conexao import get_connection

def init_routes(app):
    # Home
    @app.route('/')
    def home():
        return render_template('home.html')
    #carrinho
    @app.route('/carrinho')
    def carrinho():
        
        produtos = [
            {"nome": "Arroz Integral", "preco": 12.50, "categoria": "kg", "quantidade": 1, "img": "arroz.jpg"},
            {"nome": "Feijão Preto", "preco": 9.80, "categoria": "kg", "quantidade": 1, "img": "feijao.jpg"},
            {"nome": "Macarrão Espaguete", "preco": 6.40, "categoria": "kg", "quantidade": 0.5, "img": "macarrao.jpg"},
            {"nome": "Açúcar Refinado", "preco": 4.20, "categoria": "kg", "quantidade": 1, "img": "acucar.jpg"},
            {"nome": "Café Torrado", "preco": 15.90, "categoria": "kg", "quantidade": 0.5, "img": "cafe.jpg"},
            {"nome": "Leite Integral", "preco": 4.50, "categoria": "L", "quantidade": 1, "img": "leite.jpg"},
            {"nome": "Manteiga", "preco": 7.80, "categoria": "g", "quantidade": 200, "img": "manteiga.jpg"},
            {"nome": "Queijo Mussarela", "preco": 39.90, "categoria": "kg", "quantidade": 0.5, "img": "queijo.jpg"},
            {"nome": "Pão Francês", "preco": 14.00, "categoria": "kg", "quantidade": 1, "img": "pao.jpg"},
            {"nome": "Bolo de Chocolate", "preco": 25.00, "categoria": "unidade", "quantidade": 1, "img": "bolo.jpg"}
        ]
        return render_template('carrinho.html', produtos=produtos)

    # Cliente
    @app.route('/cliente')
    def cliente():
        produtos = Produto.listar_todos()  # chama a função que busca os produtos
        return render_template('cliente.html', produtos=produtos)

    # Funcionário
    @app.route('/funcionario')
    def funcionario():
        return render_template('funcionario.html')

    # Gerente/Adm
    @app.route('/gerente')
    def gerente():
        return render_template('gerente.html')
    @app.route("/produtos")
    def lista_produtos():
        produtos = Produto.listar_todos()  # retorna lista de dicionários
        # se quiser incluir categoria:
        # para cada produto, você pode buscar o nome da categoria ou fazer JOIN no SQL
        return render_template("produtos.html", produtos=produtos)
    @app.route("/api/buscar")
    def api_buscar():
        termo = request.args.get("q", "").strip()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        if termo:
            cursor.execute(
                "SELECT id_produto, nome, preco_unitario, imagem FROM produto WHERE nome LIKE %s AND ativo=TRUE",
                (f"%{termo}%",)
            )
        else:
            cursor.execute("SELECT id_produto, nome, preco_unitario, imagem FROM produto WHERE ativo=TRUE")
        
        produtos = cursor.fetchall()
        cursor.close()
        conn.close()

        # garante que sempre tem imagem
        for p in produtos:
            if not p.get("imagem"):
                p["imagem"] = "static/img/produtos/sem-imagem.png"

        return jsonify(produtos)
