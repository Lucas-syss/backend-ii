from challenge.vista import Vista
from challenge.modelo import Modelo


class Controlador:
    def __init__(self):
        # Cria a vista e o modelo
        self.vista = Vista()
        self.modelo = Modelo()

        # Pede os dados à vista
        pessoa = self.vista.perguntar()

        # Envia a pessoa para o modelo
        self.modelo.guardar(pessoa)

        print("Processo concluído com sucesso.")
