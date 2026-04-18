# Prompt 1.3-B Deploy Pilot

## Objetivo e escopo

Subir o `n8n` dedicado do tenant `cli-eleva-pilot` na VPS Hostinger em `https://wf-pilot.elevalocal.shop`, com Redis dedicado, labels Traefik compativeis com Coolify e rollback preservando o stack compartilhado.

Este procedimento assume que o provisioner em `main` ja contem os fixes de Redis namespaced e labels Coolify. Os antigos blocos de hotfix manual foram substituidos por verificacoes objetivas do compose gerado.

## Pre-requisitos

- DNS `A` de `wf-pilot.elevalocal.shop` apontando para `2.24.199.157`.
- SSH ou terminal web como `root` na VPS.
- Coolify e Traefik ativos.
- Network Docker externa `coolify` existente.
- Manifest validado em `tenants/manifests/cli-eleva-pilot.yaml`.
- Cofre do tenant pronto para receber os segredos gerados.
- `main` atualizado com o provisioner corrigido.

## Bloco 0 — Variaveis

Edite antes de executar se for outro tenant:

```bash
TENANT_ID="cli-eleva-pilot"
SLUG="eleva-pilot"
DOMAIN="wf-pilot.elevalocal.shop"
REPO="/root/elevalocal-infra"
STACK_DIR="${REPO}/tenants/runtime/${TENANT_ID}"
ROUTER="n8n-pilot"
```

## Bloco 1 — Atualizar repo e gerar compose

```bash
cd "${REPO}" && git pull origin main
ls ops/provision-n8n-dedicated.py && echo "OK provisioner"
python3 ops/provision-n8n-dedicated.py --tenant-id "${TENANT_ID}" --domain "${DOMAIN}" --force
ls -la "${STACK_DIR}/"
```

Esperado: `docker-compose.yml` e `.env.example` em `${STACK_DIR}`.

## Bloco 2 — Verificar Redis namespaced

```bash
grep -n "${TENANT_ID}-redis" "${STACK_DIR}/docker-compose.yml"
grep -n "QUEUE_BULL_REDIS_HOST: ${TENANT_ID}-redis" "${STACK_DIR}/docker-compose.yml"
if grep -n "QUEUE_BULL_REDIS_HOST: redis" "${STACK_DIR}/docker-compose.yml"; then
  echo "ERRO: Redis generico ainda presente"
  exit 1
fi
```

Esperado: service Redis, `depends_on` e `QUEUE_BULL_REDIS_HOST` usando `${TENANT_ID}-redis`.

## Bloco 3 — Verificar labels Coolify

```bash
grep -n "traefik.http.routers.${ROUTER}-http.entrypoints=http" "${STACK_DIR}/docker-compose.yml"
grep -n "traefik.http.routers.${ROUTER}-http.middlewares=redirect-to-https" "${STACK_DIR}/docker-compose.yml"
grep -n "traefik.http.routers.${ROUTER}.entrypoints=https" "${STACK_DIR}/docker-compose.yml"
grep -n "traefik.http.routers.${ROUTER}.tls=true" "${STACK_DIR}/docker-compose.yml"
grep -n "traefik.http.routers.${ROUTER}.service=${ROUTER}" "${STACK_DIR}/docker-compose.yml"
grep -n "traefik.http.services.${ROUTER}.loadbalancer.server.port=5678" "${STACK_DIR}/docker-compose.yml"
grep -n "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https" "${STACK_DIR}/docker-compose.yml"
if grep -n "entrypoints=websecure" "${STACK_DIR}/docker-compose.yml"; then
  echo "ERRO: label websecure antiga ainda presente"
  exit 1
fi
```

Esperado: router HTTP com redirect, router HTTPS em `https`, `tls=true`, `router.service` e service na porta `5678`.

## Bloco 4 — Gerar segredos e criar `.env`

Execute na VPS. Nao cole os valores em chat.

```bash
PG_PASS=$(openssl rand -base64 32 | tr -d '/+=\n')
ENC_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)

printf 'POSTGRES_PASSWORD=%s\n' "$PG_PASS"
printf 'N8N_ENCRYPTION_KEY=%s\n' "$ENC_KEY"
printf 'N8N_USER_MANAGEMENT_JWT_SECRET=%s\n' "$JWT_SECRET"
```

