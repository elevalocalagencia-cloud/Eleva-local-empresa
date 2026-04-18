# Backup Checklist

## Revisao minima semanal

1. listar os 3 diretorios mais recentes em `/root/eleva-backups`
2. confirmar em cada um:
   - `n8n-postgres.sql`
   - `chatwoot-postgres.sql`
   - `evolution-postgres.sql`
   - `n8n-data.tar.gz`
   - `chatwoot-rails-data.tar.gz`
   - `evolution-instances.tar.gz`
   - `manifest.txt`
3. revisar `/var/log/elevalocal-backup.log`
4. se `BACKUP_MODE=restic`, confirmar `restic snapshots` com snapshot do ultimo dia
5. registrar data da verificacao e operador

## Revisao offsite com restic

1. validar que `RESTIC_PASSWORD_FILE` aponta para segredo mantido via `sops` + `age`
2. validar que o `HEALTHCHECK_PING_URL` foi copiado da tela do Healthchecks e que o script deriva `/start` e `/fail`
3. executar `ops/restic-check.sh` no dry-run em ambiente controlado antes da janela semanal
4. confirmar que o ultimo backup enviou webhook de sucesso:
   - `✅ Backup Eleva Local OK - snapshot {snapshot_id} - {size_gb}GB - {duration}`
5. confirmar que existe teste controlado do webhook de falha:
   - `🚨 Backup Eleva Local FALHOU - stack: {stack} - erro: {error_summary} - verifique /var/log/elevalocal-backup.log`
6. confirmar que alertas de integridade estao roteados:
   - `⚠️ Restic check detectou corrupcao - snapshot {id} - NAO usar esse snapshot para restore`
7. se `OFFSITE_BUCKET_QUOTA_GB` estiver configurado, revisar se o bucket segue abaixo de 80% da cota

## Revisao por tenant

Para cada cliente novo ou alterado:

1. validar o manifest com `python ops/validate-tenant-manifest.py CAMINHO_DO_MANIFEST.yaml`
2. confirmar `tenant_id` e `slug` unicos no registry
3. registrar `last backup check`
4. registrar `restore validated`
5. confirmar owners responsaveis pelo tenant

## Restore drill minimo

- `n8n`: validado localmente; falta restore remoto controlado com snapshot restic
- `Chatwoot`: validado localmente; falta restore remoto controlado com snapshot restic
- `Evolution`: validado localmente; falta restore remoto controlado com snapshot restic

## O que falta para nivel comercial

- snapshot remoto real em `restic`
- retencao remota comprovada por evidencia
- restore bit-for-bit de um SQL remoto em ambiente controlado
- webhooks `Healthchecks.io` comprovados em sucesso e falha
- revisao trimestral do restore drill
- registry/manifest multi-cliente mantido atualizado por tenant
