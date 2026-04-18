# Runbook Executivo

## Estado atual

- `n8n`: operacional
- `Chatwoot`: operacional
- `Evolution`: operacional
- `n8m.elevalocal.shop`: operacional
- `chat.elevalocal.shop`: operacional
- `api.elevalocal.shop`: operacional em HTTPS
- `Coolify`: fora da internet publica
- `6001` e `6002`: fora da internet publica

## O que ja foi provado

- restore do `n8n`
- restore do `Chatwoot`
- restore da `Evolution`
- backup recorrente instalado
- mitigacao da superficie publica administrativa

## Modelo multi-cliente

- adotar `tenant_id` e `slug` como identificadores operacionais obrigatorios
- cada cliente deve nascer via `ops/create-tenant.py`
- cada cliente deve ter manifest YAML proprio antes de provisionamento
- o manifest deve ser validado com `ops/validate-tenant-manifest.py`
- `Evolution`, `Chatwoot`, automacoes e segredos devem ser nomeados por tenant
- nenhuma venda nova deve entrar sem inventario, backup e owners por tenant

## P0

- manter `Coolify` e `coolify-realtime` fora da internet publica
- nao reabrir `8000`, `6001` e `6002` sem necessidade operacional controlada
- nao provisionar cliente novo manualmente sem scaffolding e validacao
- fechar as 4 frentes P0 do lancamento antes de chamar operacao de pronta para vender:
  - offsite backup
  - rotacao de segredos
  - freeze de versao do `Chatwoot`
  - primeiro provisionamento externo real

## P1

- congelar versoes criticas
- registrar oficialmente `redis:7-alpine` no stack atual do `n8n`
- revisar os artefatos mais recentes em `/root/eleva-backups`
- manter revisao periodica do log de backup
- consolidar manifests de tenant e validar antes de rollout

### Versoes operacionais atuais a congelar

- `n8n`: `n8nio/n8n:2.10.4`
- `Redis do stack atual do n8n`: `redis:7-alpine`
- `Postgres do stack atual do n8n`: `postgres:16-alpine`
- `Chatwoot`: `chatwoot/chatwoot:latest` (pendente de fixar versao explicita)
- `Evolution`: `evoapicloud/evolution-api:v2.3.7`
- `Coolify`: `4.0.0-beta.473`

### Rotina minima de revisao de backup

1. verificar os 3 diretorios mais recentes em `/root/eleva-backups`
2. confirmar presenca de:
   - `n8n.sql`
   - `chatwoot.sql`
   - `evolution.sql`
   - `n8n-data.tar.gz`
   - `chatwoot-rails-data.tar.gz`
   - `evolution-instances.tar.gz`
3. revisar `/var/log/elevalocal-backup.log`
4. registrar data da ultima verificacao

## P2

- replanejar migracao definitiva do `n8n` sem duplicar Redis/Postgres

### Referencias operacionais

- [OFFSITE-BACKUP.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/OFFSITE-BACKUP.md)
- [N8N-MIGRATION.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/N8N-MIGRATION.md)
- [LAUNCH-AUDIT.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-AUDIT.md)
- [LAUNCH-READINESS-LEDGER.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-READINESS-LEDGER.md)
- [LAUNCH-EXECUTION-BOARD.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-EXECUTION-BOARD.md)

## Regra de mudanca

- sem backup novo, nao mudar stack critico
- sem rollback claro, nao mudar stack critico
- sem restore validado, nao considerar operacao pronta para vender
- sem manifest valido por tenant, nao provisionar cliente novo

## Proxima evolucao recomendada

1. copia offsite dos backups
2. runbook de rollback por stack
3. migracao definitiva do `n8n`
4. monitoramento e alertas basicos
