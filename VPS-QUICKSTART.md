# VPS Quickstart

## Objetivo

Rodar uma auditoria unica na VPS e me devolver os artefatos minimos para eu fechar o diagnostico.

## Passos

### 1. Subir o script para a VPS

Use o conteudo de:

- [ops/vps-audit-elevalocal.sh](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/vps-audit-elevalocal.sh)

### 2. Na VPS, salvar e executar

```bash
mkdir -p /root/eleva-audit
chmod +x /root/vps-audit-elevalocal.sh
/root/vps-audit-elevalocal.sh
```

### 3. Me trazer estes arquivos

- `/root/eleva-audit/docker-ps.txt`
- `/root/eleva-audit/host-ports.txt`
- `/root/eleva-audit/n8n-env-current.txt`
- `/root/eleva-audit/n8n-compose-current.yml`
- `/root/eleva-audit/chatwoot-app-env.txt`
- `/root/eleva-audit/chatwoot-labels.json`
- `/root/eleva-audit/evolution-api-env.txt`
- `/root/eleva-audit/evolution-api-labels.json`

## Se quiser ir mais rapido

Pode me mandar tambem:

- `/root/eleva-audit/chatwoot-app-logs.txt`
- `/root/eleva-audit/chatwoot-sidekiq-logs.txt`
- `/root/eleva-audit/evolution-api-logs.txt`
- `/root/eleva-audit/evolution-api-curl.txt`
- `/root/eleva-audit/coolify-8000-public.txt`

## O que eu vou responder com isso

1. causa do problema de acesso da `Evolution API`
2. risco real de persistencia do `Chatwoot`
3. correcoes permanentes do `n8n`
4. quais portas fechar primeiro
