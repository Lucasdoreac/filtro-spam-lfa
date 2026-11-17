"""Interface de terminal: perguntas ao usuário e apresentação da explicação."""
from base import OBJETIVO, PERGUNTAS, REGRAS
from motor import Motor

RESPOSTAS = {"s": True, "n": False, "?": None}
TEXTO = {True: "sim", False: "não", None: "?"}


def perguntar_console(simbolo, ler=input, escrever=print):
    while True:
        texto = ler(f"{PERGUNTAS[simbolo]} [s/n/?] ").strip().lower()
        if texto in RESPOSTAS:
            return RESPOSTAS[texto]
        escrever("Resposta inválida. Use s, n ou ?.")


def explicar(resultado):
    if resultado.valor is True:
        linhas = ["Conclusão: spam. Ação recomendada: mover para o lixo."]
    elif resultado.valor is False:
        linhas = ["Conclusão: nenhuma regra confirmou spam. Mantenha na caixa de entrada."]
    else:
        faltam = [s for s in resultado.perguntados if s in _desconhecidos(resultado)]
        linhas = ["Conclusão: inconclusiva. Faltam dados: " + ", ".join(faltam) + "."]
    linhas.append("Regras verificadas:")
    for regra_id, estado, vistas in resultado.rastro:
        fatos = ", ".join(f"{s} = {TEXTO[v]}" for s, v in vistas)
        linhas.append(f"  {regra_id} {estado}: {fatos}")
    linhas.append("As regras são hipóteses didáticas e não foram validadas por humanos.")
    return linhas


def _desconhecidos(resultado):
    return {s for _, _, vistas in resultado.rastro for s, v in vistas if v is None}


def main(ler=input, escrever=print):
    escrever("Filtro de spam por regras. Responda s (sim), n (não) ou ? (não sei).")
    motor = Motor(REGRAS, lambda s: perguntar_console(s, ler, escrever))
    for linha in explicar(motor.consultar(OBJETIVO)):
        escrever(linha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
