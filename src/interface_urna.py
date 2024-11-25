import tkinter as tk
from tkinter import messagebox
from common import *
from eleicao import Urna, Pessoa
import pickle


class UrnaEletronicaApp:
    def __init__(self, root, urna):
        self.root = root
        self.urna = urna
        self.root.title("Urna Eletrônica")
        self.eleitor_atual = None

        self.criar_interface_inicial()

    def criar_interface_inicial(self):
        self.limpar_tela()

        self.titulo_label = tk.Label(self.root, text="Digite o número do título de eleitor:")
        self.titulo_label.pack()

        self.titulo_entry = tk.Entry(self.root)
        self.titulo_entry.pack()

        self.confirmar_button = tk.Button(self.root, text="Confirmar", command=self.verificar_eleitor)
        self.confirmar_button.pack()

    def criar_interface_votacao(self, eleitor):
        self.limpar_tela()

        # Exibe as informações do eleitor
        self.info_label = tk.Label(self.root, text=f"Eleitor: {eleitor.get_nome()}")
        self.info_label.pack()

        # Linha de traços
        self.info_label_2 = tk.Label(self.root, text="------------------------")
        self.info_label_2.pack()

        # Exibe a lista de candidatos (sem botões, apenas lista simples)
        for numero, nome in self.urna.get_candidatos():
            candidato_label = tk.Label(self.root, text=f"{numero} - {nome}")
            candidato_label.pack()

        # Linha de traços após a lista de candidatos
        self.info_label_3 = tk.Label(self.root, text="------------------------")
        self.info_label_3.pack()

        # Texto para orientação, exibido como label
        self.texto_orientacao = tk.Label(self.root, text="Digite o número do candidato:")
        self.texto_orientacao.pack()

        # Campo vazio para digitar o número do candidato
        self.voto_entry = tk.Entry(self.root)
        self.voto_entry.pack()

        # Botão para registrar o voto
        self.votar_button = tk.Button(self.root, text="Votar", command=lambda: self.registrar_voto(eleitor))
        self.votar_button.pack()

    def verificar_eleitor(self):
        try:
            titulo = int(self.titulo_entry.get())
            eleitor = self.urna.get_eleitor(titulo)
            if eleitor:
                self.eleitor_atual = eleitor
                self.criar_interface_votacao(eleitor)
            else:
                self.exibir_erro("Eleitor não encontrado nesta urna")
        except ValueError:
            self.exibir_erro("Título inválido")

    def registrar_voto(self, eleitor):
        try:
            numero_votado = self.voto_entry.get()
            if numero_votado.isdigit():
                numero_votado = int(numero_votado)
                self.urna.registrar_voto(eleitor, numero_votado)
                messagebox.showinfo("Sucesso", "Voto registrado com sucesso!")

                # Limpa a tela e volta para a interface inicial
                self.limpar_tela()
                self.criar_interface_inicial()
            else:
                self.exibir_erro("Número de candidato inválido.")
        except ValueError:
            self.exibir_erro("Número de candidato inválido.")

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def exibir_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)


def carregar_dados():
    with open("eleitores.pkl", "rb") as f:
        eleitores = pickle.load(f)
    with open("candidatos.pkl", "rb") as f:
        candidatos = pickle.load(f)
    return eleitores, candidatos


if __name__ == "__main__":
    eleitores, candidatos = carregar_dados()
    mesario = Pessoa("Mesario Exemplo", "123456789", "123.456.789-00")
    urna = Urna(mesario, secao=1, zona=101, candidatos=candidatos, eleitores=eleitores)

    root = tk.Tk()
    app = UrnaEletronicaApp(root, urna)
    root.mainloop()
