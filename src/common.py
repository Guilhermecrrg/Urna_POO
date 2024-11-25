class Pessoa:
    __nome : str
    __RG : str
    __CPF : str

    def __init__(self, nome, RG, CPF):
        self.__nome = nome
        self.__RG = RG
        self.__CPF = CPF

    def get_nome(self):
        return self.__nome
    
    def get_CPF(self):
        return self.__CPF
    
    def get_RG(self):
        return self.__RG

    def __str__(self):
        info = (f'Nome: {self.__nome}\n'
               f'RG: {self.__RG}\n'
               f'CPF: {self.__CPF}\n')
        return info

    def __repr__(self):
        return f"Pessoa(nome='{self.__nome}', RG='{self.__RG}', CPF='{self.__CPF}')"

class Eleitor(Pessoa):
    __titulo: int
    __secao: int
    __zona: int

    def __init__(self, nome, RG, CPF, titulo, secao, zona):
        super().__init__(nome, RG, CPF)
        self.__titulo = titulo
        self.__secao = secao
        self.__zona = zona

    def __str__(self):
        info = super().__str__()
        info += (f'Titulo: {self.__titulo}\n'
                 f'Seção: {self.__secao}\n'
                 f'Zona: {self.__zona}\n')
        return info

    def __repr__(self):
        return f"Eleitor({super().__repr__()}, titulo='{self.__titulo}', secao='{self.__secao}', zona='{self.__zona}')"

    def get_titulo(self):
        return self.__titulo
    
    def get_secao(self):
        return self.__secao
    
    def get_zona(self):
        return self.__zona

    def __hash__(self):
        return hash(self.__titulo)

    def __eq__(self, other):
        if isinstance(other, Eleitor):
            return self.__titulo == other.__titulo
        return False

class Candidato(Pessoa):
    __numero : int

    def __init__(self, nome, RG, CPF, numero):
        super().__init__(nome, RG, CPF)
        self.__numero = numero

    def __str__(self):
        info = super().__str__()
        info += (f'Numero: {self.__numero}\n')
        return info

    def __repr__(self):
        return f"Candidato({super().__repr__()}, numero='{self.__numero}')"
    
    def get_numero(self):
        return self.__numero