Registre esses tres valores no cofre do tenant antes de continuar.

```bash
cat > "${STACK_DIR}/.env" <<EOF
N8N_IMAGE=n8nio/n8n:2.15.0
POSTGRES_IMAGE=postgres:16.4-alpine
REDIS_IMAGE=redis:7.4-alpine
N8N_DOMAIN=${DOMAIN}
POSTGRES_DB=n8n_${SLUG//-/_}
POSTGRES_USER=n8n_${SLUG//-/_}
POSTGRES_PASSWORD=${PG_PASS}
N8N_ENCRYPTION_KEY=${ENC_KEY}
N8N_USER_MANAGEMENT_JWT_SECRET=${JWT_SECRET}
TRAEFIK_NETWORK=coolify
EOF

if grep -q CHANGE_ME "${STACK_DIR}/.env"; then
  echo "ERRO: .env contem CHANGE_ME"
  exit 1
fi
echo "OK sem CHANGE_ME"
```

## Bloco 5 — Subir a stack

```bash
cd "${STACK_DIR}" && docker compose up -d
sleep 25
docker ps --format "table {{.Names}}\t{{.Status}}" | grep "${TENANT_ID}"
```

Esperado: 4 containers `Up`: `n8n`, `n8n-worker`, `postgresql` e `${TENANT_ID}-redis`.

## Bloco 6 — Smoke tests

```bash
docker exec "${TENANT_ID}-n8n-n8n-1" wget -qO- http://localhost:5678/healthz
docker logs "${TENANT_ID}-n8n-n8n-1" --tail 30 | grep -i "Editor is now accessible"
curl -sI --max-time 10 "https://${DOMAIN}" | head -3
curl -sI --max-time 10 "http://${DOMAIN}" | head -5
```

Esperado:

- healthz: `{"status":"ok"}`
- logs: linha com `https://${DOMAIN}`
- HTTPS: `HTTP/2 200` ou `HTTP/2 302`
- HTTP: redirect para `https://${DOMAIN}`

Se qualquer smoke falhar, nao criar owner. Diagnosticar logs, labels, rede `coolify` e DNS antes de continuar.

## Bloco 7 — Criar owner no navegador

Abra `https://${DOMAIN}` no navegador, preencha o setup inicial e salve imediatamente no cofre do tenant:

- URL
- email do owner
- senha do owner
- nome exibido
- data/hora da criacao

Nao cole email/senha em chat ou arquivo versionado.

## Bloco 8 — Registrar evidencia

```bash
cd "${REPO}"
cat > /tmp/prompt-1.3b-evidence.txt <<EOF
tenant: ${TENANT_ID}
slug: ${SLUG}
domain: ${DOMAIN}
data: $(date -Iseconds)
containers:
$(docker ps --format "{{.Names}} {{.Status}}" | grep "${TENANT_ID}")
healthz: $(docker exec "${TENANT_ID}-n8n-n8n-1" wget -qO- http://localhost:5678/healthz 2>/dev/null)
curl: $(curl -sI --max-time 10 "https://${DOMAIN}" | head -1)
owner: criado e registrado no cofre do tenant
EOF
cat /tmp/prompt-1.3b-evidence.txt
```

Cole esse output em `MIGRATION-PILOT.md`, na secao `Evidencia de execucao`, e no ledger operacional.

## Backlog imediato pos-execucao

- Confirmar que o provisioner segue emitindo Redis `{tenant_id}-redis`.
- Confirmar que as labels Traefik seguem o padrao Coolify deste runbook.
- Regenerar runtime de `cli-demo-externo` com o provisioner corrigido e comparar estrutura normalizada.
- Manter `docs/N8N-DEDICATED-RUNBOOK.md` atualizado com as licoes aprendidas.

## Criterios de DONE

- [ ] `https://${DOMAIN}` devolve `200` ou redirect esperado para o editor.
- [ ] owner criado e credenciais registradas no cofre.
- [ ] evidencia colada em `MIGRATION-PILOT.md` e no ledger.
- [ ] backlog pos-execucao registrado.
