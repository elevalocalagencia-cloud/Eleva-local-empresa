# Offsite Backup

## Objetivo

Subir os artefatos locais de backup da `elevalocal` para um repositorio offsite criptografado com `restic`, mantendo o modo local como safety net operacional.

## Arquitetura vigente

- camada local obrigatoria: [ops/backup-elevalocal.sh](/C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/backup-elevalocal.sh) gera SQLs + `tar.gz` em `/root/eleva-backups/<timestamp>`
- offsite preferencial: `BACKUP_MODE=restic`
- modos suportados:
  - `local_only`: somente backup local
  - `rsync`: legado/transitorio para copia remota sem criptografia nativa
  - `restic`: repositorio remoto criptografado em `b2:` ou `s3:https://...r2...`
- verificacao semanal dedicada: [ops/restic-check.sh](/C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/restic-check.sh)

## Estado atual

- backup local recorrente: instalado
- restore drill local: validado nos 3 stacks
- offsite criptografado por `restic`: pronto para bootstrap, ainda depende de configuracao e execucao real
- launch readiness: continua P0 ate existir evidencia de snapshot remoto valido + restore controlado

## Configuracao esperada

Arquivo base:

- [ops/backup-elevalocal.env.example](/C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/backup-elevalocal.env.example)
- [docs/RESTIC-RUNBOOK.md](/C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/RESTIC-RUNBOOK.md)

Variaveis obrigatorias para `restic`:

- `BACKUP_MODE=restic`
- `RESTIC_REPOSITORY=b2:elevalocal-backups-prod:/prod`
  ou `RESTIC_REPOSITORY=s3:https://{account}.r2.cloudflarestorage.com/elevalocal-backups`
- `RESTIC_PASSWORD_FILE=/caminho/seguro/restic-password`
- `HEALTHCHECK_PING_URL=https://hc-ping.com/<uuid-do-check>`
- opcionalmente, override manual de `HEALTHCHECK_URL_START`, `HEALTHCHECK_URL_SUCCESS` e `HEALTHCHECK_URL_FAIL`

Credenciais por provider:

- Backblaze B2: `B2_ACCOUNT_ID`, `B2_ACCOUNT_KEY`
- Cloudflare R2: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION=auto`

## Politica operacional

- backup diario: `03:00 UTC`
- check completo semanal: domingo `04:00 UTC`
- Healthchecks: usar um check diario para backup e, idealmente, um segundo check semanal para `ops/restic-check.sh`
- check amostral diario apos backup: `restic check --read-data-subset=5%`
- retencao remota: `--keep-daily 7 --keep-weekly 4 --keep-monthly 12`
- nos primeiros 30 dias: executar `forget` sem `--prune`
- se `restic` falhar, o backup local continua existindo e nao deve ser desativado

## Evidencia minima para tirar o bloqueio P0

1. existe snapshot remoto listado por `restic snapshots`
2. o `Healthchecks.io` recebeu sucesso e falha de teste controlado
3. um SQL restaurado em ambiente controlado ficou bit-for-bit identico ao original
4. o check semanal completo passou ao menos uma vez
5. o owner registrou data, destino e operador responsavel no checklist de backup
