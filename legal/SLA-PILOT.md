# ANEXO DE SLA - PILOTO ASSISTIDO

Este anexo integra o `CONTRATO-PSA-TEMPLATE.md`.

## 1. Escopo do SLA piloto

1.1. O SLA piloto aplica-se a tenants em onboarding controlado, homologacao assistida ou operacao inicial acompanhada pela `{{CONTRATADA_RAZAO_SOCIAL}}`.

1.2. Este anexo reflete o estado operacional descrito em `LAUNCH-AUDIT.md`: existe `GO CONTROLADO` apenas para onboarding altamente assistido, sem readiness para escala comercial ampla.

## 2. Disponibilidade alvo

2.1. Meta mensal de disponibilidade do portal e das automacoes contratadas: **99,0%** por mes civil.

2.2. A meta exclui:
- manutencoes programadas avisadas com antecedencia razoavel;
- indisponibilidade causada por provedores de terceiros fora do controle direto da CONTRATADA;
- erro operacional ou atraso da CONTRATANTE em fornecer acesso, aprovacao, conteudo, credenciais ou interlocutor;
- incidentes decorrentes de alteracoes unilaterais da CONTRATANTE ou de terceiros autorizados por ela.

## 3. Janela de atendimento

3.1. Atendimento operacional em horario comercial de `{{SLA_HORARIO_ATENDIMENTO}}`, em dias uteis, no fuso `{{SLA_FUSO_HORARIO}}`.

3.2. Chamados fora da janela serao registrados no proximo periodo util, salvo combinado diferente na proposta comercial.

## 4. Tempos de resposta

4.1. Tempo inicial de resposta para qualquer incidente operacional aberto pela CONTRATANTE: ate **48 horas uteis**.

4.2. Como se trata de piloto assistido, o prazo acima vale para triagem inicial, nao para resolucao definitiva.

## 5. Classificacao de incidentes

5.1. `P1 - Critico`: indisponibilidade total do fluxo contratado ou risco relevante de mensagem no tenant errado.

5.2. `P2 - Alto`: degradacao relevante sem parada total, falha persistente de automacao critica ou atraso operacional significativo.

5.3. `P3 - Medio`: erro contornavel, ajuste de configuracao, duvida funcional ou inconsistencias de cadastro.

5.4. `P4 - Baixo`: melhoria, ajuste cosmetico, copy, treinamento ou apoio consultivo.

## 6. Diretrizes de operacao do piloto

6.1. A CONTRATADA operara o tenant com acompanhamento manual forte, observando os gates de `FIRST-EXTERNAL-PROVISIONING.md` e `tenants/templates/onboarding-checklist.md`.

6.2. A CONTRATADA mantera:
- inbox dedicada por tenant no `Chatwoot`;
- instancia dedicada por tenant no `Evolution`;
- `n8n dedicated` para cliente externo, conforme `MULTITENANT-AUDIT.md`.

6.3. A CONTRATADA nao promete isolamento absoluto, mas adota segregacao operacional mensurada por naming, namespace, ownership de credenciais e checklist por tenant.

## 7. Backup, restore e blast radius

7.1. O piloto inclui backup recorrente e restore drill local por stack, conforme `LAUNCH-AUDIT.md`.

7.2. A copia offsite somente sera considerada coberta por este SLA se estiver formalmente validada para o tenant, nos termos de `OFFSITE-VALIDATION-CHECKLIST.md`.

7.3. A recuperacao ainda e orientada prioritariamente por stack, e nao por tenant, conforme ressalva de `MULTITENANT-AUDIT.md`.

7.4. Em caso de incidente cross-tenant, a prioridade operacional sera:
1. pausar automacoes afetadas;
2. isolar credenciais e canais;
3. limitar blast radius;
4. registrar causa, horario e tenant impactado;
5. retomar somente apos correcao e smoke test.

## 8. Credenciais e mudancas

8.1. Segredos e acessos observarao `docs/SECRETS-MANAGEMENT.md` e `SECRET-ROTATION-CHECKLIST.md`.

8.2. Mudancas relevantes em workflows, canais ou credenciais poderao exigir janela operacional curta, rollback pronto e smoke test com base em `ops/smoke-test-tenant.sh`.

## 9. Creditos de servico

9.1. Se a disponibilidade mensal ficar abaixo de 99,0%, a CONTRATANTE podera solicitar credito comercial equivalente a `{{SLA_PILOT_CREDITO_PERCENTUAL}}` da mensalidade do mes afetado.

9.2. O credito:
- nao e cumulativo com perdas e danos ou multa;
- depende de pedido em ate `{{SLA_PRAZO_REQUISICAO_CREDITO_DIAS}}` dias apos o fechamento do mes;
- nao se aplica a fases gratuitas, provas de conceito ou atrasos causados pela CONTRATANTE.

## 10. Limites

10.1. Este SLA nao cobre:
- desenvolvimento sob demanda fora do escopo contratado;
- integracoes novas nao homologadas;
- reversao de alteracoes executadas pela propria CONTRATANTE;
- indisponibilidade de terceiros como OpenAI, Anthropic, Meta, provedor de hospedagem, e-mail ou internet do cliente.

10.2. O SLA piloto nao substitui o dever da CONTRATANTE de designar interlocutor, aprovar automacoes e responder validacoes criticas.
