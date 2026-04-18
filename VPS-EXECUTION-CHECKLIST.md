# VPS Execution Checklist

## Objetivo

Executar diagnostico e estabilizacao da infra `elevalocal` na VPS sem perder dados.

## Ordem obrigatoria

1. capturar evidencia do estado atual
2. gerar backup novo
3. validar `Evolution API`
4. validar `Chatwoot`
5. estabilizar `n8n`
6. reduzir superficie publica

## Regras

- executar um comando por vez
- salvar saidas relevantes em `/root/eleva-audit`
- nao usar `reset` de usuario no `n8n` sem emergencia real
- nao alterar compose nem UI do Coolify antes do backup novo

## Fase 1 - Evidencia atual

### 1.1 Criar pasta de auditoria

```bash
mkdir -p /root/eleva-audit
```

### 1.2 Registrar containers e portas

```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}" | tee /root/eleva-audit/docker-ps.txt
```

### 1.3 Registrar redes Docker

```bash
docker network ls | tee /root/eleva-audit/docker-networks.txt
```

### 1.4 Registrar volumes Docker

```bash
docker volume ls | tee /root/eleva-audit/docker-volumes.txt
```

### 1.5 Registrar portas do host

```bash
ss -tulpn | tee /root/eleva-audit/host-ports.txt
```

### 1.6 Registrar firewall

```bash
ufw status verbose | tee /root/eleva-audit/ufw-status.txt
```

## Fase 2 - Backup novo antes de qualquer mudanca

### 2.1 Criar pasta de backup

```bash
mkdir -p /root/eleva-backups
```

### 2.2 Backup do Postgres do n8n

```bash
N8N_DB_USER="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | awk -F= '/^POSTGRES_USER=/{print $2}')"
N8N_DB_NAME="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | awk -F= '/^POSTGRES_DB=/{print $2}')"
docker exec -t postgresql-mamtm8g3b2mdh7ko0hxdcyr3 pg_dump -U "${N8N_DB_USER}" -d "${N8N_DB_NAME}" > /root/eleva-backups/n8n-$(date +%F-%H%M).sql
```

### 2.3 Descobrir envs reais do Postgres do Chatwoot

```bash
docker inspect postgres-c8ecfzoz3ddr69y9c4bto96s --format '{{range .Config.Env}}{{println .}}{{end}}' | tee /root/eleva-audit/chatwoot-postgres-env.txt
```

### 2.4 Descobrir envs reais do Postgres da Evolution

```bash
docker inspect postgres-rh7m1i3wfmf9254fhcb4pn5p --format '{{range .Config.Env}}{{println .}}{{end}}' | tee /root/eleva-audit/evolution-postgres-env.txt
```

### 2.5 Backup do banco do Chatwoot

Substituir `USUARIO`, `DATABASE` e `SENHA` pelos valores encontrados no passo 2.3.

```bash
docker exec -e PGPASSWORD='SENHA' -t postgres-c8ecfzoz3ddr69y9c4bto96s pg_dump -U USUARIO -d DATABASE > /root/eleva-backups/chatwoot-$(date +%F-%H%M).sql
```

### 2.6 Backup do banco da Evolution

Substituir `USUARIO`, `DATABASE` e `SENHA` pelos valores encontrados no passo 2.4.

```bash
docker exec -e PGPASSWORD='SENHA' -t postgres-rh7m1i3wfmf9254fhcb4pn5p pg_dump -U USUARIO -d DATABASE > /root/eleva-backups/evolution-$(date +%F-%H%M).sql
```

### 2.7 Backup dos volumes do Chatwoot

```bash
docker run --rm -v c8ecfzoz3ddr69y9c4bto96s_rails-data:/source:ro -v /root/eleva-backups:/backup alpine sh -lc "cd /source && tar czf /backup/chatwoot-rails-data-$(date +%F-%H%M).tar.gz ."
```

### 2.8 Backup dos volumes da Evolution

```bash
docker run --rm -v rh7m1i3wfmf9254fhcb4pn5p_evolution-instances:/source:ro -v /root/eleva-backups:/backup alpine sh -lc "cd /source && tar czf /backup/evolution-instances-$(date +%F-%H%M).tar.gz ."
```

## Fase 3 - Diagnostico da Evolution API

### 3.1 Estado do stack

```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | grep rh7m1i3wfmf9254fhcb4pn5p
```

### 3.2 Env da API

```bash
docker inspect api-rh7m1i3wfmf9254fhcb4pn5p --format '{{range .Config.Env}}{{println .}}{{end}}' | tee /root/eleva-audit/evolution-api-env.txt
```

### 3.3 Labels do proxy

