# CONTRATO DE PRESTACAO DE SERVICOS

Pelo presente instrumento particular, de um lado:

**{{CLIENTE_RAZAO_SOCIAL}}**, inscrita no CNPJ sob o no `{{CLIENTE_CNPJ}}`, com sede em `{{CLIENTE_ENDERECO}}`, neste ato representada por `{{CLIENTE_REPRESENTANTE}}`, doravante denominada **CONTRATANTE**; e

**{{CONTRATADA_RAZAO_SOCIAL}}**, inscrita no CNPJ sob o no `{{CONTRATADA_CNPJ}}`, com sede em `{{CONTRATADA_ENDERECO}}`, neste ato representada por `{{CONTRATADA_REPRESENTANTE}}`, doravante denominada **CONTRATADA**.

As Partes resolvem celebrar o presente Contrato de Prestacao de Servicos, regido pelas clausulas abaixo.

## 1. Partes

1.1. As qualificacoes completas das Partes constam do preambulo e de seus anexos cadastrais.

1.2. Os avisos contratuais serao enviados aos enderecos e e-mails:
- CONTRATANTE: `{{CLIENTE_EMAIL_CONTRATUAL}}`
- CONTRATADA: `{{CONTRATADA_EMAIL_CONTRATUAL}}`

## 2. Objeto

2.1. O objeto deste Contrato e a implementacao, configuracao, integracao, sustentacao e operacao continua de automacoes B2B, atendimento omnichannel, portal operacional, rotinas de acompanhamento e suporte relacionados ao ambiente da CONTRATANTE.

2.2. O servico e prestado sobre infraestrutura e componentes como `Evolution`, `Chatwoot`, `n8n`, `Supabase`, portal web e rotinas operacionais da CONTRATADA, conforme escopo contratado e anexo tecnico aplicavel.

## 3. Escopo

3.1. Integram o escopo core, quando contratados:
- provisionamento inicial do tenant;
- configuracao de canais e inbox;
- configuracao e operacao de workflows de automacao definidos no onboarding;
- suporte operacional recorrente;
- portal com visualizacao de informacoes operacionais disponibilizadas ao tenant;
- backup recorrente da operacao conforme plano contratado;
- reporting periodico resumido em `{{CADENCIA_REPORT}}`.

3.2. Ficam fora do escopo core e serao orcados a parte como upsell:
- novas integracoes nao previstas na proposta;
- desenvolvimento de automacoes fora do backlog contratado;
- operacao fora da janela padrao de atendimento;
- migracao extraordinaria, saneamento de base historica ou reprocessamento manual macico;
- BI customizado, dashboards sob demanda ou treinamento extra;
- suporte juridico, compliance setorial especifico ou due diligence de terceiros.

3.3. O detalhamento operacional do tenant deve observar o manifesto e o checklist aplicavel, especialmente:
- `tenants/templates/tenant-manifest.example.yaml`
- `tenants/templates/onboarding-checklist.md`
- `tenants/templates/client-ops-checklist.md`

## 4. Prazo e vigencia

4.1. Este Contrato entra em vigor em `{{DATA_INICIO_CONTRATO}}` e vigera por prazo inicial minimo de **3 (tres) meses**.

4.2. Apos o prazo inicial, a renovacao sera automatica por periodos sucessivos de `{{PERIODO_RENOVACAO_MESES}}` meses, salvo denuncia por qualquer Parte com antecedencia minima de 30 dias.

## 5. Preco e forma de pagamento

5.1. Pela prestacao dos servicos, a CONTRATANTE pagara:
- setup unico de `{{MOEDA}} {{VALOR_SETUP}}`;
- mensalidade recorrente de `{{MOEDA}} {{VALOR_MENSALIDADE}}`;
- eventuais servicos extras mediante aprovacao escrita.

5.2. O vencimento ocorrera todo dia `{{DIA_VENCIMENTO}}`.

5.3. O atraso no pagamento podera acarretar:
- multa de `{{MULTA_ATRASO_PERCENTUAL}}%`;
- juros de `{{JUROS_ATRASO_PERCENTUAL}}%` ao mes, pro rata;
- correcao monetaria;
- suspensao dos servicos apos `{{DIAS_ATRASO_SUSPENSAO}}` dias de inadimplencia, respeitadas obrigacoes legais de guarda e transicao.

5.4. Os valores serao reajustados anualmente pelo IPCA, ou indice que o substitua.

## 6. Responsabilidades da CONTRATADA

6.1. Sao obrigacoes da CONTRATADA:
- implementar e operar os servicos conforme este Contrato e seus anexos;
- manter trilha operacional minima de onboarding, naming, ownership e checklists por tenant;
- operar canais, automacoes e portal dentro do escopo contratado;
- reportar incidentes e indisponibilidades relevantes na forma do SLA e do DPA;
- manter medidas tecnicas e administrativas razoaveis de seguranca;
- adotar esforcos comercialmente razoaveis para limitar blast radius e evitar contaminacao cross-tenant;
- manter backup recorrente e restore conforme o plano contratado e o estado real da operacao.

6.2. A CONTRATADA nao assume obrigacao de resultado comercial, venda, conversao, receita ou performance de campanhas da CONTRATANTE.

## 7. Responsabilidades da CONTRATANTE

7.1. Sao obrigacoes da CONTRATANTE:
- fornecer informacoes, acessos e aprovacoes necessarias no prazo combinado;
- indicar ao menos um interlocutor responsavel;
- garantir que os dados, contatos, mensagens e instrucoes enviados a CONTRATADA sejam licitos;
- validar escopo, regras de negocio, copys, prompts, workflows e automacoes antes de go-live;
- revisar e aprovar o manifesto operacional do tenant;
- contratar e manter os provedores sob sua exclusiva governanca, quando houver;
- atender solicitacoes de seguranca, rotacao de credenciais e saneamento de acesso.

