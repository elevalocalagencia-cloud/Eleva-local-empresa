# Eleva Local Infra

Documentacao operacional da infraestrutura da `Eleva Local`, separada do produto e orientada agora para uma fundacao multi-cliente.

Este repositorio existe para registrar o estado real da VPS, das stacks compartilhadas e do plano de evolucao para operar com seguranca uma base inicial de ate 10 clientes sem contaminacao cruzada entre:

- WhatsApps
- inboxes
- agentes humanos
- agentes de IA
- workflows
- credenciais
- backups e restores

## Escopo

Este diretorio nao pertence ao produto `AutoVenda Pro B2B`. Ele centraliza a operacao da infraestrutura da `Eleva Local`:

- VPS Hostinger
- Traefik / `coolify-proxy`
- `n8n`
- `Chatwoot`
- `Evolution API`
- bancos e Redis associados
- runbooks operacionais, backup e seguranca

## Objetivo principal

Evitar mistura entre:

- projeto de produto (`AutoVenda Pro`)
- infraestrutura operacional da `Eleva Local`
- dados e automacoes de clientes diferentes

O objetivo tecnico agora nao e apenas "manter os servicos no ar". O objetivo e criar base para operar 10 clientes com isolamento suficiente para evitar:

- envio de mensagem pelo WhatsApp errado
- inbox errada no `Chatwoot`
- workflow do cliente A executando no cliente B
- credencial ou token compartilhado entre clientes
- prompt, memoria ou configuracao de IA cruzando tenants
- restore parcial impactando mais de um cliente

## Leitura recomendada

- [ARCHITECTURE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/ARCHITECTURE.md): arquitetura atual e arquitetura-alvo para operacao multi-cliente
- [MULTITENANT-AUDIT.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/MULTITENANT-AUDIT.md): auditoria central de riscos cross-tenant, modelo recomendado de isolamento e plano por fases
- [LAUNCH-AUDIT.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-AUDIT.md): decisao executiva de `GO / NO-GO` para lancamento, bloqueios atuais e gates minimos de liberacao
- [LAUNCH-READINESS-LEDGER.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-READINESS-LEDGER.md): fonte canonica de status, prioridade e impacto de readiness para lancamento
- [LAUNCH-EXECUTION-BOARD.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/LAUNCH-EXECUTION-BOARD.md): painel unico para executar as frentes P0 do lancamento em ordem global
- [VPS-EXECUTION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/VPS-EXECUTION-CHECKLIST.md): checklist operacional para executar comandos na VPS com seguranca e evidencia
- [INVENTORY.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/INVENTORY.md): inventario da VPS, servicos, dominios e volumes
- [N8N-STATUS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/N8N-STATUS.md): estado atual do `n8n`, incidente de auth e restricao atual de Redis 7
- [N8N-MIGRATION.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/N8N-MIGRATION.md): runbook para migracao definitiva do `n8n`
- [CHATWOOT-STATUS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/CHATWOOT-STATUS.md): estado atual do `Chatwoot`
- [EVOLUTION-STATUS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/EVOLUTION-STATUS.md): estado atual da `Evolution API`
- [OPERATIONS.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/OPERATIONS.md): rotina segura de operacao
- [tenants/README.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/README.md): contrato operacional por tenant, templates e fluxo de scaffolding
- [BACKUP-RESTORE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/BACKUP-RESTORE.md): backup, restore e restore drill
- [OFFSITE-VALIDATION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/OFFSITE-VALIDATION-CHECKLIST.md): checklist operacional para validar a primeira copia offsite completa
- [SECRET-ROTATION-CHECKLIST.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/SECRET-ROTATION-CHECKLIST.md): checklist de rotacao de credenciais antes do lancamento
- [CHATWOOT-VERSION-FREEZE.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/CHATWOOT-VERSION-FREEZE.md): roteiro para retirar `latest` do `Chatwoot` e congelar versao
- [FIRST-EXTERNAL-PROVISIONING.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/FIRST-EXTERNAL-PROVISIONING.md): checklist ponta a ponta para o primeiro provisionamento real de cliente externo
- [SECURITY-HARDENING.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/SECURITY-HARDENING.md): endurecimento minimo da VPS e reducao de superficie publica

## Estado atual resumido

- `n8n` operacional em `https://n8m.elevalocal.shop`
- `Chatwoot` operacional em `chat.elevalocal.shop`
- `Evolution API` operacional em `api.elevalocal.shop`
- `Coolify` e `coolify-realtime` retirados da internet publica como mitigacao de emergencia
- backups recorrentes instalados
- restore drill local validado para `n8n`, `Chatwoot` e `Evolution`

## Veredito atual

A operacao saiu do estado de incidente e ja e utilizavel em modo controlado. Isso
nao significa readiness comercial.

O ponto que ainda impede chamar a stack de "pronta para vender em escala" nao e
disponibilidade basica; e readiness de lancamento e isolamento entre clientes.

Hoje o principal risco de negocio e cross-tenant:

- workflow errado
- numero errado
- credencial errada
- restore errado
- agente de IA errado

Bloqueios atuais de launch:

- offsite backup nao validado
- rotacao de segredos pendente
- `Chatwoot` ainda sem freeze explicito de versao
- primeiro provisionamento externo real ainda nao provado ponta a ponta

## Proxima fronteira

A proxima fase deste repositorio e a fundacao multi-cliente:

1. definir fronteiras por cliente
2. padronizar naming e inventario por tenant
3. separar credenciais, inboxes, agentes e automacoes
4. reduzir blast radius de incidentes
5. preparar operacao segura para 10 clientes

## Fluxo operacional por tenant

1. criar o tenant com `python ops/create-tenant.py ...`
2. revisar o manifest gerado em `tenants/manifests/`
3. validar com `python ops/validate-tenant-manifest.py ...`
4. registrar ownership, segredos e checklist antes de provisionar em producao

## Regra de ouro

Nao registrar segredos reais nesta documentacao.
