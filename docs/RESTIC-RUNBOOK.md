# Restic Runbook

## Objetivo

Padronizar o bootstrap, a operacao diaria e o restore seletivo do backup offsite criptografado da Eleva Local usando `restic` com Backblaze B2 ou Cloudflare R2.

## Pre-requisitos

- `restic >= 0.17`
- segredo do repositorio guardado fora do git e acessado por `RESTIC_PASSWORD_FILE`
- inventario/owner de segredo mantido em [docs/SECRETS-MANAGEMENT.md](/C:/Users/PEDROSO/Downloads/elevalocal-infra/docs/SECRETS-MANAGEMENT.md)
- se o segredo for persistido no workspace, manter apenas o YAML cifrado via `sops` + `age`
- o arquivo lido por `RESTIC_PASSWORD_FILE` deve ser plaintext temporario no host, por exemplo em `/run/elevalocal/`, gerado a partir do inventario cifrado

## Bootstrap do repositorio

1. criar ou recuperar a senha do repositorio
2. armazenar a senha em arquivo local seguro fora do git ou em YAML cifrado via `sops`
3. preencher `backup-elevalocal.env` com:
   - `BACKUP_MODE=restic`
   - `RESTIC_REPOSITORY=...`
   - `RESTIC_PASSWORD_FILE=...`
   - credenciais do provider via env
4. se a origem da senha estiver cifrada em `sops`, decriptar para arquivo temporario antes do cron:

```bash
mkdir -p /run/elevalocal
sops -d /root/elevalocal-infra/tenants/secrets/.vault/restic-repository-password.enc.yaml \
  | awk -F': ' '/^password:/ {print $2}' > /run/elevalocal/restic-repository-password
chmod 600 /run/elevalocal/restic-repository-password
```
5. inicializar o repositorio se ainda nao existir:

```bash
restic init
```

Observacao: [ops/backup-elevalocal.sh](/C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/backup-elevalocal.sh) ja tenta inicializar automaticamente se `restic snapshots` falhar por repositorio inexistente.

## Execucao diaria

Cron recomendado:

```cron
0 3 * * * /root/elevalocal-infra/ops/backup-elevalocal.sh
0 4 * * 0 /root/elevalocal-infra/ops/restic-check.sh
```

Fluxo esperado do backup diario:

1. gerar SQLs e `tar.gz` locais em `/root/eleva-backups/<timestamp>`
2. enviar o diretorio inteiro para o repositorio `restic`
3. rodar `restic check --read-data-subset=5%`
4. aplicar `restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12`
5. enviar webhook de sucesso ou falha

## Restore seletivo

### Por snapshot

```bash
restic snapshots
restic restore <snapshot_id> --target /tmp/restore-elevalocal
```

### Por path

```bash
restic restore <snapshot_id> \
  --target /tmp/restore-elevalocal \
  --include /root/eleva-backups/<timestamp>/n8n-postgres.sql
```

### Por tag

```bash
restic snapshots --tag elevalocal
restic snapshots --tag timestamp=2026-04-17-030000
```

## Restore controlado de SQL

1. restaurar um `*.sql` aleatorio para diretorio temporario
2. calcular hash do original e do restaurado
3. comparar bit-for-bit:

```bash
sha256sum /root/eleva-backups/<timestamp>/n8n-postgres.sql
sha256sum /tmp/restore-elevalocal/root/eleva-backups/<timestamp>/n8n-postgres.sql
cmp -s /root/eleva-backups/<timestamp>/n8n-postgres.sql /tmp/restore-elevalocal/root/eleva-backups/<timestamp>/n8n-postgres.sql
```

4. registrar evidencia no checklist

## Rotacao de chave do repositorio

1. gerar nova senha
2. atualizar o arquivo referenciado por `RESTIC_PASSWORD_FILE`
3. rodar:

```bash
restic key passwd
```

4. atualizar o inventario cifrado em `tenants/secrets/.vault/`
5. validar `restic snapshots`
6. executar um backup manual controlado e um restore seletivo pequeno

## Healthchecks.io

Payloads esperados:

- sucesso:
  - `✅ Backup Eleva Local OK — snapshot {snapshot_id} — {size_gb}GB — {duration}`
- falha:
  - `🚨 Backup Eleva Local FALHOU — stack: {stack} — erro: {error_summary} — verifique /var/log/elevalocal-backup.log`
- integridade:
  - `⚠️ Restic check detectou corrupção — snapshot {id} — NÃO usar esse snapshot para restore`

## Guardrails

- nao remover `BACKUP_MODE=local_only`
- nao ativar `forget --prune` automaticamente nos primeiros 30 dias
- nao commitar credenciais de B2/R2 nem senha do repositorio
- nao considerar launch-ready sem snapshot remoto + restore testado
