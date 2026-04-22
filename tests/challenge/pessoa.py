class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def __str__(self):
        return f"Pessoa(nome={self.nome}, idade={self.idade})"
