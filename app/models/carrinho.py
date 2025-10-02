from app.conexao import get_connection
from datetime import datetime

class Carrinho:
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.id_carrinho = self._get_carrinho_aberto()

    def _get_carrinho_aberto(self):
        """Retorna o id do carrinho aberto do usuário, ou cria um novo se não existir"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_carrinho FROM carrinho WHERE id_usuario=%s AND status='aberto'", (self.id_usuario,))
            result = cursor.fetchone()
            if result:
                return result[0]
            # Cria novo carrinho
            cursor.execute("INSERT INTO carrinho (id_usuario) VALUES (%s)", (self.id_usuario,))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def adicionar_item(self, id_produto, quantidade):
        """Adiciona um item ao carrinho"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Verifica se já existe o item no carrinho
            cursor.execute("SELECT id_item, quantidade FROM item_carrinho WHERE id_carrinho=%s AND id_produto=%s",
                           (self.id_carrinho, id_produto))
            result = cursor.fetchone()
            if result:
                id_item, quantidade_atual = result
                nova_quantidade = quantidade_atual + quantidade
                cursor.execute("UPDATE item_carrinho SET quantidade=%s WHERE id_item=%s",
                               (nova_quantidade, id_item))
            else:
                cursor.execute("INSERT INTO item_carrinho (id_carrinho, id_produto, quantidade) VALUES (%s,%s,%s)",
                               (self.id_carrinho, id_produto, quantidade))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def listar_itens(self):
        """Retorna todos os itens do carrinho"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT i.id_item, i.id_produto, i.quantidade, p.nome, p.preco_unitario
                FROM item_carrinho i
                JOIN produto p ON i.id_produto = p.id_produto
                WHERE i.id_carrinho=%s
            """, (self.id_carrinho,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def atualizar_item(self, id_produto, nova_quantidade):
        """Atualiza a quantidade de um item"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE item_carrinho SET quantidade=%s WHERE id_carrinho=%s AND id_produto=%s",
                           (nova_quantidade, self.id_carrinho, id_produto))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def remover_item(self, id_produto):
        """Remove um item do carrinho"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM item_carrinho WHERE id_carrinho=%s AND id_produto=%s",
                           (self.id_carrinho, id_produto))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def finalizar(self):
        """Finaliza o carrinho"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE carrinho SET status='finalizado' WHERE id_carrinho=%s", (self.id_carrinho,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def adicionar_item_sessao(session, produto_id, quantidade=1):

        """Gerencia carrinho temporário na sessão"""
        if 'carrinho' not in session:
            session['carrinho'] = []

        for item in session['carrinho']:
            if item['produto_id'] == produto_id:
                item['quantidade'] += quantidade
                break
        else:
            session['carrinho'].append({
                "produto_id": produto_id,
                "quantidade": quantidade
            })

        session.modified = True

    @staticmethod
    def remover_item_sessao(session, produto_id):
        carrinho = session.get('carrinho', [])
        carrinho = [item for item in carrinho if item['produto_id'] != produto_id]
        session['carrinho'] = carrinho
        session.modified = True