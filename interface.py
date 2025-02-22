import tkinter as tk
from tkinter import font, messagebox
from tkinter import font as tkfont
from utils import salvar_usuario, autenticar_usuario, salvar_senha_site, visualizar_senhas_usuario, obter_senha_por_id, editar_senha, excluir_senha, abrir_janela_edicao

# Função para alternar a exibição da senha
def alternar_ou_ocultar(entry_senha, btn_mostrar_ou_ocultar):
    if entry_senha.cget("show") == "*":
        entry_senha.config(show="")  # Mostrar senha
        btn_mostrar_ou_ocultar.config(text="Ocultar")
    else:
        entry_senha.config(show="*")  # Ocultar senha
        btn_mostrar_ou_ocultar.config(text="Mostrar")

# Função para gerar senha aleatória
def gerar_senha_completa(tamanho):
    import random
    import string
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

# Função para alternar entre frames com transições
def alternar_frame(frame_atual, frame_novo):
    frame_atual.pack_forget()
    frame_novo.pack(fill="both", expand=True)

# Função para a janela principal com animações e transições de cor
def janela_principal(nome_usuario):
    janela = tk.Tk()
    janela.title(f"Gerenciador de Senhas - {nome_usuario}")
    janela.geometry("600x400")
    janela.configure(bg="#f0f0f0")
    janela.resizable(False, False)

    fonte_titulo = tkfont.Font(family="Helvetica", size=24, weight="bold")
    fonte_botao = tkfont.Font(family="Helvetica", size=12, weight="bold")
    fonte_texto = tkfont.Font(family="Helvetica", size=12)

    
    frame_principal = tk.Frame(janela, padx=30, pady=30, bg="#f0f0f0")
    frame_principal.pack(fill="both", expand=True)

    tk.Label(frame_principal, text=f"Bem-vindo, {nome_usuario}!", font=fonte_titulo, fg="#333", bg="#f0f0f0").pack(pady=20)

    
    def on_enter(btn, color):
        btn.config(bg=color)

    def on_leave(btn, color):
        btn.config(bg=color)

    tk.Button(frame_principal, text="Visualizar Senhas", command=lambda: visualizar_senhas_janela(nome_usuario), font=fonte_botao, bg="#4CAF50", fg="#fff", relief="flat", padx=20, pady=10).pack(pady=10)
    tk.Button(frame_principal, text="Adicionar Senha", command=lambda: adicionar_senha_janela(nome_usuario), font=fonte_botao, bg="#2196F3", fg="#fff", relief="flat", padx=20, pady=10).pack(pady=10)
    tk.Button(frame_principal, text="Gerar Senha", command=lambda: gerar_senha_janela(), font=fonte_botao, bg="#FFC107", fg="#fff", relief="flat", padx=20, pady=10).pack(pady=10)
    tk.Button(frame_principal, text="Sair", command=janela.quit, font=fonte_botao, bg="#FF5722", fg="#fff", relief="flat", padx=20, pady=10).pack(pady=10)

    janela.mainloop()

# Função para a janela de geração de senha com transições de animação
def gerar_senha_janela():
    janela = tk.Toplevel()
    janela.title("Gerar Senha")
    janela.geometry("400x250")
    janela.configure(bg="#f5f5f5")

    tk.Label(janela, text="Gerar Senha", font=("Arial", 18, "bold"), bg="#f5f5f5").pack(pady=10)

    tk.Label(janela, text="Tamanho da Senha", font=("Arial", 12), bg="#f5f5f5").pack(pady=5)
    entry_tamanho = tk.Entry(janela, font=("Arial", 12), width=20)
    entry_tamanho.insert(0, "16")
    entry_tamanho.pack()

    entry_senha = tk.Entry(janela, font=("Arial", 12), width=30)
    entry_senha.pack(pady=10)

    def gerar_senha():
        try:
            tamanho = int(entry_tamanho.get())
            if tamanho < 8:
                raise ValueError("O tamanho deve ser no mínimo 8.")
            senha = gerar_senha_completa(tamanho)
            entry_senha.delete(0, tk.END)
            entry_senha.insert(0, senha)
        except ValueError as e:
            messagebox.showerror("Erro", f"Tamanho inválido: {e}")

    def copiar_senha():
        senha = entry_senha.get()
        if senha:
            janela.clipboard_clear()
            janela.clipboard_append(senha)
            messagebox.showinfo("Sucesso", "Senha copiada!")

    tk.Button(janela, text="Gerar", command=gerar_senha, font=("Arial", 12), bg="#4CAF50", fg="#fff").pack(pady=10)
    tk.Button(janela, text="Copiar", command=copiar_senha, font=("Arial", 12), bg="#2196F3", fg="#fff").pack(pady=5)

