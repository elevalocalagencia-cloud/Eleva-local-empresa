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

## Ledger canonico

| Item | Status | Evidencia atual no repo | Owner atual | Prioridade | Bloqueia `GO CONTROLADO`? |
| --- | --- | --- | --- | --- | --- |
| Stacks principais operacionais | `DONE` | `n8n`, `Chatwoot` e `Evolution` descritos como operacionais | `eleva-local-ops` | `P0` | `SIM` |
| Backup local recorrente | `DONE` | script, cron e log documentados | `eleva-local-ops` | `P0` | `SIM` |
| Restore drill local dos 3 stacks | `DONE` | `BACKUP-RESTORE.md` e runbooks afirmam restore validado | `eleva-local-ops` | `P0` | `SIM` |
| Guardrail multi-tenant no onboarding | `DONE` | manifests, registry e policy de `n8n dedicated` para cliente externo | `eleva-local-ops` | `P0` | `SIM` |
| Offsite backup validado | `OPEN` | existe checklist, mas sem evidencia de execucao remota | `eleva-local-ops` | `P0` | `SIM` |
| Rotacao de segredos pos-investigacao | `OPEN` | existe checklist, mas sem evidencia de rotacao concluida | `eleva-local-ops` | `P0` | `SIM` |
| Freeze de versao do `Chatwoot` | `OPEN` | risco documentado; stack ainda referenciada em `latest` | `eleva-local-ops` | `P0` | `SIM` |
| Primeiro provisionamento externo real ponta a ponta | `OPEN` | existe baseline `cli-demo-externo`, mas nao ha go-live real provado | `eleva-local-ops` | `P0` | `SIM` |
| RPO/RTO por stack | `OPEN` | citado como pendente em auditoria | `eleva-local-ops` | `P1` | `NAO` |
| Sales enablement | `DONE` | material versionado em `docs/sales/` e estrategia de dominios em `docs/DOMAIN-STRATEGY.md`; landing publica mantida fora do repo em `elevalocal.com.br`; CTAs especificados em `docs/sales/LANDING-CTA-SPEC.md` | `eleva-local-ops` | `P1` | `NAO` |
| Monitoramento e alertas por tenant | `OPEN` | citado como pendente em auditoria | `eleva-local-ops` | `P1` | `NAO` |
| Processo recorrente de rotacao por tenant | `OPEN` | politica ainda nao formalizada com evidencia recorrente | `eleva-local-ops` | `P1` | `NAO` |
| Migracao definitiva do `n8n` | `OPEN` | runbook existe, mas mudanca definitiva nao foi executada | `eleva-local-ops` | `P1` | `NAO` |

## Estado derivado

### `GO CONTROLADO`

So pode ser declarado quando todos os itens `P0` com bloqueio `SIM` estiverem em `DONE`.

### `GO COMERCIAL`

So pode ser declarado quando:

- todos os `P0` estiverem em `DONE`
- os `P1` relevantes de governanca estiverem fechados ou formalmente aceitos

## Evidencias de tenant atualmente conhecidas

### `cli-eleva-pilot`

- tipo: tenant interno
- runtime `n8n`: `shared-foundation`
- status de restore no registry: `validated`

### `cli-demo-externo`

- tipo: tenant externo de simulacao
- runtime `n8n`: `dedicated`
- status de onboarding no registry: `pending`
- status de restore no registry: `pending`

## Regra de atualizacao

- nao marcar `DONE` sem evidencia real no repositorio ou artefato operacional explicitamente registrado
- qualquer mudanca de prioridade de launch deve ser feita primeiro aqui
