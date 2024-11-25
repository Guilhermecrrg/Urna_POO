import pickle
from common import Eleitor, Candidato

eleitores = [
    Eleitor("João Silva", "123456789", "111.222.333-44", 123456, 1, 101),
    Eleitor("Maria Souza", "987654321", "555.666.777-88", 654321, 1, 101)
]

candidatos = [
    Candidato("Candidato A", "123123123", "999.888.777-66", 10),
    Candidato("Candidato B", "321321321", "888.777.666-55", 20)
]

with open("eleitores.pkl", "wb") as f:
    pickle.dump(eleitores, f)

with open("candidatos.pkl", "wb") as f:
    pickle.dump(candidatos, f)
