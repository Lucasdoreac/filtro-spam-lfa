"""Base de conhecimento: fatos, perguntas e as três regras SE-ENTÃO. Só dados."""
from collections import namedtuple

Regra = namedtuple("Regra", "id premissas conclusao origem")

ORIGEM = "hipótese didática, sem validação"

OBJETIVO = "mover_para_lixo"

PERGUNTAS = {
    "remetente_desconhecido": "O remetente é desconhecido (número ou endereço que você nunca viu)?",
    "link_encurtado": "A mensagem traz link encurtado ou de origem duvidosa?",
    "promessa_ganho_facil": "A mensagem promete prêmio, dinheiro ou ganho fácil?",
    "urgencia": "A mensagem pressiona por resposta imediata?",
}

REGRAS = (
    Regra("R1", (("remetente_desconhecido", True), ("link_encurtado", True)), "spam", ORIGEM),
    Regra("R2", (("promessa_ganho_facil", True), ("urgencia", True)), "spam", ORIGEM),
    Regra("R3", (("spam", True),), "mover_para_lixo", ORIGEM),
)