7.2. A CONTRATANTE reconhece que atrasos na aprovacao, ausencia de interlocutor, dados inconsistentes ou restricoes tecnicas externas podem impactar cronograma, SLA e entrega.

## 8. Propriedade intelectual

8.1. Ferramentas, frameworks, conectores genericos, runbooks, templates, bibliotecas e know-how preexistentes da CONTRATADA permanecem de sua titularidade.

8.2. Workflows, configuracoes, prompts, playbooks e automacoes customizadas e pagas especificamente pela CONTRATANTE serao disponibilizadas a ela ao final da relacao, observado:
- adimplemento integral;
- ausencia de segredo de terceiros;
- prazo de transicao de **30 dias** apos a rescisao.

8.3. Durante o periodo de transicao, a CONTRATADA cooperara de forma razoavel para exportacao tecnica dos ativos customizados da CONTRATANTE.

## 9. Confidencialidade

9.1. As Partes obrigam-se a preservar a confidencialidade das informacoes trocadas, nos termos do `NDA-TEMPLATE.md` ou de instrumento equivalente assinado entre as Partes.

## 10. Protecao de dados

10.1. Quando houver tratamento de dados pessoais, aplicam-se a LGPD e o `DPA-LGPD-TEMPLATE.md`, que integra este Contrato.

10.2. A CONTRATANTE sera, em regra, a Controladora dos dados de seus clientes, leads, colaboradores e atendimentos.

10.3. A CONTRATADA atuara, em regra, como Operadora, sem prejuizo de tratamento proprio estritamente necessario para faturamento, seguranca, autenticacao, logs, prevencao a fraude e cumprimento legal.

## 11. Nivel de servico

11.1. O nivel de servico aplicavel sera aquele expressamente indicado na proposta comercial:
- `SLA-PILOT.md`, para onboarding e operacao assistida; ou
- `SLA-COMERCIAL.md`, para operacao recorrente pos-lancamento.

11.2. Nenhuma meta diversa sera valida sem aceite escrito entre as Partes.

## 12. Seguranca operacional, backup e restore

12.1. A CONTRATADA empregara controles compativeis com o estado real do repositorio e da operacao, inclusive segregacao por tenant, ownership de segredos, rotacao, backup, restore, smoke tests e rollback controlado.

12.2. As Partes reconhecem, de forma expressa, que:
- a CONTRATADA adota segregacao operacional forte, mas nao promete isolamento absoluto;
- o maior risco residual mapeado hoje e cross-tenant por erro operacional, conforme `MULTITENANT-AUDIT.md`;
- o estado de readiness comercial e o descrito em `LAUNCH-AUDIT.md`;
- copia offsite, restore por tenant e versoes congeladas por stack dependem do gate efetivamente concluido no ambiente.

## 13. Suspensao e rescisao

13.1. O Contrato podera ser rescindido:
- por qualquer Parte, sem causa, mediante aviso previo de 30 dias;
- por inadimplemento nao sanado em ate `{{PRAZO_CURA_DIAS}}` dias;
- de imediato, em caso de uso ilicito da plataforma, risco relevante a terceiros, violacao de confidencialidade ou descumprimento grave de protecao de dados.

13.2. Em caso de encerramento, a CONTRATADA entregara export tecnico razoavel dos ativos e dados da CONTRATANTE em ate **15 dias uteis**, ressalvados:
- dados de terceiros;
- segredos da CONTRATADA;
- componentes proprietarios reutilizaveis;
- dados cuja retencao seja exigida por lei.

13.3. A entrega podera ocorrer em formato de export de banco, arquivos, workflows, documentos ou outro meio tecnicamente razoavel.

## 14. Limitacao de responsabilidade

14.1. Exceto dolo, fraude, violacao de confidencialidade ou obrigacao legal inderrogavel, a responsabilidade total da CONTRATADA fica limitada ao montante pago pela CONTRATANTE nos `{{LIMITE_RESPONSABILIDADE_MESES}}` meses anteriores ao evento.

14.2. A CONTRATADA nao respondera por lucros cessantes indiretos, perda de oportunidade, dano reputacional reflexo ou prejuizo decorrente de falha exclusiva de terceiro fora de sua governanca.

## 15. Resolucao de conflitos

15.1. As Partes buscarao composicao amigavel em ate `{{PRAZO_NEGOCIACAO_DIAS}}` dias.

15.2. Nao havendo acordo, as Partes poderao optar por:
- **arbitragem**, nos termos da Lei no 9.307/1996, administrada por `{{CAMARA_ARBITRAL}}`, em `{{CIDADE_ARBITRAGEM}}`; ou
- **foro judicial** da Comarca de `{{FORO_CIDADE_UF}}`, caso a arbitragem nao seja escolhida na proposta.

## 16. Disposicoes finais

16.1. Este Contrato, seus anexos e a proposta comercial formam o acordo integral entre as Partes.

16.2. Alteracoes somente terao validade se feitas por escrito.

16.3. A eventual tolerancia de uma Parte nao implica renuncia de direito.

`{{LOCAL_ASSINATURA}}`, `{{DATA_ASSINATURA}}`.

---

**CONTRATANTE**  
`{{CLIENTE_RAZAO_SOCIAL}}`  
Nome: `{{CLIENTE_REPRESENTANTE}}`  
Cargo: `{{CLIENTE_CARGO_REPRESENTANTE}}`

**CONTRATADA**  
`{{CONTRATADA_RAZAO_SOCIAL}}`  
Nome: `{{CONTRATADA_REPRESENTANTE}}`  
Cargo: `{{CONTRATADA_CARGO_REPRESENTANTE}}`
