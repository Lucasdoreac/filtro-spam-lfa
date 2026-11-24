# Material de consulta — A1 Sistemas Especialistas (Grupo 13)

**UDF · IA e LFA · Profa. Kadidja Valéria** · Grupo 13: Lucas Dórea, Nicolas Angelo, Deivid Cerqueira

Cada seção começa com **Lacuna** (o que faltava na documentação) e depois traz o conteúdo que a preenche.

---

## 0. Resumo em 1 minuto

- **O quê:** sistema especialista didático em Python para triagem de spam. O sistema principal não usa ML nem LLM e não tem dependências; o [notebook do Colab](https://colab.research.google.com/github/Lucasdoreac/filtro-spam-lfa/blob/main/notebook.ipynb) demonstra a extensão híbrida com árvore de decisão.
- **Entrada:** 4 perguntas respondidas com `s` / `n` / `?`.
- **Base:** 3 regras SE–ENTÃO (R1, R2, R3), declaradas como hipóteses didáticas sem validação empírica.
- **Motor:** encadeamento **para trás** a partir do objetivo `revisao_recomendada`, com lógica de **3 valores** (sim, não, desconhecido).
- **Saída:** conclusão + **rastro** das regras (confirmada, refutada, inconclusiva) + limitação.
- **Ética:** nunca move nem apaga mensagens. Recomenda **revisão humana**. "Não" ≠ "seguro".

---

## 1. Descrição do SE

**Lacuna:** faltava o caso completo na forma "fatos → regras → resultado esperado".

- **Finalidade:** ajudar uma pessoa a decidir se uma mensagem (e-mail, SMS, WhatsApp) merece revisão cuidadosa antes de clicar ou responder.
- **Usuário:** qualquer pessoa que recebeu uma mensagem suspeita. Ela informa o caso e usa a orientação (papel de "usuário", slide 11).
- **Tarefa:** **diagnóstico / interpretação**, ou seja, explicar a partir de evidências (slide 7).
- **Fatos de entrada** (`base.py`, `PERGUNTAS`):

| Fato | Pergunta |
|---|---|
| `remetente_desconhecido` | O remetente é desconhecido (número ou endereço que você nunca viu)? |
| `link_encurtado` | A mensagem traz link encurtado ou de origem duvidosa? |
| `promessa_ganho_facil` | A mensagem promete prêmio, dinheiro ou ganho fácil? |
| `urgencia` | A mensagem pressiona por resposta imediata? |

- **Valores:** `s` → True, `n` → False, `?` → None (desconhecido).
- **Objetivo:** `revisao_recomendada`.
- **Caso e resultado esperado:** remetente desconhecido = **sim**, link duvidoso = **sim**.
  → R1 confirma **spam** → R3 confirma **revisão recomendada**.
  → Saída: "Conclusão: características compatíveis com spam. Ação recomendada: revisar a mensagem antes de decidir o que fazer. Nenhuma mensagem foi movida ou apagada."
  → As perguntas de promessa e urgência **nem são feitas**, porque o objetivo já foi provado.

---

## 2. Base de conhecimento e regras

**Lacuna:** faltavam a formalização (termos e valores), a origem das regras e a separação entre base e motor.

**Regras (SE–ENTÃO):**

- **R1:** SE `remetente_desconhecido` = sim **E** `link_encurtado` = sim ENTÃO `spam`.
- **R2:** SE `promessa_ganho_facil` = sim **E** `urgencia` = sim ENTÃO `spam`.
- **R3:** SE `spam` ENTÃO `revisao_recomendada`.

**Em código** (`base.py`):
```python
Regra = namedtuple("Regra", "id premissas conclusao origem")
Regra("R1", (("remetente_desconhecido", True), ("link_encurtado", True)), "spam", ORIGEM)
```

- **Fatos perguntáveis** (folhas): os 4 da tabela acima. O motor pergunta ao usuário.
- **Fatos derivados** (conclusões): `spam` e `revisao_recomendada`. Só regras os produzem.
- **R1 e R2 são alternativas** (OU): qualquer uma prova `spam`. **R3 encadeia**: depende de uma conclusão intermediária.
- **Origem:** `ORIGEM = "hipótese didática, sem validação empírica"` fica gravada em cada regra. Isso atende o slide 38: a base registra origem e responsáveis. Versão = commit do Git.
- **Separação base/motor** (slide 6): `base.py` só tem conhecimento, `motor.py` só tem raciocínio. Trocar regras não exige mexer no motor.
- **Formalização** (slide 28): termos delimitados (4 fatos), valores possíveis (s/n/?), exceção registrada (o '?' não é tratado como "não").
- **Termo padronizado:** "link encurtado ou duvidoso". Na ficha aparece "link suspeito", que significa a mesma coisa (`link_encurtado` no código).

---

## 3. Motor de inferência

**Lacuna:** faltava mostrar o passo a passo, o rastro de cada caso, as condições de parada e o Como?/Por quê?.

### Algoritmo (`motor.py`, métodos `_valor` e `_avaliar`)

1. Recebe o **objetivo** (`revisao_recomendada`).
2. Se o símbolo já está na **memória de trabalho** (`self.fatos`), devolve o valor. Por isso **cada fato é perguntado uma única vez**.
3. Se o símbolo **não é conclusão de nenhuma regra**, é folha: **pergunta ao usuário** e guarda a resposta.
4. Se é derivado, percorre **as regras cuja conclusão é ele**, na ordem da base. Cada premissa vira um **subobjetivo** (recursão).
5. Avaliação de uma regra:
   - premissa com valor contrário ao esperado → regra **refutada**, e **para de perguntar** o resto (curto-circuito);
   - alguma premissa desconhecida → regra **inconclusiva**;
   - todas conferem → regra **confirmada**.
6. Resultado do símbolo: True se alguma regra confirmou; None se nenhuma confirmou mas alguma ficou inconclusiva; False se todas foram refutadas.

- **Controle de ciclo:** se o símbolo reaparece no próprio caminho de prova, devolve None (inconclusivo) em vez de entrar em loop infinito.
- **Resolução de conflito:** ordem fixa das regras (R1 antes de R2). A primeira regra confirmada encerra a busca.
- **Condições de parada** (slide 23): objetivo provado; todas as regras refutadas; ou falta de dados (inconclusivo).

### Rastros reais (conferidos com `test_motor.py`)

| Caso | Respostas | Rastro | Resultado |
|---|---|---|---|
| A — positivo via R1 | rem=s, link=s | R1 confirmada → R3 confirmada | **revisão recomendada** |
| B — positivo via R2 | rem=n, ganho=s, urg=s | R1 refutada (link nem é perguntado) → R2 confirmada → R3 confirmada | **revisão recomendada** |
| C — negativo | rem=n, ganho=n | R1 refutada → R2 refutada → R3 refutada | **nenhuma regra confirmou** (≠ seguro) |
| D — informação ausente | rem=?, link=s, ganho=n | R1 inconclusiva → R2 refutada → R3 inconclusiva | **inconclusivo**, informa o que falta |

### Explicação (slide 26)

- **Como?** "A revisão veio de **R3**, apoiada por **R1**, porque remetente desconhecido = sim e link = sim." O CLI imprime isso na seção "Regras verificadas".
- **Por quê?** "Pergunto sobre o link **porque R1 precisa dessa premissa** para provar spam, que R3 precisa para recomendar revisão."
- **Honestidade:** o "Por quê?" **não é um comando interativo** no CLI. A justificativa aparece no rastro final, não durante a pergunta. (Os Grupos 23 e 25 implementaram o "Por quê?" interativo.)

---

## 4. Para frente × para trás

**Lacuna:** a documentação não justificava a escolha da estratégia nem mostrava a alternativa.

| | Para frente (dirigido por dados) | Para trás (dirigido por objetivo) — **o nosso** |
|---|---|---|
| Parte de | fatos disponíveis | uma hipótese ou objetivo |
| Pergunta-guia | "que conclusões os fatos permitem?" | "que evidências sustentam esta hipótese?" |
| Útil quando | queremos descobrir o que decorre dos dados | há um objetivo claro e queremos perguntar só o necessário |

- **Mesmo caso para frente:** fatos {rem=s, link=s, ganho=n, urg=n} → ciclo 1: R1 satisfeita → adiciona `spam` → ciclo 2: R3 satisfeita → adiciona `revisao_recomendada` → ciclo 3: nada novo → **para**. Exige todos os fatos antes de começar.
- **Por que escolhemos para trás:** há **um único objetivo** (`revisao_recomendada`), e o motor **pergunta só o que falta**. No caso A, ele faz 2 perguntas em vez de 4.
- **Ciclo de inferência** (slide 16): identificar regras satisfeitas → escolher uma e executar → atualizar fatos → repetir até a parada.
- **Prolog** também prova para trás: `avo(X,Z) :- pai(X,Y), pai(Y,Z).` Para a consulta `avo(X, lucas)`, as relações `pai(jose,adao)` e `pai(adao,lucas)` sustentam a regra, e a resposta é `X = jose`.

---

## 5. Incerteza e informação ausente

**Lacuna:** faltava explicar por que '?' não é "não" e como isso se compara a fator de certeza.

- **Slide 24:** "não saber se há papel ≠ saber que não há papel". **Ausência de evidência não é negação.**
- **No projeto:** `?` = None. Uma regra com premissa None fica **inconclusiva**, nunca refutada.
- **False não prova segurança:** "nenhuma regra confirmou" significa só que **esses 4 sinais** não apareceram. Golpes sem esses sinais passam (falso negativo).
- **Lógica de 3 valores × fator de certeza (CF, estilo MYCIN):**
  - nós: verdadeiro / falso / desconhecido, **sem números**;
  - CF: confiança entre 0 e 1 por regra. Evidências que apontam a mesma conclusão combinam por **CF = CF1 + CF2 × (1 − CF1)**, que nunca passa de 1 (usado pelos Grupos 6 e 20);
  - slide 25: **um valor de confiança só é probabilidade se o modelo o define assim**. CF não é probabilidade.

---

## 6. Testes, verificação e validação

**Lacuna:** faltava ligar os testes aos 3 casos exigidos e separar verificação de validação.

**Os 3 testes exigidos** (slide 42) em `test_motor.py`:

| Tipo | Teste |
|---|---|
| **Positivo** (todas as condições presentes) | `test_r1_confirma_e_encadeia_r3` → rastro `[R1, R3]` |
| **Negativo** (uma condição necessária falsa) | `test_premissa_falsa_nao_pergunta_o_resto_e_r3_refuta` |
| **Informação ausente** | `test_desconhecido_nao_vira_nao` e `test_consulta_sem_informacao_suficiente` |

- **Extras (16 testes ao todo):** via R2 com R1 refutada; R2 confirma mesmo com R1 inconclusiva; fato compartilhado perguntado uma vez; **ciclo termina**; resposta inválida gera erro; nova consulta limpa o estado; **falso positivo** só recomenda revisão; ausência de sinais não prova segurança; CLI (espaços e maiúsculas, entrada inválida).
- **Evidência:** GitHub Actions "Testes Python" passou em 17/11/2026, na execução 1 (`3aef6df`) e na execução 2 (`253701e`).
- **Verificação** (slide 36), "construímos certo?": contradições, **ciclos**, regras inalcançáveis. Feito pelos testes de lógica.
- **Validação**, "construímos a coisa certa?": a recomendação atende a casos **reais**? **Não feita.** As regras não foram testadas com mensagens reais. Os testes provam a lógica, não a acurácia.

---

## 7. Aprendizado supervisionado e arquitetura híbrida

**Lacuna:** o sistema principal não tem ML, e a 2ª aula cobra a integração de árvore de decisão com regras. **Coberto pelo [notebook do Colab](https://colab.research.google.com/github/Lucasdoreac/filtro-spam-lfa/blob/main/notebook.ipynb)**, seção 7.

- **SE × modelo supervisionado:**

| | Sistema especialista | Modelo supervisionado |
|---|---|---|
| Origem | conhecimento do domínio | exemplos rotulados |
| Construção | pessoas escrevem regras | algoritmo ajusta o modelo |
| Resultado | conclusão por regras | previsão de um rótulo |
| Revisão | revisar regras e fatos | revisar dados e modelo |

- **Classificação** → categoria discreta (ex.: apoio/autonomia, spam/legítima). **Regressão** → valor contínuo (ex.: horas de estudo).
- **Pipeline:**
```python
X = dados[["horas_estudo", "exercicios_percentual"]]   # atributos: descrevem o caso
y = dados["perfil"]                                      # rótulo: resposta conhecida
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
modelo = DecisionTreeClassifier(max_depth=2)
modelo.fit(X_treino, y_treino)
previsoes = modelo.predict(X_teste)
```
  - `test_size=0.25`: reserva 25% para teste (4 de 16 exemplos);
  - `stratify=y`: preserva a proporção das classes;
  - `random_state`: torna a divisão reproduzível;
  - `max_depth=2`: limita a árvore, o que reduz overfitting e mantém a árvore legível.
- **Árvore de decisão:** aprende condições que separam os exemplos em grupos puros (ex.: `horas_estudo ≤ 4,5` → apoio).
- **Matriz de confusão:** linhas = real, colunas = previsto. **Acurácia** = acertos / total.
- **Cautela:** 100% em 4 casos **não prova** eficácia real. A amostra é pequena e instável, e o modelo erra fora do domínio de treino.
- **Arquitetura híbrida:** Fase 1, ML: a árvore prevê um rótulo. Fase 2, SE: **a previsão vira um fato** que alimenta as regras.
- **No nosso notebook:** árvore treinada com 24 mensagens **fictícias** (atributos: nº de links, termos de urgência, termos de ganho) prevê `suspeita_ml`. Acurácia: 83% em 6 casos de teste (1 suspeita prevista como não suspeita); a árvore aprendeu a olhar só os termos de urgência.
  - **R4:** SE `suspeita_ml` = sim E `remetente_desconhecido` = sim ENTÃO `spam`. R3 continua exigindo revisão humana.
  - **Caso H1:** sem sinais informados pelo usuário, R1 e R2 são refutadas, mas a árvore prevê suspeita e R4 confirma → revisão.
  - **Comparação:** mesmos números, mudando só `remetente_desconhecido` para não → R4 é refutada. A regra humana limita o modelo.
- **Questões de fechamento:**
  - Que parte aprende com os dados? → **o modelo** (árvore).
  - Que parte aplica as regras humanas? → **o motor de inferência**.
  - Por que 100% em teste pequeno exige cautela? → poucos casos, avaliação instável, não representa uso real.

---

## 8. Teoria da Aula 12 em tópicos

**Lacuna:** a documentação não tinha os conceitos da aula.

- **Sistema especialista:** usa conhecimento de um **domínio restrito** para resolver problemas. É um sistema baseado em conhecimento: **separa o conhecimento do raciocínio**.
- **Componentes:** **base de conhecimento** (conceitos e regras), **memória de trabalho** (fatos do caso e conclusões intermediárias), **motor de inferência** (escolhe e executa regras), **interface** (coleta respostas e mostra recomendações), **mecanismo de explicação** (registra a justificativa), **ferramentas de aquisição** (manutenção da base).
  - No nosso projeto: base = `base.py`; memória = `Motor.fatos`; motor = `motor.py`; interface e explicação = `cli.py`.
- **Papéis:** especialista do domínio (fornece e valida), engenheiro do conhecimento (formaliza a base), usuário (informa o caso).
- **Tarefas adequadas:** diagnóstico, interpretação, configuração e planejamento.
- **Domínio bem delimitado:** entradas e resultados reconhecíveis, especialistas e casos para conferir, critério de sucesso.
- **Fato** = informação sobre o caso. **Regra** = relação entre condições e conclusão, que deve tornar explícitos os critérios.
- **Regras simultaneamente aplicáveis:** escolha por **prioridade**, **especificidade** (mais condições vence) ou **recência**. A estratégia deve ser explícita e previsível. Nós usamos ordem fixa.
- **Aquisição de conhecimento:** entrevistas, observação de casos reais, documentos e protocolos, comparação entre especialistas.
- **Construção:** adquirir e formalizar → implementar regras, interação e explicação → testar com casos e revisar com especialistas.
- **Ferramentas:** **shell** = recursos prontos de inferência; **CLIPS** = programação por regras; **Prolog** = fatos e regras lógicas.
- **Históricos:** **DENDRAL** (química, estruturas moleculares) e **MYCIN** (diagnóstico de infecções e antibióticos; origem do fator de certeza). Resultado em tarefa delimitada **não garante competência geral**.
- **Benefícios:** consultas recorrentes, critérios padronizados, justificativas registradas, treinamento, preservação de experiência.
- **Limitações:** conhecimento tácito difícil de formalizar; regras incompletas ou desatualizadas; fora do domínio, falha ou não responde.
- **Responsabilidade:** o usuário conhece o alcance; a base registra origem, versão e responsáveis; o que está fora do escopo vai para um humano.
- **Síntese:** o desempenho depende do conhecimento e da sua organização; explicação, testes e manutenção fazem parte do projeto.

---

## 9. Ética e uso de IA

**Lacuna:** a coluna de ética da ficha estava vazia. Relatório completo: [analise-etica.md](analise-etica.md).

### 9.1 Leitura e vídeo

- **Artigo:** Francisco Pires de Lacerda Júnior, *Da proibição à governança: uso ético da IA generativa na educação superior — revisão integrativa (2023–2026)*, Revista Foco, v. 19, n. 8, e12330, publicado em 07/08/2026 ([artigo](https://ojs.focopublicacoes.com.br/foco/article/view/12330) · [DOI](https://doi.org/10.54751/revistafoco.v19n8-017)).
  - **Resumo:** revisão integrativa qualitativa de 14 estudos científicos e 3 documentos normativos publicados entre jan. 2023 e jul. 2026, examinados por análise temática em cinco eixos: integridade e autoria; desenho da avaliação; letramento em IA e formação docente; governança institucional; e proteção de dados com supervisão humana. O debate deixa de focar só na fraude e passa a **políticas graduadas**, em que a permissão depende da finalidade pedagógica, da **declaração de uso** e da **responsabilização humana**. A proibição geral orienta pouco as práticas reais, e a liberação sem critérios transfere riscos ao estudante e ao professor. O autor propõe uma matriz de governança em cinco movimentos (**definir, ensinar, redesenhar, proteger e acompanhar**) e conclui que o caminho não é aceitar ou banir a IA generativa, mas tornar seus usos **justificáveis, verificáveis e compatíveis com os objetivos de aprendizagem**.
  - **Questão de integridade acadêmica (pedida no enunciado):** seguindo o artigo, declarar com clareza onde a IA generativa foi usada na elaboração do projeto e como o resultado foi conferido, para que a autoria e a responsabilidade pelas escolhas continuem sendo da equipe.
  - **No projeto:** declarar o uso de IA, verificar o que ela produziu e assumir a responsabilidade pelas decisões técnicas.
- **Vídeo:** IEA-USP, *O Estado da Arte em Ética na Inteligência Artificial*, evento público de 09/06/2026 (2h01), no lançamento do livro *The Palgrave Handbook on the Ethics of Artificial Intelligence*, com Veridiana Cordeiro, Steven Gouveia, João Cortese e Mateus Henrique Amorim; discute impactos sociais, éticos e institucionais da IA ([YouTube](https://www.youtube.com/watch?v=x35_NJfXrpE) · [IEA-USP](https://www.iea.usp.br/midiateca/video/videos-2026/o-estado-da-arte-em-etica-na-inteligencia-artificial/)).
  - **00:06:18** — a ética da IA não pode ser reduzida a uma "lista formal de conformidade": além de perguntar se um sistema é exato, justo ou transparente, é preciso ver como as instituições e os incentivos compõem a cena e como a noção de responsabilidade está sendo redesenhada.
  - **01:35:50 a 01:36:55** — ferramentas de IA são vendidas como neutras e como "solução mágica", mas não são neutras nem nos dados nem nos vieses; costumam ser comparadas por falsos positivos e falsos negativos em uma tarefa isolada, enquanto o problema real nunca é uma tarefa só.

### 9.2 Os 5 eixos (situação → afetados → medida)

| Eixo | Situação concreta | Quem é afetado | Medida adotada ou proposta |
|---|---|---|---|
| **Privacidade** | a mensagem pode revelar número, e-mail, relações ou dados privados | remetente e destinatário | só 4 respostas manuais; sem armazenamento, sem banco, sem integração com e-mail; minimização de dados; versão com mensagens reais exige nova revisão (LGPD) |
| **Viés e equidade** | aviso legítimo de universidade ou organização nova, com link curto e remetente desconhecido, aciona R1 | quem depende da comunicação | resultado é recomendação, não descarte; testes cobrem o falso positivo; antes de uso real, medir erros em amostras de várias origens e rever regras injustas |
| **Transparência** | usuário recebe alerta sem saber por quê | usuário | rastro mostra regras confirmadas, refutadas e inconclusivas e as premissas; aviso de que as regras não foram validadas |
| **Supervisão e responsabilidade** | comunicado de trabalho legítimo marcado como suspeito | usuário e remetente | **não move nem apaga** mensagens; decisão final humana; pode responder de novo; equipe revisa regras, testes e documentação |
| **Impacto social** | alertas ajudam a perceber golpes, mas erram nos dois sentidos | sociedade | limites explícitos; nada de bloqueio definitivo; testar falsos positivos e negativos em amostra autorizada antes de uso fora da sala de aula |

### 9.3 Dilema ético

- **Pergunta:** o sistema deve descartar automaticamente ou só alertar e pedir revisão humana?
- **A — descarte automático:** menos esforço manual; risco de **perder mensagem legítima** de forma irreversível, porque os sinais não bastam para separar os casos.
- **B — alerta + revisão humana (implementada):** mais esforço de avaliação; **preserva a autonomia** e evita perda irreversível.
- **Para debate:** em que situação a automação poderia agir sem confirmação? Quem responde por uma mensagem legítima perdida?
- **Ideia do vídeo usada no debate:** o trecho de 01:35:50 sustenta a alternativa B. O filtro também é especializado em uma tarefa estreita (quatro sinais) e erra nos dois sentidos; tratá-lo como neutro e deixá-lo descartar mensagens sozinho repetiria o problema apontado no vídeo. Por isso a saída é recomendação, e a decisão fica com uma pessoa.

### 9.4 Declaração de uso de IA

- **IA incorporada ao projeto:** sistema especialista por regras SE–ENTÃO, com encadeamento para trás; sem ação automática na caixa de e-mail. O ML aparece só no notebook (árvore com dados fictícios e regra R4).
- **Verificação:** 16 testes automatizados; GitHub Actions aprovado (execuções 1 e 2, 17/11/2026). Os testes validam a lógica, **não** a acurácia nem a equidade com mensagens reais.
- **IA usada na elaboração:** ChatGPT (OpenAI) e Claude (Anthropic) para análise do enunciado, revisão de código, testes, documentação de riscos, redação, material de consulta e notebook. A equipe conferiu o código, os testes e o texto e responde pela entrega.

### 9.5 Texto para a coluna de ética da ficha
> O Filtro de Spam usa apenas quatro respostas manuais (sim, não ou não sei), sem armazenar mensagens, sem banco de dados e sem envio a serviços externos. As regras são hipóteses didáticas, não validadas com mensagens reais. Um aviso legítimo com link encurtado pode virar falso positivo, por isso o sistema só recomenda revisão humana: nunca move nem apaga mensagens. O rastro mostra quais regras foram confirmadas, refutadas ou ficaram inconclusivas, e "não sei" nunca é tratado como "não". Entre descartar automaticamente e alertar com revisão humana, escolhemos alertar, para preservar a autonomia do usuário e evitar perda irreversível. Usamos o ChatGPT e o Claude como apoio na análise do enunciado, revisão de código, testes e redação. As regras, a verificação dos testes e a responsabilidade pela entrega são da equipe. Relatório: https://github.com/Lucasdoreac/filtro-spam-lfa/blob/main/docs/analise-etica.md

### 9.6 Reflexões individuais

- **Lucas Dórea:** Eu manteria a alternativa B, só alertar e recomendar revisão humana. Apagar uma mensagem legítima é um erro pior e irreversível, enquanto um alerta a mais custa apenas alguns segundos de conferência. Eu verificaria essa escolha contando, numa amostra autorizada de mensagens, quantas legítimas seriam marcadas por R1 ou R2: são os falsos positivos que um descarte automático teria apagado.
- **Deivid Cerqueira:** Eu manteria a alternativa B, pois alertar e recomendar revisão humana protege comunicações legítimas sem entregar ao sistema uma decisão irreversível. A discussão sobre falsos positivos e sobre a responsabilidade pelo descarte me fez perceber que a eficiência da automação não deve prevalecer sobre o custo de uma mensagem importante perdida. Eu verificaria essa medida com uma amostra autorizada de mensagens reais, comparando alertas com situações confirmadas e acompanhando a quantidade de falsos positivos e falsos negativos.

---

## 10. Comparação com os colegas

**Lacuna:** faltava situar o projeto frente às outras técnicas da turma.

| Técnica | Grupos | Grupo 13 |
|---|---|---|
| Encadeamento para trás | 6 (frente + trás), 13 | sim |
| Encadeamento para frente | 5, 7, 8, 11, 14, 15, 16, 18, 20, 23, 24, 25, 26 | — |
| '?' tratado como desconhecido | 5, 13, 15, 23, 25 | sim (3 valores) |
| Fator de certeza (MYCIN) | 6, 20 | não |
| Híbrido com árvore de decisão | 5, 6, 10, 14, 15, 16, 23, 25 | sim, no notebook (R4, dados fictícios) |
| Outro ML ou LLM | 20 (TF-IDF + reg. logística), 12 (Gemini), 26 (RAG + juiz LLM) | não |
| Conflito por prioridade ou especificidade | 5 (especificidade), 23 e 25 (prioridade) | ordem fixa |
| Como? / Por quê? interativo | 23, 25 | só Como? (rastro) |
| Testes automatizados (declarados na ficha) | 5 (3 asserts), 20 (40+), 24 (14), 25 (12) | sim (16 + CI) |

- **Projetos parecidos (filtro de mensagens):** 9 (R1/R3 quase iguais), 11, 18, 20, 23.
- **Nossos pontos fortes:** lógica de 3 valores, controle de ciclo, curto-circuito, 16 testes com CI, limites declarados, relatório de ética separado.
- **Pontos fracos:** sem CF, sem "Por quê?" interativo, só 3 regras; o ML existe só no notebook e com dados fictícios.

---

## 11. Perguntas prováveis e respostas curtas

- **Qual conhecimento foi difícil transformar em regra?** "Link duvidoso" e "urgência" dependem de julgamento: não há critério objetivo único. Por isso a pessoa responde em vez de o sistema detectar.
- **Quando a recomendação deveria ser suspensa?** Quando há '?' (fica inconclusiva) e fora do domínio (mensagens sem esses sinais). Também por isso nunca há descarte automático.
- **Que evidência mostraria que a base precisa de revisão?** Uma taxa alta de falsos positivos ou negativos medida numa amostra real e autorizada de mensagens.
- **Por que para trás e não para frente?** Objetivo único e menos perguntas: no caso A, 2 perguntas em vez de 4.
- **O que é a memória de trabalho no código?** O dicionário `Motor.fatos`, com respostas e conclusões intermediárias como `spam`.
- **Por que "não" não significa "seguro"?** Só 4 sinais são verificados. Golpe sem esses sinais passa: falso negativo.
- **O que acontece com ciclo de regras?** O motor detecta o símbolo no caminho e devolve inconclusivo (`test_ciclo_termina_como_inconclusivo`).
- **Por que não descartar automaticamente?** Falso positivo apagaria mensagem legítima de forma irreversível. Escolhemos a alternativa B do dilema.
- **Onde estão base, motor e explicação?** `base.py`, `motor.py` e `cli.py` (`explicar`).
- **Onde está o aprendizado de máquina?** No notebook do Colab: a árvore prevê `suspeita_ml`, que vira fato para a R4. O sistema principal continua só com regras.
- **Como rodar?** `python cli.py` e `python -m unittest discover -v` (Python 3.9+), ou o [notebook no Colab](https://colab.research.google.com/github/Lucasdoreac/filtro-spam-lfa/blob/main/notebook.ipynb).
