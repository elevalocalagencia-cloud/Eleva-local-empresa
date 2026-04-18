#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/backup-elevalocal.env"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

BACKUP_ROOT="${BACKUP_ROOT:-/root/eleva-backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
OFFSITE_ENABLED="${OFFSITE_ENABLED:-false}"
OFFSITE_TARGET="${OFFSITE_TARGET:-}"
BACKUP_MODE="${BACKUP_MODE:-}"
RESTIC_REPOSITORY="${RESTIC_REPOSITORY:-}"
RESTIC_PASSWORD_FILE="${RESTIC_PASSWORD_FILE:-}"
HEALTHCHECK_PING_URL="${HEALTHCHECK_PING_URL:-}"
HEALTHCHECK_URL_START="${HEALTHCHECK_URL_START:-}"
HEALTHCHECK_URL_SUCCESS="${HEALTHCHECK_URL_SUCCESS:-}"
HEALTHCHECK_URL_FAIL="${HEALTHCHECK_URL_FAIL:-}"
B2_ACCOUNT_ID="${B2_ACCOUNT_ID:-}"
B2_ACCOUNT_KEY="${B2_ACCOUNT_KEY:-}"
AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-}"
AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-auto}"
OFFSITE_BUCKET_QUOTA_GB="${OFFSITE_BUCKET_QUOTA_GB:-}"
BACKUP_LOG_FILE="${BACKUP_LOG_FILE:-/var/log/elevalocal-backup.log}"
DRY_RUN="${DRY_RUN:-false}"
TIMESTAMP="${BACKUP_TIMESTAMP:-$(date +%F-%H%M%S)}"

if [[ -n "${HEALTHCHECK_PING_URL}" ]]; then
  HEALTHCHECK_PING_URL="${HEALTHCHECK_PING_URL%/}"
  HEALTHCHECK_URL_START="${HEALTHCHECK_URL_START:-${HEALTHCHECK_PING_URL}/start}"
  HEALTHCHECK_URL_SUCCESS="${HEALTHCHECK_URL_SUCCESS:-${HEALTHCHECK_PING_URL}}"
  HEALTHCHECK_URL_FAIL="${HEALTHCHECK_URL_FAIL:-${HEALTHCHECK_PING_URL}/fail}"
fi

if [[ -z "${BACKUP_MODE}" ]]; then
  if [[ "${OFFSITE_ENABLED}" == "true" ]]; then
    BACKUP_MODE="rsync"
  else
    BACKUP_MODE="local_only"
  fi
fi

DEST_DIR="${BACKUP_ROOT}/${TIMESTAMP}"

log() {
  local line
  line="[$(date +%F' '%T)] $*"
  printf '%s\n' "${line}"
  if [[ -n "${BACKUP_LOG_FILE}" ]]; then
    mkdir -p "$(dirname "${BACKUP_LOG_FILE}")"
    printf '%s\n' "${line}" >> "${BACKUP_LOG_FILE}"
  fi
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "comando obrigatorio ausente: $1" >&2
    exit 1
  }
}

env_value() {
  local container="$1"
  local key="$2"
  docker inspect "$container" --format '{{range .Config.Env}}{{println .}}{{end}}' | grep "^${key}=" | head -n1 | cut -d= -f2-
}

format_duration() {
  local total_seconds="$1"
  printf '%02dm%02ds' "$((total_seconds / 60))" "$((total_seconds % 60))"
}

