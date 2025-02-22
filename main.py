import tkinter as tk
from tkinter import messagebox
from tkinter import font
from utils import autenticar_usuario, salvar_usuario
from interface import janela_principal

def janela_login():
    """Exibe a janela de login com design moderno, tema escuro e botões arredondados com transição."""
    def realizar_login():
        nome_usuario = entry_nome_usuario.get()
        senha = entry_senha.get()
        if autenticar_usuario(nome_usuario, senha):
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            janela.destroy()  # Fecha a janela de login
            janela_principal(nome_usuario)  # Abre a janela principal
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def realizar_cadastro():
        nome_usuario = entry_nome_usuario.get()
        senha = entry_senha.get()

        # Verificar se os campos estão preenchidos
        if nome_usuario == "" or senha == "":
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return  # Não continuar com o cadastro se os campos estiverem vazios

        # Tentar salvar o usuário no banco de dados
        if salvar_usuario(nome_usuario, senha):
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar o usuário.")

    janela = tk.Tk()
    janela.title("Login")
    janela.geometry("500x470")  # Aumentei o tamanho da janela
    janela.configure(bg="#181818")  # Tema escuro

    # Fonte
    fonte_titulo = font.Font(family="Helvetica", size=24, weight="bold")
    fonte_label = font.Font(family="Helvetica", size=12)
    fonte_botao = font.Font(family="Helvetica", size=12, weight="bold")

    # Frame principal
    frame = tk.Frame(janela, padx=30, pady=30, bg="#181818")
    frame.pack(expand=True)

    # Título
    tk.Label(frame, text="Login", font=fonte_titulo, fg="#FFEB3B", bg="#181818").pack(pady=20)

    # Campos de entrada
    tk.Label(frame, text="Usuário", font=fonte_label, fg="white", bg="#181818").pack(pady=5)
    entry_nome_usuario = tk.Entry(frame, font=fonte_label, bg="#333333", fg="white", bd=2, relief="solid")
    entry_nome_usuario.pack(pady=10, fill="x", ipadx=5, ipady=5)

    tk.Label(frame, text="Senha", font=fonte_label, fg="white", bg="#181818").pack(pady=5)
    entry_senha = tk.Entry(frame, font=fonte_label, bg="#333333", fg="white", bd=2, relief="solid", show="*")
    entry_senha.pack(pady=10, fill="x", ipadx=5, ipady=5)

    # Função para mudar a cor do botão ao passar o mouse
    def on_enter(b):
        b['background'] = '#45a049'  # Cor de fundo ao passar o mouse

    def on_leave(b):
        b['background'] = '#4CAF50'  # Cor de fundo normal

    # Botão de login
    login_button = tk.Button(frame, text="Login", command=realizar_login, font=fonte_botao, bg="#4CAF50", fg="white", relief="flat", bd=2,
                             height=2, width=20, highlightthickness=0, activebackground="#45a049")
    login_button.pack(pady=15)
    login_button.bind("<Enter>", lambda e: on_enter(login_button))
    login_button.bind("<Leave>", lambda e: on_leave(login_button))

    # Botão para ir para cadastro
    cadastro_button = tk.Button(frame, text="Cadastrar", command=realizar_cadastro, font=fonte_botao, bg="#2196F3", fg="white", relief="flat", bd=2,
                                height=2, width=20, highlightthickness=0, activebackground="#1976D2")
    cadastro_button.pack(pady=5)
    cadastro_button.bind("<Enter>", lambda e: on_enter(cadastro_button))
    cadastro_button.bind("<Leave>", lambda e: on_leave(cadastro_button))

    janela.mainloop()

if __name__ == "__main__":
    janela_login()
