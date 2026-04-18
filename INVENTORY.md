# Inventory

## VPS

- Provedor: Hostinger
- Tipo: VPS KVM 2
- Hostname observado: `srv1588299.hstgr.cloud`
- Host local observado: `eleva-local`
- IP publico: `2.24.199.157`
- SO observada: `Ubuntu 22.04.5 LTS`

## Painel de orquestracao

- Plataforma: Coolify
- Versao observada: `4.0.0-beta.473`
- Proxy publico: Traefik (`coolify-proxy`)
- Porta publica do painel Coolify: `8000`

## Dominios e subdominios observados

- dominio principal: `elevalocal.shop`
- `www.elevalocal.shop`
- `n8m.elevalocal.shop`
- `www.n8m.elevalocal.shop`
- `portainer.elevalocal.shop`
- `www.portainer.elevalocal.shop`
- `webhook.elevalocal.shop`
- `www.webhook.elevalocal.shop`
- `api.elevalocal.shop`
- `www.api.elevalocal.shop`
- `wf-demo.elevalocal.shop` (demo publica planejada)

## Servicos observados

### Core infra

- `coolify`
- `coolify-proxy`
- `coolify-db`
- `coolify-redis`
- `coolify-realtime`
- `coolify-sentinel`

### n8n stack

- `n8n-mamtm8g3b2mdh7ko0hxdcyr3`
- `n8n-worker-mamtm8g3b2mdh7ko0hxdcyr3`
- `task-runners-mamtm8g3b2mdh7ko0hxdcyr3`
- `postgresql-mamtm8g3b2mdh7ko0hxdcyr3`
- `redis-mamtm8g3b2mdh7ko0hxdcyr3`

### Chatwoot stack

- `chatwoot-c8ecfzoz3ddr69y9c4bto96s`
- `sidekiq-c8ecfzoz3ddr69y9c4bto96s`
- `postgres-c8ecfzoz3ddr69y9c4bto96s`
- `redis-c8ecfzoz3ddr69y9c4bto96s`

### Evolution API stack

- `api-rh7m1i3wfmf9254fhcb4pn5p`
- `postgres-rh7m1i3wfmf9254fhcb4pn5p`
- `redis-rh7m1i3wfmf9254fhcb4pn5p`

## Volumes observados

### n8n

- `mamtm8g3b2mdh7ko0hxdcyr3_n8n-data`
- `mamtm8g3b2mdh7ko0hxdcyr3_postgresql-data`
- `mamtm8g3b2mdh7ko0hxdcyr3_redis-data`

### Chatwoot

- `c8ecfzoz3ddr69y9c4bto96s_postgres-data`
- `c8ecfzoz3ddr69y9c4bto96s_rails-data`
- `c8ecfzoz3ddr69y9c4bto96s_redis-data`

### Evolution API

- `rh7m1i3wfmf9254fhcb4pn5p_postgres-data`
- `rh7m1i3wfmf9254fhcb4pn5p_evolution-instances`
- `rh7m1i3wfmf9254fhcb4pn5p_evolution-redis`

## Portas publicas observadas

- `80`
- `443`
- `8000`
- `8080`
- `6001-6002`

## Arquivos de auditoria criados na VPS

- `/root/eleva-audit/n8n-compose.yml`
- `/root/eleva-audit/n8n-compose-fixed.yml`
- `/root/eleva-audit/n8n-env.txt`
- `/root/eleva-audit/n8n-inspect.json`
- `/root/eleva-audit/n8n-postgres-inspect.json`
- `/root/eleva-backups/n8n-2026-04-17-1639.sql`
- `/root/eleva-backups/n8n-2026-04-17-1650.sql`
