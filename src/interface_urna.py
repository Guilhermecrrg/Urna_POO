import tkinter as tk
from tkinter import messagebox
from common import *
from eleicao import *
import csv

class UrnaEletronica:
    def __init__(self, master, urna):
        self.master = master
        self.master.config(bg="gray")
        self.master.title("Urna Eletrônica")

        largura, altura = 450, 450
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2
        self.master.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

        self.urna = urna
        self.voto = ""
    
        self.eleitor = None
        self.titulo_entry = None
        self.display_vote_titulo = None
        
        self.iniciar_titulo()

    def iniciar_titulo(self):
        self.clear_window()
        
        self.display_vote_titulo = tk.Entry(self.master, font=('Arial', 24), justify='center')
        self.display_vote_titulo.grid(row=1, column=0, columnspan=4, padx=20, pady=10)
        
        self.adicionar_botoes(voting=False)
        messagebox.showinfo("Instrução", "Por favor, insira o título de eleitor para continuar.")

    def validar_titulo(self):
        try:
            numero_titulo = self.display_vote_titulo.get()
            self.eleitor = self.urna.get_eleitor(int(numero_titulo))
            if self.eleitor:
                if self.urna.eleitor_ja_votou(self.eleitor):
                    messagebox.showinfo("Eleitor Encontrado", f"Eleitor: {numero_titulo} encontrado!")
                    self.display_vote_titulo.delete(0, tk.END)
                    self.adicionar_botoes()
                    messagebox.showinfo("Instrução", "Por favor, insira o numero do candidato para votar.")
                else:
                    messagebox.showwarning("Erro", "Eleitor já votou.")
            else:
                messagebox.showwarning("Erro", "Eleitor não encontrado.")
        except ValueError:
            messagebox.showwarning("Erro", "Número de título inválido.")


    def adicionar_botoes(self, voting=True):
        self.clear_window()

        self.display_vote_titulo = tk.Entry(self.master, font=('Arial', 24), justify='center')
        self.display_vote_titulo.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        frame_b = tk.Frame(self.master, padx=20, pady=20, bg="gray")
        frame_b.grid(row=1, column=1)

        botao_button_config = {
            'font': ('Arial', 18),
            'relief': "solid",
            'borderwidth': 0,
            'highlightthickness': 0
        }

        botao_grid_config = {
            'padx': 5,
            'pady': 5,
            'ipadx': 20,
            'ipady': 20,
            'sticky': "ewsn"
        }

        botao_button_nums = {
            **botao_button_config,
            **{ 'bg': "black", 
                'fg': "white", 
                'anchor': "nw" }
        }

        ## Numeros
        for i in range(3):
            for j in range(3):
                numero = 1 + i * 3 + j
                botao = tk.Button(frame_b, text=str(numero), command=lambda n=numero: self.adicionar_voto(n), **botao_button_nums)
                botao.grid(row=i + 1, column=j, **botao_grid_config)
        botao_zero = tk.Button(frame_b, text='0', command=lambda: self.adicionar_voto(0), **botao_button_nums)
        botao_zero.grid(row=4, column=1, **botao_grid_config)

        if voting:
            ## Botões de ação
            botao_em_branco = tk.Button(frame_b, text='Em Branco', command=self.voto_em_branco, **botao_button_config, bg="white", fg="black")
            botao_em_branco.grid(row=1, column=4, **botao_grid_config,  rowspan=1)

            botao_corrigir = tk.Button(frame_b, text='Corrigir', command=self.corrigir_voto, **botao_button_config, bg="red", fg="black")
            botao_corrigir.grid(row=2, column=4, **botao_grid_config,  rowspan=1)

            botao_confirmar = tk.Button(frame_b, text='Confirmar', command=self.confirmar_voto, **botao_button_config, bg="green", fg="black")
            botao_confirmar.grid(row=3, column=4, **botao_grid_config, rowspan=2)
        else:
            botao_corrigir = tk.Button(frame_b, text='Corrigir', command=self.corrigir_voto, **botao_button_config, bg="red", fg="black")
            botao_corrigir.grid(row=1, column=3, **botao_grid_config,  rowspan=2)

            botao_validar = tk.Button(frame_b, text="Validar", command=self.validar_titulo, **botao_button_config)
            botao_validar.grid(row=3, column=3, **botao_grid_config, rowspan=2)

    def clear_window(self):
        self.corrigir_voto() 
        for widget in self.master.winfo_children():
            widget.destroy()

    def adicionar_voto(self, numero):
        self.voto += str(numero)
        self.display_vote_titulo.delete(0, tk.END)
        self.display_vote_titulo.insert(0, self.voto)

    def confirmar_voto(self):
        if self.voto:
            if self.urna.validar_voto(self.voto):
                self.urna.registrar_voto(self.eleitor, self.voto)
                messagebox.showinfo("Voto Confirmado", f"Você votou no candidato número: {self.voto}")
                self.display_vote_titulo.delete(0, tk.END)
                self.clear_window()
                self.iniciar_titulo()
            else:
                messagebox.showinfo("Atenção", f"Número de candidato invalido: {self.voto}")
        else:
            messagebox.showwarning("Atenção", "Nenhum voto registrado.")
        

    def voto_em_branco(self):
        self.voto = "BRANCO"
        self.urna.registrar_voto(self.eleitor, self.voto)
        messagebox.showinfo("Voto Confirmado", "Você votou em branco")
        self.display_vote_titulo.delete(0, tk.END)
        self.clear_window()
        self.iniciar_titulo()

    def corrigir_voto(self):
        self.voto = ""
        if self.display_vote_titulo and self.display_vote_titulo.winfo_exists():
            self.display_vote_titulo.delete(0, tk.END)

