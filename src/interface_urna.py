import tkinter as tk
from tkinter import messagebox
from common import *
from eleicao import *
import csv

class UrnaEletronicaApp:
    def __init__(self, root, urna):
        self.root = root
        self.urna = urna
        self.info_label = None
        self.voto_entry = None

        self.criar_interface_inicial()

    def criar_interface_inicial(self):
        self.limpar_tela()

        self.titulo_label = tk.Label(self.root, text="Digite seu título de eleitor:")
        self.titulo_label.pack()

        self.titulo_entry = tk.Entry(self.root)
        self.titulo_entry.pack()

        self.verificar_button = tk.Button(self.root, text="Verificar Eleitor", command=self.verificar_eleitor)
        self.verificar_button.pack()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def registrar_voto(self, eleitor, numero_do_candidato):
        if numero_do_candidato.strip() == "":
            voto = "branco"
        else:
            candidato_valido = next((c for c in self.urna.get_candidatos() if c.get_numero() == int(numero_do_candidato)), None)
            if candidato_valido:
                voto = candidato_valido.get_numero()
            else:
                self.exibir_erro("Número do candidato inválido. Voto não registrado.")
                return

        self.urna.registrar_voto(eleitor, voto)
        self.gravar_voto_csv(eleitor.get_titulo(), voto)
        print(f"Voto registrado para: {voto}")
        self.limpar_tela()
        self.criar_interface_inicial()

    def gravar_voto_csv(self, eleitor_id, voto):
        try:
            with open("votos.csv", "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([eleitor_id, voto])
            print("Voto salvo com sucesso em CSV.")
        except Exception as e:
            print(f"Erro ao salvar voto: {e}")
            self.exibir_erro("Erro ao salvar voto.")

    def criar_interface_votacao(self, eleitor):
        self.limpar_tela()

        self.info_label = tk.Label(self.root, text=str(eleitor))
        self.info_label.pack()

        self.separador = tk.Label(self.root, text="-" * 50)
        self.separador.pack()

        self.candidatos_label = tk.Label(self.root, text="Candidatos Disponíveis:")
        self.candidatos_label.pack()

        for candidato in self.urna.get_candidatos():
            candidato_info = f"{candidato.get_numero()}: {candidato.get_nome()}"
            tk.Label(self.root, text=candidato_info).pack()

        self.instrucao_label = tk.Label(self.root, text="Para votar em branco, deixe o campo vazio e confirme.")
        self.instrucao_label.pack()

        self.voto_label = tk.Label(self.root, text="Digite o número do candidato:")
        self.voto_label.pack()

        self.voto_entry = tk.Entry(self.root)
        self.voto_entry.pack()

        self.votar_button = tk.Button(self.root, text="Votar", command=lambda: self.registrar_voto(eleitor, self.voto_entry.get()))
        self.votar_button.pack()

    def verificar_eleitor(self):
        try:
            titulo = int(self.titulo_entry.get())
            eleitor = self.urna.get_eleitor(titulo)
            if eleitor:
                self.criar_interface_votacao(eleitor)
            else:
                self.exibir_erro("Eleitor não encontrado nesta urna")
        except ValueError:
            self.exibir_erro("Título inválido")

    def exibir_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)

def carregar_dados():
    eleitores = []
    candidatos = []

    try:
        with open("eleitores.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) == 6:
                    nome = row[0]
                    rg = row[1]
                    cpf = row[2]
                    titulo = int(row[3])  
                    secao = int(row[4]) 
                    zona = int(row[5])
                    print(f"Nome: {nome}, RG: {rg}, CPF: {cpf}, Título: {titulo}, Seção: {secao}, Zona: {zona}")
                    eleitores.append(Eleitor(nome, rg, cpf, titulo, secao, zona)) 
                else:
                    print(f"Formato de dados inválido para o eleitor: {row}")
    except FileNotFoundError:
        print("Arquivo de eleitores não encontrado.")

    try:
        with open("candidatos.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) == 4:
                    nome = row[0]
                    rg = row[1]
                    cpf = row[2]
                    numero = int(row[3])
                    print(f"Nome: {nome}, RG: {rg}, CPF: {cpf}, Número: {numero}")
                    candidatos.append(Candidato(nome, rg, cpf, numero)) 
                else:
                    print(f"Formato de dados inválido para o candidato: {row}")
    except FileNotFoundError:
        print("Arquivo de candidatos não encontrado.")

    return eleitores, candidatos