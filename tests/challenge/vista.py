from challenge.pessoa import Pessoa


class Vista:
    def perguntar(self):
        # Pede ao utilizador os dados da pessoa
        nome = input("Introduza o nome: ")
        idade = int(input("Introduza a idade: "))

        # Cria e devolve o objeto Pessoa
        pessoa = Pessoa(nome, idade)
        return pessoa