# Função para adicionar uma senha com animações
def adicionar_senha_janela(nome_usuario):
    janela = tk.Toplevel()
    janela.title("Adicionar Senha")
    janela.geometry("400x300")
    janela.configure(bg="#f0f0f0")

    tk.Label(janela, text="Site:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    entry_site = tk.Entry(janela, font=("Arial", 12))
    entry_site.pack()

    tk.Label(janela, text="Usuário:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    entry_usuario = tk.Entry(janela, font=("Arial", 12))
    entry_usuario.pack()

    tk.Label(janela, text="Senha:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    entry_senha = tk.Entry(janela, font=("Arial", 12))
    entry_senha.pack()

    def salvar():
        site = entry_site.get()
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        if salvar_senha_site(nome_usuario, site, usuario, senha):
            messagebox.showinfo("Sucesso", "Senha salva!")
            janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar, font=("Arial", 12), bg="#4CAF50", fg="#fff").pack(pady=20)


# Função para visualizar senhas com efeito de degradê e animações
def visualizar_senhas_janela(nome_usuario):
    senhas = visualizar_senhas_usuario(nome_usuario)

    janela = tk.Toplevel()
    janela.title("Visualizar Senhas")
    janela.geometry("600x600")
    janela.configure(bg="#ffffff")

    if senhas:
        frame_senhas = tk.Frame(janela, bg="#ffffff")
        frame_senhas.pack(fill="both", expand=True, padx=20, pady=20)

        for senha in senhas:
            senha_id, site, usuario_site, senha_site = senha

            frame = tk.Frame(frame_senhas, bg="#f5f5f5", relief="flat", bd=2, highlightthickness=0)
            frame.pack(fill="x", padx=10, pady=10)

            tk.Label(frame, text=f"Site: {site}", font=("Arial", 12, "bold"), bg="#f5f5f5", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=5)
            tk.Label(frame, text=f"Usuário: {usuario_site}", font=("Arial", 12), bg="#f5f5f5", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=5)

            entry_senha = tk.Entry(frame, font=("Arial", 12), show="*", relief="flat", bd=0, highlightthickness=1, highlightbackground="#FF9800", fg="#FF9800")
            entry_senha.grid(row=2, column=0, sticky="w", padx=10, pady=5)
            entry_senha.insert(0, senha_site)

            btn_mostrar_ou_ocultar = tk.Button(
                frame,
                text="Mostrar",
                command=lambda entry=entry_senha: alternar_ou_ocultar(entry, btn_mostrar_ou_ocultar),
                font=("Arial", 10),
                bg="#FF9800",
                fg="white",
                relief="raised",
                bd=2,
                padx=10,
                pady=5,
                activebackground="#FF5722",
            )
            btn_mostrar_ou_ocultar.grid(row=2, column=1, padx=10, pady=5)

            # Botão Editar
            btn_editar = tk.Button(
                frame,
                text="Editar",
                command=lambda id_senha=senha_id, site=site, usuario=usuario_site, senha=senha_site: abrir_janela_edicao(id_senha, site, usuario, senha),
                font=("Arial", 10),
                bg="#4CAF50",
                fg="white",
                relief="raised",
                bd=2,
                padx=10,
                pady=5,
                activebackground="#388E3C",
            )
            btn_editar.grid(row=3, column=0, padx=10, pady=5)


            # Botão Excluir
            btn_excluir = tk.Button(
                frame,
                text="Excluir",
                command=lambda id_senha=senha_id: excluir_senha(id_senha),
                font=("Arial", 10),
                bg="#F44336",
                fg="white",
                relief="raised",
                bd=2,
                padx=10,
                pady=5,
                activebackground="#D32F2F",
            )
            btn_excluir.grid(row=3, column=1, padx=10, pady=5)

    else:
        tk.Label(
            janela,
            text="Nenhuma senha encontrada!",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="red",
        ).pack(pady=20)

    fechar_btn = tk.Button(
        janela,
        text="Fechar",
        command=janela.destroy,
        font=("Arial", 12, "bold"),
        bg="#555",
        fg="white",
        relief="raised",
        bd=2,
        padx=20,
        pady=10,
        activebackground="#333",
    )
    fechar_btn.pack(pady=20)

    janela.mainloop()



# Inicialização do programa
def main():
    janela_principal("UsuárioTeste")

if __name__ == "__main__":
    main()