```bash
docker inspect api-rh7m1i3wfmf9254fhcb4pn5p --format '{{json .Config.Labels}}' | tee /root/eleva-audit/evolution-api-labels.json
```

### 3.4 Logs da API

```bash
docker logs --tail 200 api-rh7m1i3wfmf9254fhcb4pn5p | tee /root/eleva-audit/evolution-api-logs.txt
```

### 3.5 Testar candidatos de dominio

```bash
curl -vkI https://api.elevalocal.shop | tee /root/eleva-audit/evolution-api-curl.txt
```

```bash
curl -vkI https://www.api.elevalocal.shop | tee /root/eleva-audit/evolution-api-www-curl.txt
```

### 3.6 Validar o endpoint interno

Descobrir a porta exposta pelo container e testar a partir da VPS, se necessario:

```bash
docker inspect api-rh7m1i3wfmf9254fhcb4pn5p --format '{{json .NetworkSettings.Ports}}' | tee /root/eleva-audit/evolution-api-ports.json
```

## Fase 4 - Diagnostico do Chatwoot

### 4.1 Estado do stack

```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | grep c8ecfzoz3ddr69y9c4bto96s
```

### 4.2 Env do app

```bash
docker inspect chatwoot-c8ecfzoz3ddr69y9c4bto96s --format '{{range .Config.Env}}{{println .}}{{end}}' | tee /root/eleva-audit/chatwoot-app-env.txt
```

### 4.3 Labels do proxy

```bash
docker inspect chatwoot-c8ecfzoz3ddr69y9c4bto96s --format '{{json .Config.Labels}}' | tee /root/eleva-audit/chatwoot-labels.json
```

### 4.4 Logs do app

```bash
docker logs --tail 200 chatwoot-c8ecfzoz3ddr69y9c4bto96s | tee /root/eleva-audit/chatwoot-app-logs.txt
```

### 4.5 Logs do worker

```bash
docker logs --tail 200 sidekiq-c8ecfzoz3ddr69y9c4bto96s | tee /root/eleva-audit/chatwoot-sidekiq-logs.txt
```

## Fase 5 - Estabilizacao do n8n

### 5.1 Confirmar env efetiva atual

```bash
docker inspect n8n-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | tee /root/eleva-audit/n8n-env-current.txt
```

### 5.2 Confirmar host correto

```bash
docker inspect n8n-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | grep '^N8N_HOST='
```

### 5.3 Confirmar owner atual

```bash
N8N_DB_USER="$(docker inspect postgresql-mamtm8g3b2mdh7ko0hxdcyr3 --format '{{range .Config.Env}}{{println .}}{{end}}' | awk -F= '/^POSTGRES_USER=/{print $2}')"
docker exec -it postgresql-mamtm8g3b2mdh7ko0hxdcyr3 psql -U "${N8N_DB_USER}" -d n8n -c 'select email, "firstName", "lastName", disabled from "user";'
```

### 5.4 Confirmar compose atual

```bash
cat /data/coolify/services/mamtm8g3b2mdh7ko0hxdcyr3/docker-compose.yml | tee /root/eleva-audit/n8n-compose-current.yml
```

### 5.5 Confirmar rede externa do Traefik

```bash
docker network ls | grep -i coolify
```

### 5.6 So depois disso: preparar migracao

Usar como base:

- [N8N-MIGRATION.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/N8N-MIGRATION.md)
- [n8n-compose/docker-compose.yml](C:/Users/PEDROSO/Downloads/elevalocal-infra/n8n-compose/docker-compose.yml)

## Fase 6 - Hardening inicial

### 6.1 Revisar se Coolify esta publico

```bash
curl -vkI http://127.0.0.1:8000
```

```bash
curl -vkI http://2.24.199.157:8000
```

### 6.2 Revisar exposicao das outras portas

```bash
curl -vkI http://127.0.0.1:8080
```

```bash
curl -vkI http://127.0.0.1:6001
```

```bash
curl -vkI http://127.0.0.1:6002
```

## O que me enviar depois

Depois de executar, me traga o essencial destes arquivos:

- `/root/eleva-audit/docker-ps.txt`
- `/root/eleva-audit/host-ports.txt`
- `/root/eleva-audit/chatwoot-app-env.txt`
- `/root/eleva-audit/chatwoot-labels.json`
- `/root/eleva-audit/evolution-api-env.txt`
- `/root/eleva-audit/evolution-api-labels.json`
- `/root/eleva-audit/n8n-env-current.txt`
- `/root/eleva-audit/n8n-compose-current.yml`

Com isso eu consigo te dizer exatamente:

1. por que a `Evolution API` nao entra
2. se o `Chatwoot` esta realmente persistente
3. qual o ajuste certo para travar o `n8n`
4. quais portas podem ser fechadas sem quebrar a operacao