dir_size_gb() {
  local path="$1"
  if [[ ! -d "${path}" ]]; then
    printf '0.00'
    return 0
  fi

  python3 - "$path" <<'PY'
import os
import sys

root = sys.argv[1]
total = 0
for current_root, _, files in os.walk(root):
    for name in files:
        total += os.path.getsize(os.path.join(current_root, name))
print(f"{total / (1024 ** 3):.2f}")
PY
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

notify_failure() {
  local stack="$1"
  local error_summary="$2"
  local icon_fail

  icon_fail=$'\U0001F6A8'

  notify_healthcheck \
    "${HEALTHCHECK_URL_FAIL}" \
    "${icon_fail} Backup Eleva Local FALHOU - stack: ${stack} - erro: ${error_summary} - verifique ${BACKUP_LOG_FILE}"
}

notify_start() {
  notify_healthcheck "${HEALTHCHECK_URL_START}" "backup-start"
}

write_placeholder_file() {
  local path="$1"
  local content="$2"
  printf '%s\n' "${content}" > "${path}"
}

backup_postgres() {
  local name="$1"
  local container="$2"
  local user password database

  if [[ "${DRY_RUN}" == "true" ]]; then
    log "dry-run: gerando dump placeholder de ${name}"
    write_placeholder_file "${DEST_DIR}/${name}.sql" "-- dry-run backup for ${name}"
    return 0
  fi

  user="$(env_value "${container}" POSTGRES_USER || true)"
  password="$(env_value "${container}" POSTGRES_PASSWORD || true)"
  database="$(env_value "${container}" POSTGRES_DB || true)"

  if [[ -z "${user}" || -z "${password}" || -z "${database}" ]]; then
    log "pulando dump de ${name}: envs POSTGRES_* nao encontradas em ${container}"
    return 0
  fi

  log "gerando dump SQL de ${name}"
  docker exec -e PGPASSWORD="${password}" -t "${container}" \
    pg_dump -U "${user}" -d "${database}" > "${DEST_DIR}/${name}.sql"
}

backup_volume() {
  local name="$1"
  local volume="$2"

  if [[ "${DRY_RUN}" == "true" ]]; then
    log "dry-run: empacotando volume placeholder ${volume}"
    write_placeholder_file "${DEST_DIR}/${name}.tar.gz" "dry-run archive for ${volume}"
    return 0
  fi

  log "empacotando volume ${volume}"
  docker run --rm \
    -v "${volume}:/source:ro" \
    -v "${DEST_DIR}:/backup" \
    alpine sh -lc "cd /source && tar czf /backup/${name}.tar.gz ."
}

cleanup_old_backups() {
  log "removendo backups com mais de ${RETENTION_DAYS} dias em ${BACKUP_ROOT}"
  if [[ "${DRY_RUN}" == "true" ]]; then
    log "dry-run: cleanup local nao executado"
    return 0
  fi
  find "${BACKUP_ROOT}" -mindepth 1 -maxdepth 1 -type d -mtime +"${RETENTION_DAYS}" -exec rm -rf {} +
}

ensure_restic_config() {
  if [[ -z "${RESTIC_REPOSITORY}" ]]; then
    echo "BACKUP_MODE=restic exige RESTIC_REPOSITORY" >&2
    exit 1
  fi

  if [[ -z "${RESTIC_PASSWORD_FILE}" ]]; then
    echo "BACKUP_MODE=restic exige RESTIC_PASSWORD_FILE" >&2
    exit 1
  fi

  if [[ ! -f "${RESTIC_PASSWORD_FILE}" ]]; then
    echo "RESTIC_PASSWORD_FILE nao encontrado: ${RESTIC_PASSWORD_FILE}" >&2
    exit 1
  fi
}

ensure_restic_repository() {
  if [[ "${DRY_RUN}" == "true" ]]; then
    log "dry-run: validacao/init do repositorio restic ignorados"
    return 0
  fi

  if ! restic_env snapshots >/dev/null 2>&1; then
    log "repositorio restic ainda nao inicializado; executando init"
    restic_env init
  fi
}

offsite_sync() {
  if [[ "${BACKUP_MODE}" != "rsync" ]]; then
    return 0
  fi

  if [[ -z "${OFFSITE_TARGET}" ]]; then
    echo "BACKUP_MODE=rsync exige OFFSITE_TARGET" >&2
    exit 1
  fi

  log "sincronizando backup para destino externo via rsync"
  if [[ "${DRY_RUN}" == "true" ]]; then
    log "dry-run: rsync ${DEST_DIR}/ -> ${OFFSITE_TARGET}/${TIMESTAMP}/"
    return 0
  fi
  rsync -av "${DEST_DIR}/" "${OFFSITE_TARGET}/${TIMESTAMP}/"
}

monitor_bucket_usage() {
  if [[ "${BACKUP_MODE}" != "restic" || -z "${OFFSITE_BUCKET_QUOTA_GB}" ]]; then
    return 0
  fi

  if [[ "${DRY_RUN}" == "true" ]]; then
    log "dry-run: monitor de espaco do bucket ignorado"
    return 0
  fi

  local stats_json total_bytes usage_pct
  stats_json="$(restic_env stats latest --mode raw-data --json)"
  total_bytes="$(python3 - "${stats_json}" <<'PY'
import json
import sys

payload = json.loads(sys.argv[1])
print(payload.get("total_size", 0))
PY
)"
  usage_pct="$(python3 - "${total_bytes}" "${OFFSITE_BUCKET_QUOTA_GB}" <<'PY'
import sys

total_bytes = float(sys.argv[1])
quota_gb = float(sys.argv[2])
quota_bytes = quota_gb * (1024 ** 3)
if quota_bytes <= 0:
    print("0.0")
else:
    print(f"{(total_bytes / quota_bytes) * 100:.1f}")
PY
)"

  log "uso estimado do bucket: ${usage_pct}% da cota configurada"
  if ! python3 - "${usage_pct}" <<'PY'
import sys
raise SystemExit(0 if float(sys.argv[1]) < 80 else 1)
PY
  then
    local icon_warn
    icon_warn=$'\u26A0\uFE0F'
    notify_healthcheck \
      "${HEALTHCHECK_URL_FAIL}" \
      "${icon_warn} Backup Eleva Local acima de 80% da cota offsite - uso: ${usage_pct}% - revisar bucket"
  fi
}

