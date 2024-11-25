from interface_urna import *

if __name__ == "__main__":
  eleitores, candidatos = carregar_dados()

  mesario = Pessoa("Mesario Exemplo", "123456789", "123.456.789-00")
  urna = Urna(mesario, secao=1, zona=101, candidatos=candidatos, eleitores=eleitores)

  root = tk.Tk()
  app = UrnaEletronicaApp(root, urna)
  root.mainloop()