import pytest

from main import Classificador


@pytest.mark.parametrize(
    "sardinha, destino_esperado",
    [
        (3, "free"),
        (6.9, "free"),
        (7, "tapas"),
        (8.3, "tapas"),
        (9, "canning"),
        (10.5, "canning"),
        (11, "frozen"),
        (12.8, "frozen"),
        (13, "grill"),
        (13.9, "grill"),
        (14, "portions"),
        (20, "portions"),
    ]
)
def test_classificar_sardinha(sardinha, destino_esperado):
    classificador = Classificador()

    destino_obtido = classificador.classificar(sardinha)

    assert destino_obtido == destino_esperado