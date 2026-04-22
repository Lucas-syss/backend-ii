class Modelo:
    def __init__(self):
        # Lista onde as pessoas serão guardadas
        self.pessoas = []

    def guardar(self, pessoa):
        # Guarda o objeto pessoa na lista
        self.pessoas.append(pessoa)
