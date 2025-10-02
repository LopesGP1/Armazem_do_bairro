from flask import render_template, jsonify, request, redirect, url_for, session,flash
from app.models.produto import Produto
from app.models.carrinho import Carrinho   # importa sua classe
from app.conexao import get_connection
from app.conexao import get_connection

def init_routes(app):

    # Home
    @app.route('/')
    def home():
        return render_template('home.html')

    # ==========================
    # LOGIN / LOGOUT
    # ==========================
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE email=%s AND senha=%s", (email, senha))
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()

            if usuario:
                # guarda na sessão
                session['usuario_id'] = usuario['id_usuario']
                session['usuario_nome'] = usuario['nome_completo']

                # migra carrinho da sessão -> banco
                carrinho_temp = session.get('carrinho', [])
                if carrinho_temp:
                    carrinho = Carrinho(usuario['id_usuario'])
                    for item in carrinho_temp:
                        carrinho.adicionar_item(item['produto_id'], item['quantidade'])
                    session.pop('carrinho', None)

                return redirect(url_for('home'))
            else:
                return "Usuário ou senha incorretos"
        
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))

    # ==========================
    # CARRINHO
    # ==========================
    @app.route('/adicionar/<int:produto_id>')
    def adicionar(produto_id):
        if 'usuario_id' in session:  # logado -> banco
            carrinho = Carrinho(session['usuario_id'])
            carrinho.adicionar_item(produto_id, 1)
        else:  # não logado -> sessão
            if 'carrinho' not in session:
                session['carrinho'] = []
            
            # verifica se já existe
            found = False
            for item in session['carrinho']:
                if item['produto_id'] == produto_id:
                    item['quantidade'] += 1
                    found = True
                    break
            if not found:
                session['carrinho'].append({'produto_id': produto_id, 'quantidade': 1})

            session.modified = True

        return redirect(url_for('carrinho'))

    @app.route('/carrinho')
    def carrinho():
        itens = []

        if 'usuario_id' in session:
            # Usuário logado → pega itens do banco
            carrinho = Carrinho(session['usuario_id'])
            itens = carrinho.listar_itens()
        else:
            # Usuário não logado → pega itens da sessão
            carrinho_temp = session.get('carrinho', [])
            if carrinho_temp:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                for item in carrinho_temp:
                    cursor.execute(
                        "SELECT id_produto, nome, preco_unitario, imagem FROM produto WHERE id_produto=%s",
                        (item['produto_id'],)
                    )
                    produto = cursor.fetchone()
                    if produto:
                        produto['quantidade'] = item['quantidade']
                        itens.append(produto)
                cursor.close()
                conn.close()

        return render_template('carrinho.html', produtos=itens)

    # ==========================
    # CLIENTE
    # ==========================
    @app.route('/cliente')
    def cliente():
        produtos = Produto.listar_todos()
        return render_template('cliente.html', produtos=produtos)

    # FUNCIONÁRIO
    @app.route('/funcionario')
    def funcionario():
        return render_template('funcionario.html')
    # GERENTE
    @app.route('/gerente')
    def gerente():
        return render_template('gerente.html')

    # LISTA PRODUTOS
    @app.route("/produtos")
    def lista_produtos():
        produtos = Produto.listar_todos()
        return render_template("produtos.html", produtos=produtos)

    # API BUSCAR
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

        for p in produtos:
            if not p.get("imagem"):
                p["imagem"] = "static/img/produtos/sem-imagem.png"

        return jsonify(produtos)
    @app.route('/adicionar_carrinho/<int:id_produto>', methods=['POST'])
    def adicionar_carrinho(id_produto):
        quantidade = int(request.form.get("quantidade", 1))

        if 'usuario_id' in session:
            carrinho = Carrinho(session['usuario_id'])
            carrinho.adicionar_item(id_produto, quantidade)
        else:
            Carrinho.adicionar_item_sessao(session, id_produto, quantidade)

        flash("Produto adicionado ao carrinho!")
        return redirect(url_for("carrinho"))
    @app.route("/api/adicionar_carrinho", methods=["POST"])
    def api_adicionar_carrinho():
        data = request.get_json()
        produto_id = data.get("id_produto")
        quantidade = data.get("quantidade", 1)

        if 'usuario_id' in session:
            carrinho = Carrinho(session['usuario_id'])
            carrinho.adicionar_item(produto_id, quantidade)
        else:
            Carrinho.adicionar_item_sessao(session, produto_id, quantidade)

        return jsonify({"success": True})


   