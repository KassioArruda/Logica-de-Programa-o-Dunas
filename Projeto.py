import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

ARQUIVO = "pessoas.json"

# Funções de dados
def carregar_pessoas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_pessoas(lista):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)

# Funções principais
class CadastroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Pessoas")
        self.pessoas = carregar_pessoas()
        self.pessoa_editando = None

        self.criar_widgets()
        self.atualizar_lista()

    def criar_widgets(self):
        # Entradas
        tk.Label(self.root, text="Nome").grid(row=0, column=0)
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(self.root, text="Idade").grid(row=1, column=0)
        self.entry_idade = tk.Entry(self.root)
        self.entry_idade.grid(row=1, column=1)

        tk.Label(self.root, text="Profissão").grid(row=2, column=0)
        self.entry_profissao = tk.Entry(self.root)
        self.entry_profissao.grid(row=2, column=1)

        self.btn_salvar = tk.Button(self.root, text="Salvar", command=self.salvar_pessoa)
        self.btn_salvar.grid(row=3, columnspan=2, pady=5)

        # Filtro de ordenação
        tk.Label(self.root, text="Ordenar por:").grid(row=4, column=0)
        self.ordenar_por = tk.StringVar(value="nome")
        ttk.Combobox(self.root, textvariable=self.ordenar_por,
                     values=["nome", "idade", "profissao"],
                     state="readonly").grid(row=4, column=1)

        # Campo de busca
        tk.Label(self.root, text="Buscar por nome/profissão:").grid(row=5, column=0)
        self.entry_busca = tk.Entry(self.root)
        self.entry_busca.grid(row=5, column=1)

        # Botão de atualizar
        tk.Button(self.root, text="Atualizar Lista", command=self.atualizar_lista).grid(row=6, columnspan=2, pady=5)

        # Tabela
        self.tabela = ttk.Treeview(self.root, columns=("Nome", "Idade", "Profissão"), show="headings")
        for col in ("Nome", "Idade", "Profissão"):
            self.tabela.heading(col, text=col)
        self.tabela.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        self.tabela.bind("<Double-1>", self.selecionar_pessoa)

        # Botões editar/excluir
        tk.Button(self.root, text="Editar Selecionado", command=self.editar_pessoa).grid(row=8, column=0, pady=5)
        tk.Button(self.root, text="Excluir Selecionado", command=self.excluir_pessoa).grid(row=8, column=1, pady=5)

    def salvar_pessoa(self):
        nome = self.entry_nome.get().strip()
        idade = self.entry_idade.get().strip()
        profissao = self.entry_profissao.get().strip()

        if not nome or not idade or not profissao:
            messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
            return

        try:
            idade = int(idade)
        except ValueError:
            messagebox.showerror("Idade inválida", "Idade precisa ser um número.")
            return

        nova = {"nome": nome, "idade": idade, "profissao": profissao}

        if self.pessoa_editando is not None:
            self.pessoas[self.pessoa_editando] = nova
            self.pessoa_editando = None
        else:
            self.pessoas.append(nova)

        salvar_pessoas(self.pessoas)
        self.limpar_campos()
        self.atualizar_lista()

    def atualizar_lista(self):
        termo = self.entry_busca.get().lower()
        criterio = self.ordenar_por.get()
        filtradas = [p for p in self.pessoas if termo in p["nome"].lower() or termo in p["profissao"].lower()]
        ordenadas = sorted(filtradas, key=lambda p: p[criterio])

        self.tabela.delete(*self.tabela.get_children())
        for p in ordenadas:
            self.tabela.insert("", "end", values=(p["nome"], p["idade"], p["profissao"]))

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)
        self.entry_profissao.delete(0, tk.END)

    def selecionar_pessoa(self, event):
        item = self.tabela.selection()
        if item:
            dados = self.tabela.item(item)["values"]
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, dados[0])
            self.entry_idade.delete(0, tk.END)
            self.entry_idade.insert(0, dados[1])
            self.entry_profissao.delete(0, tk.END)
            self.entry_profissao.insert(0, dados[2])
            for i, p in enumerate(self.pessoas):
                if p["nome"] == dados[0] and str(p["idade"]) == str(dados[1]) and p["profissao"] == dados[2]:
                    self.pessoa_editando = i
                    break

    def editar_pessoa(self):
        if self.pessoa_editando is not None:
            self.salvar_pessoa()
        else:
            messagebox.showinfo("Seleção", "Clique duas vezes em um item da lista para editar.")

    def excluir_pessoa(self):
        item = self.tabela.selection()
        if item:
            dados = self.tabela.item(item)["values"]
            self.pessoas = [p for p in self.pessoas if not (
                p["nome"] == dados[0] and str(p["idade"]) == str(dados[1]) and p["profissao"] == dados[2]
            )]
            salvar_pessoas(self.pessoas)
            self.atualizar_lista()
        else:
            messagebox.showinfo("Seleção", "Selecione um item para excluir.")

# Iniciar app
if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroApp(root)
    root.mainloop()
    