class Classificador:

    MEDIDAS =  (7, 9, 11, 13, 14)
    DESTINOS = ("free","tapas", "canning", "frozen", "grill", "portions")

    
    def classificar(self, sardinha):
        for medida, destino in zip( self.MEDIDAS, self.DESTINOS):
            if sardinha < medida:
                return destino
        return self.DESTINOS[-1]

if __name__ == "__main__":
    classificador = Classificador()
    print(classificador.classificar(3))
    print(classificador.classificar(8.3))
    print(classificador.classificar(10))
    print(classificador.classificar(12))
    print(classificador.classificar(13.4))
    print(classificador.classificar(15))