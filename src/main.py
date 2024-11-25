from interface_urna import *


def carregar_eleitores_candidatos():
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

if __name__ == "__main__":
  eleitores, candidatos = carregar_eleitores_candidatos()

  mesario = Pessoa("Mesario Exemplo", "123456789", "123.456.789-00")
  urna = Urna(mesario, secao=1, zona=101, candidatos=candidatos, eleitores=eleitores)
  print(urna.get_candidatos())
  root = tk.Tk()
  app = UrnaEletronica(root, urna)
  root.mainloop()