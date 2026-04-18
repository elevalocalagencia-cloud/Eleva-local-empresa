# HANDOFF

## Escopo

Infraestrutura da `elevalocal` na VPS Hostinger. Nao confundir com o repo/produto `AutoVenda Pro`.

## Estado atual

- `n8n` abre corretamente em `https://n8m.elevalocal.shop`
- owner do `n8n` foi recuperado com sucesso
- stack atual do `n8n` foi estabilizado com `redis:7-alpine`
- a tentativa de migrar o `n8n` para compose proprio falhou e foi revertida
- `Chatwoot` foi migrado de `sslip.io` para `chat.elevalocal.shop`
- `Evolution` continua funcional, mas a configuracao de Chatwoot pela API interna da versao `2.3.7` se mostrou instavel
- `api.elevalocal.shop` responde em HTTPS com certificado valido
- `8000`, `6001` e `6002` deixaram de responder externamente apos mitigacao de emergencia
- `ufw` foi habilitado
- backup recorrente foi instalado via `cron`
- restore drill foi validado para `n8n`, `Chatwoot` e `Evolution`
- fundacao multi-cliente foi iniciada no repositorio
- `ops/create-tenant.py` agora cria manifest, registry, inventario de segredos e checklists por tenant
- `ops/validate-tenant-manifest.py` valida o schema canonico aninhado do tenant manifest
- existe um tenant piloto interno validado em `tenants/manifests/cli-eleva-pilot.yaml`

## Causa do incidente

- perda de owner por estado quebrado de auth no `n8n`
- drift de configuracao por compose/template do Coolify
- falha de rollback do `n8n` causada por incompatibilidade `Redis 6` tentando ler dados gerados por `Redis 7`

## O que ja foi provado

- volumes do `n8n` existem
- Postgres do `n8n` existe
- o problema nao era falta de persistencia
- o bug real do Coolify/template foi identificado
- `Chatwoot` responde corretamente em app e API
- `Evolution` conecta no WhatsApp
- o token novo do `Chatwoot` foi validado manualmente
- `api.elevalocal.shop` e `chat.elevalocal.shop` respondem em dominios proprios
- backup deixou de ser hipotese e passou a ter restore testado nos tres stacks

## Proximo passo concreto

Implementar a matriz de provisionamento por tenant para `Evolution`, `Chatwoot` e `n8n`, definindo o que permanece `shared-foundation` e o que precisa ser `dedicated` antes de onboarding externo.

Artefatos locais ja preparados:

- [N8N-MIGRATION.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/N8N-MIGRATION.md)
- [CHATWOOT-STATUS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/CHATWOOT-STATUS.md)
- [EVOLUTION-STATUS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/EVOLUTION-STATUS.md)
- [SECURITY-HARDENING.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/SECURITY-HARDENING.md)
- [BACKUP-RESTORE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/BACKUP-RESTORE.md)
- [n8n-compose/docker-compose.yml](C:/Users/PEDROSO/Downloads/elevalocal-infra/n8n-compose/docker-compose.yml)
- [n8n-compose/.env.example](C:/Users/PEDROSO/Downloads/elevalocal-infra/n8n-compose/.env.example)
- [ops/backup-elevalocal.sh](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/backup-elevalocal.sh)
- [ops/backup-elevalocal.env.example](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/backup-elevalocal.env.example)
- [MULTITENANT-AUDIT.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/MULTITENANT-AUDIT.md)
- [tenants/README.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/README.md)
- [tenants/registry.yaml](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/registry.yaml)
- [tenants/manifests/cli-eleva-pilot.yaml](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/manifests/cli-eleva-pilot.yaml)
- [ops/create-tenant.py](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/create-tenant.py)
- [ops/validate-tenant-manifest.py](C:/Users/PEDROSO/Downloads/elevalocal-infra/ops/validate-tenant-manifest.py)

## Depois disso

1. definir matriz de provisionamento por stack/tenant
2. decidir fronteiras `shared-foundation` vs `dedicated`
3. so depois preparar onboarding do primeiro cliente externo
4. offsite backup agora deve ser tratado como bloqueio de launch para `GO CONTROLADO`
5. rotacao de segredos continua pendente
