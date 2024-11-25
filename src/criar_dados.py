import csv
from common import *

eleitores = [
    Eleitor("João Silva", "123456789", "111.222.333-44", 123456, 1, 101),
    Eleitor("Maria Souza", "987654321", "555.666.777-88", 654321, 1, 101)
]

candidatos = [
    Candidato("Candidato A", "123123123", "999.888.777-66", 10),
    Candidato("Candidato B", "321321321", "888.777.666-55", 20)
]

with open("eleitores.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Nome", "RG", "CPF", "Título", "Seção", "Zona"])
    for eleitor in eleitores:
        writer.writerow([eleitor.get_nome(), eleitor.get_RG(), eleitor.get_CPF(),
                         eleitor.get_titulo(), eleitor.get_secao(), eleitor.get_zona()])

with open("candidatos.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Nome", "RG", "CPF", "Número"])
    for candidato in candidatos:
        writer.writerow([candidato.get_nome(), candidato.get_RG(), candidato.get_CPF(), candidato.get_numero()])
