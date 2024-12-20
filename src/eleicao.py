import csv
from datetime import date
from common import *

class Urna:
    def __init__(self, mesario, secao, zona, candidatos, eleitores):
        self.mesario = mesario
        self.secao = secao
        self.zona = zona
        self.candidatos = candidatos
        self.eleitores = eleitores
        self.votos = self.carregar_dados_csv()


    def eleitor_ja_votou(self, eleitor):
        print(self.votos)
        eleitor_id = eleitor.get_titulo()
        if eleitor_id not in self.votos:
            return True
        return False

    def registrar_voto(self, eleitor, voto):
        eleitor_id = eleitor.get_titulo()
        if self.eleitor_ja_votou(eleitor):
            self.votos[eleitor_id] = voto
            self.gravar_dados_csv()
            return True
        else:
            return False

    def validar_voto(self, voto):
        for candidato in self.get_candidatos():
            if int(voto) == candidato.get_numero():
                return True
            elif voto == "BRANCO":
                return True
        return False

    def gravar_dados_csv(self):
        with open("votos.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Eleitor ID", "Voto"])
            for eleitor_id, voto in self.votos.items():
                writer.writerow([eleitor_id, voto])

    def carregar_dados_csv(self):
        try:
            with open("votos.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)
                return {int(rows[0]): rows[1] for rows in reader}
        except FileNotFoundError:
            return {}

    def get_eleitor(self, titulo: int):
        for eleitor in self.eleitores:
            if eleitor.get_titulo() == titulo:
                return eleitor
        return False

    def get_candidatos(self):
        return self.candidatos

    def get_votos(self):
        return self.votos

    def __str__(self):
        info = f'Urna da seção {self.secao}, zona {self.zona} Mesario {self.mesario}\n'
        data_atual = date.today()
        info += f'{data_atual.ctime()}\n'
        for k, v in self.votos.items():
            info += f'Candidato {v} = {k} votos\n'
        return info
