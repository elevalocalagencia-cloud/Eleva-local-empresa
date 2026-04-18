# ANEXO DE SLA - OPERACAO COMERCIAL

Este anexo integra o `CONTRATO-PSA-TEMPLATE.md`.

## 1. Escopo do SLA comercial

1.1. O SLA comercial aplica-se apos conclusao de onboarding, com tenant provisionado, smoke tests aprovados e stack aderente ao manifesto operacional.

1.2. Este anexo pressupoe operacao em modo comercial com checklist de onboarding fechado, monitoramento basico e governanca ativa por tenant.

## 2. Disponibilidade alvo

2.1. Meta mensal de disponibilidade do portal e dos servicos contratados: **99,5%** por mes civil.

2.2. A meta exclui:
- manutencao programada comunicada com antecedencia razoavel;
- falha de terceiros fora da governanca direta da CONTRATADA;
- indisponibilidade causada por erro, omissao ou atraso da CONTRATANTE;
- forca maior, falha generalizada de nuvem, internet, energia, operadora de WhatsApp ou indisponibilidade do provider de IA.

## 3. Classificacao de incidentes

3.1. `P1 - Critico`: parada total do servico contratado, risco relevante de tratamento no tenant errado ou falha que impeca operacao principal do cliente.

3.2. `P2 - Alto`: degradacao severa com alternativa parcial.

3.3. `P3 - Medio`: defeito contornavel sem impacto material imediato.

3.4. `P4 - Baixo`: melhoria, ajuste incremental ou suporte consultivo.

## 4. Tempos de resposta

4.1. `P1`: primeira resposta em ate **4 horas uteis**.

4.2. `P2`: primeira resposta em ate `{{SLA_P2_RESPOSTA_HORAS_UTEIS}}` horas uteis.

4.3. `P3`: primeira resposta em ate `{{SLA_P3_RESPOSTA_HORAS_UTEIS}}` horas uteis.

4.4. `P4`: primeira resposta em ate `{{SLA_P4_RESPOSTA_HORAS_UTEIS}}` horas uteis.

## 5. Janela de atendimento

5.1. Atendimento operacional em `{{SLA_HORARIO_ATENDIMENTO}}`, em dias uteis, no fuso `{{SLA_FUSO_HORARIO}}`.

5.2. Plantao fora de horario comercial depende de contratacao expressa.

## 6. Medidas operacionais cobertas

6.1. A CONTRATADA mantera:
- segregacao por tenant em `Evolution`, `Chatwoot` e namespace de automacao;
- checklist recorrente por tenant com base em `tenants/templates/client-ops-checklist.md`;
- backup recorrente e trilha de restore conforme `docs/RESTIC-RUNBOOK.md`;
- politica de segredos e rotacao conforme `docs/SECRETS-MANAGEMENT.md`.

6.2. Havendo `n8n dedicated`, a CONTRATADA seguira o procedimento de migracao, corte e rollback previsto em `docs/N8N-DEDICATED-RUNBOOK.md`.

## 7. Backup, restore e continuidade

7.1. Backup recorrente integra a operacao.

7.2. Restore seletivo e restore controlado obedecerao `docs/RESTIC-RUNBOOK.md`.

7.3. Cobranca por continuidade em caso de desastre pressupoe que o tenant esteja:
- com manifesto valido;
- com inventario de segredos atualizado;
- com onboarding concluido;
- com qualquer requisito de offsite marcado como ativo e validado.

7.4. A CONTRATADA empregara esforcos comercialmente razoaveis para limitar blast radius e restaurar a operacao sem afetar outros tenants.

## 8. Creditos de servico

8.1. Se a disponibilidade mensal ficar:
- entre 99,0% e 99,49%: credito de `{{SLA_COMERCIAL_CREDITO_1_PERCENTUAL}}` da mensalidade;
- abaixo de 99,0%: credito de `{{SLA_COMERCIAL_CREDITO_2_PERCENTUAL}}` da mensalidade.

8.2. O credito:
- depende de solicitacao em ate `{{SLA_PRAZO_REQUISICAO_CREDITO_DIAS}}` dias apos o mes de referencia;
- nao gera devolucao em dinheiro, salvo previsao expressa em proposta;
- nao se soma a multa rescisoria ou indenizacao sem decisao especifica entre as Partes.

## 9. Exclusoes

9.1. Este SLA nao cobre:
- alteracoes, integracoes ou canais nao contratados;
- bases legadas com qualidade deficiente fornecidas pela CONTRATANTE;
- uso do sistema em desacordo com onboarding, manifesto ou treinamento;
- falha causada por credencial, token, dominio ou conta administrada exclusivamente pela CONTRATANTE.

## 10. Revisao

10.1. O presente SLA podera ser revisto a cada renovacao contratual, sempre respeitando a capacidade operacional efetivamente demonstrada e sem promessa de disponibilidade superior a 99,5% sem nova aprovacao tecnica e comercial.
