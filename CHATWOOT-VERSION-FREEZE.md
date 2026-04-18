# Chatwoot Version Freeze

## Objetivo

Fechar o bloqueio de lancamento relacionado ao uso de `latest` no `Chatwoot`.

## Estado atual

- imagem observada no runbook: `chatwoot/chatwoot:latest`
- risco atual: drift de deploy e rollback nao deterministico

## Passos obrigatorios

1. inspecionar a imagem atualmente em execucao na VPS
2. registrar a tag ou digest efetivo
3. escolher a versao explicita alvo
4. atualizar stack para usar tag fixa
5. registrar rollback para a mesma versao

## Evidencia a coletar

- imagem atual observada:
- digest atual observado:
- versao congelada escolhida:
- data da mudanca:
- responsavel:

## Execucao 2026-04-18

- imagem atual observada antes da mudanca: `chatwoot/chatwoot:latest`
- digest atual observado antes da mudanca: `sha256:548710d17cd70b40b402eca3fced7325ebac6a3a998f2accb18fbc574393f458`
- versao congelada escolhida: `chatwoot/chatwoot:v4.12.0`
- data da mudanca: `2026-04-18`
- responsavel: `eleva-local-ops`

### Justificativa da versao

- `v4.13.0` era a ultima release publicada, mas ainda nao tinha mais de 30 dias de circulacao upstream em `2026-04-18`
- `v4.12.1` tambem ainda nao cumpria o criterio de mais de 30 dias
- `v4.12.0`, publicada em `2026-03-17`, cumpria o criterio de release estavel `v4.x` com mais de 30 dias

### Backup pre-freeze

- comando executado: `bash /root/elevalocal-infra/ops/backup-elevalocal.sh`
- resultado: backup local concluido em `/root/eleva-backups/2026-04-18-150757`
- artefatos confirmados:
  - `chatwoot-postgres.sql` (`264K`)
  - `chatwoot-rails-data.tar.gz` (`60K`)
  - `chatwoot-redis-data.tar.gz` (`39K`)
- observacao: o envio `restic` falhou por ausencia de `RESTIC_PASSWORD_FILE=/run/elevalocal/restic-repository-password`; o freeze foi executado com base no backup local confirmado

### Stack congelada

- compose alterado em `/data/coolify/services/c8ecfzoz3ddr69y9c4bto96s/docker-compose.yml`
- rails:
  - container: `chatwoot-c8ecfzoz3ddr69y9c4bto96s`
  - imagem final: `chatwoot/chatwoot:v4.12.0`
  - digest final: `sha256:40b967510e0f75d5d6af582fa321f27431b401651efbb0b545e6392f8b71d159`
- worker:
  - container: `sidekiq-c8ecfzoz3ddr69y9c4bto96s`
  - imagem final: `chatwoot/chatwoot:v4.12.0`
  - digest final: `sha256:40b967510e0f75d5d6af582fa321f27431b401651efbb0b545e6392f8b71d159`

### Smoke test pos-freeze

- status dos containers:
  - `chatwoot-c8ecfzoz3ddr69y9c4bto96s` -> `Up ... (healthy)`
  - `sidekiq-c8ecfzoz3ddr69y9c4bto96s` -> `Up ... (healthy)`
- HTTP:
  - `curl -I https://chat.elevalocal.shop` -> `HTTP/2 200`
- logs:
  - app respondeu `GET /` com sucesso apos a subida
  - `sidekiq` inicializou e conectou no Redis sem erro critico
- login pela UI: `PENDENTE_VALIDACAO_MANUAL`
- envio/recebimento em inbox existente: `PENDENTE_VALIDACAO_MANUAL`

### Rollback path

- restaurar compose anterior:

```bash
cp /root/chatwoot-freeze-before-2026-04-18.yml /data/coolify/services/c8ecfzoz3ddr69y9c4bto96s/docker-compose.yml
cd /data/coolify/services/c8ecfzoz3ddr69y9c4bto96s
docker compose up -d
```

- rollback por tag explicita, se o snapshot anterior nao estiver disponivel:

```bash
sed -i "s#chatwoot/chatwoot:v4.12.0#chatwoot/chatwoot:latest#g" /data/coolify/services/c8ecfzoz3ddr69y9c4bto96s/docker-compose.yml
cd /data/coolify/services/c8ecfzoz3ddr69y9c4bto96s
docker compose up -d
```

- backup de referencia para restore: `/root/eleva-backups/2026-04-18-150757`

## Gate de encerramento

- [x] stack nao usa mais `latest`
- [x] versao fixa registrada no runbook
- [x] rollback da mesma versao documentado
- [x] smoke test do app e worker executado
