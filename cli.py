"""Interface educativa: recomenda revisão; nunca move ou apaga mensagens."""
from base import OBJETIVO, PERGUNTAS, REGRAS
from motor import Motor

RESPOSTAS = {"s": True, "n": False, "?": None}
TEXTO = {True: "sim", False: "não", None: "desconhecido"}


def perguntar_console(simbolo, ler=input, escrever=print):
    while True:
        texto = ler(f"{PERGUNTAS[simbolo]} [s/n/?] ").strip().lower()
        if texto in RESPOSTAS:
            return RESPOSTAS[texto]
        escrever("Resposta inválida. Use s, n ou ?.")


def explicar(resultado):
    if resultado.valor is True:
        linhas = [
            "Conclusão: características compatíveis com spam.",
            "Ação recomendada: revisar a mensagem antes de decidir o que fazer.",
            "Nenhuma mensagem foi movida ou apagada. A decisão final é humana.",
        ]
    elif resultado.valor is False:
        linhas = [
            "Conclusão: nenhuma regra confirmou spam.",
            "Isso NÃO garante que a mensagem seja segura. Revise se necessário.",
        ]
    else:
        faltam = list(dict.fromkeys(
            simbolo for _, _, vistas in resultado.rastro
            for simbolo, valor in vistas if valor is None
        ))
        linhas = [
            "Conclusão: inconclusiva. Faltam dados: " + (", ".join(faltam) or "evidências suficientes") + ".",
            "Não descarte a mensagem automaticamente; faça uma revisão humana.",
        ]
    linhas.append("Regras verificadas:")
    for regra_id, estado, vistas in resultado.rastro:
        fatos = ", ".join(f"{s} = {TEXTO[v]}" for s, v in vistas)
        linhas.append(f"  {regra_id} {estado}: {fatos}")
    linhas.append("Limitação: regras são hipóteses didáticas, sem validação empírica.")
    return linhas


def main(ler=input, escrever=print):
    escrever("Filtro educativo de spam. Responda s (sim), n (não) ou ? (não sei).")
    escrever("Não insira dados pessoais; a análise é feita com respostas às perguntas.")
    motor = Motor(REGRAS, lambda s: perguntar_console(s, ler, escrever))
    for linha in explicar(motor.consultar(OBJETIVO)):
        escrever(linha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
