# Ética e impactos — filtro de spam

Material de apoio ao debate da aula de 17/11/2026 (UDF, Inteligência Artificial e LFA). A análise refere-se ao **protótipo atual**, não a um produto validado.

## Sistema e decisão

O projeto é um sistema especialista didático que pergunta quatro sinais de suspeita, aplica três regras SE–ENTÃO por encadeamento para trás e recomenda **revisão humana** quando uma regra confirma um indício. O código não utiliza modelos preditivos nem coleta mensagens reais. Quem recebe uma mensagem é a pessoa mais afetada por sua recomendação; remetentes legítimos também podem sofrer com a perda de comunicação.

## Aspectos e medidas

| Aspecto | Situação concreta e pessoas afetadas | Medida da equipe |
| --- | --- | --- |
| Privacidade e dados | Mensagens podem conter dados pessoais do remetente e do destinatário. | Entrada manual de quatro sinais; nenhum conteúdo de e-mail ou identificador é armazenado pelo protótipo. |
| Viés e equidade | Pessoa ou instituição desconhecida que envie um link legítimo pode ser marcada como suspeita. | Tratar o resultado como indício, nunca prova; testar mensagens de origens variadas e rever regras. |
| Transparência | Usuário pode não entender por que recebeu alerta. | Exibir a regra disparada, as premissas e as limitações. |
| Supervisão e responsabilidade | A exclusão de uma mensagem legítima pode causar perdas. | Recomendar revisão humana; o protótipo não move ou apaga mensagens. |
| Impacto social | Alertas podem ajudar contra fraudes, mas classificações equivocadas prejudicam comunicações. | Informar falsos positivos/negativos e não recomendar uso automático em produção. |

## Dilema para o debate

**Opção A:** exclusão automática após acionar R1 ou R2 — reduz ações manuais, mas pode descartar avisos legítimos. **Opção B (adotada no código):** oferecer explicação e revisão humana — requer mais atenção, mas preserva a autonomia e diminui o risco de perdas irreversíveis.

## Testes e limitações

Há testes unitários de inferência, incerteza, ciclos, interface e casos que ilustram falso positivo. Eles verificam lógica; **não medem precisão real, justiça entre grupos nem taxa de erros**. Para isso seria necessário obter um conjunto autorizado e diversificado de mensagens rotuladas, avaliar falsos positivos/negativos, documentar a amostra e revisar regras.

## Uso de inteligência artificial — declaração a preencher pela equipe

**IA incorporada ao projeto:** sistema especialista baseado em regras humanas explícitas; entradas são respostas manuais e saída é recomendação explicada. Não há treinamento de modelo ou previsão estatística. A equipe deve registrar quais testes realmente executou e quem revisou o resultado.

**IA usada na elaboração do trabalho:** declarar ferramentas e versões efetivamente usadas e o que foi aceito, corrigido ou testado pela equipe; não atribuir autoria ou verificações não confirmadas.

**Para a atividade:** registrar a referência e minutagem do vídeo efetivamente assistido, a ideia extraída do artigo efetivamente lido e a reflexão individual escrita após o debate. Esses itens não são substituídos pela documentação técnica do repositório.
