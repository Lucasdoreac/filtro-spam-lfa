# Relatório de análise ética — Filtro de Spam (Sistema Especialista)

**UDF — Inteligência Artificial e LFA**  
**Professora:** Kadidja Valéria · **Aula:** 17/11/2026  
**Grupo 13:** Lucas Dórea, Nicolas Angelo e Deivid Cerqueira  
**Repositório:** https://github.com/Lucasdoreac/filtro-spam-lfa

> **Estado da entrega:** parte técnica documentada e testes automatizados confirmados. Permanecem pendentes a minutagem de um trecho assistido do vídeo, a confirmação de leitura integral do artigo, a reflexão individual após o debate e a conferência do envio no Blackboard. Esses fatos não são apresentados como realizados.

## 1. Leitura, vídeo e integridade acadêmica

### Artigo científico

Francisco Pires de Lacerda Júnior. *Da proibição à governança: uso ético da inteligência artificial generativa na educação superior — uma revisão integrativa (2023–2026).* Revista Foco, v. 19, n. 8, 2026. [DOI](https://doi.org/10.54751/revistafoco.v19n8-017).

**Ideia extraída do resumo publicado:** o uso ético de IA generativa na educação superior não se resolve por mera proibição; requer práticas de governança institucional, transparência e integridade/autoria acadêmica, formação e supervisão humana, bem como atenção à proteção de dados e à avaliação. No projeto, isso se traduz em declarar claramente o uso de IA na produção dos materiais, verificar seu conteúdo e assumir responsabilidade pelas decisões técnicas.

**Limite de verificação:** ideia fundamentada no **resumo publicado**; não se declara leitura integral do artigo.

### Vídeo

*O Estado da Arte em Ética na Inteligência Artificial*, Instituto de Estudos Avançados da USP, gravação de junho de 2026. [Vídeo](https://www.youtube.com/watch?v=SHDtABmGhNw).

A apresentação é indicada pela atividade para discutir impactos sociais e responsabilidades institucionais associados à IA.

**Trecho assistido (minuto:segundo) e argumento efetivamente apresentado:** **PENDENTE**. A minutagem deverá ser registrada somente após conferir a passagem na gravação. Não foi inventada uma fala ou um horário.

## 2. Descrição e análise ética do projeto

O **Filtro de Spam** é um sistema especialista didático em Python. Uma pessoa responde a quatro perguntas sobre uma mensagem: se o remetente é desconhecido, se há link encurtado ou duvidoso, se há promessa de ganho fácil e se existe pressão por resposta imediata. O motor usa **encadeamento para trás** para aplicar regras explícitas e apresenta um rastro explicativo. A conclusão é uma recomendação de **revisão humana**, sem mover ou excluir mensagens. Não há modelo preditivo treinado nem leitura automática de e-mails.

### Regras implementadas

- **R1:** SE remetente desconhecido **E** link encurtado/duvidoso, ENTÃO há indício de spam.
- **R2:** SE promessa de ganho fácil **E** urgência, ENTÃO há indício de spam.
- **R3:** SE há indício de spam, ENTÃO revisão humana é recomendada.

As regras são **hipóteses didáticas sem validação empírica**. O programa distingue **sim**, **não** e **não sei**, preservando incerteza. A ausência de regra confirmada **não comprova** que uma mensagem é segura.

### Privacidade e dados

**Situação concreta e afetados:** uma mensagem pode revelar número, endereço eletrônico, relacionamento entre pessoas ou informação privada sobre o destinatário e o remetente.

**Medida adotada:** o protótipo consulta somente quatro características informadas manualmente e não implementa armazenamento persistente de mensagens ou integração com provedores de e-mail. A equipe deve manter minimização de dados e não solicitar conteúdo integral da mensagem sem necessidade. Uma eventual versão que trate mensagens reais exigirá revisão específica de proteção de dados.

### Viés e equidade

**Situação concreta e afetados:** o aviso legítimo de uma universidade ou de uma organização nova, com link curto e remetente desconhecido, pode acionar R1, prejudicando quem depende da comunicação.

**Medida adotada e proposta:** o resultado é uma recomendação, não um descarte. Os testes ilustram esse falso positivo possível; antes de uso real, será necessário avaliar mensagens de diferentes contextos e origens, medir erros e rever regras injustas. Não se afirma ausência de viés.

### Transparência

**Situação concreta e afetados:** um usuário recebe um alerta, mas não sabe por que a mensagem foi considerada suspeita.

**Medida adotada:** o sistema mostra quais regras foram confirmadas, refutadas ou ficaram inconclusivas e as premissas consultadas. Informa também que as regras não foram validadas com dados reais.

### Supervisão e responsabilidade

**Situação concreta e afetados:** um comunicado legítimo de trabalho pode ser classificado como suspeito, com risco de atraso ou perda se for descartado.

**Medida adotada:** o programa **não move nem apaga** mensagens. A decisão final cabe ao usuário, que pode responder novamente às perguntas. A equipe é responsável por revisar regras, testes e documentação do protótipo.

### Impacto social

**Situação concreta e afetados:** alertas podem ajudar pessoas a perceber possíveis golpes, mas falsos positivos podem bloquear comunicação importante e falsos negativos podem deixar golpes passarem.

**Medida adotada e proposta:** as recomendações apresentam limites explícitos e não são bloqueios definitivos. É necessário testar falsos positivos e falsos negativos em uma amostra autorizada antes de considerar uso fora do contexto didático.

## 3. Dilema ético, debate e reflexão individual

**Dilema:** o sistema deve recomendar descarte automático com base nas regras, ou apenas alertar e oferecer revisão humana?

**Alternativa A — descarte automático:** reduz esforço manual, mas pode levar à exclusão de comunicações legítimas, especialmente quando os sinais utilizados não são suficientes para distinguir casos.

**Alternativa B — alerta e revisão humana:** aumenta o esforço de avaliação, mas preserva a autonomia do usuário e reduz o risco de perda irrevogável de mensagens. **Foi a alternativa implementada.**

**Proposta para debate:** em que situações, se houver alguma, a automação poderia agir sem confirmação? Quem responderia por uma mensagem legítima perdida?

**Reflexão individual — a completar separadamente por integrante após o debate:**

- **Lucas Dórea:** Eu manteria a alternativa B, só alertar e recomendar revisão humana. Apagar uma mensagem legítima é um erro pior e irreversível, enquanto um alerta a mais custa apenas alguns segundos de conferência. Eu verificaria essa escolha contando, numa amostra autorizada de mensagens, quantas legítimas seriam marcadas por R1 ou R2: são os falsos positivos que um descarte automático teria apagado.
- **Nicolas Angelo:** registrar a decisão que manteria ou mudaria, o argumento efetivamente ouvido que influenciou sua posição e como verificaria a medida.
- **Deivid Cerqueira:** registrar a decisão que manteria ou mudaria, o argumento efetivamente ouvido que influenciou sua posição e como verificaria a medida.

**Não se declara que o debate aconteceu ou que os integrantes já expressaram tais posições.**

## 4. Declaração de uso de sistemas de IA

### IA incorporada ao projeto

O projeto utiliza **sistema especialista baseado em regras explícitas SE–ENTÃO** e **encadeamento para trás** para sinalizar mensagens suspeitas e explicar a recomendação de revisão. O sistema recebe quatro respostas manuais e devolve uma conclusão e o rastro de regras verificadas. Não utiliza aprendizado de máquina nem executa ações automáticas sobre caixas de e-mail.

A verificação técnica inclui testes automatizados de inferência, incerteza, ciclos, interface e situações de falso positivo potencial. O workflow [GitHub Actions — execução 44200771468](https://github.com/Lucasdoreac/filtro-spam-lfa/actions/runs/44200771468), para o commit [3aef6df](https://github.com/Lucasdoreac/filtro-spam-lfa/commit/3aef6df9972207e635566bc1346fd5ad4dc840e8), foi concluído com **sucesso em 17/11/2026**. Esses testes validam aspectos lógicos, mas **não demonstram acurácia ou equidade com mensagens reais**. A revisão final do conteúdo e das decisões de uso corresponde à equipe.

### IA utilizada na elaboração do trabalho

Foi utilizado **ChatGPT (OpenAI)** para análise do enunciado, revisão e alteração do código, ampliação dos testes, documentação de riscos e redação/revisão deste relatório. A implementação foi confrontada com os arquivos do repositório e a aprovação dos testes foi verificada no GitHub Actions. **Outras ferramentas de IA utilizadas por integrantes, se houver, e suas versões devem ser confirmadas e declaradas individualmente.** A equipe assume responsabilidade por verificar a entrega.

## 5. Verificação antes da entrega

| Exigência | Estado e evidência |
| --- | --- |
| Assistir ao vídeo e registrar minuto/segundo e argumento fiel | **Pendente:** sem trecho efetivamente conferido. |
| Ler artigo e apresentar ideia fiel | **Parcial:** ideia apoiada no resumo publicado; leitura integral ainda não confirmada. |
| Realizar debate e individualizar reflexão | **Parcial:** reflexão do Lucas registrada; Nicolas e Deivid pendentes. |
| Executar testes e registrar resultado | **Confirmado:** [GitHub Actions aprovado](https://github.com/Lucasdoreac/filtro-spam-lfa/actions/runs/44200771468) para o commit 3aef6df. |
| Confirmar outras ferramentas de IA usadas | **Parcial:** ChatGPT declarado; outros usos não confirmados. |
| Identificar integrantes do grupo | **Confirmado na ficha pública:** Grupo 13 — Lucas Dórea, Nicolas Angelo, Deivid Cerqueira. |
| Conferir modalidade de envio no Blackboard | **Pendente:** modalidade não confirmada. |

**Ficha de Avaliação A1 — Grupo 13:** [Google Docs da turma](https://docs.google.com/document/d/1P_XmJUnCDx5PEWRnfW2X_fXG95Sl9gblc_ZYvFajHSA/edit?tab=t.0), com descrição técnica, regras, motor e link do repositório preenchidos. As colunas de notas e observações da professora não devem ser preenchidas pela equipe.

### Referências técnicas

- [base.py](../base.py) — base de conhecimento e regras.
- [motor.py](../motor.py) — inferência e rastro.
- [cli.py](../cli.py) — interface e explicações.
- [test_motor.py](../test_motor.py) — testes automatizados.
- [GitHub Actions: testes concluídos com sucesso](https://github.com/Lucasdoreac/filtro-spam-lfa/actions/runs/44200771468).
- [Artigo — DOI](https://doi.org/10.54751/revistafoco.v19n8-017).
- [Vídeo — USP](https://www.youtube.com/watch?v=SHDtABmGhNw).

*Documento acadêmico do Grupo 13. Situações ainda não verificadas estão sinalizadas explicitamente, para evitar atribuição de evidências inexistentes.*
