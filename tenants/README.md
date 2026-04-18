# Tenants

Base operacional para onboarding, inventario e segregacao por cliente da `Eleva Local`.

O objetivo desta pasta e criar um contrato simples e repetivel para operar multiplos clientes sem mistura de:

- numeros de WhatsApp
- inboxes de atendimento
- automacoes
- agentes e prompts
- credenciais
- backups e restores

## Estrutura

- `manifests/`: manifests reais por cliente
- `secrets/`: inventario operacional por cliente
- `checklists/`: onboarding e operacao por cliente
- [templates/tenant-manifest.example.yaml](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/templates/tenant-manifest.example.yaml): manifesto base de um tenant
- [templates/tenant-registry.example.yaml](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/templates/tenant-registry.example.yaml): registro central de tenants
- [templates/onboarding-checklist.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/templates/onboarding-checklist.md): checklist de entrada de cliente
- [templates/secrets-inventory.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/templates/secrets-inventory.md): inventario de segredos por cliente
- [templates/client-ops-checklist.md](C:/Users/PEDROSO/Downloads/elevalocal-infra/tenants/templates/client-ops-checklist.md): checklist de operacao continua por cliente

## Fluxo recomendado

1. executar `python ops/create-tenant.py ...`
2. revisar o manifest gerado em `tenants/manifests/`
3. validar com `python ops/validate-tenant-manifest.py tenants/manifests/SEU_TENANT.yaml --registry tenants/registry.yaml`
4. preencher segredos e checklists antes de provisionar

Guardrail atual:

- `n8n shared-foundation` so pode ser usado para tenant `internal`
- cliente externo deve nascer com `n8n dedicated`

## Regra de ouro

Cada cliente deve ter pelo menos:

- `tenant_id` unico e estavel
- naming padronizado por stack e recurso
- credenciais segregadas
- manifesto proprio
- inventario proprio
- checklist proprio de onboarding e operacao

## Minimo recomendado por cliente

- 1 instancia `Evolution`
- 1 inbox `Chatwoot`
- automacoes `n8n` com namespace proprio
- prompts/agentes com contexto proprio
- referencias de backup/restore identificadas pelo `tenant_id`

## Matriz de provisionamento

| Stack | Runtime padrao | Escopo dedicado por tenant | Naming | Ownership de credenciais | Regra de rollout |
| --- | --- | --- | --- | --- | --- |
| `Evolution` | `shared-foundation` | `instance-per-tenant` | `cli-{slug}-evo` | `eleva-local-ops` com segredo exclusivo do tenant | numero e webhook so entram em producao depois de teste de envio e recebimento |
| `Chatwoot` | `shared-foundation` | `inbox-per-tenant` | `cli-{slug}-inbox` | `eleva-local-ops` com token e owner registrados no inventario do tenant | inbox, labels e roteamento precisam ser validados antes do go-live |
| `n8n` | `dedicated` para clientes externos | `workspace-per-tenant` | `cli-{slug}-wf-{dominio}` | `eleva-local-ops` com credenciais exclusivas por tenant | nenhum cliente externo entra em runtime compartilhada; excecao atual e so o tenant piloto interno |

Cada manifest deve carregar essa decisao em `provisioning.*`, enquanto o mapeamento de stack real continua em `operations.stack_mapping` quando existir.

## Naming padrao sugerido

- `tenant_id`: `cli-{slug}`
- `Evolution`: `cli-{slug}-evo`
- `Chatwoot inbox`: `cli-{slug}-inbox`
- `n8n workflow`: `cli-{slug}-wf-{nome}`
- `segredo`: `cli-{slug}-secret-{nome}`

## Regra operacional

Nao registrar segredos reais nesta pasta.
