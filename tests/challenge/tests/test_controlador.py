from unittest.mock import Mock, patch

from challenge.controlador import Controlador


def test_controlador_pergunta_e_guarda_pessoa():
    pessoa_falsa = object()

    vista_falsa = Mock()
    vista_falsa.perguntar.return_value = pessoa_falsa
    # Quando alguém chame a vista_falsa.perguntar(), retorna pessoa_falsa.

    modelo_falso = Mock()

    with patch("challenge.controlador.Vista", return_value=vista_falsa) as mock_classe_vista, \
         patch("challenge.controlador.Modelo", return_value=modelo_falso) as mock_classe_modelo:
         # patch(...) substitui temporariamente as classes reais por versões controladas pelo teste.
         # Quando o controlador chame Vista() vai receber vista_falsa.

        controlador = Controlador()

    # Fazemos as verificações
    mock_classe_vista.assert_called_once_with() # A classe Vista foi chamado só uma vez sem parâmetros 
    mock_classe_modelo.assert_called_once_with()
    vista_falsa.perguntar.assert_called_once_with()
    modelo_falso.guardar.assert_called_once_with(pessoa_falsa)

    assert controlador.vista is vista_falsa # A classe Controlador guardou a vista recebida.
    assert controlador.modelo is modelo_falso