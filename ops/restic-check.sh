#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/backup-elevalocal.env"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

RESTIC_REPOSITORY="${RESTIC_REPOSITORY:-}"
RESTIC_PASSWORD_FILE="${RESTIC_PASSWORD_FILE:-}"
HEALTHCHECK_URL_SUCCESS="${HEALTHCHECK_URL_SUCCESS:-}"
HEALTHCHECK_URL_FAIL="${HEALTHCHECK_URL_FAIL:-}"
B2_ACCOUNT_ID="${B2_ACCOUNT_ID:-}"
B2_ACCOUNT_KEY="${B2_ACCOUNT_KEY:-}"
AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-}"
AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-auto}"
DRY_RUN="${DRY_RUN:-false}"

log() {
  printf '[%s] %s\n' "$(date +%F' '%T)" "$*"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "comando obrigatorio ausente: $1" >&2
    exit 1
  }
}

restic_env() (
  export RESTIC_REPOSITORY="${RESTIC_REPOSITORY}"
  export RESTIC_PASSWORD_FILE="${RESTIC_PASSWORD_FILE}"

  if [[ -n "${B2_ACCOUNT_ID}" ]]; then
    export B2_ACCOUNT_ID="${B2_ACCOUNT_ID}"
  fi
  if [[ -n "${B2_ACCOUNT_KEY}" ]]; then
    export B2_ACCOUNT_KEY="${B2_ACCOUNT_KEY}"
  fi
  if [[ -n "${AWS_ACCESS_KEY_ID}" ]]; then
    export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
  fi
  if [[ -n "${AWS_SECRET_ACCESS_KEY}" ]]; then
    export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"
  fi
  if [[ -n "${AWS_DEFAULT_REGION}" ]]; then
    export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}"
  fi

  restic "$@"
)

notify_healthcheck() {
  local url="$1"
  local payload="$2"

  if [[ -z "${url}" ]]; then
    return 0
  fi

  if [[ "${DRY_RUN}" == "true" ]]; then
    log "dry-run: webhook ${url} <- ${payload}"
    return 0
  fi

  curl -fsS -m 15 -X POST --data-binary "${payload}" "${url}" >/dev/null
}

main() {
  local latest_snapshot latest_id

  require_cmd restic

  if [[ -n "${HEALTHCHECK_URL_SUCCESS}" || -n "${HEALTHCHECK_URL_FAIL}" ]]; then
    require_cmd curl
  fi

  if [[ -z "${RESTIC_REPOSITORY}" || -z "${RESTIC_PASSWORD_FILE}" ]]; then
    echo "RESTIC_REPOSITORY e RESTIC_PASSWORD_FILE sao obrigatorios" >&2
    exit 1
  fi

  if [[ ! -f "${RESTIC_PASSWORD_FILE}" ]]; then
    echo "RESTIC_PASSWORD_FILE nao encontrado: ${RESTIC_PASSWORD_FILE}" >&2
    exit 1
  fi

  if [[ "${DRY_RUN}" == "true" ]]; then
    log "dry-run: restic check completo"
    notify_healthcheck "${HEALTHCHECK_URL_SUCCESS}" "✅ Restic check completo OK — snapshot dry-run"
    return 0
  fi

  require_cmd python3

  if restic_env check; then
    latest_snapshot="$(restic_env snapshots --latest 1 --json)"
    latest_id="$(python3 - "${latest_snapshot}" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
print(payload[0]["short_id"] if payload else "unknown")
PY
)"
    notify_healthcheck "${HEALTHCHECK_URL_SUCCESS}" "✅ Restic check completo OK — snapshot ${latest_id}"
    return 0
  fi

  latest_snapshot="$(restic_env snapshots --latest 1 --json || printf '[]')"
  latest_id="$(python3 - "${latest_snapshot}" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
print(payload[0]["short_id"] if payload else "unknown")
PY
)"
  notify_healthcheck \
    "${HEALTHCHECK_URL_FAIL}" \
    "⚠️ Restic check detectou corrupção — snapshot ${latest_id} — NÃO usar esse snapshot para restore"
  exit 1
}

main "$@"
