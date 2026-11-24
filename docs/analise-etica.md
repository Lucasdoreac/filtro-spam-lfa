# Relatório de análise ética — Filtro de Spam (Sistema Especialista)

**UDF — Inteligência Artificial e LFA**  
**Professora:** Kadidja Valéria · **Aula:** 17/11/2026  
**Grupo 13:** Lucas Dórea, Nicolas Angelo e Deivid Cerqueira  
**Repositório:** https://github.com/Lucasdoreac/filtro-spam-lfa

## 1. Leitura, vídeo e integridade acadêmica

### Artigo científico

Francisco Pires de Lacerda Júnior. *Da proibição à governança: uso ético da inteligência artificial generativa na educação superior — uma revisão integrativa (2023–2026).* Revista Foco, v. 19, n. 8, e12330, publicado em 07/08/2026. [Artigo](https://ojs.focopublicacoes.com.br/foco/article/view/12330) · [DOI](https://doi.org/10.54751/revistafoco.v19n8-017).

**Resumo (página oficial do artigo):** revisão integrativa qualitativa de 14 estudos científicos e 3 documentos normativos publicados entre jan. 2023 e jul. 2026, examinados por análise temática em cinco eixos: integridade e autoria; desenho da avaliação; letramento em IA e formação docente; governança institucional; e proteção de dados com supervisão humana. O debate deixa de focar só na fraude e passa a **políticas graduadas**, em que a permissão depende da finalidade pedagógica, da **declaração de uso** e da **responsabilização humana**. A proibição geral orienta pouco as práticas reais, e a liberação sem critérios transfere riscos ao estudante e ao professor. O autor propõe uma matriz de governança em cinco movimentos (**definir, ensinar, redesenhar, proteger e acompanhar**) e conclui que o caminho não é aceitar ou banir a IA generativa, mas tornar seus usos **justificáveis, verificáveis e compatíveis com os objetivos de aprendizagem**.

**Questão de integridade acadêmica para a equipe:** seguindo o artigo (declaração de uso e responsabilização humana; usos justificáveis e verificáveis), declarar com clareza onde a IA generativa foi usada na elaboração do projeto e como o resultado foi conferido, para que a autoria e a responsabilidade pelas escolhas continuem sendo da equipe. No projeto, isso se traduz na declaração de uso de IA da seção 4 e na verificação do código pelos testes automatizados.

### Vídeo

*O Estado da Arte em Ética na Inteligência Artificial*, Instituto de Estudos Avançados da USP — evento público de 09/06/2026 (2h01), no lançamento do livro *The Palgrave Handbook on the Ethics of Artificial Intelligence*, com Veridiana Cordeiro, Steven Gouveia, João Cortese e Mateus Henrique Amorim; discute impactos sociais, éticos e institucionais da IA. [Gravação no YouTube](https://www.youtube.com/watch?v=x35_NJfXrpE) · [página no IEA-USP](https://www.iea.usp.br/midiateca/video/videos-2026/o-estado-da-arte-em-etica-na-inteligencia-artificial/).

**Trechos selecionados (minutagem conferida na transcrição automática da gravação):**

- **00:06:18** — a ética da IA não pode ser reduzida a uma "lista formal de conformidade": além de perguntar se um sistema é exato, justo ou transparente, é preciso ver como as instituições e os incentivos compõem a cena e como a noção de responsabilidade está sendo redesenhada.
- **01:35:50 a 01:36:55** — ferramentas de IA são vendidas como neutras e como "solução mágica", mas não são neutras nem nos dados nem nos vieses; costumam ser comparadas por falsos positivos e falsos negativos em uma tarefa isolada, enquanto o problema real nunca é uma tarefa só.

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

**Ideia do vídeo usada no debate:** o trecho de 01:35:50 sustenta a alternativa B. O filtro também é especializado em uma tarefa estreita (quatro sinais) e erra nos dois sentidos; tratá-lo como neutro e deixá-lo descartar mensagens sozinho repetiria o problema apontado no vídeo. Por isso a saída é recomendação, e a decisão fica com uma pessoa.

**Reflexão individual:**

- **Lucas Dórea:** Eu manteria a alternativa B, só alertar e recomendar revisão humana. Apagar uma mensagem legítima é um erro pior e irreversível, enquanto um alerta a mais custa apenas alguns segundos de conferência. Eu verificaria essa escolha contando, numa amostra autorizada de mensagens, quantas legítimas seriam marcadas por R1 ou R2: são os falsos positivos que um descarte automático teria apagado.
- **Deivid Cerqueira:** Eu manteria a alternativa B, pois alertar e recomendar revisão humana protege comunicações legítimas sem entregar ao sistema uma decisão irreversível. A discussão sobre falsos positivos e sobre a responsabilidade pelo descarte me fez perceber que a eficiência da automação não deve prevalecer sobre o custo de uma mensagem importante perdida. Eu verificaria essa medida com uma amostra autorizada de mensagens reais, comparando alertas com situações confirmadas e acompanhando a quantidade de falsos positivos e falsos negativos.

**Declara-se que o debate aconteceu e que os integrantes acima expressaram essas posições.**

## 4. Declaração de uso de sistemas de IA

### IA incorporada ao projeto

O projeto utiliza **sistema especialista baseado em regras explícitas SE–ENTÃO** e **encadeamento para trás** para sinalizar mensagens suspeitas e explicar a recomendação de revisão. O sistema recebe quatro respostas manuais e devolve uma conclusão e o rastro de regras verificadas. O sistema principal não utiliza aprendizado de máquina nem executa ações automáticas sobre caixas de e-mail. O [notebook do Colab](https://colab.research.google.com/github/Lucasdoreac/filtro-spam-lfa/blob/main/notebook.ipynb) demonstra, à parte, uma extensão híbrida: uma árvore de decisão treinada com **dados fictícios** gera o fato `suspeita_ml`, usado pela regra R4.

A verificação técnica inclui testes automatizados de inferência, incerteza, ciclos, interface e situações de falso positivo potencial. O workflow [GitHub Actions — execução 44200771468](https://github.com/Lucasdoreac/filtro-spam-lfa/actions/runs/44200771468), para o commit [3aef6df](https://github.com/Lucasdoreac/filtro-spam-lfa/commit/3aef6df9972207e635566bc1346fd5ad4dc840e8), foi concluído com **sucesso em 17/11/2026**. Esses testes validam aspectos lógicos, mas **não demonstram acurácia ou equidade com mensagens reais**. A revisão final do conteúdo e das decisões de uso corresponde à equipe.

### IA utilizada na elaboração do trabalho

Foram utilizados **ChatGPT (OpenAI)** e **Claude (Anthropic)** para análise do enunciado, revisão e alteração do código, ampliação dos testes, documentação de riscos e redação/revisão deste relatório, do material de consulta e do notebook. A implementação foi confrontada com os arquivos do repositório e a aprovação dos testes foi verificada no GitHub Actions. A equipe assume responsabilidade por verificar a entrega.

## 5. Ficha de avaliação

**Ficha de Avaliação A1 — Grupo 13:** [Google Docs da turma](https://docs.google.com/document/d/1P_XmJUnCDx5PEWRnfW2X_fXG95Sl9gblc_ZYvFajHSA/edit?tab=t.0), com descrição técnica, regras, motor e link do repositório preenchidos. As colunas de notas e observações da professora não devem ser preenchidas pela equipe.

### Referências técnicas

- [base.py](../base.py) — base de conhecimento e regras.
- [motor.py](../motor.py) — inferência e rastro.
- [cli.py](../cli.py) — interface e explicações.
- [test_motor.py](../test_motor.py) — testes automatizados.
- [GitHub Actions: testes concluídos com sucesso](https://github.com/Lucasdoreac/filtro-spam-lfa/actions/runs/44200771468).
- [Artigo — DOI](https://doi.org/10.54751/revistafoco.v19n8-017).
- [Vídeo — IEA-USP](https://www.iea.usp.br/midiateca/video/videos-2026/o-estado-da-arte-em-etica-na-inteligencia-artificial/).

*Documento acadêmico do Grupo 13.*
