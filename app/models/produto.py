from datetime import datetime
from app.conexao import get_connection


class Produto:
    def __init__(self,nome,id_categoria,preco_unitario,unidade_medida,estoque,descricao=None,imagem=None,ativo=True,id_produto=None,data_cadastro=None):
        self.id_produto= id_categoria
        self.nome=nome
        self.id_categoria = id_categoria
        self.preco_unitario = preco_unitario
        self.unidade_medida = unidade_medida
        self.estoque = estoque
        self.descricao = descricao
        self.imagem = imagem
        self.ativo = ativo 
        self.data_cadastro = data_cadastro or datetime.now()
    def salvarNoBancoDeDados(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO produto (nome,id_categoria,preco_unitario,unidade_medida,estoque,descricao,ativo,imagem)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """,(self.nome,self.id_categoria,self.preco_unitario,self.unidade_medida,self.estoque,self.descricao,self.ativo,self.imagem))
            conn.commit()
            self.id_produto = cursor.lastrowid
        except Exception as e:
            print(f"Erro ao salvar produto:{e}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def listar_todos():
        """Retorna todos os produtos ativos com imagem padrão se estiver vazia"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM produto WHERE ativo=TRUE")
            produtos = cursor.fetchall()
            print(produtos) 
            for p in produtos:
                if 'imagem' not in p or not p['imagem']:
                    p['imagem'] = 'sem-imagem.png'
                if 'preco_unitario' not in p:
                    p['preco_unitario'] = 0.0  
            return produtos
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def buscar_por_id(id_produto):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM produto WHERE id_produto=%s", (id_produto,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
    def atualizar(self):
            """Atualiza os dados do produto"""
            if not self.id_produto:
                raise ValueError("Produto precisa ter id para atualizar")
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE produto
                    SET nome=%s, id_categoria=%s, preco_unitario=%s, unidade_medida=%s, estoque=%s,
                        descricao=%s, ativo=%s, imagem=%s
                    WHERE id_produto=%s
                """, (self.nome, self.id_categoria, self.preco_unitario, self.unidade_medida, self.estoque,
                    self.descricao, self.ativo, self.imagem, self.id_produto))
                conn.commit()
            finally:
                cursor.close()
                conn.close()
    @staticmethod
    def deletar(id_produto):
        """Remove um produto (define como inativo)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE produto SET ativo=FALSE WHERE id_produto=%s", (id_produto,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    # Testa listar todos os produtos
    produtos = Produto.listar_todos()
    for p in produtos:
        print(f"ID: {p['id_produto']}, Nome: {p['nome']}, Preço: {p.get('preco_unitario', 0.0)}, Imagem: {p.get('imagem', 'sem-imagem.png')}")
