# Backup Restore

## Backup atual conhecido

### n8n

Dump SQLs criados inicialmente:

- `/root/eleva-backups/n8n-2026-04-17-1639.sql`
- `/root/eleva-backups/n8n-2026-04-17-1650.sql`

### Snapshots operacionais

- `/root/eleva-audit/n8n-compose.yml`
- `/root/eleva-audit/n8n-compose-fixed.yml`
- `/root/eleva-audit/n8n-env.txt`
- `/root/eleva-audit/n8n-inspect.json`
- `/root/eleva-audit/n8n-postgres-inspect.json`

## Comando de backup do banco do n8n

```bash
mkdir -p /root/eleva-backups
N8N_DB_USER="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | awk -F= '/^POSTGRES_USER=/{print $2}')"
N8N_DB_NAME="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | awk -F= '/^POSTGRES_DB=/{print $2}')"
N8N_DB_PASSWORD="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | awk -F= '/^POSTGRES_PASSWORD=/{print $2}')"
docker exec -i -e PGPASSWORD="${N8N_DB_PASSWORD}" postgresql-mamtm8g3b2mdh7ko0hxdcyr3 pg_dump -U "${N8N_DB_USER}" -d "${N8N_DB_NAME}" > /root/eleva-backups/n8n-$(date +%F-%H%M).sql
```

## Restore do banco do n8n

Somente com servico parado ou em janela controlada:

```bash
N8N_DB_USER="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | awk -F= '/^POSTGRES_USER=/{print $2}')"
N8N_DB_NAME="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | awk -F= '/^POSTGRES_DB=/{print $2}')"
N8N_DB_PASSWORD="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | awk -F= '/^POSTGRES_PASSWORD=/{print $2}')"
cat /root/eleva-backups/ARQUIVO.sql | docker exec -i -e PGPASSWORD="${N8N_DB_PASSWORD}" postgresql-mamtm8g3b2mdh7ko0hxdcyr3 psql -U "${N8N_DB_USER}" -d "${N8N_DB_NAME}"
```

## O que ainda falta

- validacao do conteudo dos diretorios mais recentes em `/root/eleva-backups`
- politica de retencao
- copia offsite
- registro formal de tempo e falhas do restore drill

## Padrao minimo agora definido

### Automacao local

Script base criado:

- [ops/backup-elevalocal.sh](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/backup-elevalocal.sh)
- [ops/backup-elevalocal.env.example](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/backup-elevalocal.env.example)

Cobertura prevista pelo script:

- dump SQL de `n8n`
- dump SQL de `Chatwoot`
- dump SQL de `Evolution API`
- empacotamento dos volumes persistentes observados dos tres stacks

Automacao efetivamente instalada na VPS:

- `/root/eleva-ops/backup-elevalocal.sh`
- `/etc/cron.d/elevalocal-backup`
- `/var/log/elevalocal-backup.log`

### Restore drill obrigatorio

Nao basta gerar arquivo. O minimo operacional passa a ser:

1. restaurar banco do `n8n` em ambiente controlado
2. restaurar banco do `Chatwoot` em ambiente controlado
3. restaurar banco da `Evolution API` em ambiente controlado
4. validar ao menos um volume critico por stack
5. registrar data e resultado do teste

Status atual:

- restore drill do `n8n`: validado
- restore drill do `Chatwoot`: validado
- restore drill da `Evolution API`: validado

## Evidencias adicionais desta sessao

- dump novo do banco do `n8n` foi gerado antes da recuperacao do owner
- a recuperacao de auth do `n8n` foi feita somente apos backup
- o restore deixou de ser hipotese e passou a ser provado nos tres stacks

## Regra operacional

Nao considerar backup pronto sem restore testado.

Tambem nao considerar backup comercialmente aceitavel sem:

- copia offsite
- revisao dos artefatos gerados
- versoes criticas congeladas no runbook
