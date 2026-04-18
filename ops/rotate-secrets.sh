#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VAULT_DIR="${REPO_ROOT}/tenants/secrets/.vault"
AGE_KEY_FILE="${VAULT_DIR}/age.key"

STACK=""

log() {
  printf '[%s] %s\n' "$(date +%F' '%T)" "$*"
}

die() {
  printf 'erro: %s\n' "$*" >&2
  exit 1
}

usage() {
  cat <<'EOF'
Uso:
  ops/rotate-secrets.sh --stack {n8n|chatwoot|evolution}

Rotacao guiada, interativa, uma stack por execucao.
EOF
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "comando obrigatorio ausente: $1"
}

confirm() {
  local prompt="$1"
  local answer=""

  read -r -p "${prompt} [y/N] " answer
  [[ "${answer}" == "y" || "${answer}" == "Y" ]]
}

env_value() {
  local container="$1"
  local key="$2"

  docker inspect "$container" --format '{{range .Config.Env}}{{println .}}{{end}}' | grep "^${key}=" | head -n1 | cut -d= -f2-
}

export -f env_value

escape_sql_literal() {
  printf '%s' "${1//\'/\'\'}"
}

stack_config() {
  case "$1" in
    n8n)
      POSTGRES_CONTAINER="postgresql-mamtm8g3b2mdh7ko0hxdcyr3"
      STACK_OWNER="eleva-local-ops"
      STACK_LABEL="n8n"
      DEFAULT_DB_NAME="n8n"
      ;;
    chatwoot)
      POSTGRES_CONTAINER="postgres-c8ecfzoz3ddr69y9c4bto96s"
      STACK_OWNER="eleva-local-ops"
      STACK_LABEL="chatwoot"
      DEFAULT_DB_NAME="chatwoot_production"
      ;;
    evolution)
      POSTGRES_CONTAINER="postgres-rh7m1i3wfmf9254fhcb4pn5p"
      STACK_OWNER="eleva-local-ops"
      STACK_LABEL="evolution"
      DEFAULT_DB_NAME="evolution"
      ;;
    *)
      die "stack invalida: $1"
      ;;
  esac

  DB_USER="$(env_value "${POSTGRES_CONTAINER}" POSTGRES_USER || true)"
  DB_NAME="$(env_value "${POSTGRES_CONTAINER}" POSTGRES_DB || true)"
  DB_PASSWORD="$(env_value "${POSTGRES_CONTAINER}" POSTGRES_PASSWORD || true)"

  DB_NAME="${DB_NAME:-${DEFAULT_DB_NAME}}"

  [[ -n "${DB_USER}" ]] || die "POSTGRES_USER nao encontrado em ${POSTGRES_CONTAINER}"
  [[ -n "${DB_PASSWORD}" ]] || die "POSTGRES_PASSWORD nao encontrado em ${POSTGRES_CONTAINER}"
}

ensure_vault_key() {
  mkdir -p "${VAULT_DIR}"

  if [[ ! -f "${AGE_KEY_FILE}" ]]; then
    log "gerando chave age local em ${AGE_KEY_FILE}"
    age-keygen -o "${AGE_KEY_FILE}" >/dev/null
    chmod 600 "${AGE_KEY_FILE}"
  fi
}

record_vault_entry() {
  require_cmd sops
  require_cmd age-keygen
  require_cmd mktemp

  ensure_vault_key

  local recipient
  local plaintext_file
  local encrypted_dir
  local encrypted_file

  recipient="$(age-keygen -y "${AGE_KEY_FILE}")"
  plaintext_file="$(mktemp)"
  encrypted_dir="${VAULT_DIR}/rotations/${STACK}"
  encrypted_file="${encrypted_dir}/$(date +%F-%H%M%S).yaml.enc"

  mkdir -p "${encrypted_dir}"

  cat > "${plaintext_file}" <<EOF
stack: ${STACK}
owner: ${STACK_OWNER}
rotated_at: $(date -Iseconds)
postgres:
  container: ${POSTGRES_CONTAINER}
  database: ${DB_NAME}
  user: ${DB_USER}
validation:
  pg_isready: success
notes:
  - rotation guided manually by operator
  - app-side secret updates must be synced separately
EOF

  sops --encrypt --age "${recipient}" "${plaintext_file}" > "${encrypted_file}"
  rm -f "${plaintext_file}"
  chmod 600 "${encrypted_file}"

  log "entrada cifrada registrada em ${encrypted_file}"
}

rotate_postgres_password() {
  local new_password="$1"
  local escaped_password

  escaped_password="$(escape_sql_literal "${new_password}")"

  log "aplicando nova senha no Postgres de ${STACK_LABEL}"
  (
    export PGPASSWORD="${DB_PASSWORD}"
    docker exec -i -e PGPASSWORD "${POSTGRES_CONTAINER}" \
      psql -U "${DB_USER}" -d "${DB_NAME}" -v ON_ERROR_STOP=1 <<SQL
ALTER USER "${DB_USER}" WITH PASSWORD '${escaped_password}';
SQL
  )

  log "validando nova senha com pg_isready"
  (
    export PGPASSWORD="${new_password}"
    docker exec -i -e PGPASSWORD "${POSTGRES_CONTAINER}" \
      pg_isready -h 127.0.0.1 -p 5432 -U "${DB_USER}" -d "${DB_NAME}"
  )
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --stack)
        STACK="${2:-}"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        die "argumento desconhecido: $1"
        ;;
    esac
  done

  [[ -n "${STACK}" ]] || die "informe --stack"
}

main() {
  parse_args "$@"

  require_cmd docker
  require_cmd age-keygen
  require_cmd sops

  stack_config "${STACK}"

  log "rotacao guiada iniciada para ${STACK}"
  log "container postgres: ${POSTGRES_CONTAINER}"
  log "usuario postgres: ${DB_USER}"
  log "banco postgres: ${DB_NAME}"
  log "owner operacional: ${STACK_OWNER}"

  if ! confirm "Confirmar que a mudanca sera feita apenas para a stack ${STACK}?"; then
    die "operacao cancelada pelo operador"
  fi

  local new_password=""
  local confirmation=""
  read -r -s -p "Digite a nova senha para ${STACK}: " new_password
  printf '\n'
  read -r -s -p "Confirme a nova senha para ${STACK}: " confirmation
  printf '\n'

  [[ -n "${new_password}" ]] || die "nova senha vazia"
  [[ "${new_password}" == "${confirmation}" ]] || die "confirmacao nao confere"

  if ! confirm "Confirmar que os secrets do app e do painel foram preparados para receber a nova senha?"; then
    die "rotacao interrompida antes da aplicacao"
  fi

  rotate_postgres_password "${new_password}"

  if confirm "Registrar evidencia cifrada em tenants/secrets/.vault/?"; then
    record_vault_entry
  else
    log "registro cifrado ignorado a pedido do operador"
  fi

  log "rotacao guiada concluida para ${STACK}"
  log "lembrete: atualizar qualquer referencia externa ao secret rotacionado fora do banco, se existir"
}

main "$@"
