# Chatwoot Status

## Estado documental atual

O stack do `Chatwoot` foi observado na VPS e ja tem prova operacional basica,
mas ainda nao tem runbook no mesmo nivel de detalhamento do `n8n`.

## Containers observados

- `chatwoot-c8ecfzoz3ddr69y9c4bto96s`
- `sidekiq-c8ecfzoz3ddr69y9c4bto96s`
- `postgres-c8ecfzoz3ddr69y9c4bto96s`
- `redis-c8ecfzoz3ddr69y9c4bto96s`

## Volumes observados

- `c8ecfzoz3ddr69y9c4bto96s_postgres-data`
- `c8ecfzoz3ddr69y9c4bto96s_rails-data`
- `c8ecfzoz3ddr69y9c4bto96s_redis-data`

## O que ja foi provado

- dominio operacional: `chat.elevalocal.shop`
- aplicacao do `Chatwoot` responde corretamente
- token novo do `Chatwoot` foi validado manualmente
- backup local recorrente cobre banco e volumes observados do stack
- restore drill do `Chatwoot`: validado em ambiente controlado

## O que ainda nao foi formalizado

- runbook de recovery de conta admin
- versao explicita congelada do `Chatwoot`
- registro de RPO/RTO do stack
- rotina de validacao periodica do `sidekiq`

## Verificacoes imediatas na VPS

### Estado dos containers

```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | grep c8ecfzoz3ddr69y9c4bto96s
```

### Env efetiva do app

```bash
docker inspect chatwoot-c8ecfzoz3ddr69y9c4bto96s --format '{{range .Config.Env}}{{println .}}{{end}}'
```

### Labels do proxy

```bash
docker inspect chatwoot-c8ecfzoz3ddr69y9c4bto96s --format '{{json .Config.Labels}}'
```

### Logs do app

```bash
docker logs --tail 200 chatwoot-c8ecfzoz3ddr69y9c4bto96s
```

### Logs do worker

```bash
docker logs --tail 200 sidekiq-c8ecfzoz3ddr69y9c4bto96s
```

### Conferencia dos volumes

```bash
docker volume ls | grep c8ecfzoz3ddr69y9c4bto96s
```

## Backup minimo necessario

### Banco

Usar [ops/backup-elevalocal.sh](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/backup-elevalocal.sh) ou executar manualmente:

```bash
docker inspect postgres-c8ecfzoz3ddr69y9c4bto96s --format '{{range .Config.Env}}{{println .}}{{end}}'
```

Depois, com usuario, senha e database confirmados:

```bash
docker exec -e PGPASSWORD='SENHA' -t postgres-c8ecfzoz3ddr69y9c4bto96s pg_dump -U USUARIO -d DATABASE > /root/eleva-backups/chatwoot-$(date +%F-%H%M).sql
```

### Arquivos persistentes

```bash
docker run --rm -v c8ecfzoz3ddr69y9c4bto96s_rails-data:/source:ro -v /root/eleva-backups:/backup alpine sh -lc "cd /source && tar czf /backup/chatwoot-rails-data-$(date +%F-%H%M).tar.gz ."
```

## Restore minimo a provar

1. restaurar dump do Postgres em ambiente controlado
2. restaurar `rails-data`
3. validar login admin
4. abrir inbox e mensagens
5. validar jobs do `sidekiq`

## Riscos abertos

- sem recovery documentado de admin
- `Chatwoot` ainda em `latest`, com risco de drift
- sem politica de retencao
