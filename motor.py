"""Motor de inferência: encadeamento para trás com três valores (True, False, None).

Não conhece o domínio nem faz entrada e saída. None significa desconhecido e
nunca é tratado como False.
"""
from collections import namedtuple

Resultado = namedtuple("Resultado", "valor rastro perguntados")


class Motor:
    def __init__(self, regras, perguntar):
        self.regras = tuple(regras)
        self.perguntar = perguntar
        self.fatos = {}
        self.rastro = []
        self.perguntados = []
        self._derivados = {r.conclusao for r in self.regras}

    def consultar(self, objetivo):
        self.fatos.clear()
        self.rastro.clear()
        self.perguntados.clear()
        valor = self._valor(objetivo, ())
        return Resultado(valor, tuple(self.rastro), tuple(self.perguntados))

    def _valor(self, simbolo, caminho):
        if simbolo in self.fatos:
            return self.fatos[simbolo]
        if simbolo not in self._derivados:
            resposta = self.perguntar(simbolo)
            self.fatos[simbolo] = resposta
            self.perguntados.append(simbolo)
            return resposta
        if simbolo in caminho:
            return None
        pendente = False
        for regra in self.regras:
            if regra.conclusao != simbolo:
                continue
            valor = self._avaliar(regra, caminho + (simbolo,))
            if valor is True:
                self.fatos[simbolo] = True
                return True
            if valor is None:
                pendente = True
        if pendente:
            return None
        self.fatos[simbolo] = False
        return False

    def _avaliar(self, regra, caminho):
        vistas = []
        pendente = False
        for simbolo, esperado in regra.premissas:
            valor = self._valor(simbolo, caminho)
            vistas.append((simbolo, valor))
            if valor is None:
                pendente = True
            elif valor != esperado:
                self.rastro.append((regra.id, "refutada", tuple(vistas)))
                return False
        estado = "inconclusiva" if pendente else "confirmada"
        self.rastro.append((regra.id, estado, tuple(vistas)))
        return None if pendente else True
