#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEMO_RUNTIME_DIR="${DEMO_RUNTIME_DIR:-${WORKSPACE_ROOT}/tenants/runtime/cli-demo-externo}"
HEALTHCHECK_PING_URL="${DEMO_RESET_HEALTHCHECK_PING_URL:-}"
KEEP_N8N_DATA="${KEEP_N8N_DATA:-false}"
DEMO_OWNER_EMAIL="${DEMO_OWNER_EMAIL:-demo@elevalocal.shop}"

notify() {
  local suffix="$1"
  local payload="$2"
  if [[ -z "${HEALTHCHECK_PING_URL}" ]]; then
    return 0
  fi

  curl -fsS -m 15 -X POST --data-binary "${payload}" "${HEALTHCHECK_PING_URL}${suffix}" >/dev/null
}

require_file() {
  local path="$1"
  if [[ ! -f "${path}" ]]; then
    echo "arquivo obrigatorio ausente: ${path}" >&2
    exit 1
  fi
}

cd "${DEMO_RUNTIME_DIR}"
require_file ".env"
require_file "docker-compose.yml"

notify "/start" "demo-reset-start"

docker compose --env-file .env down
docker volume rm -f cli-demo-externo-postgresql-data cli-demo-externo-redis-data

if [[ "${KEEP_N8N_DATA}" != "true" ]]; then
  docker volume rm -f cli-demo-externo-n8n-data
fi

docker compose --env-file .env up -d
docker compose --env-file .env exec -T n8n n8n import:workflow --separate --input=/seed-workflows

cat <<EOF
Reset da demo concluido.

Owner demo esperado: ${DEMO_OWNER_EMAIL}

Passo manual obrigatorio apos reset total de banco:
1. abrir https://wf-demo.elevalocal.shop
2. concluir o setup inicial do owner demo na UI
3. guardar a senha somente no cofre interno

Referencia oficial:
- https://docs.n8n.io/hosting/cli-commands/
- o CLI documenta 'n8n user-management:reset', mas a criacao do owner volta para o fluxo de setup na UI.
EOF

notify "" "demo-reset-ok"
