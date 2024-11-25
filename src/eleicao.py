import pickle
from datetime import date
from typing import List
from common import Pessoa, Eleitor, Candidato

class Urna:
    def __init__(self, mesario: Pessoa, secao: int, zona: int,
                 candidatos: List[Candidato], eleitores: List[Eleitor]):
        self.mesario = mesario
        self.__secao = secao
        self.__zona = zona
        self.__nome_arquivo = f'{self.__zona}_{self.__secao}.pkl'
        self.__candidatos = candidatos
        self.__eleitores = [eleitor for eleitor in eleitores if eleitor.zona == zona and eleitor.secao == secao]
        self.__eleitores_presentes: List[Eleitor] = []
        
        self.__votos = {candidato.get_numero(): 0 for candidato in self.__candidatos}
        self.__votos['BRANCO'] = 0
        self.__votos['NULO'] = 0

        with open(self.__nome_arquivo, 'wb') as arquivo:
            pickle.dump(self.__votos, arquivo)

    def get_eleitor(self, titulo: int):
        for eleitor in self.__eleitores:
            if eleitor.get_titulo() == titulo:
                return eleitor
        return False

    def registrar_voto(self, eleitor: Eleitor, n_cand: int):
        if eleitor in self.__eleitores_presentes:
            raise ValueError("Eleitor já votou.")
        
        self.__eleitores_presentes.append(eleitor)

        if n_cand in self.__votos:
            self.__votos[n_cand] += 1
        elif n_cand == 0:
            self.__votos['BRANCO'] += 1
        else:
            self.__votos['NULO'] += 1

        with open(self.__nome_arquivo, 'wb') as arquivo:
            pickle.dump(self.__votos, arquivo)

    def zeresima(self):
        votos_zerados = {key: 0 for key in self.__votos}
        with open('zeresima_' + self.__nome_arquivo, 'wb') as arquivo:
            pickle.dump(votos_zerados, arquivo)
    
    def get_candidatos(self):
        return [(candidato.get_numero(), candidato.get_nome()) for candidato in self.__candidatos]

    def encerrar(self):
        with open('final_' + self.__nome_arquivo, 'wb') as arquivo:
            pickle.dump(self.__votos, arquivo)

    def __str__(self):
        info = f'Urna da seção {self.__secao}, zona {self.__zona} - Mesário: {self.mesario}\n'
        data_atual = date.today()
        info += f'Data: {data_atual.ctime()}\n'

        for k, v in self.__votos.items():
            info += f'Candidato {k} = {v} votos\n'

        return info
