#!/usr/bin/env bash
set -euo pipefail

AUDIT_DIR="${AUDIT_DIR:-/root/eleva-audit}"
mkdir -p "${AUDIT_DIR}"

log() {
  printf '[%s] %s\n' "$(date +%F' '%T)" "$*"
}

env_value() {
  local container="$1"
  local key="$2"
  docker inspect "$container" --format '{{range .Config.Env}}{{println .}}{{end}}' | grep "^${key}=" | head -n1 | cut -d= -f2-
}

capture() {
  local name="$1"
  shift
  log "capturando ${name}"
  "$@" > "${AUDIT_DIR}/${name}" 2>&1 || true
}

capture_shell() {
  local name="$1"
  local command="$2"
  log "capturando ${name}"
  bash -lc "${command}" > "${AUDIT_DIR}/${name}" 2>&1 || true
}

log "iniciando auditoria da elevalocal em ${AUDIT_DIR}"

capture "docker-ps.txt" docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"
capture "docker-networks.txt" docker network ls
capture "docker-volumes.txt" docker volume ls
capture_shell "host-ports.txt" "ss -tulpn"
capture_shell "ufw-status.txt" "ufw status verbose"

capture_shell "n8n-env-current.txt" "docker inspect n8n-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}'"
capture_shell "n8n-compose-current.yml" "cat /data/coolify/services/mamtm8g3b2mdh7ko0hxdcyr3/docker-compose.yml"
export -f env_value
capture_shell "n8n-users.txt" "N8N_DB_USER=\"\$(env_value postgresql-mamtm8g3b2mdh7ko0hxdcyr3 POSTGRES_USER)\"; N8N_DB_NAME=\"\$(env_value postgresql-mamtm8g3b2mdh7ko0hxdcyr3 POSTGRES_DB)\"; N8N_DB_PASSWORD=\"\$(env_value postgresql-mamtm8g3b2mdh7ko0hxdcyr3 POSTGRES_PASSWORD)\"; docker exec -i -e PGPASSWORD=\"\${N8N_DB_PASSWORD}\" postgresql-mamtm8g3b2mdh7ko0hxdcyr3 psql -U \"\${N8N_DB_USER}\" -d \"\${N8N_DB_NAME}\" -c 'select email, \"firstName\", \"lastName\", disabled from \"user\";'"

capture_shell "chatwoot-app-env.txt" "docker inspect chatwoot-c8ecfzoz3ddr69y9c4bto96s --format '{{range .Config.Env}}{{println .}}{{end}}'"
capture_shell "chatwoot-labels.json" "docker inspect chatwoot-c8ecfzoz3ddr69y9c4bto96s --format '{{json .Config.Labels}}'"
capture_shell "chatwoot-app-logs.txt" "docker logs --tail 200 chatwoot-c8ecfzoz3ddr69y9c4bto96s"
capture_shell "chatwoot-sidekiq-logs.txt" "docker logs --tail 200 sidekiq-c8ecfzoz3ddr69y9c4bto96s"
capture_shell "chatwoot-postgres-env.txt" "docker inspect postgres-c8ecfzoz3ddr69y9c4bto96s --format '{{range .Config.Env}}{{println .}}{{end}}'"

capture_shell "evolution-api-env.txt" "docker inspect api-rh7m1i3wfmf9254fhcb4pn5p --format '{{range .Config.Env}}{{println .}}{{end}}'"
capture_shell "evolution-api-labels.json" "docker inspect api-rh7m1i3wfmf9254fhcb4pn5p --format '{{json .Config.Labels}}'"
capture_shell "evolution-api-logs.txt" "docker logs --tail 200 api-rh7m1i3wfmf9254fhcb4pn5p"
capture_shell "evolution-api-ports.json" "docker inspect api-rh7m1i3wfmf9254fhcb4pn5p --format '{{json .NetworkSettings.Ports}}'"
capture_shell "evolution-postgres-env.txt" "docker inspect postgres-rh7m1i3wfmf9254fhcb4pn5p --format '{{range .Config.Env}}{{println .}}{{end}}'"

capture_shell "evolution-api-curl.txt" "curl -vkI https://api.elevalocal.shop"
capture_shell "evolution-api-www-curl.txt" "curl -vkI https://www.api.elevalocal.shop"
capture_shell "n8n-curl.txt" "curl -vkI https://n8m.elevalocal.shop"

capture_shell "coolify-8000-local.txt" "curl -vkI http://127.0.0.1:8000"
capture_shell "coolify-8000-public.txt" "curl -vkI http://2.24.199.157:8000"
capture_shell "port-8080-local.txt" "curl -vkI http://127.0.0.1:8080"
capture_shell "port-6001-local.txt" "curl -vkI http://127.0.0.1:6001"
capture_shell "port-6002-local.txt" "curl -vkI http://127.0.0.1:6002"

cat > "${AUDIT_DIR}/README.txt" <<EOF
Arquivos principais para revisar:
- docker-ps.txt
- host-ports.txt
- n8n-env-current.txt
- n8n-compose-current.yml
- chatwoot-app-env.txt
- chatwoot-labels.json
- evolution-api-env.txt
- evolution-api-labels.json
EOF

log "auditoria concluida"
