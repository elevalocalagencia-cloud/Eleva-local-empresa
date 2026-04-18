#!/usr/bin/env bash
set -euo pipefail

TENANT_ID=""
DOMAIN=""
EXPECTED_WEBHOOK_STATUS="${EXPECTED_WEBHOOK_STATUS:-404}"
WEBHOOK_PATH="${WEBHOOK_PATH:-/webhook/tenant-smoke}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-15}"

usage() {
  cat <<'EOF'
Uso:
  ops/smoke-test-tenant.sh --tenant-id cli-eleva-pilot --domain wf-pilot.elevalocal.shop

Variaveis opcionais:
  EXPECTED_WEBHOOK_STATUS=200  # use 200 depois de importar um workflow de smoke
  WEBHOOK_PATH=/webhook/tenant-smoke
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tenant-id)
      TENANT_ID="${2:-}"
      shift 2
      ;;
    --domain)
      DOMAIN="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Argumento desconhecido: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "${TENANT_ID}" || -z "${DOMAIN}" ]]; then
  usage >&2
  exit 1
fi

BASE_URL="https://${DOMAIN}"

check_status() {
  local label="$1"
  local url="$2"
  local expected="$3"
  local status

  status="$(curl -sS -o /dev/null -w '%{http_code}' --max-time "${TIMEOUT_SECONDS}" "${url}")"
  if [[ "${status}" != "${expected}" ]]; then
    echo "FAIL ${label}: esperado=${expected} obtido=${status} url=${url}" >&2
    return 1
  fi
  echo "OK ${label}: ${status}"
}

echo "Smoke tenant=${TENANT_ID} domain=${DOMAIN}"
check_status "healthz" "${BASE_URL}/healthz" "200"
check_status "login-page" "${BASE_URL}/signin" "200"
check_status "webhook" "${BASE_URL}${WEBHOOK_PATH}" "${EXPECTED_WEBHOOK_STATUS}"
echo "SMOKE_OK tenant=${TENANT_ID}"
