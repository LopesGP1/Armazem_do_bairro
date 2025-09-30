# mysql.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(  # aqui era "conexao.connector.connect", errado
        host="localhost",
        user="root",
        password="senac",
        database="armazem_bd",
        port=3307  # sem aspas, deve ser inteiro
    )

# Testando a conexão
if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Conexão bem-sucedida!")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