restic_backup() {
  local started_at ended_at duration output snapshot_id size_gb
  local icon_success

  ensure_restic_config
  ensure_restic_repository

  started_at="$(date +%s)"
  size_gb="$(dir_size_gb "${DEST_DIR}")"

  log "enviando backup local para repositorio restic"
  if [[ "${DRY_RUN}" == "true" ]]; then
    snapshot_id="dry-run"
    log "dry-run: restic backup ${DEST_DIR}"
  else
    output="$(
      restic_env backup "${DEST_DIR}" \
        --host "$(hostname)" \
        --tag "elevalocal" \
        --tag "timestamp=${TIMESTAMP}" \
        --tag "mode=${BACKUP_MODE}" 2>&1
    )"
    printf '%s\n' "${output}" >> "${BACKUP_LOG_FILE}"
    snapshot_id="$(printf '%s\n' "${output}" | awk '/^snapshot [0-9a-f]+ saved$/ {print $2}' | tail -n1)"
    if [[ -z "${snapshot_id}" ]]; then
      snapshot_id="unknown"
    fi
  fi

  ended_at="$(date +%s)"
  duration="$(format_duration "$((ended_at - started_at))")"
  icon_success=$'\u2705'

  if [[ "${DRY_RUN}" == "true" ]]; then
    log "dry-run: restic check --read-data-subset=5%"
    log "dry-run: restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12"
  else
    restic_env check --read-data-subset=5%
    restic_env forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12
  fi

  monitor_bucket_usage
  notify_healthcheck \
    "${HEALTHCHECK_URL_SUCCESS}" \
    "${icon_success} Backup Eleva Local OK - snapshot ${snapshot_id} - ${size_gb}GB - ${duration}"
}

write_manifest() {
  cat > "${DEST_DIR}/manifest.txt" <<EOF
timestamp=${TIMESTAMP}
host=$(hostname)
backup_root=${BACKUP_ROOT}
backup_mode=${BACKUP_MODE}
dry_run=${DRY_RUN}
EOF
}

validate_mode() {
  case "${BACKUP_MODE}" in
    local_only|rsync|restic) ;;
    *)
      echo "BACKUP_MODE invalido: ${BACKUP_MODE}" >&2
      exit 1
      ;;
  esac
}

prepare_environment() {
  mkdir -p "${DEST_DIR}"

  require_cmd find
  require_cmd tar

  if [[ "${DRY_RUN}" != "true" ]]; then
    require_cmd docker
  fi

  if [[ -n "${HEALTHCHECK_URL_SUCCESS}" || -n "${HEALTHCHECK_URL_FAIL}" ]]; then
    require_cmd curl
  fi

  case "${BACKUP_MODE}" in
    rsync)
      require_cmd rsync
      ;;
    restic)
      require_cmd restic
      require_cmd python3
      ;;
  esac
}

main() {
  validate_mode
  prepare_environment

  trap 'notify_failure "${BACKUP_MODE}" "erro inesperado na execucao do backup"' ERR
  notify_start

  log "iniciando backup completo da elevalocal em ${DEST_DIR} (modo=${BACKUP_MODE})"
  write_manifest

  backup_postgres "n8n-postgres" "postgresql-mamtm8g3b2mdh7ko0hxdcyr3"
  backup_postgres "chatwoot-postgres" "postgres-c8ecfzoz3ddr69y9c4bto96s"
  backup_postgres "evolution-postgres" "postgres-rh7m1i3wfmf9254fhcb4pn5p"

  backup_volume "n8n-data" "mamtm8g3b2mdh7ko0hxdcyr3_n8n-data"
  backup_volume "n8n-postgresql-data" "mamtm8g3b2mdh7ko0hxdcyr3_postgresql-data"
  backup_volume "n8n-redis-data" "mamtm8g3b2mdh7ko0hxdcyr3_redis-data"
  backup_volume "chatwoot-postgres-data" "c8ecfzoz3ddr69y9c4bto96s_postgres-data"
  backup_volume "chatwoot-rails-data" "c8ecfzoz3ddr69y9c4bto96s_rails-data"
  backup_volume "chatwoot-redis-data" "c8ecfzoz3ddr69y9c4bto96s_redis-data"
  backup_volume "evolution-postgres-data" "rh7m1i3wfmf9254fhcb4pn5p_postgres-data"
  backup_volume "evolution-instances" "rh7m1i3wfmf9254fhcb4pn5p_evolution-instances"
  backup_volume "evolution-redis" "rh7m1i3wfmf9254fhcb4pn5p_evolution-redis"

  case "${BACKUP_MODE}" in
    local_only)
      ;;
    rsync)
      offsite_sync
      ;;
    restic)
      restic_backup
      ;;
  esac

  cleanup_old_backups
  log "backup concluido"
}

main "$@"
