import unittest

from base import OBJETIVO, REGRAS, Regra
from cli import main, perguntar_console
from motor import Motor


def consultar(respostas, regras=REGRAS, objetivo=OBJETIVO):
    def perguntar(simbolo):
        return respostas[simbolo]

    return Motor(regras, perguntar).consultar(objetivo)


def entradas(*valores):
    fila = iter(valores)
    return lambda _prompt: next(fila)


class TesteBase(unittest.TestCase):
    def test_tres_regras_com_origem_declarada(self):
        self.assertEqual([r.id for r in REGRAS], ["R1", "R2", "R3"])
        self.assertTrue(all("sem validação" in r.origem for r in REGRAS))


class TesteMotor(unittest.TestCase):
    def test_r1_confirma_e_encadeia_r3(self):
        r = consultar({"remetente_desconhecido": True, "link_encurtado": True})
        self.assertIs(r.valor, True)
        self.assertEqual([x[0] for x in r.rastro], ["R1", "R3"])
        self.assertEqual(r.perguntados, ("remetente_desconhecido", "link_encurtado"))

    def test_r2_confirma_quando_r1_e_refutada(self):
        r = consultar({
            "remetente_desconhecido": False,
            "promessa_ganho_facil": True,
            "urgencia": True,
        })
        self.assertIs(r.valor, True)
        self.assertEqual([x[0] for x in r.rastro], ["R1", "R2", "R3"])
        self.assertNotIn("link_encurtado", r.perguntados)

    def test_premissa_falsa_nao_pergunta_o_resto_e_r3_refuta(self):
        r = consultar({"remetente_desconhecido": False, "promessa_ganho_facil": False})
        self.assertIs(r.valor, False)
        self.assertEqual(r.perguntados, ("remetente_desconhecido", "promessa_ganho_facil"))
        self.assertEqual(r.rastro[-1][:2], ("R3", "refutada"))

    def test_desconhecido_nao_vira_nao(self):
        r = consultar({
            "remetente_desconhecido": None,
            "link_encurtado": True,
            "promessa_ganho_facil": False,
        })
        self.assertIsNone(r.valor)
        self.assertEqual(r.rastro[0][:2], ("R1", "inconclusiva"))

    def test_r2_confirma_mesmo_com_r1_inconclusiva(self):
        r = consultar({
            "remetente_desconhecido": None,
            "link_encurtado": None,
            "promessa_ganho_facil": True,
            "urgencia": True,
        })
        self.assertIs(r.valor, True)

    def test_fato_compartilhado_e_perguntado_uma_vez(self):
        regras = (
            Regra("a", (("x", True), ("y", True)), "g", ""),
            Regra("b", (("x", True), ("z", True)), "g", ""),
        )
        r = consultar({"x": True, "y": False, "z": True}, regras, "g")
        self.assertIs(r.valor, True)
        self.assertEqual(r.perguntados.count("x"), 1)

    def test_ciclo_termina_como_inconclusivo(self):
        regras = (
            Regra("a", (("x", True),), "y", ""),
            Regra("b", (("y", True),), "x", ""),
        )
        self.assertIsNone(consultar({}, regras, "x").valor)


class TesteCli(unittest.TestCase):
    def test_aceita_espacos_e_caixa(self):
        self.assertIs(perguntar_console("urgencia", entradas(" S ")), True)
        self.assertIs(perguntar_console("urgencia", entradas("N")), False)
        self.assertIsNone(perguntar_console("urgencia", entradas("?")))

    def test_entrada_invalida_pede_de_novo(self):
        avisos = []
        valor = perguntar_console("urgencia", entradas("talvez", "s"), avisos.append)
        self.assertIs(valor, True)
        self.assertEqual(len(avisos), 1)

    def test_consulta_completa_confirmada(self):
        saida = []
        main(entradas("s", "s"), saida.append)
        self.assertTrue(any("Conclusão: spam" in linha for linha in saida))

    def test_consulta_sem_informacao_suficiente(self):
        saida = []
        main(entradas("?", "?", "?", "?"), saida.append)
        self.assertTrue(any("inconclusiva" in linha for linha in saida))


if __name__ == "__main__":
    unittest.main()
