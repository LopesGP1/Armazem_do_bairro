from app.models.produto import Produto

produtos = Produto.listar_todos()
for p in produtos:
    print(f"{p['id_produto']} - {p['nome']} - {p.get('preco_unitario', 0.0)} - {p.get('imagem', 'sem-imagem.png')}")
