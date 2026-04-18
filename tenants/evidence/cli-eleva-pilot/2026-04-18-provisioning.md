# Evidencia de Provisionamento - cli-eleva-pilot

- data: 2026-04-18
- owner: eleva-local-ops
- tenant_id: cli-eleva-pilot
- slug: eleva-pilot
- status: piloto-interno

## Timeline

1. Provisionamento do `n8n` dedicado executado via `ops/provision-n8n-dedicated.py`.
2. Stack subida na VPS com `docker compose --env-file .env up -d`.
3. Smoke test parcial executado com health interno e roteamento HTTP/HTTPS.

## Smoke tests

- whatsapp: nao se aplica nesta evidencia
- chatwoot: nao se aplica nesta evidencia
- evolution: nao se aplica nesta evidencia
- n8n: containers `Up`, `healthz` retornando `{"status":"ok"}`
- portal: nao se aplica nesta evidencia
- resumo: parcial, com validacao de health interno e roteamento HTTP/HTTPS

## Evidencias anexadas

- print owner criado: owner registrado no cofre do tenant
- print go-live: nao houve go-live comercial
- output de comandos: ver resumo operacional abaixo

## Rollback e restore

- rollback_path: preservar stack compartilhada e retornar corte se houver regressao
- restore_drill: nao se aplica a esta evidencia especifica

## Observacoes

Resumo herdado de `MIGRATION-PILOT.md`:

```text
tenant: cli-eleva-pilot
slug: eleva-pilot
domain: wf-pilot.elevalocal.shop
data: 2026-04-18T10:53:41-03:00
containers:
cli-eleva-pilot-n8n-n8n-1 Up 40 minutes
cli-eleva-pilot-n8n-n8n-worker-1 Up 40 minutes
cli-eleva-pilot-n8n-postgresql-1 Up 40 minutes
cli-eleva-pilot-n8n-cli-eleva-pilot-redis-1 Up 40 minutes
healthz: {"status":"ok"}
https_code: 200
http_code: 302
http_redirect: https://wf-pilot.elevalocal.shop/
owner: criado e registrado no cofre do tenant
```
