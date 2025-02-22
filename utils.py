import bcrypt
import mysql.connector
from mysql.connector import Error
from tkinter import font, messagebox
import random
import string
import tkinter as tk

# Função para conectar ao banco de dados
def criar_conexao():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='E2004!zo',  
            database='GerenciadorSenhas'
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida com o banco de dados!")
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def fechar_conexao(conexao):
    """Fecha a conexão com o banco de dados."""
    if conexao.is_connected():
        conexao.close()
        print("Conexão com o banco de dados encerrada.")

# Função para criptografar a senha
def criptografar_senha(senha):
    # Gerar um salt e criptografar a senha
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return senha_hash

# Função para verificar se a senha fornecida corresponde ao hash armazenado
def verificar_senha(senha, senha_hash):
    senha_bytes = senha.encode('utf-8') 
    senha_hash_bytes = senha_hash.encode('utf-8')  
    return bcrypt.checkpw(senha_bytes, senha_hash_bytes)


# Função para autenticar usuário no login
def autenticar_usuario(nome_usuario, senha):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        query = "SELECT * FROM usuarios WHERE nome_usuario = %s"
        cursor.execute(query, (nome_usuario,))
        resultado = cursor.fetchone()
        
        if resultado:
            senha_hash = resultado[2]  
            if verificar_senha(senha, senha_hash):  
                fechar_conexao(conexao)
                return True
            else:
                print("Senha incorreta!")
        else:
            print("Usuário não encontrado!")
        
        fechar_conexao(conexao)
    return False


# Função para salvar um novo usuário
def salvar_usuario(nome_usuario, senha):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()

        # Certifique-se de que a senha esteja em bytes antes de gerar o hash
        senha_bytes = senha.encode('utf-8')
        senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')

        query = "INSERT INTO usuarios (nome_usuario, senha_hash) VALUES (%s, %s)"
        try:
            cursor.execute(query, (nome_usuario, senha_hash))
            conexao.commit()
            print("Usuário cadastrado com sucesso!")
            fechar_conexao(conexao)
            return True
        except Error as e:
            print(f"Erro ao cadastrar o usuário: {e}")
            fechar_conexao(conexao)
            return False
    return False

# Função para gerar uma senha segura
def gerar_senha_completa(tamanho):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for i in range(tamanho))
    return senha

# Função para salvar uma senha para um site específico
def salvar_senha_site(nome_usuario, nome_site, nome_usuario_site, senha):
    conexao = criar_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            
            # Obter o ID do usuário com base no nome de usuário
            cursor.execute("SELECT id FROM usuarios WHERE nome_usuario = %s", (nome_usuario,))
            resultado = cursor.fetchone()
            if not resultado:
                print("Usuário não encontrado!")
                return False

            id_usuario = resultado[0]

            # Inserir a senha no banco de dados
            query = """
            INSERT INTO senhas (id_usuario, nome_site, nome_usuario_site, senha)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_usuario, nome_site, nome_usuario_site, senha))
            conexao.commit()
            print(f"Senha para o site {nome_site} salva com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao salvar a senha: {e}")
            return False
        finally:
            fechar_conexao(conexao)
    return False


# Função para visualizar as senhas de um usuário
def visualizar_senhas_usuario(nome_usuario):
    conexao = criar_conexao()
    if conexao:
        cursor = conexao.cursor()
        
        # Buscando o ID do usuário pelo nome de usuário
        cursor.execute("SELECT id FROM usuarios WHERE nome_usuario = %s", (nome_usuario,))
        usuario = cursor.fetchone()
        
        if usuario:
            id_usuario = usuario[0]
            # Selecionar ID, nome_site, nome_usuario_site, senha
            query = "SELECT id, nome_site, nome_usuario_site, senha FROM senhas WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
            senhas = cursor.fetchall()  # Lista de tuplas com 4 valores
        else:
            senhas = []

        fechar_conexao(conexao)
        return senhas
    return []


# Função para editar uma senha
def editar_senha(senha_id, novo_site, novo_usuario, nova_senha):
    conn = criar_conexao()
    if conn:
        try:
            cursor = conn.cursor()

            # Atualizar a senha no banco de dados
            cursor.execute("""
                UPDATE senhas
                SET nome_site = %s, nome_usuario_site = %s, senha = %s, atualizado_em = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (novo_site, novo_usuario, nova_senha, senha_id))

            # Confirmar a transação
            conn.commit()

            if cursor.rowcount > 0:
                print("Senha editada com sucesso.")
                resultado = True
            else:
                print("Nenhuma linha foi atualizada. Verifique o ID.")
                resultado = False

            # Fechar o cursor e conexão
            cursor.close()
            conn.close()

            return resultado

        except Error as e:
            print(f"Erro ao editar senha: {e}")
            return False
    return False

def abrir_janela_edicao(senha_id, site_atual, usuario_atual, senha_atual):
    janela_edicao = tk.Toplevel()
    janela_edicao.title("Editar Senha")
    janela_edicao.geometry("400x300")
    janela_edicao.configure(bg="#f0f0f0")

    tk.Label(janela_edicao, text="Editar Senha", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    # Campo para editar o site
    tk.Label(janela_edicao, text="Site:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    entry_site = tk.Entry(janela_edicao, font=("Arial", 12))
    entry_site.insert(0, site_atual)
    entry_site.pack()

    # Campo para editar o usuário
    tk.Label(janela_edicao, text="Usuário:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    entry_usuario = tk.Entry(janela_edicao, font=("Arial", 12))
    entry_usuario.insert(0, usuario_atual)
    entry_usuario.pack()

    # Campo para editar a senha
    tk.Label(janela_edicao, text="Senha:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    entry_senha = tk.Entry(janela_edicao, font=("Arial", 12))
    entry_senha.insert(0, senha_atual)
    entry_senha.pack()

    # Função para salvar as alterações
    def salvar_edicao():
        novo_site = entry_site.get()
        novo_usuario = entry_usuario.get()
        nova_senha = entry_senha.get()

        if editar_senha(senha_id, novo_site, novo_usuario, nova_senha):
            messagebox.showinfo("Sucesso", "Senha editada com sucesso!")
            janela_edicao.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível editar a senha.")

    tk.Button(janela_edicao, text="Salvar", command=salvar_edicao, font=("Arial", 12), bg="#4CAF50", fg="#fff").pack(pady=20)

    tk.Button(janela_edicao, text="Cancelar", command=janela_edicao.destroy, font=("Arial", 12), bg="#FF5722", fg="#fff").pack(pady=10)


# Função para excluir uma senha no banco de dados
def excluir_senha(senha_id):
    conn = criar_conexao()
    if conn:
        try:
            cursor = conn.cursor()

            # Excluir a senha do banco de dados
            cursor.execute("DELETE FROM senhas WHERE id = %s", (senha_id,))

            # Confirmar a transação
            conn.commit()

            if cursor.rowcount > 0:
                print("Senha excluída com sucesso.")
                resultado = True
            else:
                print("Nenhuma linha foi excluída. Verifique o ID.")
                resultado = False

            # Fechar o cursor e conexão
            cursor.close()
            conn.close()

            return resultado

        except Error as e:
            print(f"Erro ao excluir senha: {e}")
            return False
    return False


def obter_senha_por_id(senha_id):
    """Obtém detalhes de uma senha pelo ID."""
    conexao = criar_conexao()
    try:
        cursor = conexao.cursor(dictionary=True)
        query = "SELECT * FROM senhas WHERE id = %s"
        cursor.execute(query, (senha_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao obter senha: {e}")
        return None
    finally:
        conexao.close()


