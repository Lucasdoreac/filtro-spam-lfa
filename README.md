# Filtro de spam — sistema especialista (LFA/UDF)

Protótipo didático em **Python**, com **encadeamento para trás** e regras SE–ENTÃO. Não utiliza modelo de linguagem nem aprendizado de máquina. As regras são hipóteses da equipe, ainda **sem validação empírica**.

## Executar

Requer Python 3.9+; não há dependências externas.

```bash
python cli.py
python -m unittest discover -v
```

Responda `s`, `n` ou `?` (desconhecido). A aplicação não lê e-mails automaticamente e **não apaga nem move mensagens**; suas entradas são respostas manuais a quatro perguntas.

## Regras

- **R1:** remetente desconhecido **e** link encurtado/duvidoso → indício de spam.
- **R2:** promessa de ganho fácil **e** urgência → indício de spam.
- **R3:** indício de spam → **revisão humana recomendada**.

O motor avalia o objetivo `revisao_recomendada` retroativamente. Os resultados possíveis são **verdadeiro** (a recomendação foi derivada), **falso** (nenhuma regra a comprovou) e **desconhecido** (faltaram respostas). **Falso não equivale a mensagem segura.**

## Exemplo

```text
O remetente é desconhecido...? [s/n/?] s
A mensagem traz link encurtado...? [s/n/?] s
Conclusão: características compatíveis com spam.
Ação recomendada: revisar a mensagem antes de decidir o que fazer.
Nenhuma mensagem foi movida ou apagada. A decisão final é humana.
```

## Arquivos

- `base.py`: fatos, perguntas e base de conhecimento.
- `motor.py`: inferência de três valores, trilha de regras, controle de ciclos.
- `cli.py`: interação e justificativa textual.
- `test_motor.py`: testes automatizados, incluindo cenários de falso positivo.

## Limites e uso responsável

**Falsos positivos:** mensagens legítimas (por exemplo, aviso institucional com link encurtado) podem acionar regras. **Falsos negativos:** golpes sem esses sinais podem passar despercebidos. O usuário deve conferir a origem da mensagem pelos canais oficiais, sem clicar diretamente em links suspeitos. Não use o protótipo para filtragem automática em produção.

**Privacidade:** as respostas são processadas na memória da execução, sem banco de dados, coleta de mensagens ou envio a serviços externos no código atual. Não forneça dados pessoais nas respostas. **Transparência:** a saída exibe as regras examinadas e as premissas. **Supervisão:** toda decisão de exclusão é humana.

Para a análise ética, veja [docs/analise-etica.md](docs/analise-etica.md). Evidências de execução e validação empírica exigem coleta e registro à parte.

**Material de consulta (A1):** [docs/material-de-consulta.md](docs/material-de-consulta.md) — descrição do SE, regras, motor com rastros, testes, ML híbrido, teoria das aulas, ética e comparação com a turma.
