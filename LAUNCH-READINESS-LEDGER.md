# Launch Readiness Ledger

## Objetivo

Ser a fonte canonica de readiness de lancamento da operacao `Eleva Local`.

Este arquivo existe para eliminar conflito entre:

- estado operacional
- decisao de lancamento
- execucao dos itens P0

## Regra de uso

- este ledger define prioridade, status e impacto sobre `GO / NO-GO`
- `LAUNCH-AUDIT.md` resume a decisao executiva a partir deste ledger
- `LAUNCH-EXECUTION-BOARD.md` usa este ledger para acompanhar execucao
- handoffs antigos de sessao nao devem redefinir prioridade de launch

## Legenda de status

- `DONE`: evidenciado e fechado
- `OPEN`: ainda pendente
- `PARTIAL`: trilha existe, mas evidencia de fechamento ainda nao existe
- `READY-PENDING-CLIENT`: tecnica pronta, aguardando cliente real
- `DONE-TECNICO`: base tecnica pronta; execucao comercial depende de insumo externo
- `DONE-TARGETS`: targets internos definidos e publicados
- `DONE-PLAYBOOK`: cadencia e regra operacional formalizadas

## Ledger canonico

| Item | Status | Evidencia atual no repo | Owner atual | Prioridade | Bloqueia `GO CONTROLADO`? |
| --- | --- | --- | --- | --- | --- |
| Stacks principais operacionais | `DONE` | `n8n`, `Chatwoot` e `Evolution` descritos como operacionais | `eleva-local-ops` | `P0` | `SIM` |
| Backup local recorrente | `DONE` | script, cron e log documentados | `eleva-local-ops` | `P0` | `SIM` |
| Restore drill local dos 3 stacks | `DONE` | `BACKUP-RESTORE.md` e runbooks afirmam restore validado | `eleva-local-ops` | `P0` | `SIM` |
| Guardrail multi-tenant no onboarding | `DONE` | manifests, registry e policy de `n8n dedicated` para cliente externo | `eleva-local-ops` | `P0` | `SIM` |
| Offsite backup validado | `OPEN` | existe checklist, mas sem evidencia de execucao remota | `eleva-local-ops` | `P0` | `SIM` |
| Rotacao de segredos pos-investigacao | `OPEN` | existe checklist, mas sem evidencia de rotacao concluida | `eleva-local-ops` | `P0` | `SIM` |
| Freeze de versao do `Chatwoot` | `DONE` | `CHATWOOT-VERSION-FREEZE.md` registra freeze em `2026-04-18` para `chatwoot/chatwoot:v4.12.0` com backup local pre-freeze e rollback documentado | `eleva-local-ops` | `P0` | `SIM` |
| Primeiro provisionamento externo real ponta a ponta | `READY-PENDING-CLIENT` | scaffold, checklist, portal sem hardcode do piloto, estrutura `tenants/evidence/` e `legal/signed/` prontas; aguardando cliente real para executar `2.5-B` | `eleva-local-ops` | `P0` | `SIM` |
| GO CONTROLADO tecnico | `DONE-TECNICO` | base tecnica shelf-ready para os proximos clientes; execucao comercial ainda depende do primeiro cliente real em `2.5-B` | `eleva-local-ops` | `P0` | `NAO` |
| RPO/RTO por stack | `DONE-TARGETS` | `2026-04-18`: targets internos definidos em [docs/RPO-RTO.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RPO-RTO.md); validacao pratica segue por drill trimestral | `eleva-local-ops` | `P1` | `NAO` |
| Rotina trimestral de restore drill | `DONE-PLAYBOOK` | `2026-04-18`: cadencia formalizada em [docs/RESTORE-DRILL-PLAYBOOK.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RESTORE-DRILL-PLAYBOOK.md); primeiro registro em [tenants/evidence/_drills/2026-Q2-n8n-dedicated.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/evidence/_drills/2026-Q2-n8n-dedicated.md) | `eleva-local-ops` | `P1` | `NAO` |
| Demo publica ativa | `PARTIAL` | runtime, reset, evidencias e portal demo preparados no repo; DNS `wf-demo.elevalocal.shop` e deploy VPS ainda pendentes nesta sessao | `eleva-local-ops` | `P1` | `NAO` |
| Monitoramento e alertas por tenant | `OPEN` | citado como pendente em auditoria | `eleva-local-ops` | `P1` | `NAO` |
| Processo recorrente de rotacao por tenant | `OPEN` | politica ainda nao formalizada com evidencia recorrente | `eleva-local-ops` | `P1` | `NAO` |
| Migracao definitiva do `n8n` | `OPEN` | runbook existe, mas mudanca definitiva nao foi executada | `eleva-local-ops` | `P1` | `NAO` |

## Estado derivado

### `GO CONTROLADO`

Do ponto de vista tecnico, a base pode ser tratada como `DONE-TECNICO` quando os
guardrails, freeze, scaffold e shelf-ready estiverem registrados. A entrada em
operacao comercial real continua dependendo do primeiro cliente externo em `2.5-B`.

### `GO COMERCIAL`

So pode ser declarado quando:

- todos os `P0` executaveis estiverem em `DONE`
- o primeiro cliente externo real estiver evidenciado
- os `P1` relevantes de governanca estiverem fechados ou formalmente aceitos

## Evidencias de tenant atualmente conhecidas

### `cli-eleva-pilot`

- tipo: tenant interno
- runtime `n8n`: `shared-foundation`
- status de restore no registry: `validated`
- evidencia: [tenants/evidence/cli-eleva-pilot/2026-04-18-provisioning.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/evidence/cli-eleva-pilot/2026-04-18-provisioning.md)

### `cli-demo-externo`

- tipo: tenant externo de simulacao
- runtime `n8n`: `dedicated`
- status de onboarding no registry: `pending`
- status de restore no registry: `pending`

## Regra de atualizacao

- nao marcar `DONE` sem evidencia real no repositorio ou artefato operacional explicitamente registrado
- qualquer mudanca de prioridade de launch deve ser feita primeiro aqui
